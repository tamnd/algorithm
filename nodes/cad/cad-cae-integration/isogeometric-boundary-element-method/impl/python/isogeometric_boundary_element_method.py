# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeometric-boundary-element-method/. The authors are listed in prov/JQY36Z.jsonl.
"""Isogeometric boundary element method for the 2D Laplace equation.

The boundary is a closed NURBS curve, counterclockwise, with an open knot
vector on [0, 1] whose first and last control points coincide. The same
NURBS basis, with the first and last functions merged into one, carries the
boundary values u and the normal derivatives q = du/dn. Collocation at the
images of the Greville abscissae gives the square system H u = G q of the
boundary integral equation

    (1/2) u(x) + int q*(x, y) u(y) ds_y = int u*(x, y) q(y) ds_y,

with u* = -(1/2 pi) ln r and q* = -(1/2 pi) (r . n_y) / r^2, r = y - x.
"""

from __future__ import annotations

import math
from typing import Callable, List, Sequence, Tuple

from ig2kit import all_basis, gauss_legendre, greville, solve_dense

Point = Tuple[float, float]


def circle_nurbs(radius: float, sx: float = 1.0, sy: float = 1.0):
    """Exact quadratic NURBS of the circle of this radius (an ellipse if sx != sy).

    Returns (degree, knots, control points, weights), counterclockwise from (radius sx, 0).
    """
    r = radius
    pts = [(r, 0), (r, r), (0, r), (-r, r), (-r, 0), (-r, -r), (0, -r), (r, -r), (r, 0)]
    pts = [(sx * x, sy * y) for x, y in pts]
    h = math.sqrt(0.5)
    w = [1, h, 1, h, 1, h, 1, h, 1]
    knots = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]
    return 2, [float(k) for k in knots], [(float(x), float(y)) for x, y in pts], [float(v) for v in w]


def insert_knot(p: int, knots: List[float], pts: List[Point], w: List[float], t: float):
    """Boehm insertion of one knot t, done on the homogeneous points (w x, w y, w)."""
    k = max(i for i in range(len(knots) - 1) if knots[i] <= t < knots[i + 1])
    hom = [(wi * x, wi * y, wi) for (x, y), wi in zip(pts, w)]
    new = []
    for i in range(len(hom) + 1):
        if i <= k - p:
            new.append(hom[i])
        elif i >= k + 1:
            new.append(hom[i - 1])
        else:
            a = (t - knots[i]) / (knots[i + p] - knots[i])
            new.append(tuple(a * hom[i][c] + (1 - a) * hom[i - 1][c] for c in range(3)))
    knots = knots[: k + 1] + [t] + knots[k + 1 :]
    return knots, [(X / W, Y / W) for X, Y, W in new], [W for _, _, W in new]


def refine(p, knots, pts, w, per_span: int):
    """Insert per_span - 1 equally spaced knots in each non-empty knot span."""
    spans = [(knots[i], knots[i + 1]) for i in range(len(knots) - 1) if knots[i] < knots[i + 1]]
    for a, b in spans:
        for k in range(1, per_span):
            knots, pts, w = insert_knot(p, knots, pts, w, a + (b - a) * k / per_span)
    return knots, pts, w


class Curve:
    """A closed NURBS curve with the periodic (merged) basis."""

    def __init__(self, p, knots, pts, w):
        self.p, self.knots, self.pts, self.w = p, knots, pts, w
        self.n = len(pts) - 1  # number of unknowns after merging the first and the last function

    def eval(self, t: float):
        """(point, unit tangent speed |C'|, outward normal, merged basis row) at parameter t."""
        d = all_basis(self.knots, self.p, t, 1)
        wn = [wi * v for wi, v in zip(self.w, d[0])]
        wd = [wi * v for wi, v in zip(self.w, d[1])]
        W, Wd = sum(wn), sum(wd)
        R = [v / W for v in wn]
        Rd = [(a * W - b * Wd) / (W * W) for a, b in zip(wd, wn)]
        x = sum(r * P[0] for r, P in zip(R, self.pts))
        y = sum(r * P[1] for r, P in zip(R, self.pts))
        dx = sum(r * P[0] for r, P in zip(Rd, self.pts))
        dy = sum(r * P[1] for r, P in zip(Rd, self.pts))
        jac = math.hypot(dx, dy)
        row = R[:-1]
        row[0] += R[-1]
        return (x, y), jac, (dy / jac, -dx / jac), row

    def elements(self) -> List[Tuple[float, float]]:
        k = self.knots
        return [(k[i], k[i + 1]) for i in range(len(k) - 1) if k[i] < k[i + 1]]


