# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volumetric-mesh-repair/. The authors are listed in prov/5S30QB.jsonl.

"""Volumetric repair in the plane: the 2D analogue of Ju's method (SIGGRAPH 2004).

The input is a soup of line segments that should bound regions, with gaps,
overlaps and dangling pieces. The steps are:

1. Scan conversion. A grid edge is marked when it crosses the input an odd number
   of times. The grid points are moved by a symbolic perturbation (eps, eps^2), so no
   grid point lies on a segment and each crossing falls on exactly one edge.
2. Patching. The dual curve of the marked edges has an end in each cell with an odd
   number of marked edges. These cells are joined in pairs by shortest paths of cells,
   and the edges between consecutive cells of a path change their marks.
3. Signs. A search from the outer corner gives each grid point a side; the side
   changes exactly across the marked edges.
4. Contouring. Marching squares joins the midpoints of the marked edges of each cell.

Coordinates and the cell size must be int or Fraction, so all tests are exact.
"""

from collections import deque
from fractions import Fraction
from math import ceil, floor
from typing import NamedTuple, Sequence, Union

Num = Union[int, Fraction]
Point = tuple[Num, Num]
Edge = tuple[str, int, int]  # ("h", i, j) joins (i, j) and (i + 1, j); ("v", i, j) joins (i, j) and (i, j + 1)


class Grid(NamedTuple):
    x0: Fraction
    y0: Fraction
    h: Fraction
    nx: int  # cells in x
    ny: int  # cells in y

    def point(self, i: int, j: int) -> tuple[Fraction, Fraction]:
        """The unperturbed position of the grid point (i, j)."""
        return (self.x0 + i * self.h, self.y0 + j * self.h)

    def cell_edges(self, i: int, j: int) -> list[Edge]:
        """The edges of cell (i, j) in counterclockwise order: bottom, right, top, left."""
        return [("h", i, j), ("v", i + 1, j), ("h", i, j + 1), ("v", i, j)]

    def cell_corners(self, i: int, j: int) -> list[tuple[int, int]]:
        return [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]


class Repair(NamedTuple):
    grid: Grid
    marked: set[Edge]  # the marked edges after patching
    odd_cells: list[tuple[int, int]]  # the ends of the dual curve before patching
    toggled: list[Edge]  # the edges whose mark the patching changed
    inside: dict[tuple[int, int], bool]  # the side of each grid point
    segments: list[tuple[Point, Point]]  # the output, inside on the left of each segment


def make_grid(segments: Sequence[tuple[Point, Point]], h: Num) -> Grid:
    """A grid of cell size h that contains every segment with at least one cell of margin."""
    h = Fraction(h)
    xs = [Fraction(p[0]) for s in segments for p in s] or [Fraction(0)]
    ys = [Fraction(p[1]) for s in segments for p in s] or [Fraction(0)]
    i0, j0 = floor(min(xs) / h) - 1, floor(min(ys) / h) - 1
    i1, j1 = ceil(max(xs) / h) + 1, ceil(max(ys) / h) + 1
    return Grid(i0 * h, j0 * h, h, i1 - i0, j1 - j0)


def crossed_edges(g: Grid, p: Point, q: Point) -> list[Edge]:
    """The grid edges that the segment pq crosses, with the grid points at (X + eps, Y + eps^2)."""
    px, py, qx, qy = Fraction(p[0]), Fraction(p[1]), Fraction(q[0]), Fraction(q[1])
    out: list[Edge] = []
    dx, dy = qx - px, qy - py
    # horizontal lines y = Y_j + eps^2: p is above when py > Y_j, a tie counts as below
    for j in range(g.ny + 1):
        yj = g.y0 + j * g.h
        if (py > yj) != (qy > yj):
            x = px + (yj - py) * dx / dy  # the crossing, compared with X_i + eps
            # x > X_i + eps  iff x > X_i;  x < X_{i+1} + eps  iff x <= X_{i+1}
            i = ceil((x - g.x0) / g.h) - 1
            if 0 <= i < g.nx:
                out.append(("h", i, j))
    # vertical lines x = X_i + eps: p is to the right when px > X_i, a tie counts as left
    for i in range(g.nx + 1):
        xi = g.x0 + i * g.h
        if (px > xi) != (qx > xi):
            y = py + (xi - px) * dy / dx  # the crossing at eps = 0
            t = (y - g.y0) / g.h
            j = floor(t)
            if t == j:  # on the line Y_j: the sign of eps*dy/dx - eps^2 decides
                if dy * dx <= 0:
                    j -= 1  # just below Y_j
            if 0 <= j < g.ny:
                out.append(("v", i, j))
    return out


