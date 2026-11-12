# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/completely-fair-scheduler/. The authors are listed in prov/BQCYGA.jsonl.

import heapq
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Union

Num = Union[int, Fraction]
NICE_0_WEIGHT = 1024


@dataclass(frozen=True)
class Task:
    """A task with a weight and alternating CPU bursts and sleeps:
    bursts[0] CPU, bursts[1] sleep, bursts[2] CPU, ..., ending with CPU."""

    name: str
    weight: int
    arrival: Num
    bursts: tuple


@dataclass
class Trace:
    runs: list = field(default_factory=list)  # (start, end, name) segments
    done: dict = field(default_factory=dict)  # finish time of each task
    vruntime: dict = field(default_factory=dict)  # final vruntime of each task


def cfs(
    tasks: list[Task],
    latency: Num = 48,
    min_gran: Num = 6,
    place: bool = True,
    until: Optional[Num] = None,
) -> Trace:
    """Simulate the core of the Linux Completely Fair Scheduler on one CPU.

    The runnable tasks sit in a priority queue ordered by (vruntime, join
    order); a binary heap stands in for the kernel's red-black tree. The task
    with the smallest vruntime runs for its slice, period * w / W, where the
    period is max(latency, n * min_gran). Running for d time units adds
    d * 1024 / w to its vruntime. A task that arrives or wakes is placed at
    max(its vruntime, min_vruntime) (place=False skips this, for contrast).
    A running task is not preempted before its slice or burst ends.
    Exact arithmetic with Fractions. With `until`, the simulation stops at
    the first run that ends at or after that time.
    """
    for k in tasks:
        if k.weight < 1 or not k.bursts or len(k.bursts) % 2 == 0 or min(k.bursts) <= 0:
            raise ValueError(f"bad task {k.name}")
    order = {k.name: i for i, k in enumerate(tasks)}
    by_name = {k.name: k for k in tasks}
    vr: dict[str, Num] = {k.name: Fraction(0) for k in tasks}
    phase = {k.name: 0 for k in tasks}
    left: dict[str, Num] = {k.name: Fraction(k.bursts[0]) for k in tasks}
    pending = [(Fraction(k.arrival), order[k.name], k.name) for k in tasks]  # arrivals and wakes
    heapq.heapify(pending)
    q: list = []
    weight_sum = 0
    tr = Trace()
    t: Num = Fraction(0)
    min_vr: Num = Fraction(0)  # @line L1
    while len(tr.done) < len(tasks) and (until is None or t < until):  # @line L2
        while pending and pending[0][0] <= t:  # @line L3
            _, _, name = heapq.heappop(pending)
            if place:
                vr[name] = max(vr[name], min_vr)
            heapq.heappush(q, (vr[name], order[name], name))
            weight_sum += by_name[name].weight
        if not q:  # @line L4
            t = pending[0][0]
            continue
        _, _, name = heapq.heappop(q)  # @line L5
        w = by_name[name].weight
        n = len(q) + 1  # @line L6
        period = max(Fraction(latency), n * Fraction(min_gran))
        slice_ = period * w / weight_sum  # @line L7
        d = min(slice_, left[name])  # @line L8
        tr.runs.append((t, t + d, name))
        t += d
        left[name] -= d
        vr[name] += d * NICE_0_WEIGHT / w  # @line L9
        smallest = min(vr[name], q[0][0]) if q else vr[name]  # @line L10
        min_vr = max(min_vr, smallest)
        if left[name] == 0:  # @line L11
            weight_sum -= w
            phase[name] += 1
            bursts = by_name[name].bursts
            if phase[name] == len(bursts):
                tr.done[name] = t
            else:
                heapq.heappush(pending, (t + bursts[phase[name]], order[name], name))
                phase[name] += 1
                left[name] = Fraction(bursts[phase[name]])
        else:
            heapq.heappush(q, (vr[name], order[name], name))
    tr.vruntime = dict(vr)
    return tr


def cpu_until(runs: list, name: str, time: Num) -> Num:
    """CPU time that a task received before the given time."""
    total: Num = 0
    for s, e, x in runs:
        if x == name and s < time:
            total += min(e, time) - s
    return total