def kernels(x: Point, y: Point, ny: Point) -> Tuple[float, float]:
    """(u*, q*) of the 2D Laplace equation for the source x and the field point y."""
    rx, ry = y[0] - x[0], y[1] - x[1]
    r2 = rx * rx + ry * ry
    return -math.log(r2) / (4 * math.pi), -(rx * ny[0] + ry * ny[1]) / (2 * math.pi * r2)


def _rule(a: float, b: float, gx, gw):
    return [(0.5 * (a + b) + 0.5 * (b - a) * s, 0.5 * (b - a) * v) for s, v in zip(gx, gw)]


def _graded(ts: float, d: float, m: int, gx, gw):
    """Rule on [ts, ts + d] (d of either sign) with t = ts + d w^m, w in (0, 1): it removes the log singularity at ts."""
    out = []
    for s, v in zip(gx, gw):
        u = 0.5 * (s + 1)
        out.append((ts + d * u**m, abs(d) * m * u ** (m - 1) * 0.5 * v))
    return out


def assemble(curve: Curve, ng: int = 12, ngs: int = 16, m: int = 4):
    """Collocation points and the matrices H and G of the boundary integral equation."""
    n = curve.n
    gx, gw = gauss_legendre(ng)
    sx, sw = gauss_legendre(ngs)
    tau = greville(curve.knots, curve.p)[:-1]  # @line L2
    src = [curve.eval(t) for t in tau]
    els = curve.elements()
    # The regular rule of each element does not depend on the source: evaluate it once.
    regular = [[(curve.eval(t), wt) for t, wt in _rule(a, b, gx, gw)] for a, b in els]
    H = [[0.0] * n for _ in range(n)]
    G = [[0.0] * n for _ in range(n)]
    for i, (ts, (xi, _, _, rowi)) in enumerate(zip(tau, src)):  # @line L3
        for e, (a, b) in enumerate(els):
            hits = [s for s in (ts, ts + 1.0) if a <= s <= b]
            if hits:  # @line L4
                s0 = hits[0]
                qu = []  # rule for u*: graded toward s0
                qq = []  # rule for q*: plain Gauss on both sides of s0
                for d in (a - s0, b - s0):
                    if d != 0:
                        qu += _graded(s0, d, m, sx, sw)
                        qq += _rule(s0, s0 + d, gx, gw) if d > 0 else _rule(s0 + d, s0, gx, gw)
                pts_u = [(curve.eval(t), wt) for t, wt in qu]
                pts_q = [(curve.eval(t), wt) for t, wt in qq]
            else:
                pts_u = pts_q = regular[e]  # @line L5
            for (y, jac, ny, row), wt in pts_u:
                us, _ = kernels(xi, y, ny)
                c = us * jac * wt
                for j, rj in enumerate(row):
                    if rj:
                        G[i][j] += c * rj  # @line L6
            for (y, jac, ny, row), wt in pts_q:
                _, qs = kernels(xi, y, ny)
                c = qs * jac * wt
                for j, rj in enumerate(row):
                    if rj:
                        H[i][j] += c * rj
        for j in range(n):
            H[i][j] += 0.5 * rowi[j]  # @line L7
    return tau, src, H, G


def solve_dirichlet(curve: Curve, g: Callable[[float, float], float], **quad):
    """Given u = g on the boundary, return (coefficients of u, coefficients of q, tau, src, H, G)."""
    n = curve.n  # @line L1
    tau, src, H, G = assemble(curve, **quad)
    C = [s[3] for s in src]
    u = solve_dense(C, [g(*s[0]) for s in src])  # @line L8
    rhs = [sum(H[i][j] * u[j] for j in range(n)) for i in range(n)]
    q = solve_dense(G, rhs)  # @line L9
    return u, q, tau, src, H, G


def flux_at(curve: Curve, q: Sequence[float], t: float) -> float:
    """q_h(t) = sum_j R_j(t) q_j."""
    return sum(r * c for r, c in zip(curve.eval(t)[3], q))


def interior_value(curve: Curve, u: Sequence[float], q: Sequence[float], x: Point, ng: int = 24) -> float:
    """Representation formula u(x) = int u* q - int q* u for an interior point x."""
    gx, gw = gauss_legendre(ng)
    total = 0.0
    for a, b in curve.elements():
        for t, wt in _rule(a, b, gx, gw):
            y, jac, ny, row = curve.eval(t)
            us, qs = kernels(x, y, ny)
            uh = sum(r * c for r, c in zip(row, u))
            qh = sum(r * c for r, c in zip(row, q))
            total += (us * qh - qs * uh) * jac * wt
    return total


def refined_circle(radius: float, per_span: int, sx: float = 1.0, sy: float = 1.0) -> Curve:
    p, k, P, w = circle_nurbs(radius, sx, sy)
    k, P, w = refine(p, k, P, w, per_span)
    return Curve(p, k, P, w)