def odd_cells(g: Grid, marked: set[Edge]) -> list[tuple[int, int]]:
    return [(i, j) for j in range(g.ny) for i in range(g.nx)
            if sum(e in marked for e in g.cell_edges(i, j)) % 2 == 1]


def _shared_edge(a: tuple[int, int], b: tuple[int, int]) -> Edge:
    (i, j), (k, l) = a, b
    if k == i + 1:
        return ("v", k, j)
    if k == i - 1:
        return ("v", i, j)
    if l == j + 1:
        return ("h", i, l)
    return ("h", i, j)


def repair(segments: Sequence[tuple[Point, Point]], h: Num) -> Repair:
    g = make_grid(segments, h)  # @line L1
    marked: set[Edge] = set()
    for p, q in segments:  # @line L2
        for e in crossed_edges(g, p, q):
            marked ^= {e}
    odd = odd_cells(g, marked)  # @line L3
    todo = set(odd)
    toggled: list[Edge] = []
    for c in odd:  # @line L4
        if c not in todo:
            continue
        todo.discard(c)
        prev = {c: c}
        dq = deque([c])
        found = None
        while dq:
            a = dq.popleft()
            if a in todo:
                found = a
                break
            i, j = a
            for b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= b[0] < g.nx and 0 <= b[1] < g.ny and b not in prev:
                    prev[b] = a
                    dq.append(b)
        assert found is not None  # the number of odd cells is even
        todo.discard(found)
        while found != c:  # @line L5
            e = _shared_edge(prev[found], found)
            marked ^= {e}
            toggled.append(e)
            found = prev[found]
    inside = {(0, 0): False}  # @line L6
    dq = deque([(0, 0)])
    while dq:
        i, j = dq.popleft()
        for (k, l), e in (((i + 1, j), ("h", i, j)), ((i - 1, j), ("h", i - 1, j)),
                          ((i, j + 1), ("v", i, j)), ((i, j - 1), ("v", i, j - 1))):
            if 0 <= k <= g.nx and 0 <= l <= g.ny and (k, l) not in inside:
                inside[(k, l)] = inside[(i, j)] ^ (e in marked)
                dq.append((k, l))
    out: list[tuple[Point, Point]] = []
    for j in range(g.ny):  # @line L7
        for i in range(g.nx):
            out += _cell_segments(g, i, j, inside, marked)
    return Repair(g, marked, odd, toggled, inside, out)  # @line L8


def _midpoint(g: Grid, e: Edge) -> Point:
    kind, i, j = e
    x, y = g.point(i, j)
    return (x + g.h / 2, y) if kind == "h" else (x, y + g.h / 2)


def _cell_segments(g: Grid, i: int, j: int, inside: dict[tuple[int, int], bool],
                   marked: set[Edge]) -> list[tuple[Point, Point]]:
    """Join each edge where the side goes from inside to outside, counterclockwise, to the next
    edge where it goes back. In a saddle cell this joins the two inside corners."""
    corners = g.cell_corners(i, j)
    edges = g.cell_edges(i, j)
    s = [inside[c] for c in corners]
    for k in range(4):
        assert (s[k] != s[(k + 1) % 4]) == (edges[k] in marked)
    segs = []
    for k in range(4):
        if s[k] and not s[(k + 1) % 4]:  # inside to outside
            m = (k + 1) % 4
            while not (not s[m] and s[(m + 1) % 4]):
                m = (m + 1) % 4
            segs.append((_midpoint(g, edges[k]), _midpoint(g, edges[m])))
    return segs
