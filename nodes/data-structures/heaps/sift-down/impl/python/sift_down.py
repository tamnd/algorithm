# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift-down/. The authors are listed in prov/MFM3MX.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sift_down(a: list[T], i: int, n: int | None = None) -> int:
    """Move a[i] down in the min-heap a[0:n]; return its final index.

    Precondition: in the subtree of i (0-based layout, children 2i + 1 and
    2i + 2), every parent-child pair whose parent is not i is in heap order.
    Postcondition: the subtree of i is a min-heap; no cell outside it changes.
    Cost: at most 2 * floor(log2(n / (i + 1))) comparisons, so O(log n).
    """
    if n is None:
        n = len(a)
    while True:  # @line L1
        left = 2 * i + 1  # @line L2
        if left >= n:  # @line L3
            return i
        c = left  # @line L4
        if left + 1 < n and a[left + 1] < a[left]:  # @line L5
            c = left + 1
        if not a[c] < a[i]:  # @line L6: a[i] <= a[c], with only <
            return i
        a[i], a[c] = a[c], a[i]  # @line L7
        i = c  # @line L8


def extract_min(a: list[T]) -> T:
    """Remove and return a smallest item of the nonempty min-heap a. O(log n)."""
    if not a:
        raise IndexError("extract_min from an empty heap")
    x = a[0]  # @line L9
    last = a.pop()  # @line L10
    if a:  # @line L11
        a[0] = last
        sift_down(a, 0)
    return x  # @line L12


def build_heap(a: list[T]) -> None:
    """Make a a min-heap in place by Floyd's method: sift down each internal node. O(n)."""
    for i in range(len(a) // 2 - 1, -1, -1):
        sift_down(a, i)


def increase_key(a: list[T], i: int, x: T) -> int:
    """Replace a[i] by x, where x is not smaller than a[i], and restore the heap."""
    if x < a[i]:
        raise ValueError("the new key is smaller than the old key")
    a[i] = x
    return sift_down(a, i)
