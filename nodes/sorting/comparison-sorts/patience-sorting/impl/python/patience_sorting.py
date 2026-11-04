# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patience-sorting/. The authors are listed in prov/JTB25B.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def deal(a: list[T]) -> list[list[T]]:
    """Deal the items onto piles. Each pile is a list from bottom to top.

    Each item goes on the leftmost pile whose top is greater than it, or on a new pile at the right.
    """
    piles: list[list[T]] = []
    for x in a:
        lo, hi = 0, len(piles)
        while lo < hi:  # the tops are non-decreasing from left to right
            mid = (lo + hi) // 2
            if x < piles[mid][-1]:
                hi = mid
            else:
                lo = mid + 1
        if lo == len(piles):
            piles.append([])
        piles[lo].append(x)
    return piles


def longest_nondecreasing_subsequence(a: list[T]) -> list[T]:
    """Return a longest non-decreasing subsequence of a, using the piles and back links."""
    tops: list[int] = []  # the index in a of the top of each pile
    back: list[int] = [-1] * len(a)
    for idx, x in enumerate(a):
        lo, hi = 0, len(tops)
        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[tops[mid]]:
                hi = mid
            else:
                lo = mid + 1
        back[idx] = tops[lo - 1] if lo > 0 else -1
        if lo == len(tops):
            tops.append(idx)
        else:
            tops[lo] = idx
    out: list[T] = []
    j = tops[-1] if tops else -1
    while j >= 0:
        out.append(a[j])
        j = back[j]
    out.reverse()
    return out


def patience_sorting(a: list[T]) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is stable."""
    piles: list[list[T]] = []  # @line L1
    for x in a:  # @line L2
        lo, hi = 0, len(piles)  # @line L3
        while lo < hi:
            mid = (lo + hi) // 2
            if x < piles[mid][-1]:
                hi = mid
            else:
                lo = mid + 1
        if lo == len(piles):  # @line L4
            piles.append([])
        piles[lo].append(x)  # @line L5

    def less(p: int, q: int) -> bool:
        # Order the piles by their top item, and on a tie by their index.
        x, y = piles[p][-1], piles[q][-1]
        if x < y:
            return True
        if y < x:
            return False
        return p < q

    heap = list(range(len(piles)))

    def sift_down(i: int) -> None:
        while True:
            left, s = 2 * i + 1, i
            if left < len(heap) and less(heap[left], heap[s]):
                s = left
            if left + 1 < len(heap) and less(heap[left + 1], heap[s]):
                s = left + 1
            if s == i:
                return
            heap[i], heap[s] = heap[s], heap[i]
            i = s

    for i in range(len(heap) // 2 - 1, -1, -1):  # @line L6
        sift_down(i)
    for t in range(len(a)):  # @line L7
        p = heap[0]  # @line L8
        a[t] = piles[p].pop()
        if not piles[p]:  # @line L9
            heap[0] = heap[-1]
            heap.pop()
        if heap:
            sift_down(0)
