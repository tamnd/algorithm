# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-with-release-dates/. The authors are listed in prov/N7DJXC.jsonl.

"""Makespan with release dates: earliest release date first (ERD).

On one machine ERD is optimal for 1|r_j|C_max. On m identical machines,
ERD list scheduling gives C_max <= 2 OPT - p_l / m for P|r_j|C_max, where l
is a job that completes last.
"""

import heapq
from typing import Sequence


def erd_schedule(p: Sequence[int], r: Sequence[int], m: int = 1) -> tuple[list[int], list[int], int]:
    """Take the jobs by release date; start each on the machine that is free first,
    as soon as both the machine and the job are ready.

    Returns (machine of each job, start time of each job, makespan).
    """
    n = len(p)
    if len(r) != n or m < 1:
        raise ValueError("need len(p) == len(r) and m >= 1")
    if any(x < 0 for x in p) or any(x < 0 for x in r):
        raise ValueError("p and r must be nonnegative")
    order = sorted(range(n), key=lambda j: (r[j], j))  # @line L1
    free = [(0, i) for i in range(m)]  # @line L2
    machine, start = [0] * n, [0] * n
    cmax = 0
    for j in order:  # @line L3
        t, i = heapq.heappop(free)  # @line L4
        s = max(t, r[j])  # @line L5
        machine[j], start[j] = i, s
        heapq.heappush(free, (s + p[j], i))
        cmax = max(cmax, s + p[j])
    return machine, start, cmax  # @line L6


def single_machine_lower_bound(p: Sequence[int], r: Sequence[int]) -> int:
    """max over j of r_j + the total work released at or after r_j; equals OPT of 1|r_j|C_max."""
    return max((r[j] + sum(p[k] for k in range(len(p)) if r[k] >= r[j]) for j in range(len(p))), default=0)


def is_feasible(p, r, machine, start) -> bool:
    n = len(p)
    if any(start[j] < r[j] for j in range(n)):
        return False
    by_machine: dict[int, list[int]] = {}
    for j in range(n):
        by_machine.setdefault(machine[j], []).append(j)
    for jobs in by_machine.values():
        jobs.sort(key=lambda j: (start[j], start[j] + p[j]))
        for a, b in zip(jobs, jobs[1:]):
            if start[a] + p[a] > start[b]:
                return False
    return True
