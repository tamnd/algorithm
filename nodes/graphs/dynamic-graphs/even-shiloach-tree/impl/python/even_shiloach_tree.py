# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/even-shiloach-tree/. The authors are listed in prov/VS2KBW.jsonl.

"""Even-Shiloach tree: single-source distances up to a depth D under deletions.

Directed graph with positive integer edge weights (1 for the classic
unweighted case). Each vertex v keeps a level l(v), which equals the distance
from the source when that distance is at most D, and infinity otherwise. Each
vertex also keeps a scan pointer into its list of incoming edges; edges before
the pointer are known not to give l(v). Levels only grow, by one at a time,
so the total time over all deletions is O(m D). Deletions only (decremental);
deterministic; the bound is a total, so per deletion it is amortized.
"""

import heapq

INF = float("inf")


class EvenShiloachTree:
    def __init__(self, n: int, edges: list[tuple[int, int, int]], source: int, depth: int) -> None:
        self.n, self.s, self.depth = n, source, depth
        self.tail: list[int] = []
        self.head: list[int] = []
        self.w: list[int] = []
        self.alive: list[bool] = []
        self.inc: list[list[int]] = [[] for _ in range(n)]
        self.out: list[list[int]] = [[] for _ in range(n)]
        for u, v, w in edges:
            if w <= 0:
                raise ValueError("weights must be positive integers")
            e = len(self.tail)
            self.tail.append(u)
            self.head.append(v)
            self.w.append(w)
            self.alive.append(True)
            self.inc[v].append(e)
            self.out[u].append(e)
        # L1: initial levels by Dijkstra, cut at the depth bound.
        lev = [INF] * n
        lev[source] = 0
        heap = [(0, source)]
        while heap:
            d, x = heapq.heappop(heap)
            if d > lev[x]:
                continue
            for e in self.out[x]:
                y, nd = self.head[e], d + self.w[e]
                if nd <= depth and nd < lev[y]:
                    lev[y] = nd
                    heapq.heappush(heap, (nd, y))
        self.level = lev  # @line L1
        self.ptr = [0] * n
        for v in range(n):
            if v != source and lev[v] != INF:
                self._settle_pointer(v)

    def _attains(self, e: int, x: int) -> bool:
        return self.alive[e] and self.level[self.tail[e]] + self.w[e] == self.level[x]

    def _settle_pointer(self, x: int) -> bool:
        """Advance the scan pointer of x to an edge that gives l(x)."""
        lst = self.inc[x]
        p = self.ptr[x]
        while p < len(lst) and not self._attains(lst[p], x):
            p += 1  # @line L5
        self.ptr[x] = p
        return p < len(lst)

    def delete(self, e: int) -> None:
        """Delete the edge with id e (ids follow the order of the input list)."""
        if not self.alive[e]:
            return
        self.alive[e] = False  # @line L2
        queue = [self.head[e]]  # @line L3
        while queue:
            x = queue.pop()  # @line L4
            if x == self.s or self.level[x] == INF:
                continue
            if self._settle_pointer(x):
                continue
            # No incoming edge gives l(x): raise the level by one.
            self.level[x] += 1  # @line L6
            self.ptr[x] = 0
            if self.level[x] > self.depth:
                self.level[x] = INF  # @line L7
            else:
                queue.append(x)
            for f in self.out[x]:
                if self.alive[f]:
                    queue.append(self.head[f])  # @line L8

    def distance(self, v: int) -> float:
        return self.level[v]  # @line L9

    def parent(self, v: int) -> int:
        """The tail of the tree edge into v, or -1 at the source or if unreachable."""
        if v == self.s or self.level[v] == INF:
            return -1
        return self.tail[self.inc[v][self.ptr[v]]]
