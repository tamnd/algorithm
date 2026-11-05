# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thorup-zwick-oracle/. The authors are listed in prov/Q2T1JE.jsonl.

import heapq
import math
import random


def _check_weight(w) -> None:
    if isinstance(w, bool) or not isinstance(w, (int, float)):
        raise ValueError(f"weight {w!r} is not a number")
    if not (0 <= w < math.inf):
        raise ValueError(f"weight {w!r} is negative or not finite")


class ThorupZwickOracle:
    """Approximate distance oracle of Thorup and Zwick for undirected graphs.

    The graph has vertices 0..n-1 and undirected edges (u, v, w) with finite
    nonnegative weights. A query returns an estimate e with
    d(u, v) <= e <= (2k - 1) d(u, v), and math.inf exactly when u and v are
    in different components. With k = 1 the answers are exact.

    levels, if given, is the list [A_1, ..., A_{k-1}] of nested vertex sets;
    otherwise they are sampled with probability n^(-1/k) using seed.
    """

    def __init__(self, n: int, edges, k: int, seed: int = 0, levels=None):
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        self.n, self.k = n, k
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            _check_weight(w)
            adj[u].append((v, w))
            adj[v].append((u, w))
        self._adj = adj

        # @line L1
        A = [set(range(n))]
        if levels is None:
            rng = random.Random(seed)
            prob = n ** (-1.0 / k) if n > 0 else 0.0
            # @line L2
            for _ in range(1, k):
                A.append({v for v in sorted(A[-1]) if rng.random() < prob})
        else:
            if len(levels) != k - 1:
                raise ValueError("levels must hold k - 1 sets")
            for S in levels:
                S = set(S)
                if not S <= A[-1]:
                    raise ValueError("levels must be nested")
                A.append(S)
        A.append(set())
        self.levels = A

        # @line L3
        self.dist_level = []  # dist_level[i][v] = d(A_i, v)
        self.pivot = []  # pivot[i][v] = a nearest vertex of A_i, or None
        for i in range(k):
            d, p = self._nearest(A[i])
            self.dist_level.append(d)
            self.pivot.append(p)
        # @line L4
        self.dist_level.append([math.inf] * n)
        self.pivot.append([None] * n)

        # @line L5
        self.bunch = [dict() for _ in range(n)]  # bunch[v][w] = d(w, v)
        for i in range(k):
            bound = self.dist_level[i + 1]
            for w in sorted(A[i] - A[i + 1]):
                # @line L6
                for x, dx in self._grow_cluster(w, bound):
                    # @line L7
                    self.bunch[x][w] = dx
        # @line L8

    def _nearest(self, sources):
        """Multi-source Dijkstra: distance to and a nearest vertex of sources."""
        dist = [math.inf] * self.n
        piv = [None] * self.n
        heap = [(0, s, s) for s in sorted(sources)]
        heapq.heapify(heap)
        while heap:
            d, s, x = heapq.heappop(heap)
            if dist[x] <= d:
                continue
            dist[x], piv[x] = d, s
            for y, w in self._adj[x]:
                if d + w < dist[y]:
                    heapq.heappush(heap, (d + w, s, y))
        return dist, piv

    def _grow_cluster(self, w, bound):
        """Dijkstra from w that admits x with key D only if D < bound[x]."""
        done = {}
        if not 0 < bound[w]:
            return []
        heap = [(0, w)]
        best = {w: 0}
        while heap:
            d, x = heapq.heappop(heap)
            if x in done:
                continue
            done[x] = d
            for y, wt in self._adj[x]:
                nd = d + wt
                if y not in done and nd < bound[y] and nd < best.get(y, math.inf):
                    best[y] = nd
                    heapq.heappush(heap, (nd, y))
        return list(done.items())

    def query(self, u: int, v: int) -> float:
        """Return an estimate of d(u, v) with stretch at most 2k - 1."""
        # @line L9
        w, i = u, 0
        # @line L10
        while w not in self.bunch[v]:
            # @line L11
            i += 1
            # @line L12
            u, v = v, u
            # @line L13
            if i == self.k or self.pivot[i][u] is None:
                return math.inf
            # @line L14
            w = self.pivot[i][u]
        # @line L15
        return self.dist_level[i][u] + self.bunch[v][w]

    def size(self) -> int:
        """Number of stored bunch entries, the main part of the space."""
        return sum(len(b) for b in self.bunch)
