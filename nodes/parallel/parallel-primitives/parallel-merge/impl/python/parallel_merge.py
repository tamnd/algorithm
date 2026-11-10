# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-merge/. The authors are listed in prov/GDEWS9.jsonl.

"""P-MERGE: merge two sorted ranges by a median split and two parallel recursive calls.

The recursion is the fork-join program of the page; the two calls of one level would be
spawned in parallel, so the code returns the work (the sum over all calls) and the span
(the cost of the longest chain of calls). One call costs 2 units (the split choice and the
write) plus one unit for each probe of the binary search; a call with no items costs 1.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Cost:
    work: int
    span: int


def lower_bound(t: list[Any], lo: int, hi: int, x: Any) -> tuple[int, int]:
    """Return (the least r in [lo, hi] with r = hi or x <= t[r], the number of probes)."""
    probes = 0
    while lo < hi:
        mid = (lo + hi) // 2
        probes += 1
        if t[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo, probes


def p_merge(t: list[Any], p1: int, r1: int, p2: int, r2: int, a: list[Any], p3: int) -> Cost:
    """Merge the sorted ranges t[p1:r1] and t[p2:r2] into a[p3 : p3 + (r1 - p1) + (r2 - p2)].

    The ranges must not overlap the output range. Returns the work and span of the call.
    """
    n1, n2 = r1 - p1, r2 - p2  # @line L1
    if n1 < n2:  # @line L2: make the first range the longer one
        p1, r1, p2, r2 = p2, r2, p1, r1  # @line L3
        n1, n2 = n2, n1  # @line L4
    if n1 == 0:  # @line L5: both ranges are empty
        return Cost(1, 1)
    q1 = (p1 + r1) // 2  # @line L6: the median of the longer range
    q2, probes = lower_bound(t, p2, r2, t[q1])  # @line L7
    q3 = p3 + (q1 - p1) + (q2 - p2)  # @line L8
    a[q3] = t[q1]  # @line L9
    left = p_merge(t, p1, q1, p2, q2, a, p3)  # @line L10: spawn
    right = p_merge(t, q1 + 1, r1, q2, r2, a, q3 + 1)  # @line L11
    # @line L12: sync
    own = 2 + probes
    return Cost(own + left.work + right.work, own + max(left.span, right.span))


def p_merge_sort(a: list[Any], p: int, r: int, b: list[Any], s: int) -> Cost:
    """Sort a[p:r] into b[s : s + r - p] (CLRS 3rd edition, P-MERGE-SORT). Returns work and span."""
    n = r - p
    if n == 0:
        return Cost(1, 1)
    if n == 1:
        b[s] = a[p]
        return Cost(1, 1)
    t: list[Any] = [None] * n
    q = (p + r) // 2
    q2 = q - p
    left = p_merge_sort(a, p, q, t, 0)  # spawn
    right = p_merge_sort(a, q, r, t, q2)
    # sync
    m = p_merge(t, 0, q2, q2, n, b, s)
    return Cost(1 + left.work + right.work + m.work, 1 + max(left.span, right.span) + m.span)
