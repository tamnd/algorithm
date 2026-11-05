# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymmetric-lsh/. The authors are listed in prov/NNNB37.jsonl.
"""Asymmetric LSH for maximum inner product search (the simple transformation with random hyperplanes)."""

import math
import random
from typing import Optional, Sequence

Vector = Sequence[float]


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Vector) -> float:
    return math.sqrt(dot(a, a))


def transform_data(x: Vector, m: float) -> list[float]:
    """P(x) = [x/M ; sqrt(1 - |x|^2/M^2)], a unit vector when |x| <= M."""
    y = [v / m for v in x]
    return y + [math.sqrt(max(0.0, 1.0 - dot(y, y)))]


def transform_query(q: Vector) -> list[float]:
    """Q(q) = [q/|q| ; 0], a unit vector."""
    s = norm(q)
    return [v / s for v in q] + [0.0]


def l2_alsh_transforms(x: Vector, q: Vector, m: int) -> tuple[list[float], list[float]]:
    """The L2-ALSH maps: P(x) = [x; |x|^2; |x|^4; ...; |x|^(2^m)], Q(q) = [q; 1/2; ...; 1/2].

    x must already be scaled so that |x| < 1, and q normalized to |q| = 1.
    """
    s = dot(x, x)
    tail = []
    for _ in range(m):
        tail.append(s)
        s = s * s
    return list(x) + tail, list(q) + [0.5] * m


class SimpleALSH:
    def __init__(self, points: Sequence[Vector], k: int, L: int,
                 rng: Optional[random.Random] = None) -> None:
        rng = rng or random.Random()
        self.points = [list(p) for p in points]
        self.k, self.L = k, L
        self.m = max((norm(p) for p in self.points), default=0.0) or 1.0  # @line L1
        dim = len(self.points[0]) + 1 if self.points else 1
        self.planes = [[[rng.gauss(0.0, 1.0) for _ in range(dim)] for _ in range(k)]
                       for _ in range(L)]  # @line L3
        self.tables: list[dict[tuple[bool, ...], list[int]]] = [{} for _ in range(L)]
        for i, p in enumerate(self.points):
            px = transform_data(p, self.m)  # @line L2
            for j in range(L):  # @line L4
                self.tables[j].setdefault(self.key(j, px), []).append(i)

    def key(self, j: int, v: Vector) -> tuple[bool, ...]:
        return tuple(dot(a, v) >= 0.0 for a in self.planes[j])

    def candidates(self, q: Vector) -> set[int]:
        qq = transform_query(q)  # @line L5
        cand: set[int] = set()
        for j in range(self.L):  # @line L6
            cand.update(self.tables[j].get(self.key(j, qq), ()))
        return cand

    def query(self, q: Vector) -> Optional[int]:
        """Index of the candidate with the largest inner product with q, or None."""
        cand = self.candidates(q)
        if not cand:
            return None
        return max(sorted(cand), key=lambda i: dot(q, self.points[i]))  # @line L7


def collision_probability(s: float) -> float:
    """Pr[one hyperplane bit agrees] for unit vectors with inner product s."""
    return 1.0 - math.acos(max(-1.0, min(1.0, s))) / math.pi


def parameters(n: int, s: float, c: float) -> tuple[int, int, float]:
    """k, L and rho for an (S, cS) guarantee on the normalized inner product, success >= 1 - 1/e."""
    p1, p2 = collision_probability(s), collision_probability(c * s)
    rho = math.log(1 / p1) / math.log(1 / p2)
    k = max(1, math.ceil(math.log(n) / math.log(1 / p2)))
    L = math.ceil(n ** rho / p1)
    return k, L, rho
