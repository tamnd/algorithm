# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-list-intersection-two-pointers/. The authors are listed in prov/ZRYF9N.jsonl.

from typing import TypeVar

T = TypeVar("T", int, float)


def interval_list_intersection_two_pointers(
    a: list[tuple[T, T]], b: list[tuple[T, T]], closed: bool = True
) -> list[tuple[T, T]]:
    """Return the sorted nonempty intersections of an interval of a with one of b.

    Precondition: each list is sorted and its intervals are pairwise disjoint.
    With closed=True the intervals are closed [l, r] (l <= r), and a common end
    point gives a point interval. With closed=False they are half-open [l, r)
    (l < r), and a common end point gives nothing.
    Time O(m + n), extra space O(1) besides the output.
    """
    i, j = 0, 0  # @line L1
    out: list[tuple[T, T]] = []
    while i < len(a) and j < len(b):  # @line L2
        lo = max(a[i][0], b[j][0])  # @line L3
        hi = min(a[i][1], b[j][1])  # @line L4
        if lo < hi or (closed and lo == hi):  # @line L5
            out.append((lo, hi))
        if a[i][1] < b[j][1]:  # @line L6
            i += 1
        else:
            j += 1  # @line L7
    return out  # @line L8
