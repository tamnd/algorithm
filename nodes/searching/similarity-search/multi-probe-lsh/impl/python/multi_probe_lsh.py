# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-probe-lsh/. The authors are listed in prov/9SW2DV.jsonl.

import heapq
import math
import random
from typing import Iterator, Sequence

Vector = Sequence[float]


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def perturbations(x_minus: Sequence[float], w: float) -> Iterator[tuple[tuple[int, ...], float]]:
    """Yield every perturbation vector in {-1, 0, 1}^M other than 0, with its score, in nondecreasing score.

    x_minus[j] is the distance from f_j(q) to the left end of its slot, in [0, w).
    The score of a vector delta is the sum over j with delta_j != 0 of x_j(delta_j)^2.
    """
    m = len(x_minus)
    pairs = []
    for j, xm in enumerate(x_minus):
        pairs.append((xm, j, -1))
        pairs.append((w - xm, j, +1))
    pairs.sort()  # @line L9
    z2 = [p[0] ** 2 for p in pairs]
    if m == 0:
        return
    heap = [(z2[0], (0,))]  # @line L10
    while heap:
        score, a = heapq.heappop(heap)  # @line L11
        top = a[-1]
        if top + 1 < 2 * m:  # @line L12
            heapq.heappush(heap, (score - z2[top] + z2[top + 1], a[:-1] + (top + 1,)))  # shift
            heapq.heappush(heap, (score + z2[top + 1], a + (top + 1,)))  # expand
        coords = [pairs[i][1] for i in a]
        if len(set(coords)) == len(coords):  # @line L13
            delta = [0] * m
            for i in a:
                delta[pairs[i][1]] = pairs[i][2]
            yield tuple(delta), score


class MultiProbeLSH:
    """Euclidean LSH with p-stable hashes h(v) = floor((a.v + b) / w) and query-directed multi-probing."""

    def __init__(self, points: Sequence[Vector], m: int, num_tables: int, w: float,
                 seed: int = 0, functions=None) -> None:
        self.points = [tuple(p) for p in points]
        self.m, self.w = m, w
        if functions is None:
            rng = random.Random(seed)
            d = len(self.points[0]) if self.points else 0
            functions = [  # @line L1
                ([[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(m)], [rng.uniform(0.0, w) for _ in range(m)])
                for _ in range(num_tables)
            ]
        self.functions = functions
        self.tables: list[dict[tuple[int, ...], list[int]]] = []
        for a, b in self.functions:
            table: dict[tuple[int, ...], list[int]] = {}
            for idx, p in enumerate(self.points):
                table.setdefault(self._key(a, b, p)[0], []).append(idx)  # @line L2
            self.tables.append(table)

    def _key(self, a, b, v: Vector) -> tuple[tuple[int, ...], list[float]]:
        f = [dot(aj, v) + bj for aj, bj in zip(a, b)]
        h = tuple(math.floor(fj / self.w) for fj in f)
        x_minus = [fj - self.w * hj for fj, hj in zip(f, h)]
        return h, x_minus

    def probed_keys(self, q: Vector, probes: int) -> list[list[tuple[int, ...]]]:
        """For each table, the home key of q followed by the keys of its first `probes` perturbations."""
        out = []
        for a, b in self.functions:
            h, x_minus = self._key(a, b, q)  # @line L5
            keys = [h]  # @line L6
            for delta, _ in perturbations(x_minus, self.w):  # @line L7
                if len(keys) > probes:
                    break
                keys.append(tuple(hj + dj for hj, dj in zip(h, delta)))
            out.append(keys)
        return out

    def candidates(self, q: Vector, probes: int) -> set[int]:
        cand: set[int] = set()  # @line L3
        for table, keys in zip(self.tables, self.probed_keys(q, probes)):  # @line L4
            for k in keys:
                cand.update(table.get(k, ()))
        return cand

    def query(self, q: Vector, probes: int) -> int | None:
        """Index of the nearest point of q among the candidates, or None if there is none."""
        cand = self.candidates(q, probes)
        if not cand:
            return None
        return min(cand, key=lambda i: (math.dist(self.points[i], q), i))  # @line L8
