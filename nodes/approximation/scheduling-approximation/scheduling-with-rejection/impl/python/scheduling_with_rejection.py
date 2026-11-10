# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-with-rejection/. The authors are listed in prov/NKR10R.jsonl.

"""Makespan with rejection on m identical machines: minimize the makespan of the
accepted jobs plus the total penalty of the rejected jobs.

threshold_rejection guesses the longest accepted job T, accepts the jobs with
p_j <= T and p_j / m <= e_j, and list-schedules them. The best guess costs at
most (2 - 1/m) OPT, and with m = 1 it is optimal.
"""

import heapq
from typing import Sequence


def list_schedule(p: Sequence[int], jobs: Sequence[int], m: int) -> tuple[list[list[int]], int]:
    """Longest job first, each on the machine with the least load."""
    loads = [(0, i) for i in range(m)]
    machines: list[list[int]] = [[] for _ in range(m)]
    for j in sorted(jobs, key=lambda j: (-p[j], j)):
        t, i = heapq.heappop(loads)
        machines[i].append(j)
        heapq.heappush(loads, (t + p[j], i))
    return machines, max(t for t, _ in loads)


def threshold_rejection(p: Sequence[int], e: Sequence[int], m: int) -> tuple[list[list[int]], list[int], int]:
    """Returns (jobs on each machine, rejected jobs, makespan + total penalty)."""
    n = len(p)
    if len(e) != n or m < 1:
        raise ValueError("need len(p) == len(e) and m >= 1")
    if any(x < 0 for x in p) or any(x < 0 for x in e):
        raise ValueError("p and e must be nonnegative")
    best = None
    for T in sorted({0, *p}):  # @line L1
        A = [j for j in range(n) if p[j] <= T and p[j] <= m * e[j]]  # @line L2
        machines, cmax = list_schedule(p, A, m)  # @line L3
        inA = set(A)
        rejected = [j for j in range(n) if j not in inA]
        value = cmax + sum(e[j] for j in rejected)  # @line L4
        if best is None or value < best[2]:  # @line L5
            best = (machines, rejected, value)
    return best  # @line L6


def cost(p: Sequence[int], e: Sequence[int], machines: Sequence[Sequence[int]], rejected: Sequence[int]) -> int:
    return max((sum(p[j] for j in mach) for mach in machines), default=0) + sum(e[j] for j in rejected)
