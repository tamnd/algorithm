# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volume-decomposition-feature-recognition/. The authors are listed in prov/Y3M61K.jsonl.

"""Cell-based feature recognition for a rectilinear polygon in the plane.

The part P is a simple rectilinear polygon with integer vertices, given as a
list of vertices in order. The stock W is its bounding box, and the removal
volume, here an area, is the delta D = W minus P. The method:

1. Extends every edge of P to a full line across W. The lines cut W into
   grid cells, and each cell lies in P or in D.
2. Composes the cells of D into all maximal rectangles of D cells: those
   that cannot grow by one row or column of cells and stay in D.
3. Picks a set of maximal rectangles that covers every D cell, with the
   fewest rectangles, by a depth-first branch and bound.
4. Returns the expression P = W -* (R_1 u ... u R_k), where -* is the
   regularized difference, and for each rectangle the sides that lie on the
   boundary of W, which say from where a tool can enter.

The expression is exact: the chosen rectangles lie in D and cover it, so
their union is D, and W -* D = P.

Precondition: the polygon is simple and rectilinear, with integer
coordinates, and its vertices are distinct.
Cost: for n vertices the grid has c = O(n^2) cells. Step 2 checks O(c^2)
rectangles in O(1) each with prefix sums. Step 3 is a set cover search,
O(m^k c) in the worst case for m maximal rectangles and an optimal cover of
size k, since set cover is NP-hard in general.
"""

from __future__ import annotations

from fractions import Fraction

Point = tuple[int, int]
Rect = tuple[int, int, int, int]      # x0, y0, x1, y1


def point_in_polygon(poly: list[Point], x: Fraction, y: Fraction) -> bool:
    """Crossing number test for a point that is not on the boundary."""
    inside = False
    n = len(poly)
    for k in range(n):
        (x0, y0), (x1, y1) = poly[k], poly[(k + 1) % n]
        if (y0 > y) != (y1 > y):
            xc = x0 + Fraction(x1 - x0) * (y - y0) / (y1 - y0)
            if xc > x:
                inside = not inside
    return inside


class Decomposition:
    def __init__(self, poly: list[Point]):
        self.poly = poly
        xs = sorted({p[0] for p in poly})  # @line L1
        ys = sorted({p[1] for p in poly})
        self.xs, self.ys = xs, ys
        self.stock = (xs[0], ys[0], xs[-1], ys[-1])
        nx, ny = len(xs) - 1, len(ys) - 1
        self.nx, self.ny = nx, ny
        self.delta = set()
        for i in range(nx):
            for j in range(ny):
                cx, cy = Fraction(xs[i] + xs[i + 1], 2), Fraction(ys[j] + ys[j + 1], 2)
                if not point_in_polygon(poly, cx, cy):  # @line L2
                    self.delta.add((i, j))
        # prefix sums of D cells, to test a block of cells in O(1)
        S = [[0] * (ny + 1) for _ in range(nx + 1)]
        for i in range(nx):
            for j in range(ny):
                S[i + 1][j + 1] = S[i][j + 1] + S[i + 1][j] - S[i][j] + ((i, j) in self.delta)
        self._S = S

    def all_delta(self, i0: int, j0: int, i1: int, j1: int) -> bool:
        """Are all cells i0 <= i < i1, j0 <= j < j1 in D?"""
        if not (0 <= i0 < i1 <= self.nx and 0 <= j0 < j1 <= self.ny):
            return False
        S = self._S
        return S[i1][j1] - S[i0][j1] - S[i1][j0] + S[i0][j0] == (i1 - i0) * (j1 - j0)

    def maximal_blocks(self) -> list[tuple[int, int, int, int]]:
        """All maximal blocks of D cells, as cell index ranges [i0, i1) x [j0, j1)."""
        out = []
        for i0 in range(self.nx):
            for i1 in range(i0 + 1, self.nx + 1):
                for j0 in range(self.ny):
                    for j1 in range(j0 + 1, self.ny + 1):
                        if not self.all_delta(i0, j0, i1, j1):  # @line L3
                            continue
                        if (self.all_delta(i0 - 1, j0, i1, j1) or self.all_delta(i0, j0, i1 + 1, j1)
                                or self.all_delta(i0, j0 - 1, i1, j1) or self.all_delta(i0, j0, i1, j1 + 1)):
                            continue  # @line L4
                        out.append((i0, j0, i1, j1))
        return out

    def to_rect(self, b) -> Rect:
        i0, j0, i1, j1 = b
        return (self.xs[i0], self.ys[j0], self.xs[i1], self.ys[j1])

    def open_sides(self, r: Rect) -> tuple[str, ...]:
        """The sides of r on the boundary of the stock, from which it is open."""
        X0, Y0, X1, Y1 = self.stock
        sides = []
        if r[0] == X0: sides.append("left")
        if r[2] == X1: sides.append("right")
        if r[1] == Y0: sides.append("bottom")
        if r[3] == Y1: sides.append("top")
        return tuple(sides)


def minimum_cover(cells: set, blocks: list) -> list:
    """The fewest blocks whose cells cover all of cells, by depth-first
    branch and bound on the first uncovered cell."""
    members = [frozenset((i, j) for i in range(b[0], b[2]) for j in range(b[1], b[3])) for b in blocks]
    by_cell: dict = {}
    for k, m in enumerate(members):
        for c in m:
            by_cell.setdefault(c, []).append(k)
    order = sorted(cells)
    best = [list(range(len(blocks)))]

    def search(chosen: list, covered: frozenset):
        if len(chosen) >= len(best[0]):
            return
        first = next((c for c in order if c not in covered), None)
        if first is None:
            best[0] = list(chosen)
            return
        for k in by_cell[first]:  # @line L5
            search(chosen + [k], covered | members[k])

    search([], frozenset())
    return [blocks[k] for k in best[0]]


def recognize(poly: list[Point]):
    """Return (stock, features), where features is a list of (rectangle,
    open sides), such that P = stock -* (union of the rectangles)."""
    dec = Decomposition(poly)
    blocks = dec.maximal_blocks()
    cover = minimum_cover(dec.delta, blocks)
    rects = sorted(dec.to_rect(b) for b in cover)
    return dec.stock, [(r, dec.open_sides(r)) for r in rects]  # @line L6


def in_expression(stock: Rect, rects: list[Rect], x: Fraction, y: Fraction) -> bool:
    """Membership in stock -* (union of rects), for a point on no grid line."""
    X0, Y0, X1, Y1 = stock
    if not (X0 < x < X1 and Y0 < y < Y1):
        return False
    return not any(a < x < c and b < y < d for a, b, c, d in rects)
