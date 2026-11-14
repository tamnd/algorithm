# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hint-based-feature-recognition/. The authors are listed in prov/0YXFJ0.jsonl.

"""Hint-based feature recognition for a rectilinear polygon in the plane.

The part P is a simple rectilinear polygon with integer vertices, and the
stock W is its bounding box. Every vertex coordinate gives a grid line, and
each grid cell lies in P or in the removal area D = W -* P. The method:

1. Hints. Every unit piece of the boundary of P between a P cell and a D
   cell is a hint, a trace of some feature, with its outward normal: the
   direction from the P cell into the D cell.
2. Completion. Sweep the D cell along the normal to the boundary of W. If
   the strip meets P, the face cannot be reached by a tool moving against
   the normal, and the hint is dropped. Otherwise grow the strip sideways,
   one column of cells at a time, while the new column stays in D.
3. Verification and classification. The completed rectangle lies in D and
   is open on the side the tool comes from, so it is a machinable feature.
   Its open sides give its type: a slot or a step.
4. Leftovers. D cells that no completed feature covers cannot be reached
   along any axis. In each row, the maximal run of D cells around them is
   reported as an undercut.

The result is exact: P = W -* (union of all feature rectangles).

Precondition: the polygon is simple and rectilinear, with integer
coordinates and distinct vertices.
Cost: for n vertices the grid has O(n^2) cells and O(n^2) hints. With 2D
prefix sums each strip test is O(1), and each completion grows by at most
O(n) columns. Distinct blocks reached from one side with the same inner
edge are disjoint, so marking their cells costs O(n^3) in all. The whole
method takes O(n^3) time and O(n^2) space.
"""

from __future__ import annotations

from fractions import Fraction

Rect = tuple[int, int, int, int]       # x0, y0, x1, y1

# the four normals, by the side of the stock that a feature opens onto
NORMALS = {"right": (1, 0), "left": (-1, 0), "top": (0, 1), "bottom": (0, -1)}


def point_in_polygon(poly, x, y) -> bool:
    inside = False
    n = len(poly)
    for k in range(n):
        (x0, y0), (x1, y1) = poly[k], poly[(k + 1) % n]
        if (y0 > y) != (y1 > y) and x0 + Fraction(x1 - x0) * (y - y0) / (y1 - y0) > x:
            inside = not inside
    return inside


class Grid:
    def __init__(self, poly):
        self.xs = sorted({p[0] for p in poly})
        self.ys = sorted({p[1] for p in poly})
        self.nx, self.ny = len(self.xs) - 1, len(self.ys) - 1
        self.stock = (self.xs[0], self.ys[0], self.xs[-1], self.ys[-1])
        self.D = set()
        for i in range(self.nx):
            for j in range(self.ny):
                cx = Fraction(self.xs[i] + self.xs[i + 1], 2)
                cy = Fraction(self.ys[j] + self.ys[j + 1], 2)
                if not point_in_polygon(poly, cx, cy):
                    self.D.add((i, j))
        S = [[0] * (self.ny + 1) for _ in range(self.nx + 1)]
        for i in range(self.nx):
            for j in range(self.ny):
                S[i + 1][j + 1] = S[i][j + 1] + S[i + 1][j] - S[i][j] + ((i, j) in self.D)
        self._S = S

    def all_D(self, i0, j0, i1, j1) -> bool:
        """Are all cells in [i0, i1) x [j0, j1) inside the grid and in D?"""
        if not (0 <= i0 < i1 <= self.nx and 0 <= j0 < j1 <= self.ny):
            return False
        S = self._S
        return S[i1][j1] - S[i0][j1] - S[i1][j0] + S[i0][j0] == (i1 - i0) * (j1 - j0)

    def rect(self, b) -> Rect:
        return (self.xs[b[0]], self.ys[b[1]], self.xs[b[2]], self.ys[b[3]])

    def open_sides(self, b) -> tuple[str, ...]:
        out = []
        if b[0] == 0: out.append("left")
        if b[2] == self.nx: out.append("right")
        if b[1] == 0: out.append("bottom")
        if b[3] == self.ny: out.append("top")
        return tuple(out)


def hints(g: Grid):
    """Every unit boundary piece between a P cell and a D cell, as the D
    cell and the outward normal of P there."""
    for (i, j) in sorted(g.D):
        for side, (di, dj) in NORMALS.items():
            q = (i - di, j - dj)
            if 0 <= q[0] < g.nx and 0 <= q[1] < g.ny and q not in g.D:
                yield (i, j), side


def complete(g: Grid, cell, side):
    """Sweep the cell to the stock along the normal, then grow sideways.
    Returns the block (i0, j0, i1, j1), or None if the strip meets P."""
    i, j = cell
    if side == "top":
        b = [i, j, i + 1, g.ny]
    elif side == "bottom":
        b = [i, 0, i + 1, j + 1]
    elif side == "right":
        b = [i, j, g.nx, j + 1]
    else:
        b = [0, j, i + 1, j + 1]
    if not g.all_D(*b):
        return None  # @line L3
    if side in ("top", "bottom"):
        while g.all_D(b[0] - 1, b[1], b[0], b[3]):
            b[0] -= 1
        while g.all_D(b[2], b[1], b[2] + 1, b[3]):
            b[2] += 1  # @line L4
    else:
        while g.all_D(b[0], b[1] - 1, b[2], b[1]):
            b[1] -= 1
        while g.all_D(b[0], b[3], b[2], b[3] + 1):
            b[3] += 1
    return tuple(b)


def kind(sides: tuple[str, ...]) -> str:
    """One open side is a slot, two (always adjacent, since every row and
    column of the grid holds a P cell) are a step, none is an undercut."""
    return ("undercut", "slot", "step")[len(sides)]


def undercut_runs(g: Grid, covered):
    """In each row, the maximal runs of D cells that hold a cell no feature
    covers. Runs of one row are disjoint, so this takes O(nx * ny) time."""
    out = []
    for j in range(g.ny):
        i = 0
        while i < g.nx:
            if (i, j) not in g.D:
                i += 1
                continue
            k = i
            while k < g.nx and (k, j) in g.D:
                k += 1
            if any((t, j) not in covered for t in range(i, k)):
                out.append((i, j, k, j + 1))
            i = k
    return out


def recognize(poly):
    """Return (stock, features). Each feature is a dict with the rectangle,
    its open sides, its kind, and the sides a tool can come from."""
    g = Grid(poly)  # @line L1
    found: dict = {}
    for cell, side in hints(g):  # @line L2
        b = complete(g, cell, side)
        if b is not None:
            found.setdefault(b, set()).add(side)  # @line L5
    covered = set()
    for b in found:
        covered |= {(i, j) for i in range(b[0], b[2]) for j in range(b[1], b[3])}
    undercuts = {b: set() for b in undercut_runs(g, covered)}  # @line L6
    feats = []
    for b, approach in list(found.items()) + list(undercuts.items()):
        sides = g.open_sides(b)
        feats.append({"rect": g.rect(b), "open": sides, "kind": kind(sides) if approach else "undercut",
                      "approach": tuple(sorted(approach))})
    feats.sort(key=lambda f: (f["kind"] == "undercut", f["rect"]))
    return g.stock, feats  # @line L7


def in_expression(stock: Rect, rects, x, y) -> bool:
    """Membership in stock -* (union of rects), for a point on no grid line."""
    X0, Y0, X1, Y1 = stock
    return X0 < x < X1 and Y0 < y < Y1 and not any(a < x < c and b < y < d for a, b, c, d in rects)
