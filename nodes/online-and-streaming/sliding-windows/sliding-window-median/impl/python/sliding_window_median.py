# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-median/. The authors are listed in prov/08ESMB.jsonl.
"""Sliding window median of a count-based window: two heaps with lazy deletion."""

import heapq
from collections import deque
from typing import Any, Iterable, Iterator, List, Tuple


class SlidingMedian:
    """Lower median of the last w items.

    lo is a max-heap (stored as negated keys) of the smaller half and hi a
    min-heap of the larger half. A key is (value, index), so equal values
    are distinct keys. An entry is dead when its index is below head.
    """

    SLACK = 8

    def __init__(self, w: int) -> None:
        if w < 1:
            raise ValueError("window size must be at least 1")
        self.w = w
        self.t = 0
        self.head = 1
        self.window: deque = deque()  # live items, oldest first
        self.lo: List[Tuple[Any, int]] = []  # entries (-value, -index)
        self.hi: List[Tuple[Any, int]] = []  # entries (value, index)
        self.n_lo = 0
        self.n_hi = 0

    # keys of the heap tops; valid only when the heap is not empty
    def _top_lo(self) -> Tuple[Any, int]:
        v, i = self.lo[0]
        return (-v, -i)

    def _prune(self) -> None:
        lo, hi = self.lo, self.hi
        while lo and -lo[0][1] < self.head:  # @line L12
            heapq.heappop(lo)
        while hi and hi[0][1] < self.head:  # @line L12
            heapq.heappop(hi)

    def _compact(self) -> None:
        if len(self.lo) > 2 * self.n_lo + self.SLACK:  # @line L13
            self.lo = [e for e in self.lo if -e[1] >= self.head]
            heapq.heapify(self.lo)
        if len(self.hi) > 2 * self.n_hi + self.SLACK:  # @line L13
            self.hi = [e for e in self.hi if e[1] >= self.head]
            heapq.heapify(self.hi)

    def step(self, x: Any) -> Any:
        """Add item x, evict the item that leaves, and return the lower median."""
        self.t += 1  # @line L1
        k = (x, self.t)
        self.window.append(x)
        if self.n_lo == 0 or k < self._top_lo():  # @line L2
            heapq.heappush(self.lo, (-x, -self.t))
            self.n_lo += 1
        else:  # @line L3
            heapq.heappush(self.hi, k)
            self.n_hi += 1
        if self.t > self.w:  # @line L4
            e = (self.window.popleft(), self.t - self.w)  # @line L5
            self.head = self.t - self.w + 1
            if e <= self._top_lo():  # @line L6
                self.n_lo -= 1
            else:
                self.n_hi -= 1
        self._prune()  # @line L7
        if self.n_lo > self.n_hi + 1:  # @line L8
            v, i = heapq.heappop(self.lo)
            heapq.heappush(self.hi, (-v, -i))
            self.n_lo -= 1
            self.n_hi += 1
        elif self.n_lo < self.n_hi:  # @line L9
            v, i = heapq.heappop(self.hi)
            heapq.heappush(self.lo, (-v, -i))
            self.n_lo += 1
            self.n_hi -= 1
        self._prune()  # @line L10
        self._compact()
        return self._top_lo()[0]  # @line L11

    def upper(self) -> Any:
        """Upper median: the top of hi for an even count, else the lower median."""
        if self.n_hi == self.n_lo:
            return self.hi[0][0]
        return self._top_lo()[0]

    def check_invariant(self) -> None:
        live_lo = sorted((-v, -i) for v, i in self.lo if -i >= self.head)
        live_hi = sorted((v, i) for v, i in self.hi if i >= self.head)
        assert len(live_lo) == self.n_lo and len(live_hi) == self.n_hi
        assert self.n_hi <= self.n_lo <= self.n_hi + 1
        assert self.n_lo + self.n_hi == len(self.window)
        if live_lo and live_hi:
            assert live_lo[-1] < live_hi[0]
        if self.lo:
            assert self._top_lo() == live_lo[-1]
        if self.hi:
            assert self.hi[0] == live_hi[0]
        assert len(self.lo) <= 2 * self.n_lo + self.SLACK
        assert len(self.hi) <= 2 * self.n_hi + self.SLACK


def sliding_medians(xs: Iterable[Any], w: int) -> Iterator[Any]:
    """Yield the lower median of the last w items after each item."""
    s = SlidingMedian(w)
    for x in xs:
        yield s.step(x)
