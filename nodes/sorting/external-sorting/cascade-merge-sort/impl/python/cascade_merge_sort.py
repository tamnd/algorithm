# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascade-merge-sort/. The authors are listed in prov/KG5YAF.jsonl.

import heapq
from collections import deque
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _Head:
    """The head of the run from input d, at position j."""

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
    """Merge sorted runs with a heap. An empty run is a dummy run."""
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


def cascade_distribution(s: int, p: int) -> tuple[int, list[int]]:
    """The smallest level l and the cascade distribution a_1 >= ... >= a_p with sum >= s."""
    level, a = 0, [1] + [0] * (p - 1)
    while sum(a) < s:
        a = [sum(a[:p - i]) for i in range(p)]
        level += 1
    return level, a


def cascade_merge_sort(f: list[T], m: int = 4, t: int = 4) -> int:
    """Sort f in place with a cascade merge on t simulated tapes and a memory of m items.

    A tape is a queue of runs; an empty run is a dummy run. Precondition:
    m >= 1 and t >= 3. The sort is not stable. Returns the number of passes,
    which is the level of the smallest cascade distribution with at least
    s = ceil(n / m) runs. Each pass moves almost all of the data, in merges
    of order t - 1, t - 2, ..., 2; the time in memory is O(n log n).
    """
    if m < 1 or t < 3:
        raise ValueError("need m >= 1 and t >= 3")
    p = t - 1
    runs = [sorted(f[i:i + m]) for i in range(0, len(f), m)]  # @line L1
    if len(runs) <= 1:
        f[:] = runs[0] if runs else []
        return 0
    level, a = cascade_distribution(len(runs), p)  # @line L2
    got = [0] * p
    tape_runs: list[list[list[T]]] = [[] for _ in range(p)]
    for r in runs:  # @line L3
        d = max(range(p), key=lambda i: (a[i] - got[i], -i))
        tape_runs[d].append(r)
        got[d] += 1
    tapes: list[deque[list[T]]] = []
    for d in range(p):  # @line L4
        dummies: list[list[T]] = [[] for _ in range(a[d] - got[d])]
        tapes.append(deque(dummies + tape_runs[d]))
    tapes.append(deque())
    out = p  # @line L5
    passes = 0
    while sum(len(q) for q in tapes) > 1:  # @line L6
        active = [d for d in range(t) if d != out]  # @line L7
        while len(active) >= 2:  # @line L8
            k = min(len(tapes[d]) for d in active)  # @line L9
            for _ in range(k):  # @line L10
                tapes[out].append(_merge([tapes[d].popleft() for d in active]))  # @line L11
            emptied = [d for d in active if not tapes[d]]  # @line L12
            active = [d for d in active if tapes[d]]
            out = emptied[0]
        passes += 1  # @line L13
    last = next(q for q in tapes if q)
    f[:] = last[0]  # @line L14
    assert passes == level
    return passes
