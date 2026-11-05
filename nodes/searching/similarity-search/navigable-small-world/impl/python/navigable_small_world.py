# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/navigable-small-world/. The authors are listed in prov/XDDYQ2.jsonl.

import heapq
import math
import random
from typing import Callable, Hashable, Sequence


class NSW:
    """Navigable small world graph (Malkov et al.): incremental insertion with links to the f nearest found."""

    def __init__(self, d: Callable[[object, object], float] = math.dist, f: int = 3,
                 ef_construction: int = 10, entries: int = 1, seed: int = 0) -> None:
        if f < 1 or entries < 1:
            raise ValueError("f and entries must be at least 1")
        self.d, self.f, self.ef_construction, self.entries = d, f, ef_construction, entries
        self.rng = random.Random(seed)
        self.points: list = []
        self.adj: list[set[int]] = []
        self.evaluations = 0

    def _dist(self, i: int, q) -> float:
        self.evaluations += 1
        return self.d(self.points[i], q)

    def _entry_points(self) -> list[int]:
        n = len(self.points)
        extra = [self.rng.randrange(n) for _ in range(self.entries - 1)]
        return list(dict.fromkeys([0] + extra))

    def search(self, q, k: int, ef: int, entries: Sequence[int] | None = None) -> list[tuple[float, int]]:
        """The k nearest (distance, index) pairs among the nodes the beam search evaluates, nearest first."""
        if not self.points or k < 1:
            return []
        ef = max(ef, k)
        starts = self._entry_points() if entries is None else list(dict.fromkeys(entries))
        visited: set[int] = set()
        cand: list[tuple[float, int]] = []
        best: list[tuple[float, int]] = []  # @line L1
        for e in starts:  # @line L2
            de = self._dist(e, q)
            visited.add(e)
            heapq.heappush(cand, (de, e))  # @line L3
            heapq.heappush(best, (-de, -e))
            if len(best) > ef:
                heapq.heappop(best)
        while cand:  # @line L4
            dc, c = heapq.heappop(cand)  # @line L5
            if len(best) == ef and (dc, c) > (-best[0][0], -best[0][1]):  # @line L6
                break
            for e in sorted(self.adj[c]):  # @line L7
                if e in visited:
                    continue
                visited.add(e)
                de = self._dist(e, q)  # @line L8
                if len(best) < ef or (de, e) < (-best[0][0], -best[0][1]):  # @line L9
                    heapq.heappush(cand, (de, e))
                    heapq.heappush(best, (-de, -e))
                    if len(best) > ef:
                        heapq.heappop(best)
        self.last_visited = visited
        return sorted((-nd, -ni) for nd, ni in best)[:k]  # @line L10

    def insert(self, p) -> int:
        i = len(self.points)
        if i == 0:  # @line L11
            self.points.append(p)
            self.adj.append(set())
            return 0
        found = self.search(p, self.f, max(self.ef_construction, self.f))  # @line L12
        self.points.append(p)
        self.adj.append(set())
        for _, j in found:  # @line L13
            self.adj[i].add(j)
            self.adj[j].add(i)
        return i
