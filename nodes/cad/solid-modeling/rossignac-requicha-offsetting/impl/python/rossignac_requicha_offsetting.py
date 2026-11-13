# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rossignac-requicha-offsetting/. The authors are listed in prov/B7AHTM.jsonl.

"""Growing and shrinking a planar CSG solid by the method of Rossignac and Requicha, exactly.

A solid is a CSG tree of closed axis-aligned boxes with rational corners and
the regularized operations union, intersection and difference. Growing by r
replaces the solid S by the union of S with the boundary edges of S swept by
r along their normals (closed rectangles, the "slabs") and the boundary
vertices swept by r (closed disks). Shrinking uses the same primitives: a
point of S is in the regularized shrink when it is not inside their union,
which is the complement of the grown complement.

Membership is exact in rational arithmetic. A point is classified as "in",
"on" or "out" of a union of primitives with a neighborhood test: the
primitives that hold the point on their boundary must cover every direction
around it, and a disk only covers the open half plane on its side of its
tangent.
"""

from fractions import Fraction
from functools import cmp_to_key

# --- CSG of boxes -----------------------------------------------------------


def box(x0, x1, y0, y1):
    return ("box", (Fraction(x0), Fraction(x1), Fraction(y0), Fraction(y1)))


def union(a, b):
    return ("union", a, b)


def inter(a, b):
    return ("inter", a, b)


def diff(a, b):
    return ("diff", a, b)


def boxes_of(t):
    if t[0] == "box":
        return [t[1]]
    return boxes_of(t[1]) + boxes_of(t[2])


def open_member(t, p) -> bool:
    """Membership of a point that lies on no box boundary, so no rule for ties is needed."""
    if t[0] == "box":
        x0, x1, y0, y1 = t[1]
        return x0 < p[0] < x1 and y0 < p[1] < y1
    a, b = open_member(t[1], p), open_member(t[2], p)
    if t[0] == "union":
        return a or b
    if t[0] == "inter":
        return a and b
    return a and not b


class Solid:
    """The regularized set of a CSG tree, as the closed cells of the grid of its box coordinates."""

    def __init__(self, tree):
        bs = boxes_of(tree)
        self.xs = sorted({b[0] for b in bs} | {b[1] for b in bs})
        self.ys = sorted({b[2] for b in bs} | {b[3] for b in bs})
        nx, ny = len(self.xs) - 1, len(self.ys) - 1
        self.cell = [[open_member(tree, ((self.xs[i] + self.xs[i + 1]) / 2, (self.ys[j] + self.ys[j + 1]) / 2)) for j in range(ny)] for i in range(nx)]
        self.cells = [(self.xs[i], self.xs[i + 1], self.ys[j], self.ys[j + 1]) for i in range(nx) for j in range(ny) if self.cell[i][j]]
        self.edges = self._boundary()
        self.vertices = sorted({p for e in self.edges for p in e})

    def _in(self, i, j) -> bool:
        return 0 <= i < len(self.cell) and 0 <= j < len(self.cell[0]) and self.cell[i][j]

    def _boundary(self):
        """Maximal boundary segments: grid edges between an inside cell and an outside cell, merged."""
        nx, ny = len(self.xs) - 1, len(self.ys) - 1
        edges = []
        for j in range(ny + 1):  # horizontal edges at y = ys[j]
            run = None
            for i in range(nx):
                if self._in(i, j - 1) != self._in(i, j):
                    run = (self.xs[i] if run is None else run[0], self.xs[i + 1])
                else:
                    if run:
                        edges.append(((run[0], self.ys[j]), (run[1], self.ys[j])))
                    run = None
            if run:
                edges.append(((run[0], self.ys[j]), (run[1], self.ys[j])))
        for i in range(nx + 1):  # vertical edges at x = xs[i]
            run = None
            for j in range(ny):
                if self._in(i - 1, j) != self._in(i, j):
                    run = (self.ys[j] if run is None else run[0], self.ys[j + 1])
                else:
                    if run:
                        edges.append(((self.xs[i], run[0]), (self.xs[i], run[1])))
                    run = None
            if run:
                edges.append(((self.xs[i], run[0]), (self.xs[i], run[1])))
        return edges

    def contains(self, p) -> bool:
        return any(c[0] <= p[0] <= c[1] and c[2] <= p[1] <= c[3] for c in self.cells)

    def on_boundary(self, p) -> bool:
        for (a, b) in self.edges:
            if min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
                return True
        return False


# --- the swept primitives ---------------------------------------------------


def slab(edge, r):
    """An axis-parallel edge swept by r on both sides along its normal: a closed box."""
    (a, b) = edge
    if a[1] == b[1]:
        return ("rect", (min(a[0], b[0]), max(a[0], b[0]), a[1] - r, a[1] + r))
    return ("rect", (a[0] - r, a[0] + r, min(a[1], b[1]), max(a[1], b[1])))


