# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-permutation/. The authors are listed in prov/V6C3MR.jsonl.

from collections.abc import Iterator
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def next_permutation(a: list[T]) -> bool:
    """Rearrange a into the next arrangement in lexicographic order.

    Return True if a had a successor. If a was the last arrangement
    (non-increasing), sort it into the first one and return False.
    Repeated items are allowed: each distinct arrangement comes once.
    """
    n = len(a)
    i = n - 2  # @line L1
    while i >= 0 and not a[i] < a[i + 1]:  # @line L2: a[i] >= a[i + 1]
        i -= 1
    if i < 0:  # @line L3
        a.reverse()  # @line L4
        return False  # @line L5
    j = n - 1  # @line L6
    while not a[i] < a[j]:  # @line L7: a[j] <= a[i]
        j -= 1
    a[i], a[j] = a[j], a[i]  # @line L8
    lo, hi = i + 1, n - 1  # @line L9
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1
        hi -= 1
    return True  # @line L10


def lexicographic_permutations(items: list[T]) -> Iterator[list[T]]:
    """Yield a copy of each distinct arrangement of items, in lexicographic order."""
    a = sorted(items)
    while True:
        yield list(a)
        if not next_permutation(a):
            return
