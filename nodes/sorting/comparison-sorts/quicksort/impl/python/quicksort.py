# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quicksort/. The authors are listed in prov/5TYMK3.jsonl.

import sys
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

# The recursion is n - 1 calls deep on a sorted input (the worst case of the page).
# Python stops at 1000 calls by default, so this module raises the limit.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))


def quicksort(a: list[T], lo: int = 0, hi: int | None = None) -> None:
    """Sort a[lo:hi] in place, in non-decreasing order. The pivot is the last item."""
    if hi is None:
        hi = len(a)
    if hi - lo <= 1:  # @line L1
        return
    p = partition(a, lo, hi)  # @line L2
    quicksort(a, lo, p)  # @line L3
    quicksort(a, p + 1, hi)  # @line L4


def partition(a: list[T], lo: int, hi: int) -> int:
    """Lomuto partition of a[lo:hi] around x = a[hi - 1]. Return the final index p of x.

    After the call, a[lo:p] holds the items <= x, a[p] == x, and a[p + 1:hi] holds the items > x.
    """
    x = a[hi - 1]  # @line L5
    i = lo  # @line L6
    for j in range(lo, hi - 1):  # @line L7
        if not x < a[j]:  # @line L8: a[j] <= x, with only <
            a[i], a[j] = a[j], a[i]  # @line L9
            i += 1  # @line L10
    a[i], a[hi - 1] = a[hi - 1], a[i]  # @line L11
    return i  # @line L12
