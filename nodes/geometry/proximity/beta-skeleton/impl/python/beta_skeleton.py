# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beta-skeleton/. The authors are listed in prov/8WP4AF.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def dist2(p: Point, q: Point) -> Number:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def in_region(p: Point, q: Point, r: Point, beta: Number, closed: bool = False) -> bool:
    """True if r lies in the lune-based beta region of p and q (exact for rational beta > 0).

    For beta >= 1 the region is the intersection of the two disks of radius beta |pq| / 2
    centered at p + (beta/2)(q - p) and q + (beta/2)(p - q). For 0 < beta < 1 it is the set of
    points that see pq at an angle larger than pi - arcsin(beta). The region is open unless
    closed is True.
    """
    if beta >= 1:  # @line L7
        h = Fraction(beta) / 2
        c1 = (p[0] + h * (q[0] - p[0]), p[1] + h * (q[1] - p[1]))  # @line L8
        c2 = (q[0] + h * (p[0] - q[0]), q[1] + h * (p[1] - q[1]))
        rho2 = h * h * dist2(p, q)
        a, b = dist2(r, c1), dist2(r, c2)
        if closed:  # @line L9
            return a <= rho2 and b <= rho2
        return a < rho2 and b < rho2
    u = (p[0] - r[0], p[1] - r[1])  # @line L10
    v = (q[0] - r[0], q[1] - r[1])
    dot = u[0] * v[0] + u[1] * v[1]
    rhs = (1 - Fraction(beta) ** 2) * (u[0] ** 2 + u[1] ** 2) * (v[0] ** 2 + v[1] ** 2)
    if closed:  # @line L11
        return dot <= 0 and dot * dot >= rhs
    return dot < 0 and dot * dot > rhs


class BetaSkeleton:
    """The lune-based beta-skeleton of a set of distinct points in the plane, for rational beta > 0.

    {i, j} is an edge when no third point lies in the beta region of P[i] and P[j].
    beta = 1 with closed=True is the Gabriel graph; beta = 2 with closed=False is the
    relative neighborhood graph. Built by the definition in O(n^3) time; O(n + m) space for m edges.
    """

    def __init__(self, points: list[Point], beta: Number, closed: bool = False) -> None:
        if beta <= 0:
            raise ValueError("beta must be positive")
        if len(set(points)) != len(points):
            raise ValueError("the points must be distinct")
        self.points = list(points)
        self.beta = beta
        self.closed = closed
        n = len(points)
        self.adj: list[set[int]] = [set() for _ in range(n)]
        for i in range(n):  # @line L1
            for j in range(i + 1, n):
                empty = True  # @line L2
                for k in range(n):  # @line L3
                    if k != i and k != j and in_region(points[i], points[j], points[k], beta, closed):  # @line L4
                        empty = False  # @line L5
                        break
                if empty:  # @line L6
                    self.adj[i].add(j)
                    self.adj[j].add(i)

    def has_edge(self, i: int, j: int) -> bool:
        return j in self.adj[i]  # @line L12

    def neighbors(self, i: int) -> list[int]:
        return sorted(self.adj[i])  # @line L13

    def edges(self) -> list[tuple[int, int]]:
        return sorted((i, j) for i in range(len(self.adj)) for j in self.adj[i] if i < j)
