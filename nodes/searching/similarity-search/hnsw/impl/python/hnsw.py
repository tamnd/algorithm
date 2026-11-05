# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hnsw/. The authors are listed in prov/ZFDM4P.jsonl.

import heapq
import math
import random
from collections.abc import Callable, Sequence

Vector = Sequence[float]


def euclidean(x: Vector, y: Vector) -> float:
    return math.sqrt(sum((a - b) * (a - b) for a, b in zip(x, y)))


class HNSW:
    """Hierarchical navigable small world graph (Malkov and Yashunin).

    Each element gets a top level floor(-ln U * mL) with mL = 1/ln M, so Pr[level >= j] = M^-j.
    Layer l > 0 keeps at most M links per element and layer 0 at most m_max0.
    """

    def __init__(
        self,
        dist: Callable[[Vector, Vector], float] = euclidean,
        M: int = 8,
        ef_construction: int = 32,
        m_max0: int | None = None,
        heuristic: bool = True,
        rng: random.Random | None = None,
    ) -> None:
        if M < 2:
            raise ValueError("M must be at least 2")
        self.dist = dist
        self.M = M
        self.m_max0 = m_max0 if m_max0 is not None else 2 * M
        self.ef_c = ef_construction
        self.mL = 1 / math.log(M)
        self.heuristic = heuristic
        self.rng = rng if rng is not None else random.Random()
        self.points: list[Vector] = []
        self.links: list[list[list[int]]] = []  # links[i][l] = neighbors of i at layer l
        self.entry: int | None = None
        self.top = -1

    def _d(self, q: Vector, i: int) -> float:
        return self.dist(q, self.points[i])

    def search_layer(self, q: Vector, entry: list[int], ef: int, layer: int) -> list[tuple[float, int]]:
        """Beam search on one layer; return up to ef pairs (distance, id), nearest first."""
        visited = set(entry)  # @line L1
        cand = [(self._d(q, e), e) for e in entry]
        heapq.heapify(cand)
        best = [(-d, e) for d, e in cand]
        heapq.heapify(best)
        while len(best) > ef:
            heapq.heappop(best)
        while cand:  # @line L2
            dc, c = heapq.heappop(cand)  # @line L3
            if dc > -best[0][0]:  # @line L4
                break
            for e in self.links[c][layer]:  # @line L5
                if e in visited:
                    continue
                visited.add(e)
                de = self._d(q, e)
                if len(best) < ef or de < -best[0][0]:  # @line L6
                    heapq.heappush(cand, (de, e))
                    heapq.heappush(best, (-de, e))
                    if len(best) > ef:
                        heapq.heappop(best)
        return sorted((-d, e) for d, e in best)  # @line L7

    def search(self, q: Vector, k: int, ef: int = 32) -> list[tuple[float, int]]:
        """Return up to k pairs (distance, id), nearest first."""
        if self.entry is None:
            return []
        ep = [self.entry]  # @line L8
        for layer in range(self.top, 0, -1):
            ep = [self.search_layer(q, ep, 1, layer)[0][1]]
        w = self.search_layer(q, ep, max(ef, k), 0)  # @line L9
        return w[:k]  # @line L10

    def _select(self, x: Vector, cands: list[tuple[float, int]], m: int) -> list[int]:
        """Neighbor choice: the m nearest, or the heuristic that keeps e only if it is nearer to x
        than to every neighbor already kept (Malkov and Yashunin, Algorithm 4 without extensions)."""
        cands = sorted(cands)
        if not self.heuristic:
            return [e for _, e in cands[:m]]
        out: list[int] = []
        for de, e in cands:
            if len(out) >= m:
                break
            if all(de < self.dist(self.points[e], self.points[s]) for s in out):
                out.append(e)
        return out

    def random_level(self) -> int:
        u = 1.0 - self.rng.random()  # uniform in (0, 1]
        return math.floor(-math.log(u) * self.mL)  # @line L11

    def insert(self, x: Vector, level: int | None = None) -> int:
        """Insert x and return its id. The level may be fixed for tests."""
        lvl = self.random_level() if level is None else level
        i = len(self.points)
        self.points.append(x)
        self.links.append([[] for _ in range(lvl + 1)])
        if self.entry is None:
            self.entry, self.top = i, lvl
            return i
        ep = [self.entry]
        for layer in range(self.top, lvl, -1):  # @line L12
            ep = [self.search_layer(x, ep, 1, layer)[0][1]]
        for layer in range(min(self.top, lvl), -1, -1):  # @line L13
            w = self.search_layer(x, ep, self.ef_c, layer)  # @line L14
            m_max = self.m_max0 if layer == 0 else self.M
            nbrs = self._select(x, w, self.M if layer > 0 else min(self.M, m_max))
            self.links[i][layer] = list(nbrs)
            for e in nbrs:
                self.links[e][layer].append(i)
                if len(self.links[e][layer]) > m_max:  # @line L15
                    pe = self.points[e]
                    pool = [(self.dist(pe, self.points[f]), f) for f in self.links[e][layer]]
                    self.links[e][layer] = self._select(pe, pool, m_max)
            ep = [e for _, e in w]  # @line L16
        if lvl > self.top:  # @line L17
            self.entry, self.top = i, lvl
        return i
