# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyphase-merge-sort/. The authors are listed in prov/VP4CSM.jsonl.

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


def perfect_distribution(s: int, p: int) -> tuple[int, list[int]]:
    """The smallest level l and the perfect distribution a_1 >= ... >= a_p with sum >= s."""
    level, a = 0, [1] + [0] * (p - 1)
    while sum(a) < s:
        a = [a[0] + a[i] for i in range(1, p)] + [a[0]]
        level += 1
    return level, a


def polyphase_merge_sort(f: list[T], m: int = 4, t: int = 4) -> int:
    """Sort f in place with a polyphase merge on t simulated tapes and a memory of m items.

    A tape is a queue of runs; an empty run is a dummy run. Precondition:
    m >= 1 and t >= 3. The sort is not stable. Returns the number of merge
    phases, which is the level of the smallest perfect distribution with at
    least s = ceil(n / m) runs, about log s / log phi_p for the growth rate
    phi_p of the distribution. Each phase moves only part of the data; the
    time in memory is O(n log n).
    """
    if m < 1 or t < 3:
        raise ValueError("need m >= 1 and t >= 3")
    p = t - 1
    runs = [sorted(f[i:i + m]) for i in range(0, len(f), m)]  # @line L1
    if len(runs) <= 1:
        f[:] = runs[0] if runs else []
        return 0
    level, a = perfect_distribution(len(runs), p)  # @line L2
    want = a[:]  # @line L3
    got = [0] * p
    tape_runs: list[list[list[T]]] = [[] for _ in range(p)]
    for r in runs:  # @line L4
        d = max(range(p), key=lambda i: (want[i] - got[i], -i))
        tape_runs[d].append(r)
        got[d] += 1
    tapes: list[deque[list[T]]] = []
    for d in range(p):  # @line L5
        dummies: list[list[T]] = [[] for _ in range(want[d] - got[d])]
        tapes.append(deque(dummies + tape_runs[d]))
    tapes.append(deque())
    out = p  # @line L6
    phases = 0
    while sum(len(q) for q in tapes) > 1:  # @line L7
        inputs = [d for d in range(t) if d != out]
        k = min(len(tapes[d]) for d in inputs)  # @line L8
        for _ in range(k):  # @line L9
            tapes[out].append(_merge([tapes[d].popleft() for d in inputs]))  # @line L10
        out = next(d for d in inputs if not tapes[d])  # @line L11
        phases += 1
    last = next(q for q in tapes if q)
    f[:] = last[0]  # @line L12
    assert phases == level
    return phases
