# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-spline-linear-independence/. The authors are listed in prov/8C8B3H.jsonl.

"""Linear independence of bicubic T-spline blending functions, checked exactly.

The T-mesh is in index space, as on the t-spline page: vertical lines 0..m
with knot values sv, horizontal lines 0..n with values tv, and sets of unit
edges h and v. The outer two lines on each side must be complete.

nurbs_matrix(mesh) builds the T-spline-to-NURBS matrix M column by column:
column A holds the coefficients of the blending function T_A in the tensor
B-splines on all index lines, found by Boehm insertion into the local knot
vectors of A. Theorem 1 of Li, Zheng, Sederberg, Hughes and Scott says that
the T_A are linearly independent if and only if M has full column rank;
rank and null_vector decide this exactly with Fraction.
"""

from fractions import Fraction

DIRS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
OPP = {"R": "L", "L": "R", "U": "D", "D": "U"}


class TMesh:
    def __init__(self, sv, tv):
        self.sv, self.tv = list(sv), list(tv)
        self.m, self.n = len(sv) - 1, len(tv) - 1
        self.h, self.v = set(), set()

    def copy(self):
        o = TMesh(self.sv, self.tv)
        o.h, o.v = set(self.h), set(self.v)
        return o

    def add_h(self, i0, i1, j):
        self.h.update((i, j) for i in range(min(i0, i1), max(i0, i1)))

    def add_v(self, i, j0, j1):
        self.v.update((i, j) for j in range(min(j0, j1), max(j0, j1)))

    def add_lines(self, cols, rows):
        for i in cols:
            self.add_v(i, 0, self.n)
        for j in rows:
            self.add_h(0, self.m, j)

    def on_v(self, i, j):
        return (i, j) in self.v or (i, j - 1) in self.v

    def on_h(self, i, j):
        return (i, j) in self.h or (i - 1, j) in self.h

    def is_vertex(self, i, j):
        return self.on_v(i, j) and self.on_h(i, j)

    def has_edge(self, i, j, d):
        return {"R": (i, j) in self.h, "L": (i - 1, j) in self.h, "U": (i, j) in self.v, "D": (i, j - 1) in self.v}[d]

    def inside(self, i, j):
        return 0 <= i <= self.m and 0 <= j <= self.n

    def march(self, i, j, d, count):
        """The first count points from (i, j) in direction d that lie on perpendicular edges."""
        di, dj = DIRS[d]
        out = []
        while len(out) < count:
            i, j = i + di, j + dj
            if not self.inside(i, j):
                break
            if (self.on_v(i, j) if d in "RL" else self.on_h(i, j)):
                out.append((i, j))
        return out

    def anchors(self):
        return [(i, j) for j in range(2, self.n - 1) for i in range(2, self.m - 1) if self.is_vertex(i, j)]

    def local_index_vectors(self, i, j):
        r = [p[0] for p in self.march(i, j, "R", 2)]
        l = [p[0] for p in self.march(i, j, "L", 2)]
        u = [p[1] for p in self.march(i, j, "U", 2)]
        d = [p[1] for p in self.march(i, j, "D", 2)]
        if min(len(r), len(l), len(u), len(d)) < 2:
            raise ValueError("a ray left the mesh; complete the outer lines")
        return (tuple(l[::-1] + [i] + r), tuple(d[::-1] + [j] + u))


def extensions(mesh):
    """T-junction extensions as closed segments (horizontal?, line, lo, hi)."""
    out = []
    for i in range(mesh.m + 1):
        for j in range(mesh.n + 1):
            if not mesh.is_vertex(i, j):
                continue
            for d in "RLUD":
                di, dj = DIRS[d]
                if mesh.inside(i + di, j + dj) and not mesh.has_edge(i, j, d) and mesh.has_edge(i, j, OPP[d]):
                    f = mesh.march(i, j, d, 2)[-1]
                    e = mesh.march(i, j, OPP[d], 1)[0]
                    if d in "RL":
                        out.append((True, j, min(f[0], e[0]), max(f[0], e[0])))
                    else:
                        out.append((False, i, min(f[1], e[1]), max(f[1], e[1])))
    return out


