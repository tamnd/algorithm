# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cover-tree/. The authors are listed in prov/GE45W4.jsonl.
"""Cover tree with base 2: insertion and nearest neighbor search (Beygelzimer, Kakade and Langford)."""

import math
from typing import Callable, Optional, Sequence

Point = Sequence[float]


def euclidean(a: Point, b: Point) -> float:
    return math.dist(a, b)


class CoverTree:
    """Points are kept by index. children[p][i] lists the points whose top level is i - 1
    and whose parent at level i is p. Every point is its own child at each level below its top."""

    def __init__(self, dist: Callable[[Point, Point], float] = euclidean) -> None:
        self.dist = dist
        self.points: list[Point] = []
        self.children: list[dict[int, list[int]]] = []
        self.dups: dict[int, list[int]] = {}
        self.root: Optional[int] = None
        self.top = 0          # level of the root
        self.bottom = 0       # lowest level of any node

    def _d(self, p: Point, i: int) -> float:
        return self.dist(p, self.points[i])

    def _kids(self, qs: Sequence[int], i: int) -> list[int]:
        """Children at level i - 1 of the nodes qs at level i, including the nodes themselves."""
        out = list(qs)
        for q in qs:
            out.extend(self.children[q].get(i, ()))
        return out

    def insert(self, p: Point) -> int:
        idx = len(self.points)
        self.points.append(p)
        self.children.append({})
        if self.root is None:
            self.root = idx
            return idx
        d0 = self._d(p, self.root)
        if d0 == 0:
            self.dups.setdefault(self.root, []).append(idx)
            return idx
        while d0 > 2.0 ** self.top:  # raise the root until it covers p
            self.top += 1
        self._insert(idx, [self.root], self.top)
        return idx

    def _insert(self, idx: int, qi: list[int], i: int) -> bool:
        """Returns True for "parent found"."""
        p = self.points[idx]
        q_all = self._kids(qi, i)  # @line L1
        dists = {q: self._d(p, q) for q in q_all}
        dmin = min(dists.values())
        if dmin == 0:  # a duplicate of an existing point
            self.dups.setdefault(min(q_all, key=dists.__getitem__), []).append(idx)
            return True
        if dmin > 2.0 ** i:  # @line L2
            return False
        q_next = [q for q in q_all if dists[q] <= 2.0 ** i]  # @line L3
        if self._insert(idx, q_next, i - 1):  # @line L4
            return True
        near = [q for q in qi if dists[q] <= 2.0 ** i]  # @line L5
        if not near:
            return False
        parent = min(near, key=dists.__getitem__)
        self.children[parent].setdefault(i, []).append(idx)  # @line L6
        self.bottom = min(self.bottom, i - 1)
        return True

    def nearest(self, p: Point) -> Optional[tuple[float, int]]:
        """(distance, index) of a nearest stored point, or None if empty."""
        if self.root is None:
            return None
        qi = [self.root]  # @line L7
        for i in range(self.top, self.bottom, -1):  # @line L8
            q_all = self._kids(qi, i)
            dists = {q: self._d(p, q) for q in q_all}
            bound = min(dists.values()) + 2.0 ** i
            qi = [q for q in q_all if dists[q] <= bound]  # @line L9
        return min((self._d(p, q), q) for q in qi)  # @line L10

    def levels(self) -> dict[int, list[int]]:
        """C_i for each level from top down to bottom (as sorted index lists)."""
        out: dict[int, list[int]] = {}
        if self.root is None:
            return out
        cur = [self.root]
        for i in range(self.top, self.bottom - 1, -1):
            out[i] = sorted(cur)
            cur = self._kids(cur, i)
        return out

    def parent_at(self) -> dict[tuple[int, int], int]:
        """(point, level) -> parent at level + 1, for explicit and implicit nodes."""
        par: dict[tuple[int, int], int] = {}
        if self.root is None:
            return par
        cur = [self.root]
        for i in range(self.top, self.bottom, -1):
            nxt = []
            for q in cur:
                par[(q, i - 1)] = q
                nxt.append(q)
                for c in self.children[q].get(i, ()):
                    par[(c, i - 1)] = q
                    nxt.append(c)
            cur = nxt
        return par
