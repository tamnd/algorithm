# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lsh-forest/. The authors are listed in prov/TVZ64D.jsonl.

import bisect
import math
import random
from typing import Sequence

Vector = Sequence[float]


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def angle(u: Vector, v: Vector) -> float:
    nu, nv = math.sqrt(dot(u, u)), math.sqrt(dot(v, v))
    if nu == 0 or nv == 0:
        return math.pi / 2
    return math.acos(max(-1.0, min(1.0, dot(u, v) / (nu * nv))))


class LSHForest:
    """LSH forest (Bawa, Condie and Ganesan) with random hyperplane bits, for the angular distance.

    Each of the num_trees trees stores the points sorted by a label of max_depth bits; a sorted array
    with binary search plays the role of the prefix tree.
    """

    def __init__(self, points: Sequence[Vector], max_depth: int, num_trees: int,
                 seed: int = 0, planes=None) -> None:
        self.points = [tuple(p) for p in points]
        self.K = max_depth
        if planes is None:
            rng = random.Random(seed)
            dim = len(self.points[0]) if self.points else 0
            planes = [[[rng.gauss(0.0, 1.0) for _ in range(dim)] for _ in range(max_depth)]  # @line L1
                      for _ in range(num_trees)]
        self.planes = planes
        self.trees: list[tuple[list[tuple[int, ...]], list[int]]] = []
        for r in self.planes:
            labelled = sorted((self.label(r, p), i) for i, p in enumerate(self.points))  # @line L2
            self.trees.append(([lab for lab, _ in labelled], [i for _, i in labelled]))  # @line L3

    @staticmethod
    def label(r, v: Vector) -> tuple[int, ...]:
        return tuple(1 if dot(rj, v) >= 0 else 0 for rj in r)

    @staticmethod
    def _range(labels: list[tuple[int, ...]], prefix: tuple[int, ...]) -> tuple[int, int]:
        lo = bisect.bisect_left(labels, prefix)
        hi = bisect.bisect_left(labels, prefix + (2,))
        return lo, hi

    def _depth(self, labels: list[tuple[int, ...]], lam: tuple[int, ...]) -> int:
        """Length of the longest prefix of lam shared by some stored label."""
        best = 0
        pos = bisect.bisect_left(labels, lam)
        for j in (pos - 1, pos):
            if 0 <= j < len(labels):
                lcp = 0
                while lcp < self.K and labels[j][lcp] == lam[lcp]:
                    lcp += 1
                best = max(best, lcp)
        return best

    def candidates(self, q: Vector, m: int) -> tuple[set[int], int]:
        """The candidate set and the depth at which the synchronous descent stopped."""
        n = len(self.points)
        if n == 0:
            return set(), 0
        lams = [self.label(r, q) for r in self.planes]
        x = max(self._depth(labels, lam) for (labels, _), lam in zip(self.trees, lams))  # @line L4
        while True:  # @line L5
            cand: set[int] = set()
            for (labels, ids), lam in zip(self.trees, lams):  # @line L6
                lo, hi = self._range(labels, lam[:x])
                cand.update(ids[lo:hi])
            if len(cand) >= min(m, n) or x == 0:  # @line L7
                return cand, x
            x -= 1  # @line L8

    def query(self, q: Vector, k: int, m: int) -> list[int]:
        """Indices of the k points of smallest angle to q among the candidates, at least min(m, n) of them."""
        cand, _ = self.candidates(q, m)
        return sorted(cand, key=lambda i: (angle(self.points[i], q), i))[:k]  # @line L9
