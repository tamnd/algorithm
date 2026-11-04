# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/introsort/. The authors are listed in prov/S172EG.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

SMALL = 16


def _insertion_sort(a: list[T], lo: int, hi: int) -> None:
    for i in range(lo + 1, hi):
        x = a[i]
        j = i
        while j > lo and x < a[j - 1]:
            a[j] = a[j - 1]
            j -= 1
        a[j] = x


def _sift_down(a: list[T], lo: int, i: int, size: int) -> None:
    x = a[lo + i]
    while True:
        c = 2 * i + 1
        if c >= size:
            break
        if c + 1 < size and a[lo + c] < a[lo + c + 1]:
            c += 1
        if not x < a[lo + c]:
            break
        a[lo + i] = a[lo + c]
        i = c
    a[lo + i] = x


def _heapsort(a: list[T], lo: int, hi: int) -> None:
    size = hi - lo
    for i in range(size // 2 - 1, -1, -1):
        _sift_down(a, lo, i, size)
    for end in range(size - 1, 0, -1):
        a[lo], a[lo + end] = a[lo + end], a[lo]
        _sift_down(a, lo, 0, end)


def _median_index(a: list[T], i: int, j: int, k: int) -> int:
    if a[j] < a[i]:
        i, j = j, i
    if a[k] < a[j]:
        j = k
        if a[j] < a[i]:
            j = i
    return j


def hoare_partition(a: list[T], p: int, r: int) -> int:
    """Split a[p..r] at j, p <= j < r, so that a[p..j] <= x <= a[j+1..r], x = a[p]."""
    x = a[p]  # @line L11
    i, j = p - 1, r + 1
    while True:  # @line L12
        j -= 1  # @line L13
        while x < a[j]:
            j -= 1
        i += 1  # @line L14
        while a[i] < x:
            i += 1
        if i < j:  # @line L15
            a[i], a[j] = a[j], a[i]
        else:
            return j


def _intro(a: list[T], lo: int, hi: int, d: int) -> None:
    while hi - lo > SMALL:  # @line L2
        if d == 0:  # @line L3
            _heapsort(a, lo, hi)
            return
        d -= 1  # @line L4
        m = _median_index(a, lo, (lo + hi) // 2, hi - 1)  # @line L5
        a[lo], a[m] = a[m], a[lo]  # @line L6
        j = hoare_partition(a, lo, hi - 1)  # @line L7
        if j + 1 - lo < hi - j - 1:  # @line L8
            _intro(a, lo, j + 1, d)
            lo = j + 1
        else:  # @line L9
            _intro(a, j + 1, hi, d)
            hi = j + 1
    _insertion_sort(a, lo, hi)  # @line L10


def introsort(a: list[T]) -> None:
    """Sort a in place in non-decreasing order.

    Quicksort with a median-of-three pivot and Hoare partitioning, which
    switches a range to heapsort when the recursion is deeper than 2 lg n,
    and sorts ranges of at most 16 items by insertion sort.
    Cost: O(n log n) worst case, O(log n) stack. Not stable.
    """
    n = len(a)
    if n > 1:  # @line L1
        _intro(a, 0, n, 2 * (n.bit_length() - 1))
