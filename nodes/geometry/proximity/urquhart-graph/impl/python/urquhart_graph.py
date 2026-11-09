# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/urquhart-graph/. The authors are listed in prov/XMCR03.jsonl.

from fractions import Fraction
from itertools import combinations
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def dist2(p: Point, q: Point) -> Number:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def orient(a: Point, b: Point, c: Point) -> Number:
    """Twice the signed area of abc: positive for a left turn."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def incircle(a: Point, b: Point, c: Point, d: Point) -> Number:
    """For counterclockwise abc: positive if d is inside the circumcircle, 0 on it, negative outside."""
    rows = [(x[0] - d[0], x[1] - d[1], (x[0] - d[0]) ** 2 + (x[1] - d[1]) ** 2) for x in (a, b, c)]
    (a1, a2, a3), (b1, b2, b3), (c1, c2, c3) = rows
    return a1 * (b2 * c3 - b3 * c2) - a2 * (b1 * c3 - b3 * c1) + a3 * (b1 * c2 - b2 * c1)


def delaunay_triangles(points: list[Point]) -> list[tuple[int, int, int]]:
    """All triangles whose circumcircle has no other point inside or on it, in O(n^4) time.

    Precondition: no four points are cocircular (checked; ValueError otherwise). Collinear
    triples are allowed. Under this condition the result is the unique Delaunay triangulation.
    """
    n = len(points)
    out = []
    for i, j, k in combinations(range(n), 3):
        a, b, c = points[i], points[j], points[k]
        o = orient(a, b, c)
        if o == 0:
            continue
        if o < 0:
            b, c = c, b
        empty = True
        for m in range(n):
            if m in (i, j, k):
                continue
            s = incircle(a, b, c, points[m])
            if s == 0:
                raise ValueError("four points are cocircular; the Delaunay triangulation is not unique")
            if s > 0:
                empty = False
                break
        if empty:
            out.append((i, j, k))
    return out


class UrquhartGraph:
    """The Urquhart graph: the Delaunay triangulation minus the longest edge of each triangle.

    A triangle whose longest edge is not unique (an isosceles triangle with a short base) loses
    no edge; with this rule the graph always contains the relative neighborhood graph.
    Precondition: distinct points, no four cocircular. Cost: O(n^4) to build here (brute-force
    Delaunay), O(n) after a Delaunay triangulation; O(n) space.
    """

    def __init__(self, points: list[Point]) -> None:
        if len(set(points)) != len(points):
            raise ValueError("the points must be distinct")
        self.points = list(points)
        n = len(points)
        self.triangles = delaunay_triangles(self.points)  # @line L1
        E: set[tuple[int, int]] = set()  # @line L2
        for t in self.triangles:
            for e in combinations(t, 2):
                E.add(e)
        if not self.triangles and n >= 2:  # all points on one line: the triangulation is the path
            order = sorted(range(n), key=lambda i: self.points[i])
            E = {tuple(sorted(e)) for e in zip(order, order[1:])}
        for t in self.triangles:  # @line L3
            sides = sorted((dist2(self.points[a], self.points[b]), (a, b)) for a, b in combinations(t, 2))
            if sides[2][0] > sides[1][0]:  # @line L4
                E.discard(sides[2][1])  # @line L5
        self.adj: list[set[int]] = [set() for _ in range(n)]
        for i, j in E:  # @line L6
            self.adj[i].add(j)
            self.adj[j].add(i)

    def has_edge(self, i: int, j: int) -> bool:
        return j in self.adj[i]  # @line L7

    def neighbors(self, i: int) -> list[int]:
        return sorted(self.adj[i])  # @line L8

    def edges(self) -> list[tuple[int, int]]:
        return sorted((i, j) for i in range(len(self.adj)) for j in self.adj[i] if i < j)
