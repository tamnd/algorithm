# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locality-sensitive-hashing/. The authors are listed in prov/XTR0CK.jsonl.

import math
import random
from collections.abc import Callable, Hashable, Sequence
from typing import Generic, TypeVar

P = TypeVar("P")
HashFn = Callable[[P], Hashable]
Family = Callable[[random.Random], HashFn]


class LSHIndex(Generic[P]):
    """Locality-sensitive hashing for the (c, r)-near neighbor problem.

    `family(rng)` draws one function of a locality-sensitive family. The index
    builds L tables, each keyed by the tuple of k functions. Space O(nL) keys,
    build time O(nLk) hash evaluations, query time O(Lk) evaluations plus at
    most 3L distance computations.
    """

    def __init__(
        self,
        points: Sequence[P],
        family: Family,
        k: int,
        L: int,
        dist: Callable[[P, P], float],
        rng: random.Random | None = None,
    ) -> None:
        if k < 1 or L < 1:
            raise ValueError("k and L must be at least 1")
        rng = rng if rng is not None else random.Random()
        self.points = list(points)
        self.dist = dist
        self.L = L
        self.g: list[list[HashFn]] = []
        self.tables: list[dict[tuple, list[int]]] = []
        for _ in range(L):  # @line L1
            fns = [family(rng) for _ in range(k)]  # @line L2
            self.g.append(fns)
            table: dict[tuple, list[int]] = {}
            for i, x in enumerate(self.points):
                table.setdefault(self._key(fns, x), []).append(i)  # @line L3 @line L4
            self.tables.append(table)

    @staticmethod
    def _key(fns: list[HashFn], x: P) -> tuple:
        return tuple(h(x) for h in fns)

    def query(self, q: P, c: float, r: float) -> int | None:
        """Return the index of a point within c*r of q, or None.

        A returned point is always within c*r. If some point is within r, a
        point is returned with probability at least 2/3 - 1/e when k and L are
        set as on the page.
        """
        count = 0  # @line L5
        for j in range(self.L):  # @line L6
            for i in self.tables[j].get(self._key(self.g[j], q), []):  # @line L7
                count += 1  # @line L8
                if self.dist(q, self.points[i]) <= c * r:  # @line L9
                    return i
                if count >= 3 * self.L:  # @line L10
                    return None
        return None  # @line L11

    def candidates(self, q: P) -> set[int]:
        """Return the indices of all points that share a bucket with q in some table."""
        out: set[int] = set()
        for j in range(self.L):
            out.update(self.tables[j].get(self._key(self.g[j], q), []))
        return out


def parameters(n: int, p1: float, p2: float) -> tuple[int, int]:
    """Return (k, L) = (ceil(log_{1/p2} n), ceil(n^rho / p1)) for 0 < p2 < p1 <= 1 and n >= 2."""
    rho = math.log(1 / p1) / math.log(1 / p2)
    k = max(1, math.ceil(math.log(n) / math.log(1 / p2)))
    L = math.ceil(n**rho / p1)
    return k, L
