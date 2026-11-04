# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoare-partition/. The authors are listed in prov/HR9MYC.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def hoare_partition(a: list[T], lo: int, hi: int) -> int:
    """Partition a[lo..hi] (both ends included) around the pivot a[lo].

    Precondition: lo < hi. Returns j with lo <= j < hi such that each item of
    a[lo..j] is <= each item of a[j+1..hi]. The pivot is not always at j.
    Cost: at most hi - lo + 3 comparisons and (hi - lo + 1) // 2 exchanges.
    """
    x = a[lo]  # @line L1
    i, j = lo - 1, hi + 1  # @line L2
    while True:  # @line L3
        j -= 1  # @line L4
        while x < a[j]:  # repeat until a[j] <= x
            j -= 1
        i += 1  # @line L5
        while a[i] < x:  # repeat until a[i] >= x
            i += 1
        if i < j:  # @line L6
            a[i], a[j] = a[j], a[i]
        else:
            return j  # @line L7


def quicksort(a: list[T]) -> None:
    """Sort a in place with quicksort over hoare_partition, recursing on the smaller side."""
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            j = hoare_partition(a, lo, hi)
            if j - lo < hi - j:
                stack.append((j + 1, hi))
                hi = j
            else:
                stack.append((lo, j))
                lo = j + 1
