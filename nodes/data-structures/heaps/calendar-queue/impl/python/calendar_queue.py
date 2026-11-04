# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calendar-queue/. The authors are listed in prov/CZJZK8.jsonl.

import bisect
import heapq
import math
from typing import Generic, Optional, TypeVar

E = TypeVar("E")


class CalendarQueue(Generic[E]):
    """Brown's calendar queue: a min-priority queue of events with real times.

    There are N buckets of width w. An event with time t has the virtual
    bucket vb(t) = floor(t / w) and lives in the bucket vb(t) mod N, which is
    kept sorted by (time, arrival). V is a virtual bucket with vb(t) >= V for
    every event in the queue. extract_min scans at most one year of N
    buckets from V, then falls back to a direct search. With resize=True,
    N doubles when the size exceeds 2N and halves when it falls below N/2,
    and w is estimated from the gaps between the first events.
    """

    def __init__(self, nbuckets: int = 2, width: float = 1.0, resize: bool = True) -> None:
        if nbuckets < 1 or not width > 0:
            raise ValueError("nbuckets must be at least 1 and width positive")
        self.n_buckets = nbuckets
        self.width = width
        self.resize_on = resize
        self.buckets: list[list[tuple[float, int, E]]] = [[] for _ in range(nbuckets)]
        self.size = 0
        self.v = 0
        self.seq = 0
        self.resizes = 0

    def __len__(self) -> int:
        return self.size

    def _vb(self, t: float) -> int:
        return math.floor(t / self.width)

    def insert(self, e: E, t: float) -> None:
        vb = self._vb(t)
        i = vb % self.n_buckets  # @line L1
        bisect.insort(self.buckets[i], (t, self.seq, e))  # @line L2
        self.seq += 1
        if self.size == 0 or vb < self.v:  # @line L3
            self.v = vb
        self.size += 1
        if self.resize_on and self.size > 2 * self.n_buckets:  # @line L4
            self._resize(2 * self.n_buckets)

    def _take(self, i: int) -> tuple[E, float]:
        t, _, e = self.buckets[i].pop(0)
        self.size -= 1
        if self.resize_on and self.n_buckets > 2 and self.size < self.n_buckets // 2:
            self._resize(self.n_buckets // 2)
        return e, t

    def peek_min(self) -> tuple[E, float]:
        if self.size == 0:
            raise IndexError("peek_min from an empty queue")
        best = min(b[0] for b in self.buckets if b)
        return best[2], best[0]

    def extract_min(self) -> tuple[E, float]:
        if self.size == 0:  # @line L5
            raise IndexError("extract_min from an empty queue")
        n = self.n_buckets
        for _ in range(n):  # @line L6
            b = self.buckets[self.v % n]
            if b and self._vb(b[0][0]) == self.v:  # @line L7
                return self._take(self.v % n)  # @line L8 @line L9
            self.v += 1  # @line L10
        best: Optional[tuple[float, int, E]] = None
        best_i = -1
        for i, b in enumerate(self.buckets):  # @line L11
            if b and (best is None or b[0] < best):
                best, best_i = b[0], i
        assert best is not None
        self.v = self._vb(best[0])  # @line L12
        return self._take(best_i)

    def _new_width(self, events: list[tuple[float, int, E]]) -> float:
        front = heapq.nsmallest(25, events)  # @line L14
        gaps = [b[0] - a[0] for a, b in zip(front, front[1:])]
        if not gaps:
            return self.width
        avg = sum(gaps) / len(gaps)
        kept = [g for g in gaps if g <= 2 * avg]
        w = 3 * sum(kept) / len(kept) if kept else 0.0  # @line L15
        return w if w > 0 else self.width

    def _resize(self, new_n: int) -> None:
        events = [x for b in self.buckets for x in b]  # @line L13
        self.width = self._new_width(events)
        self.n_buckets = new_n
        self.buckets = [[] for _ in range(new_n)]
        for x in events:
            self.buckets[self._vb(x[0]) % new_n].append(x)
        for b in self.buckets:
            b.sort()
        self.v = min((self._vb(x[0]) for x in events), default=0)
        self.resizes += 1

    def check_invariant(self) -> None:
        count = 0
        for i, b in enumerate(self.buckets):
            assert b == sorted(b)
            for t, _, _ in b:
                vb = self._vb(t)
                assert vb % self.n_buckets == i
                assert vb >= self.v
                count += 1
        assert count == self.size
