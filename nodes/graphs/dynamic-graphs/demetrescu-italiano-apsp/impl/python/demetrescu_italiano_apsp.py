# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/demetrescu-italiano-apsp/. The authors are listed in prov/5HVW8R.jsonl.

"""Fully dynamic all-pairs shortest paths with locally shortest paths.

This is the core of the Demetrescu-Italiano method: vertex updates with a
cleanup phase and a fixup phase over a store of paths. Old paths stay in the
store until a cleanup removes them. The smoothing step of the paper, which
gives the amortized bound, is not implemented.
"""

import heapq
import math


class _Path:
    """A path x..y. l is the path without its last edge, r without its first."""

    __slots__ = ("pid", "x", "y", "w", "mask", "l", "r", "last", "lext", "rext")

    def __init__(self, pid, x, y, w, mask, l, r, last):
        self.pid = pid
        self.x, self.y = x, y
        self.w, self.mask = w, mask  # weight, and a tie-break bit per edge
        self.l, self.r = l, r
        self.last = last if last is not None else self  # the last edge as a path
        self.lext = {}  # paths P with P.l is self
        self.rext = {}  # paths P with P.r is self


class DynamicAPSP:
    """Directed graph on vertices 0..n-1 with nonnegative edge weights."""

    def __init__(self, n):
        self.n = n
        self._next = 0
        self._triv = [self._new(v, v, 0, 0, None, None) for v in range(n)]
        self.weights = {}  # (a, b) -> weight of the edge from a to b
        self.edges = {}  # (a, b) -> edge path
        self.store = {}  # (l.pid, r.pid) -> path, for paths with at least two edges
        self.cand = {}  # (x, y) -> heap of (w, mask, pid, path) of stored paths
        self.alive = set()  # pids of stored paths
        self.sp = {}  # (x, y) -> the shortest path from x to y
        self.lstar = {}  # pid of s -> {pid: P} for registered P with P.r is s
        self.rstar = {}  # pid of s -> {pid: P} for registered P with P.l is s

    def _new(self, x, y, w, mask, l, r, last=None):
        p = _Path(self._next, x, y, w, mask, l, r, last)
        self._next += 1
        return p

    def _add(self, p):
        self.alive.add(p.pid)
        heapq.heappush(self.cand.setdefault((p.x, p.y), []), (p.w, p.mask, p.pid, p))

    def _register(self, p):
        self.sp[(p.x, p.y)] = p
        self.lstar.setdefault(p.r.pid, {})[p.pid] = p
        self.rstar.setdefault(p.l.pid, {})[p.pid] = p

    def _unregister(self, p):
        del self.sp[(p.x, p.y)]
        self.lstar.get(p.r.pid, {}).pop(p.pid, None)
        self.rstar.get(p.l.pid, {}).pop(p.pid, None)

    def update(self, v, changes):
        """Vertex update. changes maps (a, b) with v in (a, b) to a weight, or None to delete."""
        for (a, b), w in changes.items():
            if v not in (a, b) or a == b:
                raise ValueError("each changed edge must touch v and not be a loop")
            if w is not None and (w < 0 or math.isnan(w)):
                raise ValueError("weights must be nonnegative")
        self._cleanup(v)  # @line L1
        for (a, b), w in changes.items():  # @line L2
            if w is None:
                self.weights.pop((a, b), None)
            else:
                self.weights[(a, b)] = w
        self._fixup(v)  # @line L3

    def _cleanup(self, v):
        queue = [p for (a, b), p in self.edges.items() if v in (a, b)]  # @line L4
        for p in queue:
            del self.edges[(p.x, p.y)]
        while queue:  # @line L5
            p = queue.pop()
            if p.pid not in self.alive:
                continue
            self.alive.discard(p.pid)  # @line L6
            if p.l is not None and p.l.l is not None:
                self.store.pop((p.l.pid, p.r.pid), None)
                p.l.lext.pop(p.pid, None)
                p.r.rext.pop(p.pid, None)
            if self.sp.get((p.x, p.y)) is p:  # @line L7
                self._unregister(p)
            queue.extend(p.lext.values())  # @line L8
            queue.extend(p.rext.values())

    def _fixup(self, v):
        for (a, b), w in self.weights.items():  # @line L9
            if v in (a, b) and (a, b) not in self.edges:
                p = self._new(a, b, w, 1 << self._next, self._triv[a], self._triv[b])
                self.edges[(a, b)] = p
                self._add(p)
        heap = []  # @line L10
        for h in self.cand.values():
            while h and h[0][2] not in self.alive:
                heapq.heappop(h)
            if h:
                heap.append(h[0])
        heapq.heapify(heap)
        settled = set()
        while heap:  # @line L11
            _, _, _, p = heapq.heappop(heap)  # @line L12
            if p.pid not in self.alive or (p.x, p.y) in settled:  # @line L13
                continue
            settled.add((p.x, p.y))  # @line L14
            old = self.sp.get((p.x, p.y))
            if old is p:  # @line L15
                continue
            if old is not None:  # @line L16
                self._unregister(old)
            self._register(p)  # @line L17
            for q in list(self.lstar.get(p.l.pid, {}).values()):  # @line L18
                if q.x != p.y:
                    self._combine(q, p, heap)
            for q in list(self.rstar.get(p.r.pid, {}).values()):  # @line L19
                if q.y != p.x:
                    self._combine(p, q, heap)

    def _combine(self, a, b, heap):
        """Store the path a.x .. b.y with l = a and r = b, if it is new."""
        k = (a.pid, b.pid)
        if k in self.store:  # @line L20
            return
        e = b.last
        p = self._new(a.x, b.y, a.w + e.w, a.mask + e.mask, a, b, e)  # @line L21
        self.store[k] = p  # @line L22
        a.lext[p.pid] = p
        b.rext[p.pid] = p
        self._add(p)
        heapq.heappush(heap, (p.w, p.mask, p.pid, p))  # @line L23

    def insert_edge(self, a, b, w):
        self.update(a, {(a, b): w})

    def delete_edge(self, a, b):
        self.update(a, {(a, b): None})

    def dist(self, x, y):
        """The weight of a shortest path from x to y, or math.inf."""
        if x == y:
            return 0
        p = self.sp.get((x, y))
        return math.inf if p is None else p.w

    def path(self, x, y):
        """The vertices of a shortest path from x to y, or None."""
        if x == y:
            return [x]
        p = self.sp.get((x, y))
        if p is None:
            return None
        out = []
        while p.l is not None:
            out.append(p.y)
            p = p.l
        out.append(p.x)
        return out[::-1]
