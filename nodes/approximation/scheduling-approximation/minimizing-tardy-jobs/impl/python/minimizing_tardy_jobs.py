# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimizing-tardy-jobs/. The authors are listed in prov/192FEE.jsonl.

"""Moore-Hodgson algorithm for 1||sum U_j: the most jobs that can meet their due dates."""

import heapq
from typing import Sequence


def moore_hodgson(p: Sequence[int], d: Sequence[int]) -> tuple[list[int], list[int]]:
    """Return (on-time jobs in EDD order, late jobs) for one machine.

    Run the on-time jobs in the returned order from time 0, then the late
    jobs in any order. The number of late jobs is the least possible.
    Time O(n log n).
    """
    n = len(p)
    if len(d) != n:
        raise ValueError("p and d must have the same length")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    edd = sorted(range(n), key=lambda j: (d[j], j))  # @line L1
    heap: list[tuple[int, int]] = []  # @line L2
    t = 0
    late: list[int] = []
    for k in edd:  # @line L3
        heapq.heappush(heap, (-p[k], k))  # @line L4
        t += p[k]
        if t > d[k]:  # @line L5
            neg, ell = heapq.heappop(heap)
            t += neg
            late.append(ell)
    kept = {j for _, j in heap}
    on_time = [j for j in edd if j in kept]  # @line L6
    return on_time, late


def is_feasible(p: Sequence[int], d: Sequence[int], jobs) -> bool:
    """True if all the given jobs meet their due dates when run in EDD order from time 0."""
    t = 0
    for j in sorted(jobs, key=lambda j: d[j]):
        t += p[j]
        if t > d[j]:
            return False
    return True


def tardy_count(p: Sequence[int], d: Sequence[int], order: Sequence[int]) -> int:
    """Number of late jobs when the order runs back to back from time 0."""
    t, late = 0, 0
    for j in order:
        t += p[j]
        late += t > d[j]
    return late
