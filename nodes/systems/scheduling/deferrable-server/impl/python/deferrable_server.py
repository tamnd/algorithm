# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferrable-server/. The authors are listed in prov/D4EFKC.jsonl.

"""Deferrable server under preemptive fixed priorities, in discrete time.

A periodic task is (priority, C, T, D, phase); a larger priority number is
more urgent. The server is (priority, Cs, Ts). Aperiodic requests are
(arrival, demand) pairs served first come, first served. At each multiple
of Ts the budget is set to Cs; unused budget is kept until then, so the
server can run at any time in its period while it has budget.

Cost: O(n) work per time unit for n periodic tasks, so O(n * horizon).
"""

from dataclasses import dataclass, field

Task = tuple[int, int, int, int, int]


@dataclass
class Result:
    timeline: list[object] = field(default_factory=list)
    jobs: list[list[tuple[int, int | None]]] = field(default_factory=list)
    aperiodic: list[int | None] = field(default_factory=list)

    def worst_response(self, i: int) -> int:
        return max((f - r for r, f in self.jobs[i] if f is not None), default=0)

    def misses(self, tasks: list[Task]) -> int:
        return sum(1 for i, (_, _, _, d, _) in enumerate(tasks) for r, f in self.jobs[i] if f is None or f - r > d)


def deferrable_server(tasks: list[Task], server: tuple[int, int, int],
                      requests: list[tuple[int, int]], horizon: int) -> Result:
    """Simulate time units 0 .. horizon - 1. A finish time is None if the job is not done."""
    ps, cs, ts = server
    if len({p for p, *_ in tasks} | {ps}) != len(tasks) + 1:
        raise ValueError("priorities must be distinct")
    res = Result(jobs=[[] for _ in tasks], aperiodic=[None] * len(requests))
    left = [0] * len(tasks)
    queue: list[int] = []
    need = [d for _, d in requests]
    c = 0
    for t in range(horizon):  # @line L1
        if t % ts == 0:  # @line L2
            c = cs
        for i, (_, ci, ti, _, ph) in enumerate(tasks):  # @line L3
            if t >= ph and (t - ph) % ti == 0:
                if left[i] > 0:
                    raise ValueError("a job is still running at its next release")
                res.jobs[i].append((t, None))
                left[i] = ci
        queue += [k for k, (a, _) in enumerate(requests) if a == t and need[k] > 0]
        best, who = None, None
        if queue and c > 0:  # @line L4
            best, who = ps, "S"
        for i, (p, *_rest) in enumerate(tasks):
            if left[i] > 0 and (best is None or p > best):
                best, who = p, i
        res.timeline.append(who)  # @line L5
        if who == "S":  # @line L6
            c -= 1
            k = queue[0]
            need[k] -= 1
            if need[k] == 0:
                res.aperiodic[k] = t + 1
                queue.pop(0)
        elif who is not None:
            left[who] -= 1
            if left[who] == 0:
                r, _ = res.jobs[who][-1]
                res.jobs[who][-1] = (r, t + 1)
    return res
