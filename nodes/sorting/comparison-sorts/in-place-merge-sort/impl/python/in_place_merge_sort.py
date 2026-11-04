# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/in-place-merge-sort/. The authors are listed in prov/JZA43S.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def _reverse(a: list[T], i: int, j: int) -> None:
    j -= 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def rotate(a: list[T], i: int, m: int, j: int) -> None:
    """Turn a[i:m] + a[m:j] into a[m:j] + a[i:m] with three reversals."""
    if i == m or m == j:  # @line L16
        return
    _reverse(a, i, m)
    _reverse(a, m, j)
    _reverse(a, i, j)


def _lower_bound(a: list[T], lo: int, hi: int, x: T) -> int:
    while lo < hi:  # @line L17
        m = (lo + hi) // 2
        if a[m] < x:
            lo = m + 1
        else:
            hi = m
    return lo  # @line L18


def _upper_bound(a: list[T], lo: int, hi: int, x: T) -> int:
    while lo < hi:  # @line L19
        m = (lo + hi) // 2
        if x < a[m]:
            hi = m
        else:
            lo = m + 1
    return lo  # @line L20


def merge_in_place(a: list[T], lo: int, mid: int, hi: int) -> None:
    """Stably merge the sorted runs a[lo:mid] and a[mid:hi] with no buffer."""
    if lo == mid or mid == hi:  # @line L6
        return
    if hi - lo == 2:  # @line L7
        if a[mid] < a[lo]:
            a[lo], a[mid] = a[mid], a[lo]
        return
    if mid - lo >= hi - mid:  # @line L8
        cut1 = lo + (mid - lo) // 2  # @line L9
        cut2 = _lower_bound(a, mid, hi, a[cut1])
    else:  # @line L10
        cut2 = mid + (hi - mid) // 2  # @line L11
        cut1 = _upper_bound(a, lo, mid, a[cut2])
    rotate(a, cut1, mid, cut2)  # @line L12
    new_mid = cut1 + (cut2 - mid)  # @line L13
    merge_in_place(a, lo, cut1, new_mid)  # @line L14
    merge_in_place(a, new_mid, cut2, hi)  # @line L15


def _sort(a: list[T], lo: int, hi: int) -> None:
    if hi - lo < 2:  # @line L1
        return
    mid = (lo + hi) // 2  # @line L2
    _sort(a, lo, mid)  # @line L3
    _sort(a, mid, hi)  # @line L4
    merge_in_place(a, lo, mid, hi)  # @line L5


def in_place_merge_sort(a: list[T]) -> None:
    """Sort a in place, stably, in non-decreasing order.

    Top-down merge sort whose merge uses no buffer: it splits the longer run
    at its middle item, finds the matching cut in the other run by binary
    search, swaps the two middle blocks with a rotation, and merges the two
    smaller pairs of runs that result.
    Cost: O(n log n) comparisons, O(n log² n) moves and time, O(log n) stack.
    """
    _sort(a, 0, len(a))
