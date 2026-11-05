# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-interval-dp/. The authors are listed in prov/YZT11N.jsonl.
"""Weighted interval scheduling by dynamic programming over right ends.

Each interval is (l, r, w). kind is "closed" ([l, r], l <= r), "half-open"
([l, r), l < r) or "open" ((l, r), l < r). Closed intervals that touch,
r_i = l_j, conflict; half-open and open ones do not.
"""

from bisect import bisect_left, bisect_right
from typing import Sequence, Tuple

Job = Tuple[float, float, float]


def weighted_interval_dp(jobs: Sequence[Job], kind: str = "closed") -> tuple[float, list[int]]:
    """Return (best total weight, indices of an optimal set in increasing right end)."""
    if kind not in ("closed", "half-open", "open"):
        raise ValueError("kind must be closed, half-open or open")
    order = sorted(range(len(jobs)), key=lambda k: (jobs[k][1], k))  # @line L1
    n = len(order)
    right = [jobs[k][1] for k in order]
    find = bisect_left if kind == "closed" else bisect_right
    # p[j] = number of intervals that end in time for the j-th one (1-based j)
    p = [0] * (n + 1)
    for j in range(1, n + 1):  # @line L2
        p[j] = find(right, jobs[order[j - 1]][0])  # @line L2
    m = [0.0] * (n + 1)  # @line L3
    for j in range(1, n + 1):  # @line L4
        w = jobs[order[j - 1]][2]
        m[j] = max(m[j - 1], w + m[p[j]])  # @line L5
    chosen: list[int] = []  # @line L6
    j = n
    while j > 0:  # @line L7
        w = jobs[order[j - 1]][2]
        if w + m[p[j]] >= m[j - 1]:  # @line L8
            chosen.append(order[j - 1])
            j = p[j]
        else:
            j -= 1  # @line L9
    chosen.reverse()
    return m[n], chosen  # @line L10
