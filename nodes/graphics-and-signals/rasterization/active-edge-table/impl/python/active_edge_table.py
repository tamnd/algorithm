# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-edge-table/. The authors are listed in prov/3J25VA.jsonl.

"""An edge table and an active edge table for scanline work on a pixel grid.

Row j has its center line at y = j + 1/2, and y grows downward. An edge is
active on row j when top_y <= j + 1/2 < bottom_y, so horizontal edges are
never active and a vertex on a center line is counted once. Each record holds
exact Fraction values, so the x order is exact.
"""

from fractions import Fraction
from math import ceil
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
HALF = Fraction(1, 2)


class Edge:
    """One active edge record: the end row, the x on the current center line, the x step per row, the direction."""

    __slots__ = ("end_row", "x", "dxdy", "d")

    def __init__(self, end_row: int, x: Fraction, dxdy: Fraction, d: int):
        self.end_row = end_row
        self.x = x
        self.dxdy = dxdy
        self.d = d  # +1 when the edge goes down (y grows), -1 when it goes up


class ActiveEdgeTable:
    def __init__(self, rings: Sequence[Sequence[Point]], height: int):
        self.height = height
        self.buckets: list[list[Edge]] = [[] for _ in range(height)]  # @line L1
        for ring in rings:
            n = len(ring)
            for k in range(n):
                a, b = ring[k], ring[(k + 1) % n]
                if a[1] == b[1]:
                    continue
                d = 1 if a[1] < b[1] else -1
                top, bot = (a, b) if d == 1 else (b, a)
                j0 = max(ceil(Fraction(top[1]) - HALF), 0)
                j1 = ceil(Fraction(bot[1]) - HALF)
                if j0 < min(j1, height):
                    dxdy = Fraction(bot[0] - top[0]) / (bot[1] - top[1])
                    self.buckets[j0].append(Edge(j1, top[0] + (j0 + HALF - top[1]) * dxdy, dxdy, d))
        for bucket in self.buckets:  # @line L2
            bucket.sort(key=lambda e: (e.x, e.dxdy))  # equal x: the edge that moves left goes first
        self.active: list[Edge] = []
        self.row = -1
        self.swaps = 0  # order changes made by the re-sort: each is one pair of edges that cross

    def next_row(self) -> int:
        """Move to the next row and return its index."""
        if self.row >= 0:
            for e in self.active:  # @line L3
                e.x += e.dxdy
        self.row += 1
        j = self.row
        self.active = [e for e in self.active if e.end_row > j]  # @line L4
        a = self.active
        for k in range(1, len(a)):  # @line L5
            e, m = a[k], k - 1
            while m >= 0 and a[m].x > e.x:
                a[m + 1] = a[m]
                m -= 1
                self.swaps += 1
            a[m + 1] = e
        new = self.buckets[j] if j < self.height else []
        merged, p, q = [], 0, 0  # @line L6
        while p < len(a) or q < len(new):
            if q == len(new) or (p < len(a) and (a[p].x, a[p].dxdy) <= (new[q].x, new[q].dxdy)):
                merged.append(a[p])
                p += 1
            else:
                merged.append(new[q])
                q += 1
        self.active = merged
        return j

    def crossings(self) -> list[tuple[Fraction, int]]:
        """The (x, direction) pairs on the current center line, sorted by x."""
        return [(e.x, e.d) for e in self.active]  # @line L7


def fill_spans(rings: Sequence[Sequence[Point]], width: int, height: int, rule: str = "evenodd") -> list[tuple[int, int, int]]:
    """Use the table to list filled spans (row, first column, last column + 1) under a fill rule."""
    aet = ActiveEdgeTable(rings, height)
    spans = []
    for _ in range(height):
        j = aet.next_row()
        xs = aet.crossings()
        w = 0
        for k in range(len(xs) - 1):
            w += 1 if rule == "evenodd" else xs[k][1]
            if (w % 2 == 1) if rule == "evenodd" else (w != 0):
                lo = max(ceil(xs[k][0] - HALF), 0)
                hi = min(ceil(xs[k + 1][0] - HALF), width)
                if lo < hi:
                    spans.append((j, lo, hi))
    return spans
