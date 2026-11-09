# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabriel-graph/. The authors are listed in prov/T3DGB2.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def in_diametral_disk(p: Point, q: Point, r: Point) -> bool:
    """True if r lies in the closed disk with diameter pq, that is, (p - r) . (q - r) <= 0 (exact)."""
    return (p[0] - r[0]) * (q[0] - r[0]) + (p[1] - r[1]) * (q[1] - r[1]) <= 0


class GabrielGraph:
    """The Gabriel graph of a set of distinct points in the plane.

    Vertices are the indices 0..n-1 of the points. {i, j} is an edge when the closed disk with
    diameter P[i]P[j] contains no other point. Built by the definition in O(n^3) time and O(n + m)
    space, where m <= 3n - 6 is the number of edges; queries cost O(1) (has_edge) and O(deg) (neighbors).
    """

    def __init__(self, points: list[Point]) -> None:
        if len(set(points)) != len(points):
            raise ValueError("the points must be distinct")
        self.points = list(points)
        n = len(points)
        self.adj: list[set[int]] = [set() for _ in range(n)]
        for i in range(n):  # @line L1
            for j in range(i + 1, n):
                empty = True  # @line L2
                for k in range(n):  # @line L3
                    if k != i and k != j and in_diametral_disk(points[i], points[j], points[k]):  # @line L4
                        empty = False  # @line L5
                        break
                if empty:  # @line L6
                    self.adj[i].add(j)
                    self.adj[j].add(i)

    def has_edge(self, i: int, j: int) -> bool:
        return j in self.adj[i]  # @line L7

    def neighbors(self, i: int) -> list[int]:
        return sorted(self.adj[i])  # @line L8

    def edges(self) -> list[tuple[int, int]]:
        return sorted((i, j) for i in range(len(self.adj)) for j in self.adj[i] if i < j)

    def check_invariant(self) -> None:
        """Recheck the empty-disk condition for every pair and the symmetry of the adjacency sets."""
        P = self.points
        n = len(P)
        for i in range(n):
            for j in range(n):
                if i == j:
                    assert i not in self.adj[i]
                    continue
                assert (j in self.adj[i]) == (i in self.adj[j])
                want = not any(in_diametral_disk(P[i], P[j], P[k]) for k in range(n) if k != i and k != j)
                assert (j in self.adj[i]) == want
