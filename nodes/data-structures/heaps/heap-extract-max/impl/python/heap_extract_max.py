# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-extract-max/. The authors are listed in prov/4GYGY9.jsonl.

from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def max_heapify(a: list[T], n: int, i: int) -> None:
    """Sift a[i] down in a[0:n]. All edges of a[0:n] must hold except the ones out of i."""
    while True:  # @line L7
        left, right, m = 2 * i + 1, 2 * i + 2, i  # @line L8
        if left < n and a[m] < a[left]:  # @line L9
            m = left
        if right < n and a[m] < a[right]:  # @line L10
            m = right
        if m == i:  # @line L11
            return
        a[i], a[m] = a[m], a[i]  # @line L12
        i = m


def heap_extract_max(a: list[T]) -> T:
    """Remove and return the largest key of the max-heap a (0-based). O(log n) time.

    a must satisfy a[(j - 1) // 2] >= a[j] for each j >= 1; it stays a max-heap.
    """
    if len(a) < 1:  # @line L1
        raise IndexError("heap underflow")
    top = a[0]  # @line L2
    last = a.pop()  # @line L4
    if a:
        a[0] = last  # @line L3
        max_heapify(a, len(a), 0)  # @line L5
    return top  # @line L6