def disk(p, r):
    return ("disk", (p, r))


def where(prim, x):
    """-1 inside, 0 on the boundary, +1 outside the closed primitive."""
    kind, d = prim
    if kind == "rect":
        x0, x1, y0, y1 = d
        if x0 < x[0] < x1 and y0 < x[1] < y1:
            return -1
        return 0 if (x0 <= x[0] <= x1 and y0 <= x[1] <= y1) else 1
    (c, r) = d
    s = (x[0] - c[0]) ** 2 + (x[1] - c[1]) ** 2 - r * r
    return (s > 0) - (s < 0)


# --- neighborhood classification --------------------------------------------


def half(v) -> int:
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def sort_by_angle(vs):
    def cmp(a, b):
        ha, hb = half(a), half(b)
        if ha != hb:
            return ha - hb
        c = cross(a, b)
        return -1 if c > 0 else (1 if c < 0 else 0)

    out = []
    for v in sorted(vs, key=cmp_to_key(cmp)):
        if not out or cmp(out[-1], v) != 0:
            out.append(v)
    return out


def in_cone(prim, x, v) -> bool:
    """For a rectangle with x on its boundary: is direction v in its closed tangent cone at x?"""
    x0, x1, y0, y1 = prim[1]
    return (x[0] != x0 or v[0] >= 0) and (x[0] != x1 or v[0] <= 0) and (x[1] != y0 or v[1] >= 0) and (x[1] != y1 or v[1] <= 0)


def disk_covers(prim, x, v) -> bool:
    """A disk with x on its circle covers the directions in the open half plane towards its center."""
    (c, _) = prim[1]
    return v[0] * (c[0] - x[0]) + v[1] * (c[1] - x[1]) > 0


def covers_neighborhood(touching, x) -> bool:
    """Do the primitives that hold x on their boundary cover a whole neighborhood of x?"""
    rays = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for prim in touching:
        if prim[0] == "disk":
            (c, _) = prim[1]
            w = (c[0] - x[0], c[1] - x[1])
            rays += [(-w[1], w[0]), (w[1], -w[0])]
    rays = sort_by_angle(rays)
    rects = [p for p in touching if p[0] == "rect"]
    disks = [p for p in touching if p[0] == "disk"]

    def generic(m):
        return any(in_cone(p, x, m) for p in rects) or any(disk_covers(p, x, m) for p in disks)

    n = len(rays)
    for k in range(n):
        v, nxt, prv = rays[k], rays[(k + 1) % n], rays[k - 1]
        m_after = (v[0] + nxt[0], v[1] + nxt[1])
        m_before = (v[0] + prv[0], v[1] + prv[1])
        if not generic(m_after):  # the open sector after v
            return False
        if not generic(v):  # the ray v itself
            return False
        for m in (m_before, m_after):  # the thin germs on each side of v
            if not (any(in_cone(p, x, v) and in_cone(p, x, m) for p in rects) or any(disk_covers(p, x, v) for p in disks)):
                return False
    return True


# --- the method -------------------------------------------------------------


class Grown:
    """S grown by r, as the union of S with its swept boundary edges and vertices."""

    def __init__(self, S: Solid, r):
        self.S, self.r, self.prims = S, Fraction(r), []

    def classify_primitives(self, x) -> str:
        """in, on or out of the union of the swept primitives alone."""
        w = [where(p, x) for p in self.prims]
        if any(s < 0 for s in w):  # @line L6
            return "in"
        touching = [p for p, s in zip(self.prims, w) if s == 0]
        if not touching:  # @line L7
            return "out"
        if covers_neighborhood(touching, x):  # @line L8
            return "in"
        return "on"  # @line L9

    def classify(self, x) -> str:
        """in, on or out of the grown solid."""
        x = (Fraction(x[0]), Fraction(x[1]))
        if self.S.contains(x) and not self.S.on_boundary(x):
            return "in"
        return self.classify_primitives(x)

    def contains(self, x) -> bool:
        return self.classify(x) != "out"


def grow(tree, r) -> Grown:
    if Fraction(r) <= 0:
        raise ValueError("the distance must be positive")
    S = Solid(tree)  # @line L1
    T = Grown(S, r)  # @line L2
    T.prims += [slab(e, T.r) for e in S.edges]  # @line L3
    T.prims += [disk(p, T.r) for p in S.vertices]  # @line L4
    return T  # @line L5


def shrink_classify(tree_or_grown, r, x) -> str:
    """in, on or out of the regularized shrink of S by r."""
    G = tree_or_grown if isinstance(tree_or_grown, Grown) else grow(tree_or_grown, r)
    x = (Fraction(x[0]), Fraction(x[1]))
    if not G.S.contains(x):  # @line L10
        return "out"
    c = G.classify_primitives(x)  # @line L11
    return {"out": "in", "on": "on", "in": "out"}[c]  # @line L12
