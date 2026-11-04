# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-delete/. The authors are listed in prov/8TNZV0.jsonl.

from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sift_up(a: list[T], i: int) -> None:
    while i > 0 and a[(i - 1) // 2] < a[i]:  # @line L9
        p = (i - 1) // 2
        a[i], a[p] = a[p], a[i]  # @line L10
        i = p  # @line L11


def max_heapify(a: list[T], n: int, i: int) -> None:
    while True:  # @line L12
        left, right, m = 2 * i + 1, 2 * i + 2, i  # @line L13
        if left < n and a[m] < a[left]:  # @line L14
            m = left
        if right < n and a[m] < a[right]:  # @line L15
            m = right
        if m == i:  # @line L16
            return
        a[i], a[m] = a[m], a[i]  # @line L17
        i = m


def heap_delete(a: list[T], i: int) -> T:
    """Remove and return a[i] from the max-heap a (0-based). O(log n) time."""
    if not 0 <= i < len(a):  # @line L1
        raise IndexError("index out of range")
    x = a[i]  # @line L2
    last = a.pop()  # @line L3 @line L4
    if i < len(a):  # @line L5
        a[i] = last
        if i > 0 and a[(i - 1) // 2] < a[i]:  # @line L6
            sift_up(a, i)
        else:
            max_heapify(a, len(a), i)  # @line L7
    return x  # @line L8
