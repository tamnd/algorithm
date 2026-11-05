# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-hyperplane-lsh/. The authors are listed in prov/7MZBA9.jsonl.

import math
import random
from typing import Optional, Sequence

Vector = Sequence[float]


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def angle(a: Vector, b: Vector) -> float:
    """The angle between two nonzero vectors, in radians, in [0, pi]."""
    c = dot(a, b) / (math.sqrt(dot(a, a)) * math.sqrt(dot(b, b)))
    return math.acos(max(-1.0, min(1.0, c)))


def hash_key(x: Vector, hyperplanes: Sequence[Vector]) -> tuple[int, ...]:
    """The k-bit key of x: bit i is 1 when hyperplanes[i] . x >= 0. Cost O(dk)."""
    return tuple(1 if dot(r, x) >= 0 else 0 for r in hyperplanes)  # @line L1


def parameters(n: int, theta1: float, theta2: float) -> tuple[int, int]:
    """k = ceil(log_{1/p2} n) and L = ceil(n^rho / p1), for angles in radians."""
    p1, p2 = 1 - theta1 / math.pi, 1 - theta2 / math.pi
    rho = math.log(1 / p1) / math.log(1 / p2)
    k = max(1, math.ceil(math.log(n) / math.log(1 / p2)))
    return k, math.ceil(n**rho / p1)


class RandomHyperplaneLSH:
    """L hash tables, each keyed by the signs of k random Gaussian hyperplanes."""

    def __init__(self, points: Sequence[Vector], k: int, num_tables: int, seed: int = 0) -> None:
        if any(dot(p, p) == 0 for p in points):
            raise ValueError("zero vectors have no angle")
        self.points = [tuple(p) for p in points]
        d = len(self.points[0]) if self.points else 0
        rng = random.Random(seed)
        self.planes: list[list[tuple[float, ...]]] = []
        self.tables: list[dict[tuple[int, ...], list[int]]] = []
        for _ in range(num_tables):  # @line L2
            planes = [tuple(rng.gauss(0, 1) for _ in range(d)) for _ in range(k)]  # @line L3
            table: dict[tuple[int, ...], list[int]] = {}
            for i, x in enumerate(self.points):  # @line L4
                table.setdefault(hash_key(x, planes), []).append(i)
            self.planes.append(planes)
            self.tables.append(table)

    def query(self, q: Vector, theta2: float) -> Optional[int]:
        """Return the index of a point within angle theta2 of q, or None.

        Stops after 3L rejected candidates. Cost O(dkL) plus at most 3L + 1 angles.
        """
        num_tables = len(self.tables)
        c = 0  # @line L5
        for planes, table in zip(self.planes, self.tables):  # @line L6
            for i in table.get(hash_key(q, planes), []):  # @line L7
                if angle(q, self.points[i]) <= theta2:  # @line L8
                    return i
                c += 1  # @line L9
                if c >= 3 * num_tables:  # @line L10
                    return None
        return None  # @line L11
