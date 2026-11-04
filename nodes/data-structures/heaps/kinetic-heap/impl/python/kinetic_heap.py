# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kinetic-heap/. The authors are listed in prov/NF6DCE.jsonl.

"""Kinetic binary min-heap over items whose keys are linear functions of time.

The key of item e at time t is a + b * t. All times are exact fractions. Each
parent-child edge has a certificate "parent <= child" with a failure time, and
the event queue holds the certificates in order of failure time.
"""

import heapq
from fractions import Fraction
from typing import Dict, Hashable, List, Optional, Tuple, Union

Num = Union[int, Fraction]
INF = None  # a certificate that never fails


class KineticHeap:
    """Binary min-heap kept in an array; keys move as a + b * t."""

    def __init__(self, now: Num = 0) -> None:
        self.now = Fraction(now)
        self.heap: List[Hashable] = []
        self.pos: Dict[Hashable, int] = {}
        self.line: Dict[Hashable, Tuple[Fraction, Fraction]] = {}
        self.queue: List[Tuple[Fraction, int, int]] = []  # (failure time, version, child index)
        self.cert: Dict[int, Tuple[Optional[Fraction], int]] = {}  # child index -> (time, version)
        self.version = 0
        self.events = 0

    def __len__(self) -> int:
        return len(self.heap)

    def value(self, e: Hashable, t: Optional[Fraction] = None) -> Fraction:
        a, b = self.line[e]
        return a + b * (self.now if t is None else t)

    def _order(self, e: Hashable) -> Tuple[Fraction, Fraction]:
        """The order just after now: value at now, then slope."""
        a, b = self.line[e]
        return (a + b * self.now, b)

    # -- certificates -------------------------------------------------------

    def _cert(self, i: int) -> None:
        """Compute the certificate of the edge from parent(i) to i."""
        if i <= 0 or i >= len(self.heap):
            self.cert.pop(i, None)
            return
        ap, bp = self.line[self.heap[(i - 1) // 2]]
        ac, bc = self.line[self.heap[i]]
        self.version += 1
        if bp > bc:  # @line L1
            fail: Optional[Fraction] = (ac - ap) / (bp - bc)
            assert fail is not None and fail >= self.now
            heapq.heappush(self.queue, (fail, self.version, i))  # @line L2
        else:
            fail = INF
        self.cert[i] = (fail, self.version)

    def _recert_around(self, i: int) -> None:
        """Recompute every certificate that involves position i."""
        for j in (i, 2 * i + 1, 2 * i + 2):
            self._cert(j)

    def _swap(self, i: int, j: int) -> None:
        h = self.heap
        h[i], h[j] = h[j], h[i]
        self.pos[h[i]], self.pos[h[j]] = i, j

    # -- kinetic operations -------------------------------------------------

    def _next(self) -> Optional[Tuple[Fraction, int]]:
        """The earliest certificate that is still current, or None."""
        while self.queue:
            t, ver, i = self.queue[0]
            c = self.cert.get(i)
            if c is not None and c[1] == ver:
                return t, i
            heapq.heappop(self.queue)
        return None

    def advance(self, t: Num) -> None:
        """Move time forward to t and process every event on the way."""
        t = Fraction(t)
        if t < self.now:
            raise ValueError("time cannot go back")
        while True:
            nxt = self._next()
            if nxt is None or nxt[0] > t:  # @line L3
                break
            tau, i = nxt
            heapq.heappop(self.queue)
            self.now = tau  # @line L4
            self.events += 1
            p = (i - 1) // 2
            self._swap(p, i)  # @line L5
            for j in (p, i, 2 * p + 1, 2 * p + 2, 2 * i + 1, 2 * i + 2):  # @line L6
                self._cert(j)
        self.now = t  # @line L7

    def find_min(self) -> Hashable:
        """Return the item of smallest key at the current time."""
        if not self.heap:
            raise IndexError("the heap is empty")
        return self.heap[0]  # @line L8

    def _sift(self, i: int, touched: List[int]) -> int:
        """Move the item at i up or down to its place in the order just after now."""
        h = self.heap
        while i > 0 and self._order(h[i]) < self._order(h[(i - 1) // 2]):
            p = (i - 1) // 2
            self._swap(i, p)
            touched.append(p)
            i = p
        while True:
            m = i
            for c in (2 * i + 1, 2 * i + 2):
                if c < len(h) and self._order(h[c]) < self._order(h[m]):
                    m = c
            if m == i:
                return i
            self._swap(i, m)
            touched.append(m)
            i = m

    def _recert_all(self, touched: List[int]) -> None:
        """Recompute the certificates of the edges at every touched position."""
        for j in set(touched):
            self._recert_around(j)

    def insert(self, e: Hashable, a: Num, b: Num) -> None:
        """Insert item e with the key a + b * t."""
        if e in self.pos:
            raise KeyError("the item is already in the heap")
        self.line[e] = (Fraction(a), Fraction(b))
        self.heap.append(e)  # @line L9
        self.pos[e] = len(self.heap) - 1
        touched = [len(self.heap) - 1]
        self._sift(len(self.heap) - 1, touched)
        self._recert_all(touched)  # @line L10

    def delete(self, e: Hashable) -> None:
        """Remove item e."""
        i = self.pos.pop(e)
        last = self.heap.pop()
        del self.line[e]
        n = len(self.heap)
        self.cert.pop(n, None)
        if i < n:
            self.heap[i] = last  # @line L11
            self.pos[last] = i
            touched = [i]
            self._sift(i, touched)
            self._recert_all(touched)  # @line L12

    def delete_min(self) -> Hashable:
        """Remove and return the item of smallest key now."""
        e = self.find_min()
        self.delete(e)
        return e

    def check_invariant(self) -> None:
        """Heap order just after now, and a current certificate for every edge."""
        h = self.heap
        assert len(self.pos) == len(h) == len(self.line)
        for i, e in enumerate(h):
            assert self.pos[e] == i
            if i > 0:
                assert not self._order(e) < self._order(h[(i - 1) // 2])
                ap, bp = self.line[h[(i - 1) // 2]]
                ac, bc = self.line[e]
                want = (ac - ap) / (bp - bc) if bp > bc else INF
                assert self.cert[i][0] == want
                if want is not None:
                    assert want > self.now
        assert set(self.cert) == set(range(1, len(h)))
