# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-form-deformation/. The authors are listed in prov/5QACBN.jsonl.
"""Free-form deformation of Sederberg and Parry (1986).

A lattice is a parallelepiped with the corner X0 and the edge vectors S, T
and U. A point X inside it has the local coordinates (s, t, u) in [0, 1]^3
with X = X0 + s S + t T + u U. The lattice holds (l + 1)(m + 1)(n + 1)
control points P[i][j][k]. The deformed point is the trivariate Bernstein
polynomial

    X' = sum_ijk B_i^l(s) B_j^m(t) B_k^n(u) P[i][j][k],

with B_i^l(s) = C(l, i) (1 - s)^(l - i) s^i. In the undeformed lattice,
P[i][j][k] = X0 + (i / l) S + (j / m) T + (k / n) U, and X' = X.

All arithmetic works with int, float or fractions.Fraction. With Fraction
inputs the result is exact.
"""

from fractions import Fraction
from math import comb


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def bernstein(deg, x):
    """Return the list [B_0^deg(x), ..., B_deg^deg(x)]."""
    return [comb(deg, i) * (1 - x) ** (deg - i) * x ** i for i in range(deg + 1)]


def bernstein_derivative(deg, x):
    """Return the derivatives d/dx B_i^deg(x) for i = 0..deg."""
    if deg == 0:
        return [0 * x]
    low = bernstein(deg - 1, x)
    out = []
    for i in range(deg + 1):
        a = low[i - 1] if i >= 1 else 0
        b = low[i] if i <= deg - 1 else 0
        out.append(deg * (a - b))
    return out


class Lattice:
    """A parallelepiped lattice of degree (l, m, n) with movable control points."""

    def __init__(self, x0, s_axis, t_axis, u_axis, l, m, n):
        self.x0 = tuple(x0)
        self.axes = (tuple(s_axis), tuple(t_axis), tuple(u_axis))
        self.deg = (l, m, n)
        s, t, u = self.axes
        # Each local coordinate is a dot product with a fixed covector:
        # s = (T x U).(X - X0) / ((T x U).S), and the same for t and u.
        self.covectors = []
        for a, b, c in ((t, u, s), (s, u, t), (s, t, u)):
            w = _cross(a, b)
            den = _dot(w, c)
            if den == 0:
                raise ValueError("the lattice axes are linearly dependent")
            self.covectors.append(tuple(_div(x, den) for x in w))
        self.points = self.rest_points()

    def rest_points(self):
        """Return the control points of the undeformed lattice."""
        l, m, n = self.deg
        s, t, u = self.axes
        pts = []
        for i in range(l + 1):
            plane = []
            for j in range(m + 1):
                row = []
                for k in range(n + 1):
                    row.append(tuple(
                        self.x0[d] + _frac(i, l) * s[d] + _frac(j, m) * t[d] + _frac(k, n) * u[d]
                        for d in range(3)
                    ))
                plane.append(row)
            pts.append(plane)
        return pts

    def local(self, x):
        """Return the local coordinates (s, t, u) of the point x."""
        r = _sub(x, self.x0)
        return tuple(_dot(c, r) for c in self.covectors)

    def deform(self, x):
        """Return the deformed position of x. Points outside the lattice do not move."""
        r = _sub(x, self.x0)
        s = _dot(self.covectors[0], r)  # @line L1
        t = _dot(self.covectors[1], r)  # @line L2
        u = _dot(self.covectors[2], r)  # @line L3
        if not (0 <= s <= 1 and 0 <= t <= 1 and 0 <= u <= 1):  # @line L4
            return tuple(x)
        return self.evaluate(s, t, u)

    def evaluate(self, s, t, u):
        """Return sum_ijk B_i^l(s) B_j^m(t) B_k^n(u) P[i][j][k]."""
        l, m, n = self.deg
        bs, bt, bu = bernstein(l, s), bernstein(m, t), bernstein(n, u)
        out = [0 * s, 0 * s, 0 * s]  # @line L5
        for i in range(l + 1):
            for j in range(m + 1):
                wij = bs[i] * bt[j]
                for k in range(n + 1):  # @line L6
                    w = wij * bu[k]
                    p = self.points[i][j][k]
                    out[0] += w * p[0]
                    out[1] += w * p[1]
                    out[2] += w * p[2]
        return tuple(out)  # @line L7

    def jacobian(self, x):
        """Return the 3 by 3 matrix dX'/dX at a point x inside the lattice.

        By the chain rule, dX'/dX = (dX'/d(s, t, u)) (d(s, t, u)/dX), and the
        second factor has the three covectors as its rows.
        """
        l, m, n = self.deg
        s, t, u = self.local(x)
        bs, bt, bu = bernstein(l, s), bernstein(m, t), bernstein(n, u)
        ds, dt, du = bernstein_derivative(l, s), bernstein_derivative(m, t), bernstein_derivative(n, u)
        cols = [[0 * s] * 3 for _ in range(3)]
        for i in range(l + 1):
            for j in range(m + 1):
                for k in range(n + 1):
                    p = self.points[i][j][k]
                    ws = (ds[i] * bt[j] * bu[k], bs[i] * dt[j] * bu[k], bs[i] * bt[j] * du[k])
                    for a in range(3):
                        for d in range(3):
                            cols[a][d] += ws[a] * p[d]
        # cols[a] is the derivative by the local coordinate a.
        return [[sum(cols[a][r] * self.covectors[a][c] for a in range(3)) for c in range(3)] for r in range(3)]


def _frac(i, n):
    """Return i / n as a Fraction; a degree of 0 gives 0."""
    if n == 0:
        return Fraction(0)
    return Fraction(i, n)


def _div(x, d):
    """Return x / d, as an exact Fraction when both are int."""
    if isinstance(x, int) and isinstance(d, int):
        return Fraction(x, d)
    return x / d


def det3(a):
    """Return the determinant of a 3 by 3 matrix."""
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def de_casteljau_volume(points, s, t, u):
    """Evaluate the same trivariate Bezier volume by repeated linear interpolation.

    This is an independent second method, used by the tests.
    """

    def lerp_list(pts, x):
        while len(pts) > 1:
            pts = [tuple((1 - x) * a + x * b for a, b in zip(p, q)) for p, q in zip(pts, pts[1:])]
        return pts[0]

    rows = []
    for plane in points:
        cols = [lerp_list(list(row), u) for row in plane]
        rows.append(lerp_list(cols, t))
    return lerp_list(rows, s)
