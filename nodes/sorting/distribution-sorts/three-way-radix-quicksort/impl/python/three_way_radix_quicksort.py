# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-way-radix-quicksort/. The authors are listed in prov/PC1TJR.jsonl.
import random


def _c(s: str, d: int) -> int:
    """The character code of s at index d, or -1 when s has ended."""
    return ord(s[d]) if d < len(s) else -1


def _insertion_sort(a: list[str], lo: int, hi: int, d: int) -> None:
    """Sort a[lo:hi] by the suffixes from index d; the strings share d characters."""
    for i in range(lo + 1, hi):
        x = a[i]
        j = i
        while j > lo and x[d:] < a[j - 1][d:]:
            a[j] = a[j - 1]
            j -= 1
        a[j] = x


def _sort(a: list[str], lo: int, hi: int, d: int, m: int) -> None:
    while hi - lo > m:  # @line L1
        v = _c(a[lo], d)  # @line L2
        lt, gt, i = lo, hi - 1, lo + 1  # @line L3
        while i <= gt:  # @line L4
            t = _c(a[i], d)  # @line L5
            if t < v:  # @line L6
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif t > v:  # @line L7
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:  # @line L8
                i += 1
        _sort(a, lo, lt, d, m)  # @line L9
        _sort(a, gt + 1, hi, d, m)  # @line L10
        if v == -1:  # @line L11
            return
        lo, hi, d = lt, gt + 1, d + 1  # @line L12
    _insertion_sort(a, lo, hi, d)  # @line L13


def three_way_radix_quicksort(a: list[str], cutoff: int = 15, seed: int | None = None, shuffle: bool = True) -> list[str]:
    """Sort the list a of strings in lexicographic order, in place, and return it.

    Precondition: the items are str and cutoff >= 1. The sort is not stable.
    After the shuffle the expected cost is O(n log n + D) character reads,
    where D is the total length of the distinguishing prefixes.
    """
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")
    if shuffle:
        random.Random(seed).shuffle(a)
    _sort(a, 0, len(a), 0, cutoff)
    return a
