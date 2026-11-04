# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift-down-sink/. The authors are listed in prov/RCFB8N.jsonl.

from collections.abc import Callable
from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sink(less: Callable[[int, int], bool], exch: Callable[[int, int], None], k: int, n: int) -> None:
    """Sink the item at position k of a 1-based max-heap of n items.

    less(i, j) says whether the item at position i is smaller than the item at
    position j, and exch(i, j) swaps them. Precondition: the subtrees of the
    children 2k and 2k + 1 are max-heaps. Postcondition: the subtree of k is a
    max-heap. Cost: at most 2 * floor(log2(n / k)) calls of less.
    """
    while 2 * k <= n:  # @line L1
        j = 2 * k  # @line L2
        if j < n and less(j, j + 1):  # @line L3
            j += 1
        if not less(k, j):  # @line L4
            break
        exch(k, j)  # @line L5
        k = j  # @line L6


def del_max(pq: list[T]) -> T:
    """Remove and return a largest item of the max-heap pq[1:]; pq[0] is not used. O(log n)."""
    n = len(pq) - 1
    if n < 1:
        raise IndexError("del_max from an empty priority queue")

    def less(i: int, j: int) -> bool:
        return pq[i] < pq[j]

    def exch(i: int, j: int) -> None:
        pq[i], pq[j] = pq[j], pq[i]

    top = pq[1]  # @line L7
    exch(1, n)  # @line L8
    n -= 1
    sink(less, exch, 1, n)  # @line L9
    pq.pop()  # @line L10: drop the old maximum from the last cell
    return top  # @line L11


def heapsort(a: list[T]) -> None:
    """Sort a in place in non-decreasing order with heap construction by sink and the sortdown.

    The heap uses positions 1 to n, and position p is the cell a[p - 1].
    Cost: fewer than 2n lg n + 2n comparisons, O(1) extra space.
    """

    def less(i: int, j: int) -> bool:
        return a[i - 1] < a[j - 1]

    def exch(i: int, j: int) -> None:
        a[i - 1], a[j - 1] = a[j - 1], a[i - 1]

    n = len(a)
    for k in range(n // 2, 0, -1):  # @line L12
        sink(less, exch, k, n)
    while n > 1:  # @line L13
        exch(1, n)  # @line L14
        n -= 1
        sink(less, exch, 1, n)  # @line L15
