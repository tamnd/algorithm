# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-search/. The authors are listed in prov/V34DA8.jsonl.

from collections.abc import Sequence
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def exponential_search(a: Sequence[T], x: T) -> int:
    """Return the smallest index i with a[i] == x, or -1 when x is not in a.

    The list a must be sorted in non-decreasing order. The search tests
    a[0], a[1], a[3], a[7], ... until one is not less than x, then runs a
    binary search on the last gap. For a key whose lower bound is l >= 1 it
    makes at most 2 * floor(lg l) + 3 comparisons.
    """
    n = len(a)
    b = 1  # @line L1
    while b <= n and a[b - 1] < x:  # @line L2
        b *= 2  # @line L3
    lo, hi = b // 2, min(b - 1, n)  # @line L4
    while lo < hi:  # @line L5
        mid = lo + (hi - lo) // 2  # @line L6
        if a[mid] < x:  # @line L7
            lo = mid + 1
        else:  # @line L8
            hi = mid
    if lo < n and a[lo] == x:  # @line L9
        return lo
    return -1  # @line L10
