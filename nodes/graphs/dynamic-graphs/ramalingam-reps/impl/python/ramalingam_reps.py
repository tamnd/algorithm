# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ramalingam-reps/. The authors are listed in prov/Q56GAS.jsonl.

"""Ramalingam-Reps fully dynamic single-source shortest paths.

The graph is directed with positive edge weights. The structure keeps the
distance d(v) from a source s and, for every vertex, the number of tight
in-edges (u, v) with d(u) + w(u, v) = d(v). An insertion or a decrease of a
weight runs Dijkstra's algorithm from the head of the edge, only over the
vertices whose distance drops. A deletion or an increase first finds the
affected vertices, those that lose all tight in-edges, and then runs
Dijkstra's algorithm over them only. Each update takes O(A log A) time,
where A counts the vertices whose distance changes plus their incident
edges. Fully dynamic, deterministic, no amortization.
"""

import heapq

INF = float("inf")


class RamalingamReps:
    def __init__(self, n: int, source: int,
                 edges: list[tuple[int, int, int]] = ()) -> None:
        self.n, self.s = n, source
        self.out: list[dict[int, int]] = [dict() for _ in range(n)]
        self.inn: list[dict[int, int]] = [dict() for _ in range(n)]
        for u, v, w in edges:
            self._check(u, v, w)
            self.out[u][v] = w
            self.inn[v][u] = w
        self.d = self._dijkstra()  # @line L1
        self.cnt = [0] * n
        for v in range(n):
            self._recount(v)

    @staticmethod
    def _check(u: int, v: int, w: int) -> None:
        if w <= 0:
            raise ValueError("weights must be positive")
        if u == v:
            raise ValueError("loops are not allowed")

    def _dijkstra(self) -> list[float]:
        d = [INF] * self.n
        d[self.s] = 0
        pq = [(0, self.s)]
        while pq:
            dx, x = heapq.heappop(pq)
            if dx > d[x]:
                continue
            for z, w in self.out[x].items():
                if dx + w < d[z]:
                    d[z] = dx + w
                    heapq.heappush(pq, (d[z], z))
        return d

    def _recount(self, v: int) -> None:
        dv = self.d[v]
        if v == self.s or dv == INF:
            self.cnt[v] = 0
            return
        self.cnt[v] = sum(1 for u, w in self.inn[v].items() if self.d[u] + w == dv)

    def distance(self, v: int) -> float:
        return self.d[v]  # @line L11

    def set_edge(self, u: int, v: int, w: int | None) -> None:
        """Insert, delete (w is None) or change the weight of the edge (u, v)."""
        old = self.out[u].get(v)
        if w is not None:
            self._check(u, v, w)
        if old is not None and (w is None or w > old):
            self._increase(u, v, old, w)
        elif w is not None and (old is None or w < old):
            self._decrease(u, v, w)

    def insert(self, u: int, v: int, w: int) -> None:
        self.set_edge(u, v, w)

    def delete(self, u: int, v: int) -> None:
        self.set_edge(u, v, None)

    def _decrease(self, u: int, v: int, w: int) -> None:
        self.out[u][v] = w
        self.inn[v][u] = w
        cand = self.d[u] + w  # @line L2
        if cand > self.d[v] or v == self.s or cand == INF:
            return  # the edge was not tight before and is not tight now
        if cand == self.d[v]:
            self.cnt[v] += 1  # a new tight edge; no distance changes
            return
        old = {v: self.d[v]}
        self.d[v] = cand  # @line L3
        pq = [(cand, v)]
        changed = {v}
        while pq:  # @line L4
            dx, x = heapq.heappop(pq)
            if dx > self.d[x]:
                continue
            for z, wz in self.out[x].items():
                if dx + wz < self.d[z]:
                    old.setdefault(z, self.d[z])
                    self.d[z] = dx + wz
                    heapq.heappush(pq, (self.d[z], z))
        self._recount_around(old, True)  # @line L5

    def _increase(self, u: int, v: int, old: int, w: int | None) -> None:
        was_tight = v != self.s and self.d[u] + old == self.d[v] < INF
        if w is None:
            del self.out[u][v], self.inn[v][u]
        else:
            self.out[u][v] = w
            self.inn[v][u] = w
        if not was_tight:
            return
        self.cnt[v] -= 1  # @line L6
        if self.cnt[v] > 0:
            return
        # Phase 1: the affected vertices lose all tight in-edges.
        affected = {v: self.d[v]}
        work = [v]
        while work:  # @line L7
            x = work.pop()
            for z, wz in self.out[x].items():
                if z != self.s and z not in affected and self.d[x] + wz == self.d[z]:
                    self.cnt[z] -= 1
                    if self.cnt[z] == 0:
                        affected[z] = self.d[z]
                        work.append(z)
        # Phase 2: Dijkstra over the affected vertices only.
        pq = []
        for x in affected:  # @line L8
            best = INF
            for y, wy in self.inn[x].items():
                if y not in affected and self.d[y] + wy < best:
                    best = self.d[y] + wy
            self.d[x] = best
            if best < INF:
                pq.append((best, x))
        heapq.heapify(pq)
        while pq:  # @line L9
            dx, x = heapq.heappop(pq)
            if dx > self.d[x]:
                continue
            for z, wz in self.out[x].items():
                if z in affected and dx + wz < self.d[z]:
                    self.d[z] = dx + wz
                    heapq.heappush(pq, (self.d[z], z))
        self._recount_around(affected, False)  # @line L10

    def _recount_around(self, old: dict[int, float], undo_old: bool) -> None:
        """Fix the counts after the vertices in old changed their distance.

        A changed vertex is recounted from its in-edges. For an unchanged
        out-neighbor z of a changed vertex x, only the edge (x, z) can change
        its tightness; its old tightness was already removed from the count
        by phase 1 of a deletion, or is removed here after an insertion.
        """
        for x in old:
            self._recount(x)
        for x, dold in old.items():
            dx = self.d[x]
            for z, w in self.out[x].items():
                if z in old or z == self.s:
                    continue
                dz = self.d[z]
                if dz == INF:
                    continue
                if undo_old and dold + w == dz:
                    self.cnt[z] -= 1
                if dx + w == dz:
                    self.cnt[z] += 1
