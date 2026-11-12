# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-feedback-queue/. The authors are listed in prov/1E6C07.jsonl.

from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Job:
    """A job with alternating CPU bursts and I/O waits: bursts[0] CPU,
    bursts[1] I/O, bursts[2] CPU, ..., ending with a CPU burst."""

    name: str
    arrival: int
    bursts: tuple[int, ...]


@dataclass
class _State:
    job: Job
    phase: int = 0  # index into bursts
    left: int = 0  # ticks left in the current burst
    level: int = 0
    used: int = 0  # CPU ticks used at this level (the allotment counter)
    slice: int = 0  # CPU ticks used in the current quantum
    wake: int = -1  # tick at which the current I/O ends


@dataclass
class Trace:
    timeline: list[Optional[str]] = field(default_factory=list)  # job run in each tick
    levels: list[dict[str, int]] = field(default_factory=list)  # level of each job after each tick
    done: dict[str, int] = field(default_factory=dict)  # completion tick


def mlfq(
    jobs: list[Job],
    quantum: list[int],
    allotment: list[int],
    boost: int = 0,
    accounting: bool = True,
) -> Trace:
    """Simulate the multilevel feedback queue of Arpaci-Dusseau (OSTEP, Ch. 8).

    Queue 0 is the highest priority. quantum[i] is the time slice of queue i,
    allotment[i] the CPU time a job may use at level i before it moves down.
    boost > 0 moves every job to queue 0 every boost ticks (Rule 5).
    accounting=True is Rule 4 (the allotment counts all CPU use at a level);
    accounting=False is the gameable Rules 4a and 4b (the counter is reset
    whenever the job blocks for I/O). One CPU, unit ticks.

    Order inside tick t: the boost, then I/O completions, then arrivals, then
    one tick of CPU. Time O(T (k + 1) + B) for T ticks, k levels and B jobs
    boosted in total.
    """
    k = len(quantum)
    if k == 0 or len(allotment) != k or min(quantum) < 1 or min(allotment) < 1:
        raise ValueError("need k >= 1 levels with positive quanta and allotments")
    for j in jobs:
        if not j.bursts or len(j.bursts) % 2 == 0 or min(j.bursts) < 1:
            raise ValueError(f"bad bursts for {j.name}")
    st = {j.name: _State(j, 0, j.bursts[0]) for j in jobs}
    arrivals = sorted(jobs, key=lambda j: j.arrival)
    nxt = 0
    q: list[deque[str]] = [deque() for _ in range(k)]
    blocked: list[str] = []  # in the order they blocked
    tr = Trace()
    t = 0  # @line L1
    while len(tr.done) < len(jobs):  # @line L2
        if boost > 0 and t > 0 and t % boost == 0:  # @line L3
            moved = [name for lvl in q for name in lvl]
            for lvl in q:
                lvl.clear()
            q[0].extend(moved)
            for s in st.values():
                s.level, s.used, s.slice = 0, 0, 0
        for name in [b for b in blocked if st[b].wake == t]:  # @line L4
            blocked.remove(name)
            q[st[name].level].append(name)
        while nxt < len(arrivals) and arrivals[nxt].arrival == t:  # @line L5
            q[0].append(arrivals[nxt].name)
            nxt += 1
        i = next((lvl for lvl in range(k) if q[lvl]), None)  # @line L6
        if i is None:  # @line L7
            tr.timeline.append(None)
            tr.levels.append({n: s.level for n, s in st.items()})
            t += 1
            continue
        name = q[i][0]  # @line L8
        s = st[name]
        tr.timeline.append(name)
        t += 1
        s.left -= 1
        s.used += 1
        s.slice += 1
        demoted = False
        if s.used == allotment[i]:  # @line L9
            s.level, s.used, s.slice, demoted = min(i + 1, k - 1), 0, 0, True
        if s.left == 0:  # @line L10
            q[i].popleft()
            s.slice = 0
            s.phase += 1
            if s.phase == len(s.job.bursts):
                tr.done[name] = t
            else:
                s.wake = t + s.job.bursts[s.phase]
                s.phase += 1
                s.left = s.job.bursts[s.phase]
                blocked.append(name)
                if not accounting:
                    s.used = 0  # Rule 4b: giving up the CPU resets the allotment
        elif demoted or s.slice == quantum[i]:  # @line L11
            q[i].popleft()
            s.slice = 0
            q[s.level].append(name)
        tr.levels.append({n: x.level for n, x in st.items()})
    return tr
