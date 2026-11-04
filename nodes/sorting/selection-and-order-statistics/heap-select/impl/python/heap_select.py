# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-select/. The authors are listed in prov/0YXEH5.jsonl.

from typing import Iterable, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sift_down(h: list[T], i: int, m: int) -> None:
    """Restore the max-heap order of h[0 .. m - 1] below index i.

    Assumes that the subtrees of the children of i are max-heaps. Moves h[i]
    down, swapping it with its larger child, until no child is larger.
    """
    while True:  # @line L11
        c = 2 * i + 1  # @line L12
        if c >= m:  # @line L13
            return
        if c + 1 < m and h[c] < h[c + 1]:  # @line L14
            c += 1
        if not h[i] < h[c]:  # @line L15
            return
        h[i], h[c] = h[c], h[i]  # @line L16
        i = c


def heap_select(a: Iterable[T], k: int) -> list[T]:
    """Return the k smallest items of a, in increasing order.

    Reads a once and keeps a max-heap of the k smallest items seen so far,
    so it works on a stream. It takes O(n log k) time and O(k) extra space.
    If a has fewer than k items, all of them are returned, sorted.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    it = iter(a)
    h: list[T] = []
    if k == 0:
        return h
    for x in it:  # @line L1
        h.append(x)
        if len(h) == k:
            break
    m = len(h)
    for i in range(m // 2 - 1, -1, -1):  # @line L2
        sift_down(h, i, m)
    for x in it:  # @line L3
        if x < h[0]:  # @line L4
            h[0] = x  # @line L5
            sift_down(h, 0, m)  # @line L6
    for j in range(m - 1, 0, -1):  # @line L7
        h[0], h[j] = h[j], h[0]  # @line L8
        sift_down(h, 0, j)  # @line L9
    return h  # @line L10
