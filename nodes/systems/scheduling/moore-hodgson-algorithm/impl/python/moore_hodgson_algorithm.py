# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moore-hodgson-algorithm/. The authors are listed in prov/KEY8Q5.jsonl.

import heapq
from typing import Sequence


def edd_order(d: Sequence[int], jobs: Sequence[int]) -> list[int]:
    """The jobs in order of nondecreasing due date, ties by index."""
    return sorted(jobs, key=lambda j: (d[j], j))


def all_on_time(p: Sequence[int], d: Sequence[int], jobs: Sequence[int]) -> bool:
    """True when the jobs, run back to back from time 0 in EDD order, all meet their due dates."""
    t = 0
    for j in edd_order(d, jobs):
        t += p[j]
        if t > d[j]:
            return False
    return True


def moore_hodgson_algorithm(p: Sequence[int], d: Sequence[int]) -> tuple[list[int], list[int]]:
    """Moore-Hodgson for 1||sum U_j, with a max-heap on the processing times.

    Return (on_time, late). The on-time jobs are in EDD order and all meet their
    due dates when run first, back to back from time 0. The late jobs follow in
    any order. The number of late jobs is the minimum possible.
    Cost: O(n log n) time and O(n) space.
    """
    if len(p) != len(d):
        raise ValueError("p and d must have the same length")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    jobs = edd_order(d, range(len(p)))  # @line L1
    heap: list[tuple[int, int]] = []  # @line L2 (-p_j, -j): the longest job on top, ties to the later index
    kept: set[int] = set()
    late: list[int] = []
    t = 0
    for k in jobs:  # @line L3
        heapq.heappush(heap, (-p[k], -k))  # @line L4
        kept.add(k)
        t += p[k]
        if t > d[k]:  # @line L5
            neg_p, neg_j = heapq.heappop(heap)  # @line L6
            kept.remove(-neg_j)
            late.append(-neg_j)  # @line L7
            t += neg_p
    return edd_order(d, kept), late  # @line L8


def moore_original(p: Sequence[int], d: Sequence[int]) -> list[int]:
    """Moore's 1968 form, for tests: run the kept jobs in EDD order, find the first
    late job, remove the longest job up to it, and repeat. O(n^2) time."""
    kept = edd_order(d, range(len(p)))
    while True:
        t = 0
        first_late = -1
        for i, j in enumerate(kept):
            t += p[j]
            if t > d[j]:
                first_late = i
                break
        if first_late < 0:
            return kept
        longest = max(range(first_late + 1), key=lambda i: (p[kept[i]], kept[i]))
        del kept[longest]
