# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-spline/. The authors are listed in prov/80ZTCE.jsonl.

"""Bicubic T-splines in index space (Sederberg and coauthors, 2003).

A T-mesh lives on the integer grid of index space. Vertical index lines
0..m carry the s knot values sv[0..m], horizontal index lines 0..n carry the
t knot values tv[0..n]; both lists are nondecreasing, and a repeated value
gives a zero knot interval. The mesh is a set of unit edges:

- (i, j) in h means the horizontal edge from (i, j) to (i + 1, j);
- (i, j) in v means the vertical edge from (i, j) to (i, j + 1).

The four outer lines on each side (0, 1, m - 1, m and 0, 1, n - 1, n) must be
complete, so that every ray finds two knots. The anchors (control points) of
a bicubic T-spline are the vertices (i, j) with 2 <= i <= m - 2 and
2 <= j <= n - 2. Use Fraction for exact results.
"""

from fractions import Fraction


class TMesh:
    def __init__(self, sv, tv):
        self.sv = list(sv)
        self.tv = list(tv)
        self.m = len(sv) - 1
        self.n = len(tv) - 1
        self.h = set()
        self.v = set()

    @classmethod
    def full_grid(cls, sv, tv):
        mesh = cls(sv, tv)
        for j in range(mesh.n + 1):
            mesh.add_h(0, mesh.m, j)
        for i in range(mesh.m + 1):
            mesh.add_v(i, 0, mesh.n)
        return mesh

    @classmethod
    def frame(cls, sv, tv):
        """The four outer lines on each side, complete, and nothing inside."""
        mesh = cls(sv, tv)
        m, n = mesh.m, mesh.n
        for j in (0, 1, n - 1, n):
            mesh.add_h(0, m, j)
        for i in (0, 1, m - 1, m):
            mesh.add_v(i, 0, n)
        for j in range(n + 1):
            mesh.add_h(0, 1, j)
            mesh.add_h(m - 1, m, j)
        for i in range(m + 1):
            mesh.add_v(i, 0, 1)
            mesh.add_v(i, n - 1, n)
        return mesh

    def copy(self):
        other = TMesh(self.sv, self.tv)
        other.h = set(self.h)
        other.v = set(self.v)
        return other

    def add_h(self, i0, i1, j):
        """Add the horizontal segment from (i0, j) to (i1, j)."""
        for i in range(i0, i1):
            self.h.add((i, j))

    def add_v(self, i, j0, j1):
        """Add the vertical segment from (i, j0) to (i, j1)."""
        for j in range(j0, j1):
            self.v.add((i, j))

    def on_v(self, i, j):
        return (i, j) in self.v or (i, j - 1) in self.v

    def on_h(self, i, j):
        return (i, j) in self.h or (i - 1, j) in self.h

    def is_vertex(self, i, j):
        return self.on_v(i, j) and self.on_h(i, j)

    def anchors(self):
        return [
            (i, j)
            for j in range(2, self.n - 1)
            for i in range(2, self.m - 1)
            if self.is_vertex(i, j)
        ]

    def local_index_vectors(self, i, j):
        """Index lines of the local knot vectors of the anchor (i, j)."""
        s = [i]  # @line L1
        right = [k for k in range(i + 1, self.m + 1) if self.on_v(k, j)][:2]  # @line L2
        left = [k for k in range(i - 1, -1, -1) if self.on_v(k, j)][:2]  # @line L3
        s = left[::-1] + s + right
        up = [k for k in range(j + 1, self.n + 1) if self.on_h(i, k)][:2]  # @line L4
        down = [k for k in range(j - 1, -1, -1) if self.on_h(i, k)][:2]
        t = down[::-1] + [j] + up
        if len(s) != 5 or len(t) != 5:
            raise ValueError("a ray left the mesh; complete the outer lines")
        return s, t

    def local_knots(self, i, j):
        si, ti = self.local_index_vectors(i, j)
        return [self.sv[k] for k in si], [self.tv[k] for k in ti]  # @line L5


