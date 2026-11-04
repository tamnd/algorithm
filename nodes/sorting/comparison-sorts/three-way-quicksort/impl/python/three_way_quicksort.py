# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-way-quicksort/. The authors are listed in prov/JD10F7.jsonl.

import sys
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

# The pivot is the middle item, so some inputs still give a recursion about
# n / 2 calls deep. Python stops at 1000 calls by default, so this module
# raises the limit.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))


def three_way_quicksort(a: list[T], lo: int = 0, hi: int | None = None) -> None:
    """Sort a[lo:hi] in place, with Dijkstra's three-way partition around the middle item."""
    if hi is None:
        hi = len(a)
    if hi - lo <= 1:  # @line L1
        return
    lt, gt = partition3(a, lo, hi)
    three_way_quicksort(a, lo, lt)  # @line L10
    three_way_quicksort(a, gt, hi)  # @line L11


def partition3(a: list[T], lo: int, hi: int) -> tuple[int, int]:
    """Rearrange a[lo:hi] around v, the old middle item, and return (lt, gt).

    After the call, a[lo:lt] < v, a[lt:gt] == v and a[gt:hi] > v.
    """
    v = a[lo + (hi - lo) // 2]  # @line L2
    lt, i, gt = lo, lo, hi  # @line L3
    while i < gt:  # @line L4
        if a[i] < v:  # @line L5
            a[lt], a[i] = a[i], a[lt]  # @line L6
            lt += 1
            i += 1
        elif v < a[i]:  # @line L7
            gt -= 1  # @line L8
            a[i], a[gt] = a[gt], a[i]
        else:
            i += 1  # @line L9
    return lt, gt
