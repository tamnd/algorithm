# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oscillating-sort/. The authors are listed in prov/P385WS.jsonl.

import heapq
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _Head:
    """The head of input d at position j; with up=False the largest key comes first."""

    __slots__ = ("x", "d", "j", "up")

    def __init__(self, x: T, d: int, j: int, up: bool) -> None:
        self.x, self.d, self.j, self.up = x, d, j, up

    def __lt__(self, other: "_Head") -> bool:
        a, b = (self.x, other.x) if self.up else (other.x, self.x)
        if a < b:
            return True
        if b < a:
            return False
        return self.d < other.d


def _merge(seqs: list[list[T]], up: bool) -> list[T]:
    """Merge sequences that are sorted in the direction up (non-decreasing) or down."""
    heap = [_Head(s[0], d, 0, up) for d, s in enumerate(seqs) if s]
    heapq.heapify(heap)
    out: list[T] = []
    while heap:
        h = heap[0]
        out.append(h.x)
        if h.j + 1 < len(seqs[h.d]):
            heapq.heapreplace(heap, _Head(seqs[h.d][h.j + 1], h.d, h.j + 1, up))
        else:
            heapq.heappop(heap)
    return out


def oscillating_sort(f: list[T], m: int = 4, t: int = 5) -> int:
    """Sort f in place with an oscillating sort on t simulated tapes and a memory of m items.

    Tape 0 is the input; tapes 1 .. t-1 are work tapes that are read backward,
    so each one is a stack of runs, and no tape is ever rewound. Precondition:
    m >= 1 and t >= 4, so that the merge order p = t - 2 is at least 2.
    Returns the number of merge levels, ceil(log_p s) for s = ceil(n / m)
    initial runs (0 if s <= 1). Each item is merged once per level; the time
    in memory is O(n log n).
    """
    if m < 1 or t < 4:
        raise ValueError("need m >= 1 and t >= 4")
    p = t - 2
    s = -(-len(f) // m)  # @line L1
    tapes: list[list[list[T]]] = [[] for _ in range(t)]
    pos = 0

    def build(n: int, x: int, up: bool) -> int:
        nonlocal pos
        if n == 1:  # @line L3
            run = sorted(f[pos:pos + m], reverse=not up)  # @line L4
            pos += m
            tapes[x].append(run)
            return 0
        others = [y for y in range(1, t) if y != x]  # @line L5
        parts = [n // p + (1 if i < n % p else 0) for i in range(p)]
        used = [(k, y) for k, y in zip(parts, others) if k > 0]
        depth = 0
        for k, y in used:  # @line L6
            depth = max(depth, build(k, y, not up))
        backward = [tapes[y].pop()[::-1] for _, y in used]  # @line L7
        tapes[x].append(_merge(backward, up))  # @line L8
        return depth + 1

    if s == 0:
        return 0
    levels = build(s, 1, True)  # @line L2
    f[:] = tapes[1].pop()
    assert not any(tapes)
    return levels
