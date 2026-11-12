# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scanline-polygon-fill/. The authors are listed in prov/VS80AE.jsonl.

"""Scanline polygon fill with an edge table and an active edge table.

The image has W columns and H rows. Pixel (i, j) has its center at
(i + 1/2, j + 1/2), and y grows downward (row 0 is the top row).
The input is a list of closed rings (outer boundaries and holes), with int or
Fraction coordinates. A pixel is filled when its center, moved by an
infinitesimal step e to the right and e^2 down, is inside under the fill rule.
So a center on a left or top edge is filled, and a center on a right or bottom
edge is not. All x positions are exact Fractions, so every decision is exact.
"""

from fractions import Fraction
from math import ceil
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
HALF = Fraction(1, 2)


def _ceil(v: Number) -> int:
    return ceil(Fraction(v))


def build_edge_table(rings: Sequence[Sequence[Point]], height: int) -> list[list[list]]:
    """Bucket each non-horizontal edge by the first row whose center line it crosses.

    An entry is [j1, x, dxdy, d]: the edge is active for the rows before j1, x is
    its x on the center line of its first row, dxdy is the change of x from one
    row to the next, and d is +1 for an edge that goes down and -1 for one that
    goes up. Each bucket is sorted by x, then by dxdy.
    """
    table: list[list[list]] = [[] for _ in range(height)]  # @line L1
    for ring in rings:
        n = len(ring)
        for k in range(n):  # @line L2
            a, b = ring[k], ring[(k + 1) % n]
            if a[1] == b[1]:
                continue  # a horizontal edge crosses no center line
            d = 1 if a[1] < b[1] else -1  # @line L3
            top, bot = (a, b) if d == 1 else (b, a)
            j0 = _ceil(top[1] - HALF)  # @line L4
            j1 = _ceil(bot[1] - HALF)  # rows j with top_y <= j + 1/2 < bot_y are j0 .. j1 - 1
            dxdy = Fraction(bot[0] - top[0]) / (bot[1] - top[1])
            first = max(j0, 0)  # @line L5
            if first < min(j1, height):
                x = top[0] + (first + HALF - top[1]) * dxdy
                table[first].append([j1, x, dxdy, d])
    for bucket in table:
        bucket.sort(key=lambda e: (e[1], e[2]))
    return table


def _inside(w: int, rule: str) -> bool:
    return (w % 2 == 1) if rule == "evenodd" else (w != 0)


def scanline_spans(rings: Sequence[Sequence[Point]], width: int, height: int, rule: str = "evenodd") -> list[tuple[int, int, int]]:
    """The filled spans as (row j, first column, last column + 1), row by row, left to right."""
    if rule not in ("evenodd", "nonzero"):
        raise ValueError("rule must be 'evenodd' or 'nonzero'")
    table = build_edge_table(rings, height)
    aet: list[list] = []  # @line L6
    spans = []
    for j in range(height):  # @line L7
        aet = [e for e in aet if e[0] > j]  # @line L8
        for k in range(1, len(aet)):  # @line L9
            e, m = aet[k], k - 1  # insertion sort: one move for each pair of edges that crossed
            while m >= 0 and aet[m][1] > e[1]:
                aet[m + 1] = aet[m]
                m -= 1
            aet[m + 1] = e
        new, merged, p, q = table[j], [], 0, 0  # @line L10
        while p < len(aet) or q < len(new):
            if q == len(new) or (p < len(aet) and (aet[p][1], aet[p][2]) <= (new[q][1], new[q][2])):
                merged.append(aet[p])
                p += 1
            else:
                merged.append(new[q])
                q += 1
        aet = merged
        w = 0
        for k in range(len(aet) - 1):  # @line L11
            w += 1 if rule == "evenodd" else aet[k][3]
            if _inside(w, rule):
                lo = max(_ceil(aet[k][1] - HALF), 0)  # first i with i + 1/2 >= x_k
                hi = min(_ceil(aet[k + 1][1] - HALF), width)  # first i with i + 1/2 >= x_(k+1)
                if lo < hi:
                    if spans and spans[-1][0] == j and spans[-1][2] == lo:
                        spans[-1] = (j, spans[-1][1], hi)  # join touching spans
                    else:
                        spans.append((j, lo, hi))
        for e in aet:  # @line L12
            e[1] += e[2]
    return spans


def scanline_polygon_fill(rings: Sequence[Sequence[Point]], width: int, height: int, rule: str = "evenodd") -> set[tuple[int, int]]:
    """The set of filled pixels (i, j)."""
    return {(i, j) for j, lo, hi in scanline_spans(rings, width, height, rule) for i in range(lo, hi)}
