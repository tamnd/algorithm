# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replacement-selection/. The authors are listed in prov/H4VBFM.jsonl.

import heapq
from typing import Iterable, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _Entry:
    """An item x in the heap, tagged with its run number r and its input position s."""

    __slots__ = ("r", "x", "s")

    def __init__(self, r: int, x: T, s: int) -> None:
        self.r, self.x, self.s = r, x, s

    def __lt__(self, other: "_Entry") -> bool:
        if self.r != other.r:
            return self.r < other.r
        if self.x < other.x:
            return True
        if other.x < self.x:
            return False
        return self.s < other.s


def replacement_selection(f: Iterable[T], p: int) -> list[list[T]]:
    """Cut the input stream f into sorted runs with a heap of p items.

    Precondition: p >= 1. Each run is sorted; equal items keep their input
    order inside a run, and an item never goes to an earlier run than an equal
    item that was read before it. Each run except the last has at least p
    items. On random input the runs have about 2p items on average. The time is
    O(n log p) for n items and the extra space is O(p).
    """
    if p < 1:
        raise ValueError("need p >= 1")
    it = iter(f)
    seq = 0
    heap: list[_Entry] = []  # @line L1
    for x in it:  # @line L2
        heap.append(_Entry(0, x, seq))
        seq += 1
        if len(heap) == p:
            break
    heapq.heapify(heap)
    runs: list[list[T]] = []  # @line L3
    while heap:  # @line L4
        e = heap[0]  # @line L5
        if e.r == len(runs):  # @line L6
            runs.append([])
        runs[e.r].append(e.x)  # @line L7
        y = next(it, _END)  # @line L8
        if y is not _END:
            r = e.r if not y < e.x else e.r + 1  # @line L9
            heapq.heapreplace(heap, _Entry(r, y, seq))  # @line L10
            seq += 1
        else:
            heapq.heappop(heap)  # @line L11
    return runs  # @line L12


_END = object()
