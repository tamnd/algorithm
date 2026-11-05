# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/e2lsh/. The authors are listed in prov/K84C3G.jsonl.

import math
import random
from collections.abc import Sequence

Vector = Sequence[float]


def euclidean(x: Vector, y: Vector) -> float:
    return math.sqrt(sum((a - b) * (a - b) for a, b in zip(x, y)))


def collision_probability(u: float, w: float) -> float:
    """Pr[h(x) = h(y)] for ||x - y|| = u under h(v) = floor((a.v + b)/w), a Gaussian, b uniform in [0, w)."""
    if u == 0:
        return 1.0
    t = w / u
    phi = 0.5 * (1 + math.erf(-t / math.sqrt(2)))
    return 1 - 2 * phi - 2 / (math.sqrt(2 * math.pi) * t) * (1 - math.exp(-t * t / 2))


def parameters(n: int, w: float, r: float, c: float) -> tuple[int, int]:
    """k and L of the LSH theorem for the (r, cr, p(r), p(cr)) family."""
    p1, p2 = collision_probability(r, w), collision_probability(c * r, w)
    rho = math.log(1 / p1) / math.log(1 / p2)
    k = max(1, math.ceil(math.log(n) / math.log(1 / p2)))
    return k, math.ceil(n**rho / p1)


class E2LSH:
    """LSH for the Euclidean distance with quantized Gaussian projections.

    Build: O(n L k d). Query: O(L k d) for the keys plus at most 3L distances of O(d) each.
    """

    def __init__(
        self, points: Sequence[Vector], k: int, L: int, w: float, rng: random.Random | None = None
    ) -> None:
        rng = rng if rng is not None else random.Random()
        self.points = [tuple(p) for p in points]
        d = len(self.points[0]) if self.points else 0
        self.L, self.w = L, w
        self.funcs: list[list[tuple[list[float], float]]] = []
        self.tables: list[dict[tuple[int, ...], list[int]]] = []
        for _ in range(L):  # @line L1
            g = [([rng.gauss(0, 1) for _ in range(d)], rng.uniform(0, w)) for _ in range(k)]  # @line L2
            self.funcs.append(g)
            table: dict[tuple[int, ...], list[int]] = {}
            for i, x in enumerate(self.points):
                table.setdefault(self.key(g, x), []).append(i)  # @line L3
            self.tables.append(table)

    def key(self, g: list[tuple[list[float], float]], v: Vector) -> tuple[int, ...]:
        return tuple(math.floor((sum(ai * vi for ai, vi in zip(a, v)) + b) / self.w) for a, b in g)

    def query(self, q: Vector, c: float, r: float) -> int | None:
        """Return the index of a point within c*r of q, or None."""
        count = 0  # @line L4
        for j in range(self.L):  # @line L5
            for i in self.tables[j].get(self.key(self.funcs[j], q), []):
                count += 1  # @line L6
                if euclidean(q, self.points[i]) <= c * r:
                    return i
                if count >= 3 * self.L:  # @line L7
                    return None
        return None  # @line L8
