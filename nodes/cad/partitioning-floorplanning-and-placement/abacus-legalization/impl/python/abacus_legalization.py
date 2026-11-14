# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abacus-legalization/. The authors are listed in prov/4DKME3.jsonl.

"""Abacus legalization (Spindler, Schlichtmann and Johannes, ISPD 2008).

Rows r = 0 .. K-1 lie at y = r * row_height and span the sites x = 0 .. S-1 of width 1.
Cell i has an integer width w[i] (in sites), a weight e[i] > 0 and a global position
(xg[i], yg[i]) of its lower left corner. All arithmetic is exact (Fraction).
"""

from fractions import Fraction
from math import floor
from typing import Sequence


class Cluster:
    __slots__ = ("cells", "e", "w", "q", "x")

    def __init__(self):
        self.cells: list[int] = []
        self.e = Fraction(0)  # total weight
        self.w = 0  # total width
        self.q = Fraction(0)  # sum of e_i (xg_i - offset of i in the cluster)
        self.x = Fraction(0)  # position of the left edge


def add_cell(c: Cluster, i: int, xg, w, e) -> None:
    c.cells.append(i)
    c.q += e[i] * (Fraction(xg[i]) - c.w)  # @line L12
    c.e += e[i]
    c.w += w[i]


def add_cluster(c: Cluster, d: Cluster) -> None:
    """Append cluster d to the right end of cluster c."""
    c.cells += d.cells
    c.q += d.q - d.e * c.w  # @line L18
    c.e += d.e
    c.w += d.w


def collapse(clusters: list, xmin: int, xmax: int) -> None:
    while True:
        c = clusters[-1]
        c.x = c.q / c.e  # @line L14
        if c.x < xmin:  # @line L15
            c.x = Fraction(xmin)
        if c.x > xmax - c.w:
            c.x = Fraction(xmax - c.w)
        if len(clusters) >= 2 and clusters[-2].x + clusters[-2].w > c.x:  # @line L16
            prev = clusters[-2]
            add_cluster(prev, c)  # @line L17
            clusters.pop()
            continue
        return


def place_row(order: Sequence[int], xg, w, e, xmin: int, xmax: int) -> list:
    """PlaceRow: the cells in the given left-to-right order, each pulled to xg with weight e.
    Returns the clusters; together they minimize sum e_i (x_i - xg_i)^2 with no overlap,
    keeping the order, inside [xmin, xmax]. The total width must fit."""
    clusters: list = []
    for i in order:  # @line L10
        last = clusters[-1] if clusters else None
        if last is None or last.x + last.w <= xg[i]:  # @line L11
            last = Cluster()
            clusters.append(last)
        add_cell(last, i, xg, w, e)
        collapse(clusters, xmin, xmax)  # @line L13
    return clusters


def cell_positions(clusters, w) -> dict:
    """Exact positions of the cells of the clusters: each cluster is a block of abutting cells."""
    out = {}
    for c in clusters:
        off = 0
        for i in c.cells:
            out[i] = c.x + off
            off += w[i]
    return out


def abacus(xg, yg, w, num_rows: int, sites: int, row_height=1, e=None):
    """Return (x, y): integer site positions and row heights for all cells, or raise ValueError
    if a cell fits in no row. Cells are taken in order of xg; each is tried in the rows in order
    of vertical distance, and the trial cost is the squared movement of that cell."""
    n = len(xg)
    if e is None:
        e = [Fraction(1)] * n
    e = [Fraction(v) for v in e]
    rows: list[list[int]] = [[] for _ in range(num_rows)]
    used = [0] * num_rows
    order = sorted(range(n), key=lambda i: (Fraction(xg[i]), i))  # @line L1
    for i in order:  # @line L2
        best, best_row = None, None
        by_dist = sorted(range(num_rows), key=lambda r: (abs(Fraction(r * row_height) - Fraction(yg[i])), r))
        for r in by_dist:  # @line L3
            dy2 = (Fraction(r * row_height) - Fraction(yg[i])) ** 2
            if best is not None and dy2 >= best:  # @line L4
                break
            if used[r] + w[i] > sites:  # @line L5
                continue
            trial = place_row(rows[r] + [i], xg, w, e, 0, sites)  # @line L6
            xi = cell_positions(trial[-1:], w)[i]
            cost = (xi - Fraction(xg[i])) ** 2 + dy2  # @line L7
            if best is None or cost < best:
                best, best_row = cost, r
        if best_row is None:
            raise ValueError(f"cell {i} fits in no row")
        rows[best_row].append(i)  # @line L8
        used[best_row] += w[i]
    x = [0] * n
    y = [0] * n
    for r in range(num_rows):  # @line L9
        for c in place_row(rows[r], xg, w, e, 0, sites):
            left = floor(c.x + Fraction(1, 2))  # round to a site; clusters stay apart
            off = 0
            for i in c.cells:
                x[i] = left + off
                y[i] = r * row_height
                off += w[i]
    return x, y


def movement(x, y, xg, yg, e=None) -> Fraction:
    """Total weighted squared movement."""
    n = len(x)
    e = [1] * n if e is None else e
    return sum(Fraction(e[i]) * ((Fraction(x[i]) - Fraction(xg[i])) ** 2 + (Fraction(y[i]) - Fraction(yg[i])) ** 2) for i in range(n))
