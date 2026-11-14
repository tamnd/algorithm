# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/event-driven-logic-simulation/. The authors are listed in prov/V1JG2T.jsonl.
"""Event-driven gate-level logic simulation with a time wheel (Ulrich 1969).

Only the gates with an input that changed are evaluated (selective trace).
Every gate has an integer delay d >= 0. With d = 0, the new event goes into
the same time slot and is handled in the next delta pass. The default delay
model is transport delay: every change of the gate function reaches the
output d time units later. With inertial=True, a new value cancels the
pending events of the output, so pulses shorter than d are removed.
"""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Sequence, Tuple

from logicnet import Circuit, eval2

Event = Tuple[str, int, Optional[int]]  # (net, value, generation of a gate event or None)


class Oscillation(RuntimeError):
    """The delta passes at one time did not settle within the limit."""


class TimeWheel:
    """Ulrich's time mapping: slot t mod M holds the events of time t for now <= t < now + M.

    Events further in the future wait in an overflow heap and move into the
    wheel when the wheel reaches them.
    """

    def __init__(self, size: int):
        self.size = size
        self.slots: List[List[Event]] = [[] for _ in range(size)]
        self.far: List[Tuple[int, int, Event]] = []
        self.now = 0
        self.seq = 0

    def schedule(self, time: int, ev: Event) -> None:
        if time < self.now:
            raise ValueError("an event in the past")
        if time < self.now + self.size:
            self.slots[time % self.size].append(ev)
        else:
            self.seq += 1
            heapq.heappush(self.far, (time, self.seq, ev))

    def take(self, time: int) -> List[Event]:
        slot = self.slots[time % self.size]
        self.slots[time % self.size] = []
        return slot

    def has(self, time: int) -> bool:
        return bool(self.slots[time % self.size])

    def next_time(self) -> Optional[int]:
        for t in range(self.now, self.now + self.size):
            if self.slots[t % self.size]:
                return t
        return self.far[0][0] if self.far else None

    def advance(self, time: int) -> None:
        self.now = time
        while self.far and self.far[0][0] < time + self.size:
            t, _, ev = heapq.heappop(self.far)
            self.slots[t % self.size].append(ev)


def simulate(c: Circuit, delay: Dict[str, int], init: Dict[str, int],
             events: Sequence[Tuple[int, str, int]], t_end: int,
             inertial: bool = False, max_delta: int = 1000):
    """Simulate from time 0 to t_end.

    delay maps each gate output net to its delay. init gives a value in {0, 1}
    to every net. events is a list of input changes (time, net, value).
    Returns (val, changes, evals): the values at t_end, the list of applied
    changes (time, net, value) in order, and the number of gate evaluations.
    """
    size = max([delay[g[0]] for g in c.gates] + [0]) + 1
    val = dict(init)  # @line L1
    proj = dict(init)
    gen = {n: 0 for n in c.nets}
    wheel = TimeWheel(size)  # @line L2
    for t, n, v in sorted(events, key=lambda e: e[0]):
        wheel.schedule(t, (n, v, None))
    changes: List[Tuple[int, str, int]] = []
    evals = 0
    t: Optional[int] = 0
    first = True
    while t is not None and t <= t_end:  # @line L3
        wheel.advance(t)
        passes = 0
        while first or wheel.has(t):
            passes += 1
            if passes > max_delta:
                raise Oscillation(f"no settling at time {t} after {max_delta} delta passes")
            batch: Dict[str, int] = {}
            for n, v, g in wheel.take(t):  # @line L4
                if g is None or g == gen[n]:
                    batch[n] = v  # a later event on the same net replaces an earlier one
            active = [n for n, v in batch.items() if v != val[n]]  # @line L5
            for n in active:
                val[n] = batch[n]
                changes.append((t, n, val[n]))
            if first:
                todo = list(range(len(c.gates)))
                first = False
            else:
                todo = sorted({gi for n in active for gi in c.fanout[n]})  # @line L6
            for gi in todo:  # @line L7
                out, op, ins = c.gates[gi]
                v = eval2(op, [val[n] for n in ins])  # @line L8
                evals += 1
                if v != proj[out]:  # @line L9
                    proj[out] = v  # @line L10
                    if inertial:
                        gen[out] += 1  # cancel the pending events of out
                        if v != val[out]:
                            wheel.schedule(t + delay[out], (out, v, gen[out]))
                    else:
                        wheel.schedule(t + delay[out], (out, v, None))
        t = wheel.next_time()
    return val, changes, evals  # @line L11


def waveform(init: Dict[str, int], changes: Sequence[Tuple[int, str, int]], net: str) -> List[Tuple[int, int]]:
    """The (time, value) steps of one net, starting with its initial value at time 0."""
    w = [(0, init[net])]
    for t, n, v in changes:
        if n == net:
            w.append((t, v))
    return w
