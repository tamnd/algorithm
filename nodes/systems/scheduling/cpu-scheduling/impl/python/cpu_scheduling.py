# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cpu-scheduling/. The authors are listed in prov/DMSXXK.jsonl.

"""A small discrete-event model of one CPU, its ready queue and its dispatcher.

Each process alternates CPU bursts and I/O bursts. The I/O devices run in
parallel with the CPU and with each other. The short-term scheduler is a key
function on the ready queue: the dispatcher runs the ready process with the
least key, and breaks ties by the order in which processes entered the queue.
Time is an explicit clock: int or Fraction, never the wall clock.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

Key = Callable[["Process", int, object], tuple]


@dataclass
class Process:
    name: str
    arrival: object
    bursts: list  # CPU, I/O, CPU, ..., CPU: an odd number of positive lengths
    priority: int = 0


@dataclass
class Trace:
    segments: list = field(default_factory=list)  # (start, end, name); "*" marks dispatch
    completion: dict = field(default_factory=dict)
    first_run: dict = field(default_factory=dict)
    ready_time: dict = field(default_factory=dict)  # total time spent in the ready queue
    decisions: dict = field(default_factory=lambda: {1: 0, 2: 0, 3: 0, 4: 0})
    dispatches: int = 0


def fcfs_key(p: Process, burst: int, remaining: object) -> tuple:
    """Every process has the same key, so the queue order decides: FCFS."""
    return ()


def burst_key(p: Process, burst: int, remaining: object) -> tuple:
    """Least remaining time of the current CPU burst first."""
    return (remaining,)


def priority_key(p: Process, burst: int, remaining: object) -> tuple:
    """Smallest priority number first."""
    return (p.priority,)


def simulate(procs: list, key: Key = fcfs_key, preemptive: bool = False,
             quantum: Optional[object] = None, dispatch: object = 0) -> Trace:
    """Run the processes on one CPU and return the trace.

    Decision points (Silberschatz, Section 5.1.3): 1 running to waiting,
    2 running to ready, 3 waiting to ready, 4 termination. A process that is
    preempted at time t joins the ready queue after the processes that arrive
    or finish I/O at t. Each dispatch costs `dispatch` time units of CPU.
    Cost: O(E * n) time for E events and n processes (a linear scan of the queue).
    """
    tr = Trace()
    burst_i = {p.name: 0 for p in procs}
    rem = {p.name: p.bursts[0] for p in procs}
    by_name = {p.name: p for p in procs}
    pending = sorted(((p.arrival, i, p.name, False) for i, p in enumerate(procs)),
                     key=lambda e: (e[0], e[1]))
    ready: list = []  # entries (seq, name, time entered)
    seq = 0
    t = min((p.arrival for p in procs), default=0)
    running: Optional[str] = None
    slice_start = t
    requeue: Optional[str] = None
    left = len(procs)

    def k(name: str) -> tuple:
        return key(by_name[name], burst_i[name], rem[name])

    def push(name: str) -> None:
        nonlocal seq
        ready.append((seq, name, t))
        seq += 1

    def take(idx: int) -> str:
        s, name, entered = ready.pop(idx)
        tr.ready_time[name] = tr.ready_time.get(name, 0) + (t - entered)
        return name

    while left:
        while pending and pending[0][0] <= t:  # admit arrivals and I/O completions
            _, _, name, from_io = pending.pop(0)
            if from_io:
                tr.decisions[3] += 1
            push(name)
        if requeue is not None:  # the preempted process goes behind them
            if ready:
                tr.decisions[2] += 1
                push(requeue)
            else:  # nobody else is ready: it keeps the CPU for a new quantum
                running, slice_start = requeue, t
            requeue = None
        if running is not None and preemptive and ready:
            best = min(range(len(ready)), key=lambda i: (k(ready[i][1]), ready[i][0]))
            if k(ready[best][1]) < k(running):
                tr.decisions[2] += 1
                push(running)
                running = None
        if running is None and ready:
            best = min(range(len(ready)), key=lambda i: (k(ready[i][1]), ready[i][0]))
            running = take(best)
            tr.dispatches += 1
            if dispatch:
                tr.segments.append((t, t + dispatch, "*"))
                t = t + dispatch
                while pending and pending[0][0] <= t:
                    _, _, name, from_io = pending.pop(0)
                    if from_io:
                        tr.decisions[3] += 1
                    push(name)
            tr.first_run.setdefault(running, t)
            slice_start = t
        if running is None:
            if not pending:
                break
            t = pending[0][0]  # the CPU is idle until the next event
            continue
        stop = t + rem[running]
        if quantum is not None:
            stop = min(stop, slice_start + quantum)
        if pending and preemptive:
            stop = min(stop, pending[0][0])
        if pending and pending[0][0] < stop and pending[0][0] > t:
            stop = pending[0][0]  # wake up to admit, so the queue order stays exact
        if stop > t:
            if tr.segments and tr.segments[-1][2] == running and tr.segments[-1][1] == t:
                s0 = tr.segments.pop()[0]
                tr.segments.append((s0, stop, running))
            else:
                tr.segments.append((t, stop, running))
        rem[running] = rem[running] - (stop - t)
        t = stop
        if rem[running] == 0:
            name = running
            running = None
            b = burst_i[name]
            p = by_name[name]
            if b + 1 < len(p.bursts):
                tr.decisions[1] += 1
                burst_i[name] = b + 2
                rem[name] = p.bursts[b + 2]
                pending.append((t + p.bursts[b + 1], seq, name, True))
                seq += 1
                pending.sort(key=lambda e: (e[0], e[1]))
            else:
                tr.decisions[4] += 1
                tr.completion[name] = t
                left -= 1
        elif quantum is not None and t - slice_start >= quantum:
            requeue = running
            running = None
    return tr
