# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-merge-sort/. The authors are listed in prov/V917JH.jsonl.

import heapq
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def blocks(length: int, b: int) -> int:
    """The number of blocks of b items that hold a run of the given length."""
    return -(-length // b)


class _Head:
    """The head of run i at position j. Equal keys order by the run number."""

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
    """Merge sorted runs into one sorted run. Equal items keep the order of their runs."""
    heap = [_Head(run[0], i, 0) for i, run in enumerate(runs) if run]
    heapq.heapify(heap)
    out: list[T] = []
    while heap:
        h = heap[0]
        out.append(h.x)
        if h.j + 1 < len(runs[h.i]):
            heapq.heapreplace(heap, _Head(runs[h.i][h.j + 1], h.i, h.j + 1))
        else:
            heapq.heappop(heap)
    return out


def external_merge_sort(f: list[T], m: int = 16, b: int = 4) -> int:
    """Sort the list f in place as an external merge sort with a memory of m items and blocks of b items.

    The disk is simulated: a run is a list, and each read or write of a block
    of a run counts as one I/O. Precondition: b >= 1 and m >= 3 * b, so that
    the fan-in k = m // b - 1 is at least 2. Returns the number of block I/Os. When b divides m, this number is at most
    2 * ceil(n / b) * (1 + passes) with passes = ceil(log_k ceil(n / m)).
    The in-memory time is O(n log n). The sort is stable.
    """
    if b < 1 or m < 3 * b:
        raise ValueError("need b >= 1 and m >= 3 * b")
    k = m // b - 1  # @line L1
    ios = 0
    runs: list[list[T]] = []  # @line L2
    for start in range(0, len(f), m):  # @line L3
        load = f[start:start + m]  # @line L4
        ios += blocks(len(load), b)
        load.sort()  # @line L5: a stable sort in memory
        ios += blocks(len(load), b)
        runs.append(load)
    while len(runs) > 1:  # @line L6
        merged: list[list[T]] = []  # @line L7
        for g in range(0, len(runs), k):  # @line L8
            group = runs[g:g + k]
            if len(group) == 1:  # @line L9: a single run is kept, with no I/O
                merged.append(group[0])
                continue
            ios += sum(blocks(len(r), b) for r in group)  # @line L10
            out = k_way_merge(group)
            ios += blocks(len(out), b)
            merged.append(out)
        runs = merged  # @line L11
    f[:] = runs[0] if runs else []  # @line L12
    return ios
