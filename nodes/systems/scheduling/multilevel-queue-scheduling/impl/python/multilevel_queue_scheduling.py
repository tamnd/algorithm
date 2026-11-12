# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-queue-scheduling/. The authors are listed in prov/KWDCKZ.jsonl.

from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Job:
    name: str
    arrival: int  # the tick at which the job becomes ready
    burst: int  # the CPU time it needs, in ticks (at least 1)
    cls: int  # the index of its queue, 0 is the highest


@dataclass(frozen=True)
class QueueSpec:
    policy: str  # "rr" or "fcfs"
    quantum: int = 1  # used only by "rr"


def multilevel_queue(
    jobs: list[Job],
    queues: list[QueueSpec],
    between: str = "priority",
    shares: Optional[list[int]] = None,
) -> tuple[list[Optional[str]], dict[str, int]]:
    """Simulate multilevel queue scheduling on one CPU in unit ticks.

    Each job stays for its whole life in the queue queues[job.cls]. Inside a
    queue the policy is round robin with that queue's quantum, or FCFS.
    Between the queues the rule is "priority" (the lowest-index non-empty
    queue runs, preemptively, at every tick) or "slice" (the queues take
    turns of shares[i] ticks; an empty queue gives its turn away).

    At tick t, first a job whose quantum ended at t goes to the tail of its
    queue, then the jobs with arrival t join their queues, in input order.

    Returns the timeline (the job name run in each tick, None when idle) and
    the completion tick of each job. Time O((T + n) k) for T ticks, n jobs
    and k queues.
    """
    k = len(queues)
    if between == "slice":
        if shares is None or len(shares) != k or min(shares) < 1:
            raise ValueError("slice mode needs one positive share per queue")
    elif between != "priority":
        raise ValueError("between must be 'priority' or 'slice'")
    for j in jobs:
        if not 0 <= j.cls < k or j.burst < 1 or j.arrival < 0:
            raise ValueError(f"bad job {j}")
    pending = sorted(range(len(jobs)), key=lambda i: (jobs[i].arrival, i))
    nxt = 0
    remaining = {j.name: j.burst for j in jobs}
    used = {j.name: 0 for j in jobs}
    q: list[deque[str]] = [deque() for _ in range(k)]
    timeline: list[Optional[str]] = []
    done: dict[str, int] = {}
    turn, turn_used = 0, 0
    t = 0  # @line L1
    while len(done) < len(jobs):  # @line L2
        while nxt < len(pending) and jobs[pending[nxt]].arrival == t:  # @line L3
            j = jobs[pending[nxt]]
            q[j.cls].append(j.name)
            nxt += 1
        i = _select_queue(q, between, shares, turn, turn_used)  # @line L4
        if i is None:  # @line L5
            timeline.append(None)
            t += 1
            continue
        if between == "slice":
            if i != turn:
                turn, turn_used = i, 0
            turn_used += 1
        name = q[i][0]  # @line L6
        timeline.append(name)  # @line L7
        remaining[name] -= 1
        used[name] += 1
        t += 1
        if remaining[name] == 0:  # @line L8
            q[i].popleft()
            done[name] = t
            used[name] = 0
        elif queues[i].policy == "rr" and used[name] == queues[i].quantum:  # @line L9
            q[i].rotate(-1)
            used[name] = 0
        if between == "slice" and turn_used == shares[turn]:  # type: ignore[index]
            turn, turn_used = (turn + 1) % k, 0
    return timeline, done


def _select_queue(
    q: list[deque[str]], between: str, shares: Optional[list[int]], turn: int, turn_used: int
) -> Optional[int]:
    """The queue that runs in this tick, or None if all queues are empty."""
    k = len(q)
    if between == "priority":
        for i in range(k):
            if q[i]:
                return i
        return None
    for step in range(k):
        i = (turn + step) % k
        if q[i]:
            return i
    return None
