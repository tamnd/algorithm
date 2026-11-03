# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def merge_sort(a: list[T], lo: int = 0, hi: int | None = None) -> None:
    """Sort a[lo:hi] in place, in non-decreasing order. The sort is stable."""
    if hi is None:
        hi = len(a)
    if hi - lo <= 1:  # @line L1
        return
    mid = lo + (hi - lo) // 2  # @line L2
    merge_sort(a, lo, mid)  # @line L3
    merge_sort(a, mid, hi)  # @line L4
    merge(a, lo, mid, hi)  # @line L5


def merge(a: list[T], lo: int, mid: int, hi: int) -> None:
    """Merge the sorted parts a[lo:mid] and a[mid:hi] into one sorted part."""
    b = a[lo:mid]  # @line L6
    i, j, k = 0, mid, lo  # @line L7
    while i < len(b) and j < hi:  # @line L8
        if not a[j] < b[i]:  # @line L9: b[i] <= a[j], with only <
            a[k] = b[i]
            i += 1
        else:
            a[k] = a[j]  # @line L10
            j += 1
        k += 1  # @line L11
    while i < len(b):  # @line L12
        a[k] = b[i]  # @line L13
        i += 1
        k += 1
