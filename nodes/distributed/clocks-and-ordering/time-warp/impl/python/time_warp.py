# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-warp/. The authors are listed in prov/GQ6HAV.jsonl.

"""Time Warp (Jefferson 1985) on a seeded simulator of a parallel machine, and
the sequential simulation it must match.

The model is PHOLD-like. Each logical process (LP) has an integer state. An
event is (ts, eid, dst). When LP i executes event e, its new state and the one
event it schedules are pure functions of (state, e). Events run in order of the
key (ts, eid), so the sequential result is well defined.

The machine runs the LPs in a random order, and every message has a random
delay. An LP executes its earliest pending event at once, so a message can
arrive with a key below the LP's last executed event: a straggler. The LP then
rolls back: it restores the saved state, puts the undone events back, and sends
an antimessage for each message the undone events sent.
"""

import bisect
import random
from dataclasses import dataclass, field

M61 = (1 << 61) - 1


def mix(*xs: int) -> int:
    h = 1469598103934665603
    for x in xs:
        h = ((h ^ (x & M61)) * 1099511628211 + 0x9E3779B97F4A7C15) % M61
    return h


Key = tuple[int, int]  # (ts, eid)


@dataclass(frozen=True, order=True)
class Event:
    ts: int
    eid: int
    dst: int


def execute(state: int, e: Event, n: int, end: int) -> tuple[int, Event | None]:
    """The model: the new state and the scheduled event (none past `end`)."""
    h = mix(state, e.ts, e.eid)
    new_state = h % 1000003
    ts = e.ts + 1 + h % 7  # positive increment
    child = Event(ts, mix(e.eid, 17), (h >> 8) % n)
    return new_state, (child if ts <= end else None)


def initial_events(n: int, per_lp: int, seed: int) -> list[Event]:
    rng = random.Random(seed)
    return [Event(rng.randrange(0, 10), mix(seed, i, k), i) for i in range(n) for k in range(per_lp)]


def sequential(n: int, events: list[Event], end: int) -> tuple[list[int], list[list[Key]]]:
    import heapq

    state = [0] * n
    done: list[list[Key]] = [[] for _ in range(n)]
    q = [(e.ts, e.eid, e) for e in events]
    heapq.heapify(q)
    while q:
        _, _, e = heapq.heappop(q)
        state[e.dst], child = execute(state[e.dst], e, n, end)
        done[e.dst].append((e.ts, e.eid))
        if child:
            heapq.heappush(q, (child.ts, child.eid, child))
    return state, done


@dataclass
class LP:
    state: int = 0
    pending: list = field(default_factory=list)  # sorted list of (ts, eid, Event)
    processed: list = field(default_factory=list)  # (Event, state before, sent child or None)
    early_anti: set = field(default_factory=set)  # antimessages that came before their message
    committed: list = field(default_factory=list)  # keys made final by fossil collection


@dataclass
class Stats:
    rollbacks: int = 0
    undone: int = 0
    antimessages: int = 0
    gvt_values: list = field(default_factory=list)


class TimeWarp:
    def __init__(self, n: int, events: list[Event], end: int, seed: int, max_delay: int = 6) -> None:
        self.n, self.end = n, end
        self.lp = [LP() for _ in range(n)]
        self.rng = random.Random(seed)
        self.max_delay = max_delay
        self.transit: list[tuple[int, int, str, Event]] = []  # (arrive step, seq, sign, event)
        self.seq = 0
        self.step = 0
        self.last_gvt = float("-inf")
        self.stats = Stats()
        for e in events:
            self.insert(self.lp[e.dst], e)

    def insert(self, lp: LP, e: Event) -> None:
        bisect.insort(lp.pending, (e.ts, e.eid, e))

    def send(self, sign: str, e: Event) -> None:
        self.transit.append((self.step + self.rng.randint(1, self.max_delay), self.seq, sign, e))
        self.seq += 1

    def rollback(self, i: int, key: Key) -> None:
        """Undo every executed event of LP i with key >= key."""
        lp = self.lp[i]
        if lp.processed and (lp.processed[-1][0].ts, lp.processed[-1][0].eid) >= key:
            self.stats.rollbacks += 1
            assert key[0] >= self.last_gvt  # no rollback reaches below GVT
        while lp.processed and (lp.processed[-1][0].ts, lp.processed[-1][0].eid) >= key:
            e, before, child = lp.processed.pop()
            lp.state = before  # @line L6
            self.insert(lp, e)
            self.stats.undone += 1
            if child is not None:
                self.send("-", child)  # @line L7
                self.stats.antimessages += 1

    def receive(self, sign: str, e: Event) -> None:
        lp = self.lp[e.dst]
        key = (e.ts, e.eid)
        last = (lp.processed[-1][0].ts, lp.processed[-1][0].eid) if lp.processed else None
        if sign == "+":
            if key in lp.early_anti:
                lp.early_anti.discard(key)  # the pair annihilates
                return
            if last is not None and key < last:  # @line L3
                self.rollback(e.dst, key)
            self.insert(lp, e)
        else:
            if any(p[0] == e for p in lp.processed):
                self.rollback(e.dst, key)  # @line L4
            pos = bisect.bisect_left(lp.pending, (e.ts, e.eid, e))
            if pos < len(lp.pending) and lp.pending[pos][2] == e:
                lp.pending.pop(pos)  # @line L5
            else:
                lp.early_anti.add(key)

    def execute_one(self, i: int) -> None:
        lp = self.lp[i]
        _, _, e = lp.pending.pop(0)  # @line L1
        before = lp.state
        lp.state, child = execute(lp.state, e, self.n, self.end)
        lp.processed.append((e, before, child))  # @line L2
        if child is not None:
            self.send("+", child)

    def gvt(self) -> float:
        """The true GVT, read by an observer that sees the whole machine."""
        ts = [lp.pending[0][0] for lp in self.lp if lp.pending]
        ts += [e.ts for _, _, _, e in self.transit]
        return min(ts, default=float("inf"))

    def fossil_collect(self) -> None:
        g = self.gvt()
        self.stats.gvt_values.append(g)
        self.last_gvt = g
        for lp in self.lp:
            k = 0
            while k < len(lp.processed) and lp.processed[k][0].ts < g:  # @line L8
                k += 1
            lp.committed += [(e.ts, e.eid) for e, _, _ in lp.processed[:k]]
            del lp.processed[:k]

    def run(self, fossil_every: int = 10) -> None:
        while True:
            self.step += 1
            ready = [m for m in self.transit if m[0] <= self.step]
            if ready:
                self.transit = [m for m in self.transit if m[0] > self.step]
                for _, _, sign, e in sorted(ready, key=lambda m: m[1]):
                    self.receive(sign, e)
            busy = [i for i in range(self.n) if self.lp[i].pending]
            for i in self.rng.sample(busy, len(busy)):
                if self.rng.random() < 0.7:
                    self.execute_one(i)
            if self.step % fossil_every == 0:
                before = [list(lp.committed) for lp in self.lp]
                self.fossil_collect()
                assert all(lp.committed[: len(b)] == b for lp, b in zip(self.lp, before))
            if not self.transit and not any(lp.pending for lp in self.lp):
                break
        self.fossil_collect()

    def result(self) -> tuple[list[int], list[list[Key]]]:
        return [lp.state for lp in self.lp], [lp.committed for lp in self.lp]
