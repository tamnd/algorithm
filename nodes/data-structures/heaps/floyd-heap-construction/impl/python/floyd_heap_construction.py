# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-heap-construction/. The authors are listed in prov/ADHNWH.jsonl.

from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def max_heapify(a: list[T], n: int, i: int) -> None:
    """Sift a[i] down in the max-heap a[0:n]. The subtrees of the children of i must be max-heaps."""
    while True:  # @line L3
        left, right, m = 2 * i + 1, 2 * i + 2, i  # @line L4
        if left < n and a[m] < a[left]:  # @line L5
            m = left
        if right < n and a[m] < a[right]:  # @line L6
            m = right
        if m == i:  # @line L7
            return
        a[i], a[m] = a[m], a[i]  # @line L8
        i = m  # @line L9


def floyd_heap_construction(a: list[T]) -> None:
    """Rearrange a in place into a max-heap: a[(j - 1) // 2] >= a[j] for each j >= 1.

    Runs in O(n) time with fewer than 2n comparisons and O(1) extra space.
    """
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):  # @line L1
        max_heapify(a, n, i)  # @line L2
