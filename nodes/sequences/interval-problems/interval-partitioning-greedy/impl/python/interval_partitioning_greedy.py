# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-partitioning-greedy/. The authors are listed in prov/48TJ7A.jsonl.
"""Greedy interval partitioning by start time with a min-heap of free times.

kind is "closed" ([l, r], l <= r: intervals that share an end point conflict),
"half-open" ([l, r), l < r) or "open" ((l, r), l < r); for the last two,
intervals that only touch are compatible.
"""

import heapq
from typing import Sequence, Tuple

Interval = Tuple[float, float]


def interval_partitioning_greedy(intervals: Sequence[Interval], kind: str = "half-open") -> tuple[int, list[int]]:
    """Return (k, res): k resources and res[j] in 1..k for each interval j.

    Intervals on one resource are pairwise disjoint, and k is the depth.
    """
    if kind not in ("closed", "half-open", "open"):
        raise ValueError("kind must be closed, half-open or open")
    closed = kind == "closed"
    n = len(intervals)
    order = sorted(range(n), key=lambda j: intervals[j][0])  # @line L1
    heap: list[tuple[float, int]] = []  # @line L2
    k = 0
    res = [0] * n
    for j in order:  # @line L3
        l, r = intervals[j]
        if heap and (heap[0][0] < l if closed else heap[0][0] <= l):  # @line L4
            _, c = heapq.heappop(heap)  # @line L5
        else:
            k += 1  # @line L6
            c = k
        res[j] = c  # @line L7
        heapq.heappush(heap, (r, c))
    return k, res  # @line L8
