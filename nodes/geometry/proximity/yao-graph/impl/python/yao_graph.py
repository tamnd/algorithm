# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-graph/. The authors are listed in prov/78899M.jsonl.

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def dist2(p: Point, q: Point) -> Number:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def octant(dx: Number, dy: Number) -> int:
    """Index j in 0..7 of the half-open cone [j*45, (j+1)*45) degrees containing (dx, dy) != (0, 0).

    Uses only sign tests and comparisons, so it is exact.
    """
    base = 0
    if dy < 0 or (dy == 0 and dx < 0):
        dx, dy, base = -dx, -dy, 4
    # now the angle is in [0, 180)
    if dx > 0 and dy < dx:
        return base
    if dx > 0:
        return base + 1
    if -dx < dy:
        return base + 2
    return base + 3


def cone(dx: Number, dy: Number, k: int) -> int:
    """Cone index for k = 8 (octants) or k = 4 (quadrants [0, 90), [90, 180), ...)."""
    j = octant(dx, dy)
    return j if k == 8 else j // 2


class YaoGraph:
    """The Yao graph with k = 4 or k = 8 cones: each point is joined to a nearest point in each cone.

    Cones are half-open and bounded by the axes (and the diagonals for k = 8). Ties within a cone
    go to the smallest index. The undirected graph is stored; it has at most k*n edges.
    Precondition: distinct points. Built in O(n^2) time, O(k n) space.
    """

    def __init__(self, points: list[Point], k: int = 8) -> None:
        if k not in (4, 8):
            raise ValueError("this implementation supports k = 4 or k = 8 cones")
        if len(set(points)) != len(points):
            raise ValueError("the points must be distinct")
        self.points = list(points)
        self.k = k
        n = len(points)
        self.adj: list[set[int]] = [set() for _ in range(n)]
        self.out: list[list[Optional[int]]] = []
        for i in range(n):  # @line L1
            best: list[Optional[int]] = [None] * k  # @line L2
            p = points[i]
            for j in range(n):  # @line L3
                if j == i:
                    continue
                q = points[j]
                c = cone(q[0] - p[0], q[1] - p[1], k)  # @line L4
                if best[c] is None or dist2(p, q) < dist2(p, points[best[c]]):  # @line L5
                    best[c] = j
            for j in best:  # @line L6
                if j is not None:
                    self.adj[i].add(j)
                    self.adj[j].add(i)
            self.out.append(best)

    def has_edge(self, i: int, j: int) -> bool:
        return j in self.adj[i]  # @line L7

    def neighbors(self, i: int) -> list[int]:
        return sorted(self.adj[i])  # @line L8

    def edges(self) -> list[tuple[int, int]]:
        return sorted((i, j) for i in range(len(self.adj)) for j in self.adj[i] if i < j)
