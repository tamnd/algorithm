# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift-up/. The authors are listed in prov/9J3JJD.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sift_up(a: list[T], i: int) -> int:
    """Move a[i] up until a is a binary min-heap; return its final index.

    Precondition: a is a min-heap in the 0-based array layout (the parent of
    index j is (j - 1) // 2), except that a[i] may be smaller than its parent,
    and the parent of i is at most each child of i. This holds after a[i] is
    decreased, or after a new item is appended at index i = len(a) - 1.
    Cost: at most floor(log2(i + 1)) comparisons and swaps, so O(log n).
    """
    while i > 0:  # @line L1
        p = (i - 1) // 2  # @line L2
        if not a[i] < a[p]:  # @line L3: a[p] <= a[i], with only <
            return i
        a[i], a[p] = a[p], a[i]  # @line L4
        i = p  # @line L5
    return i  # @line L6


def heap_insert(a: list[T], x: T) -> int:
    """Insert x into the min-heap a; return the index where x ends. O(log n)."""
    a.append(x)  # @line L7
    return sift_up(a, len(a) - 1)  # @line L8


def decrease_key(a: list[T], i: int, x: T) -> int:
    """Replace a[i] by x, where x is not larger than a[i], and restore the heap."""
    if a[i] < x:
        raise ValueError("the new key is larger than the old key")
    a[i] = x
    return sift_up(a, i)
