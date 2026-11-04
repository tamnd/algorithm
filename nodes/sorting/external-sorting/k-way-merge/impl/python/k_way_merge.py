# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-way-merge/. The authors are listed in prov/04PNZQ.jsonl.

import heapq
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _Head:
    """The head of run i, at position j. Equal keys order by the run number i."""

    __slots__ = ("x", "i", "j")

    def __init__(self, x: T, i: int, j: int) -> None:
        self.x, self.i, self.j = x, i, j

    def __lt__(self, other: "_Head") -> bool:
        if self.x < other.x:
            return True
        if other.x < self.x:
            return False
        return self.i < other.i


def k_way_merge(runs: list[list[T]]) -> list[T]:
    """Merge k sorted runs into one sorted list with a binary heap of the run heads.

    Precondition: each run is sorted in non-decreasing order. Equal items come
    out in the order of their runs, and in their order inside a run, so the
    merge is stable. With n items in total, the merge uses O(k + n log k)
    comparisons and time, and O(k) extra space besides the output.
    """
    heap: list[_Head] = []  # @line L1
    for i, run in enumerate(runs):  # @line L2
        if run:  # @line L3
            heap.append(_Head(run[0], i, 0))
    heapq.heapify(heap)
    out: list[T] = []  # @line L4
    while heap:  # @line L5
        h = heap[0]  # @line L6
        out.append(h.x)  # @line L7
        if h.j + 1 < len(runs[h.i]):  # @line L8
            heapq.heapreplace(heap, _Head(runs[h.i][h.j + 1], h.i, h.j + 1))
        else:
            heapq.heappop(heap)  # @line L9
    return out  # @line L10
