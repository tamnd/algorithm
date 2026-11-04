# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-merge-sort/. The authors are listed in prov/K6SD9E.jsonl.

import heapq
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _Head:
    """The head of the run from tape d, at position j. Equal keys order by tape number."""

    __slots__ = ("x", "d", "j")

    def __init__(self, x: T, d: int, j: int) -> None:
        self.x, self.d, self.j = x, d, j

    def __lt__(self, other: "_Head") -> bool:
        if self.x < other.x:
            return True
        if other.x < self.x:
            return False
        return self.d < other.d


def _merge(runs: list[list[T]]) -> list[T]:
    """A stable merge of runs; on equal keys the run with the smaller index wins."""
    heap = [_Head(r[0], d, 0) for d, r in enumerate(runs) if r]
    heapq.heapify(heap)
    out: list[T] = []
    while heap:
        h = heap[0]
        out.append(h.x)
        if h.j + 1 < len(runs[h.d]):
            heapq.heapreplace(heap, _Head(runs[h.d][h.j + 1], h.d, h.j + 1))
        else:
            heapq.heappop(heap)
    return out


def balanced_merge_sort(f: list[T], m: int = 4, t: int = 4) -> int:
    """Sort f in place with a balanced merge on t simulated tapes and a memory of m items.

    A tape is a list of runs. Precondition: m >= 1 and t >= 4, so that the
    merge order p = t // 2 is at least 2. The sort is stable. Returns the
    number of merge passes, which is ceil(log_p s) for s = ceil(n / m) initial
    runs (0 if s <= 1). Each pass reads and writes all n items; the time in
    memory is O(n log n).
    """
    if m < 1 or t < 4:
        raise ValueError("need m >= 1 and t >= 4")
    p = t // 2  # @line L1
    a: list[list[list[T]]] = [[] for _ in range(p)]
    j = 0  # @line L2
    for start in range(0, len(f), m):  # @line L3
        a[j % p].append(sorted(f[start:start + m]))  # @line L4
        j += 1
    passes = 0
    while sum(len(tape) for tape in a) > 1:  # @line L5
        b: list[list[list[T]]] = [[] for _ in range(p)]
        i = 0  # @line L6
        while any(i < len(tape) for tape in a):  # @line L7
            group = [tape[i] for tape in a if i < len(tape)]
            b[i % p].append(_merge(group))  # @line L8
            i += 1
        a = b  # @line L9
        passes += 1
    f[:] = a[0][0] if a[0] else []  # @line L10
    return passes
