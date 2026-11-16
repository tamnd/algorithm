# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boustrophedon-cell-decomposition/. The authors are listed in prov/E8C6B2.jsonl.

"""Boustrophedon cell decomposition (Choset and Pignon 1998) and the coverage path.

The region is the rectangle [0, W] x [0, H] minus disjoint convex polygonal obstacles in
its interior. Coordinates are Fractions (or ints), so all tests are exact. General
position: each obstacle has a unique leftmost and a unique rightmost vertex, and no two
obstacles share the x of such a vertex.

A vertical line sweeps from left to right. Between critical points, the slice of free
space is a fixed number of intervals; each interval traces one cell. At the leftmost
vertex of an obstacle (an IN event) one interval splits into two; at the rightmost
vertex (an OUT event) two intervals merge into one. Each cell is then covered by
vertical lanes, up and down, and the cells are visited in depth-first order.
"""

from fractions import Fraction
import math


def polygon_slice(poly, x):
    """(ylo, yhi) of a convex polygon on the vertical line at x, or None if it misses."""
    ys = []
    m = len(poly)
    for i in range(m):
        (ax, ay), (bx, by) = poly[i], poly[(i + 1) % m]
        if ax == bx:
            if ax == x:
                ys += [ay, by]
        elif min(ax, bx) <= x <= max(ax, bx):
            ys.append(ay + (by - ay) * (x - ax) / (bx - ax))
    return (min(ys), max(ys)) if ys else None


class Cell:
    """A cell between x0 and x1. low and high are obstacle indices, or None for the
    bottom (y = 0) and top (y = H) of the rectangle."""

    def __init__(self, cid, x0, low, high):
        self.id, self.x0, self.x1, self.low, self.high = cid, x0, None, low, high

    def __repr__(self):
        return f"Cell({self.id}, {self.x0}..{self.x1}, low={self.low}, high={self.high})"


def floor_y(cell, obstacles, x):
    """The y of the lower wall of the cell at x."""
    return Fraction(0) if cell.low is None else polygon_slice(obstacles[cell.low], x)[1]


def ceil_y(cell, obstacles, x, height):
    """The y of the upper wall of the cell at x."""
    return Fraction(height) if cell.high is None else polygon_slice(obstacles[cell.high], x)[0]


def decompose(width, height, obstacles):
    """Returns (cells, adjacency): a list of Cells and a dict from cell id to a set of ids."""
    events = []
    for k, poly in enumerate(obstacles):
        xs = [p[0] for p in poly]
        events.append((min(xs), 0, k))  # IN
        events.append((max(xs), 1, k))  # OUT
    events.sort()  # @line L1
    cells, adj = [], {}

    def open_cell(x, low, high):
        c = Cell(len(cells), x, low, high)
        cells.append(c)
        adj[c.id] = set()
        return c

    def link(a, b):
        adj[a.id].add(b.id)
        adj[b.id].add(a.id)

    active = []  # obstacles crossing the sweep line, from bottom to top
    gaps = [open_cell(Fraction(0), None, None)]  # @line L2
    for x, kind, k in events:  # @line L3
        poly = obstacles[k]
        if kind == 0:  # @line L4
            yv = next(p[1] for p in poly if p[0] == x)
            pos = sum(1 for j in active if polygon_slice(obstacles[j], x)[1] < yv)
            old = gaps[pos]
            old.x1 = x
            below, above = open_cell(x, old.low, k), open_cell(x, k, old.high)
            link(old, below)
            link(old, above)
            active.insert(pos, k)
            gaps[pos:pos + 1] = [below, above]  # @line L4
        else:  # @line L5
            pos = active.index(k)
            below, above = gaps[pos], gaps[pos + 1]
            below.x1 = above.x1 = x
            merged = open_cell(x, below.low, above.high)
            link(below, merged)
            link(above, merged)
            del active[pos]
            gaps[pos:pos + 2] = [merged]  # @line L5
    for c in gaps:  # @line L6
        c.x1 = Fraction(width)
    return cells, adj


def cell_area(cell, obstacles, height):
    """Exact area: the height of the cell is linear between vertex abscissas."""
    xs = {cell.x0, cell.x1}
    for k in (cell.low, cell.high):
        if k is not None:
            xs |= {p[0] for p in obstacles[k] if cell.x0 < p[0] < cell.x1}
    xs = sorted(xs)
    gap = [ceil_y(cell, obstacles, x, height) - floor_y(cell, obstacles, x) for x in xs]
    return sum((xs[i + 1] - xs[i]) * (gap[i] + gap[i + 1]) / 2 for i in range(len(xs) - 1))


def locate(cells, obstacles, height, x, y):
    """The ids of the cells whose interior contains (x, y) (one for a free point off the event lines)."""
    return [c.id for c in cells
            if c.x0 < x < c.x1 and floor_y(c, obstacles, x) < y < ceil_y(c, obstacles, x, height)]


def dfs_order(adj, start=0):
    """Cells in the order a depth-first search first reaches them, smallest id first."""
    order, seen, stack = [], set(), [start]
    while stack:
        c = stack.pop()
        if c in seen:
            continue
        seen.add(c)
        order.append(c)
        stack.extend(sorted(adj[c] - seen, reverse=True))
    return order  # @line L7


def lanes(cell, obstacles, height, w):
    """ceil(width / w) evenly spaced vertical lanes; returns (x, ylo, yhi) for each, bottom-up."""
    span = cell.x1 - cell.x0
    m = max(1, math.ceil(span / w))
    out = []
    for i in range(m):
        x = cell.x0 + (2 * i + 1) * span / (2 * m)  # @line L8
        out.append((x, floor_y(cell, obstacles, x), ceil_y(cell, obstacles, x, height)))
    return out


def coverage_path(cells, adj, obstacles, height, w):
    """The lane segments in visiting order, alternating up and down inside each cell."""
    path = []
    for cid in dfs_order(adj):
        for i, (x, lo, hi) in enumerate(lanes(cells[cid], obstacles, height, w)):
            path.append(((x, lo), (x, hi)) if i % 2 == 0 else ((x, hi), (x, lo)))  # @line L8
    return path
