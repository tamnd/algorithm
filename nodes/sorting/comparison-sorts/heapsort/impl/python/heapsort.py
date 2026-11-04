# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heapsort/. The authors are listed in prov/CSPR1S.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def heapsort(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order.

    The items need only the < operator. The sort is not stable.
    It makes O(n log n) comparisons and uses O(1) extra space.
    """
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):  # @line L1
        sift_down(a, i, n)
    for end in range(n - 1, 0, -1):  # @line L2
        a[0], a[end] = a[end], a[0]  # @line L3
        sift_down(a, 0, end)  # @line L4


def sift_down(a: list[T], i: int, m: int) -> None:
    """Move a[i] down in the max-heap a[0:m] until no child is larger.

    Precondition: the subtrees of the children of i are max-heaps.
    Cost: O(log m) comparisons and swaps.
    """
    while 2 * i + 1 < m:  # @line L5
        c = 2 * i + 1  # @line L6
        if c + 1 < m and a[c] < a[c + 1]:  # @line L7
            c += 1
        if not a[i] < a[c]:  # @line L8: a[i] >= a[c]
            return
        a[i], a[c] = a[c], a[i]  # @line L9
        i = c  # @line L10
