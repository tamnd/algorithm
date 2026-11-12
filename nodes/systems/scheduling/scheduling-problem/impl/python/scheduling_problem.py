# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-problem/. The authors are listed in prov/X20JQV.jsonl.

"""The scheduling problem on small instances: a checker and an exact solver.

A job is (release r, processing time p, due date d, weight w). A schedule is a
list of pieces (machine, start, end, job). The checker tests the constraints of
the problem; the solver finds the best nonpreemptive schedule on one machine by
trying every order, which is exact because some optimal schedule starts each
job as early as its order allows. It takes O(n! * n) time, so use n <= 8.
"""

from dataclasses import dataclass
from itertools import permutations


@dataclass(frozen=True)
class Job:
    r: int
    p: int
    d: int = 0
    w: int = 1


def is_feasible(jobs: list, pieces: list, machines: int = 1, preemptive: bool = False) -> bool:
    """True when the pieces form a legal schedule of all jobs."""
    for m, s, e, j in pieces:
        if not (0 <= m < machines and s < e and s >= jobs[j].r):
            return False
    for m in range(machines):  # a machine runs one job at a time
        mine = sorted((s, e) for mm, s, e, _ in pieces if mm == m)
        if any(e1 > s2 for (_, e1), (s2, _) in zip(mine, mine[1:])):
            return False
    for j, job in enumerate(jobs):
        mine = sorted((s, e) for _, s, e, jj in pieces if jj == j)
        if sum(e - s for s, e in mine) != job.p:
            return False
        if any(e1 > s2 for (_, e1), (s2, _) in zip(mine, mine[1:])):
            return False  # a job runs on one machine at a time
        if not preemptive and len(mine) != 1:
            return False
    return True


def completion_times(jobs: list, pieces: list) -> list:
    return [max(e for _, _, e, jj in pieces if jj == j) for j in range(len(jobs))]


OBJECTIVES = {
    "Cmax": lambda jobs, c: max(c),
    "sumC": lambda jobs, c: sum(c),
    "sumwC": lambda jobs, c: sum(j.w * x for j, x in zip(jobs, c)),
    "sumF": lambda jobs, c: sum(x - j.r for j, x in zip(jobs, c)),
    "Lmax": lambda jobs, c: max(x - j.d for j, x in zip(jobs, c)),
    "sumU": lambda jobs, c: sum(1 for j, x in zip(jobs, c) if x > j.d),
}


def schedule_order(jobs: list, order: list) -> list:
    """Run the jobs in this order on one machine, each as early as possible."""
    t, pieces = 0, []
    for j in order:
        s = max(t, jobs[j].r)
        t = s + jobs[j].p
        pieces.append((0, s, t, j))
    return pieces


def best_nonpreemptive(jobs: list, objective: str) -> tuple:
    """Return (value, order) of an optimal nonpreemptive one-machine schedule."""
    f = OBJECTIVES[objective]
    best = None
    for order in permutations(range(len(jobs))):
        v = f(jobs, completion_times(jobs, schedule_order(jobs, list(order))))
        if best is None or v < best[0]:
            best = (v, list(order))
    return best