def is_analysis_suitable(mesh):
    """Definition 7 of Li and coauthors: no horizontal extension meets a vertical one."""
    ext = extensions(mesh)
    hor = [x for x in ext if x[0]]
    ver = [x for x in ext if not x[0]]
    return not any(lo <= i <= hi and lo2 <= j <= hi2 for _, j, lo, hi in hor for _, i, lo2, hi2 in ver)


def insert_one(knots, x, values):
    """Boehm's rule for one cubic B-spline with index knots."""
    tau = sorted(list(knots) + [x])
    t = [values[k] for k in knots]
    u = values[x]
    c0 = Fraction(1) if u >= t[3] else (u - t[0]) / (t[3] - t[0])
    c1 = Fraction(1) if u <= t[1] else (t[4] - u) / (t[4] - t[1])
    return [(c0, tuple(tau[:5])), (c1, tuple(tau[1:]))]


def to_global(knots, values):
    """Coefficients of N[knots] in the B-splines on all index lines: {first index: coefficient}."""
    funcs = {tuple(knots): Fraction(1)}
    for x in range(knots[0] + 1, knots[-1]):
        if x in knots:
            continue
        nxt = {}
        for kn, c in funcs.items():
            parts = insert_one(kn, x, values) if kn[0] < x < kn[-1] and x not in kn else [(1, kn)]
            for c2, k2 in parts:
                if c2:
                    nxt[k2] = nxt.get(k2, Fraction(0)) + c * c2
        funcs = nxt
    return {kn[0]: c for kn, c in funcs.items()}


def nurbs_matrix(mesh):
    """The anchors and the columns of M: column A is {(a, b): coefficient of B_a(s) B_b(t)}."""
    anchors = mesh.anchors()
    cols = []
    for A in anchors:
        s, t = mesh.local_index_vectors(*A)
        ds, dt = to_global(s, mesh.sv), to_global(t, mesh.tv)
        cols.append({(a, b): x * y for a, x in ds.items() for b, y in dt.items()})
    return anchors, cols


def _echelon(cols):
    keys = sorted({k for c in cols for k in c})
    rows = [[c.get(k, Fraction(0)) for c in cols] for k in keys]
    pivots, r = [], 0
    for c in range(len(cols)):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        p = rows[r][c]
        rows[r] = [x / p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
    return rows[:r], pivots


def rank(cols):
    return len(_echelon(cols)[1])


def null_vector(cols):
    """A nonzero delta with sum_A delta_A column_A = 0, or None if the rank is full."""
    rows, pivots = _echelon(cols)
    free = [c for c in range(len(cols)) if c not in pivots]
    if not free:
        return None
    f = free[0]
    delta = [Fraction(0)] * len(cols)
    delta[f] = Fraction(1)
    for row, c in zip(rows, pivots):
        delta[c] = -row[f]
    return delta


def bspline(knots, x, last):
    """Cubic B-spline on five knot values at x, by Cox-de Boor (closed at the last knot)."""
    vals = [Fraction(int(a <= x < b or (a < b == last == x))) for a, b in zip(knots, knots[1:])]
    for d in range(1, 4):
        vals = [
            ((x - knots[k]) / (knots[k + d] - knots[k]) * vals[k] if knots[k + d] != knots[k] else 0)
            + ((knots[k + d + 1] - x) / (knots[k + d + 1] - knots[k + 1]) * vals[k + 1] if knots[k + d + 1] != knots[k + 1] else 0)
            for k in range(len(vals) - 1)
        ]
    return vals[0]


def blend(mesh, A, s, t):
    si, ti = mesh.local_index_vectors(*A)
    return bspline([mesh.sv[k] for k in si], s, mesh.sv[-1]) * bspline([mesh.tv[k] for k in ti], t, mesh.tv[-1])