def bspline(knots, x, last=None):
    """The B-spline with the given knots (degree len - 2) at x, by Cox-de Boor.

    The pieces are half open, [a, b). If last is given, the interval that ends
    at last is closed, so the basis is right continuous at the domain end.
    """
    p = len(knots) - 2
    x = Fraction(x)
    vals = []
    for a, b in zip(knots, knots[1:]):
        inside = a <= x < b or (last is not None and a < b == last == x)
        vals.append(Fraction(1) if inside else Fraction(0))
    for d in range(1, p + 1):
        nxt = []
        for k in range(len(vals) - 1):
            val = Fraction(0)
            if knots[k + d] != knots[k]:
                val += (x - knots[k]) / (knots[k + d] - knots[k]) * vals[k]
            if knots[k + d + 1] != knots[k + 1]:
                val += (knots[k + d + 1] - x) / (knots[k + d + 1] - knots[k + 1]) * vals[k + 1]
            nxt.append(val)
        vals = nxt
    return vals[0]


def blend(mesh, anchor, s, t):
    """The blending function T_A(s, t) = N[s_A](s) N[t_A](t)."""
    sk, tk = mesh.local_knots(*anchor)
    return bspline(sk, s, mesh.sv[-1]) * bspline(tk, t, mesh.tv[-1])


def evaluate(mesh, P, w, s, t):
    """The rational T-spline surface at (s, t); P and w are dicts on the anchors."""
    dim = len(next(iter(P.values())))
    num = [Fraction(0)] * dim  # @line L6
    den = Fraction(0)
    for A in mesh.anchors():  # @line L7
        T = blend(mesh, A, s, t)  # @line L8
        if T:
            den += w[A] * T  # @line L9
            for c in range(dim):
                num[c] += w[A] * P[A][c] * T
    return tuple(x / den for x in num)  # @line L10


def insert_one(knots, x, values):
    """Boehm's rule for one B-spline: insert index line x into the index knots.

    Returns [(c0, k0), (c1, k1)] with B[knots] = c0 B[k0] + c1 B[k1].
    """
    p = len(knots) - 2
    tau = sorted(knots + [x])
    t = [values[k] for k in knots]
    u = values[x]
    c0 = Fraction(1) if u >= t[p] else (u - t[0]) / (t[p] - t[0])
    c1 = Fraction(1) if u <= t[1] else (t[p + 1] - u) / (t[p + 1] - t[1])
    return [(c0, tau[: p + 2]), (c1, tau[1:])]


def refine_to_global(index_knots, values):
    """Write B[index_knots] in the global B-splines of its range, by insertion.

    Returns {start: coefficient}, where start is the first index line of a
    global B-spline with consecutive index knots start .. start + p + 1.
    """
    funcs = {tuple(index_knots): Fraction(1)}
    lo, hi = index_knots[0], index_knots[-1]
    for x in range(lo, hi + 1):  # @line L12
        nxt = {}
        for kn, c in funcs.items():
            if kn[0] < x < kn[-1] and x not in kn:
                for c2, k2 in insert_one(list(kn), x, values):
                    if c2:
                        nxt[tuple(k2)] = nxt.get(tuple(k2), Fraction(0)) + c * c2
            else:
                nxt[kn] = nxt.get(kn, Fraction(0)) + c
        funcs = nxt
    out = {}
    for kn, c in funcs.items():
        assert list(kn) == list(range(kn[0], kn[0] + len(kn)))
        out[kn[0]] = c
    return out


def to_nurbs_matrix(mesh):
    """The T-spline-to-NURBS matrix M of Li and coauthors.

    Rows are the tensor B-splines B_a(s) B_b(t) on the global knot vectors,
    numbered a * (n - 3) + b; columns are the anchors in the order of
    mesh.anchors(). Column A holds the coefficients of T_A.
    """
    anchors = mesh.anchors()
    ns, nt = mesh.m - 3, mesh.n - 3
    M = [[Fraction(0)] * len(anchors) for _ in range(ns * nt)]
    for col, A in enumerate(anchors):  # @line L11
        si, ti = mesh.local_index_vectors(*A)
        ds = refine_to_global(si, mesh.sv)
        dt = refine_to_global(ti, mesh.tv)
        for a, ca in ds.items():  # @line L13
            for b, cb in dt.items():
                M[a * nt + b][col] = ca * cb
    return anchors, M  # @line L14


def tensor_basis(mesh, a, b, s, t):
    """The global tensor B-spline with s index knots a..a+4 and t index knots b..b+4."""
    return bspline(mesh.sv[a : a + 5], s, mesh.sv[-1]) * bspline(mesh.tv[b : b + 5], t, mesh.tv[-1])


def rank(M):
    """Rank of a matrix of Fractions by exact Gaussian elimination."""
    A = [list(r) for r in M]
    rows, cols = len(A), len(A[0]) if A else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(r + 1, rows):
            if A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r
