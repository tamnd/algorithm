# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relative-neighborhood-graph/. The authors are listed in prov/5F7BZ4.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def dist2(p: Point, q: Point) -> Number:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def in_lune(p: Point, q: Point, r: Point) -> bool:
    """True if r is strictly closer to both p and q than they are to each other (exact)."""
    d = dist2(p, q)
    return dist2(p, r) < d and dist2(q, r) < d


class RelativeNeighborhoodGraph:
    """The relative neighborhood graph of a set of distinct points in the plane.

    Vertices are the indices 0..n-1. {i, j} is an edge when no third point r has
    max(|P[i] r|, |P[j] r|) < |P[i] P[j]|, that is, the open lune of P[i] and P[j] is empty.
    Built by the definition in O(n^3) time; O(n) space, since the graph is planar.
    """

    def __init__(self, points: list[Point]) -> None:
        if len(set(points)) != len(points):
            raise ValueError("the points must be distinct")
        self.points = list(points)
        n = len(points)
        self.adj: list[set[int]] = [set() for _ in range(n)]
        for i in range(n):  # @line L1
            for j in range(i + 1, n):
                d = dist2(points[i], points[j])  # @line L2
                empty = True  # @line L3
                for k in range(n):  # @line L4
                    if k != i and k != j and max(dist2(points[i], points[k]), dist2(points[j], points[k])) < d:  # @line L5
                        empty = False  # @line L6
                        break
                if empty:  # @line L7
                    self.adj[i].add(j)
                    self.adj[j].add(i)

    def has_edge(self, i: int, j: int) -> bool:
        return j in self.adj[i]  # @line L8

    def neighbors(self, i: int) -> list[int]:
        return sorted(self.adj[i])  # @line L9

    def edges(self) -> list[tuple[int, int]]:
        return sorted((i, j) for i in range(len(self.adj)) for j in self.adj[i] if i < j)

    def check_invariant(self) -> None:
        """Recheck the empty-lune condition for every pair and the symmetry of the adjacency sets."""
        P = self.points
        n = len(P)
        for i in range(n):
            assert i not in self.adj[i]
            for j in range(n):
                if i != j:
                    assert (j in self.adj[i]) == (i in self.adj[j])
                    want = not any(in_lune(P[i], P[j], P[k]) for k in range(n) if k != i and k != j)
                    assert (j in self.adj[i]) == want
