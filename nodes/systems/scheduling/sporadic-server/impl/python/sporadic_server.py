# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sporadic-server/. The authors are listed in prov/NBTSC8.jsonl.

"""Sporadic server under preemptive fixed priorities, in discrete time.

A periodic task is (priority, C, T, D, phase); a larger priority number is
more urgent. The server is (priority Ps, capacity Cs, period Ts). Aperiodic
requests are (arrival, demand) pairs, served first come, first served.

Replenishment rules (Sprunt, Sha and Lehoczky 1989, in the form given by
Buttazzo): the server is active while the running job has priority >= Ps.
When it becomes active with capacity > 0, or gets capacity while active,
the replenishment time RT = t + Ts is set. When it becomes idle, or the
capacity reaches 0, the amount used since RT was set is added back at RT.

Cost: O(n + q) work per time unit for n tasks and q pending replenishments.
"""

from dataclasses import dataclass, field

Task = tuple[int, int, int, int, int]


@dataclass
class Result:
    timeline: list[object] = field(default_factory=list)
    jobs: list[list[tuple[int, int | None]]] = field(default_factory=list)
    aperiodic: list[int | None] = field(default_factory=list)
    replenishments: list[tuple[int, int]] = field(default_factory=list)

    def worst_response(self, i: int) -> int:
        return max((f - r for r, f in self.jobs[i] if f is not None), default=0)

    def misses(self, tasks: list[Task]) -> int:
        return sum(1 for i, (_, _, _, d, _) in enumerate(tasks) for r, f in self.jobs[i] if f is None or f - r > d)


def sporadic_server(tasks: list[Task], server: tuple[int, int, int],
                    requests: list[tuple[int, int]], horizon: int) -> Result:
    """Simulate time units 0 .. horizon - 1. A finish time is None if the job is not done."""
    ps, cs, ts = server
    if len({p for p, *_ in tasks} | {ps}) != len(tasks) + 1:
        raise ValueError("priorities must be distinct")
    res = Result(jobs=[[] for _ in tasks], aperiodic=[None] * len(requests))
    left = [0] * len(tasks)
    queue: list[int] = []
    need = [d for _, d in requests]
    c = cs
    due: dict[int, int] = {}
    active = armed = False
    rt = used = 0

    def finalize() -> None:
        nonlocal armed, used
        if armed and used > 0:
            due[rt] = due.get(rt, 0) + used
            res.replenishments.append((rt, used))
        armed, used = False, 0

    for t in range(horizon):
        c += due.pop(t, 0)  # @line L1
        for i, (_, ci, ti, _, ph) in enumerate(tasks):  # @line L2
            if t >= ph and (t - ph) % ti == 0:
                if left[i] > 0:
                    raise ValueError("a job is still running at its next release")
                res.jobs[i].append((t, None))
                left[i] = ci
        queue += [k for k, (a, _) in enumerate(requests) if a == t and need[k] > 0]
        best, who = None, None
        if queue and c > 0:  # @line L3
            best, who = ps, "S"
        for i, (p, *_rest) in enumerate(tasks):
            if left[i] > 0 and (best is None or p > best):
                best, who = p, i
        res.timeline.append(who)  # @line L4
        now_active = best is not None and best >= ps
        if active and not now_active:  # @line L5
            finalize()
        active = now_active
        if active and not armed and c > 0:  # @line L6
            armed, rt, used = True, t + ts, 0
        if who == "S":  # @line L7
            c -= 1
            used += 1
            k = queue[0]
            need[k] -= 1
            if need[k] == 0:
                res.aperiodic[k] = t + 1
                queue.pop(0)
            if c == 0:  # @line L8
                finalize()
        elif who is not None:
            left[who] -= 1
            if left[who] == 0:
                r, _ = res.jobs[who][-1]
                res.jobs[who][-1] = (r, t + 1)
    return res
