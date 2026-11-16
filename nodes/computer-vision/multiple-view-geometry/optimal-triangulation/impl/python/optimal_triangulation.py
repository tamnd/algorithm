# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-triangulation/. The authors are listed in prov/FJGF9W.jsonl.
"""Hartley-Sturm optimal two-view triangulation.

Given a fundamental matrix F (x2^T F x1 = 0) and two measured image points
x1, x2, find the points x1h, x2h with x2h^T F x1h = 0 that minimize
d(x1, x1h)^2 + d(x2, x2h)^2. The epipolar lines through x1h and x2h form a
pencil with one parameter t; after a Euclidean change of each image frame
the cost is a rational function s(t), and its stationary points are the
real roots of a polynomial g(t) of degree 6 (Hartley and Sturm 1997,
Hartley and Zisserman 2004, Algorithm 12.1). The corrected points are
then triangulated exactly by the linear method.

The image coordinates must be in a Euclidean frame (pixels with square
pixels and no skew, or normalized coordinates), because the cost is a
Euclidean distance in the image.

Cost: Theta(1).
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from cvla import inv, matvec, mul, nullvec, polyroots_real, skew, transpose

Matrix = List[List[float]]
Vector = List[float]


# ------------------------------------------------------------ polynomials

def _pmul(p: Sequence[float], q: Sequence[float]) -> Vector:
    """Product of two polynomials, coefficients highest power first."""
    out = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _padd(p: Sequence[float], q: Sequence[float]) -> Vector:
    n = max(len(p), len(q))
    p = [0.0] * (n - len(p)) + list(p)
    q = [0.0] * (n - len(q)) + list(q)
    return [a + b for a, b in zip(p, q)]


def _pscale(p: Sequence[float], k: float) -> Vector:
    return [k * a for a in p]


def cost_polynomial(a: float, b: float, c: float, d: float, f: float, f2: float) -> Vector:
    """The coefficients (degree 6 first) of
    g(t) = t ((a t + b)^2 + f2^2 (c t + d)^2)^2
           - (a d - b c) (1 + f^2 t^2)^2 (a t + b) (c t + d)."""
    atb, ctd = [a, b], [c, d]
    q = _padd(_pmul(atb, atb), _pscale(_pmul(ctd, ctd), f2 * f2))
    left = _pmul([1.0, 0.0], _pmul(q, q))
    r = [f * f, 0.0, 1.0]
    right = _pscale(_pmul(_pmul(r, r), _pmul(atb, ctd)), a * d - b * c)
    return _padd(left, _pscale(right, -1.0))


def cost_s(t: float, a: float, b: float, c: float, d: float, f: float, f2: float) -> float:
    """s(t) = t^2 / (1 + f^2 t^2) + (c t + d)^2 / ((a t + b)^2 + f2^2 (c t + d)^2).
    t = math.inf gives the limit 1/f^2 + c^2 / (a^2 + f2^2 c^2)."""
    if math.isinf(t):
        first = math.inf if f == 0 else 1.0 / (f * f)
        den = a * a + f2 * f2 * c * c
        return first + (c * c / den if den > 0 else math.inf)
    den = (a * t + b) ** 2 + f2 * f2 * (c * t + d) ** 2
    second = (c * t + d) ** 2 / den if den > 0 else math.inf
    return t * t / (1.0 + f * f * t * t) + second


# ------------------------------------------------------------ geometry

def fundamental_from_cameras(P1: Sequence[Sequence[float]],
                             P2: Sequence[Sequence[float]]) -> Matrix:
    """F = [e2]_x P2 P1^+, with e2 = P2 C1 and P1^+ = P1^T (P1 P1^T)^-1."""
    C1 = nullvec(P1)
    e2 = matvec(P2, C1)
    P1t = transpose(P1)
    pinv = mul(P1t, inv(mul(P1, P1t)))
    return mul(skew(e2), mul(P2, pinv))


def _translation(x: Sequence[float]) -> Matrix:
    return [[1.0, 0.0, -x[0]], [0.0, 1.0, -x[1]], [0.0, 0.0, 1.0]]


def _unit_epipole(e: Sequence[float]) -> Vector:
    n = math.hypot(e[0], e[1])
    if n <= 1e-12 * max(1.0, abs(e[2])):
        raise ValueError("optimal triangulation: an image point is at the epipole")
    return [e[0] / n, e[1] / n, e[2] / n]


def _closest_to_origin(line: Sequence[float]) -> Vector:
    lam, mu, nu = line
    return [-lam * nu, -mu * nu, lam * lam + mu * mu]


def optimal_correction(F: Sequence[Sequence[float]], x1: Sequence[float],
                       x2: Sequence[float], details: bool = False):
    """The corrected points (x1h, x2h) with x2h^T F x1h = 0 of least
    d(x1, x1h)^2 + d(x2, x2h)^2, and that least cost."""
    T1, T2 = _translation(x1), _translation(x2)                     # @line L1
    T1i, T2i = inv(T1), inv(T2)                                      # @line L1
    Fn = mul(transpose(T2i), mul(F, T1i))                            # @line L1
    e1 = _unit_epipole(nullvec(Fn))                                  # @line L2
    e2 = _unit_epipole(nullvec(transpose(Fn)))                       # @line L2
    R1 = [[e1[0], e1[1], 0.0], [-e1[1], e1[0], 0.0], [0.0, 0.0, 1.0]]  # @line L3
    R2 = [[e2[0], e2[1], 0.0], [-e2[1], e2[0], 0.0], [0.0, 0.0, 1.0]]  # @line L3
    Fr = mul(R2, mul(Fn, transpose(R1)))                             # @line L3
    f, f2 = e1[2], e2[2]                                             # @line L4
    a, b, c, d = Fr[1][1], Fr[1][2], Fr[2][1], Fr[2][2]              # @line L4
    g = cost_polynomial(a, b, c, d, f, f2)                           # @line L5
    cands = polyroots_real(g) + [math.inf]                           # @line L6
    t = min(cands, key=lambda u: cost_s(u, a, b, c, d, f, f2))       # @line L6
    if math.isinf(t):                                                # @line L7
        l1, l2 = [f, 0.0, -1.0], [-f2 * c, a, c]                     # @line L7
    else:                                                            # @line L7
        l1 = [t * f, 1.0, -t]                                        # @line L7
        l2 = [-f2 * (c * t + d), a * t + b, c * t + d]               # @line L7
    p1, p2 = _closest_to_origin(l1), _closest_to_origin(l2)          # @line L8
    q1 = matvec(T1i, matvec(transpose(R1), p1))                      # @line L9
    q2 = matvec(T2i, matvec(transpose(R2), p2))                      # @line L9
    x1h = [q1[0] / q1[2], q1[1] / q1[2]]                             # @line L9
    x2h = [q2[0] / q2[2], q2[1] / q2[2]]                             # @line L9
    cost = ((x1h[0] - x1[0]) ** 2 + (x1h[1] - x1[1]) ** 2
            + (x2h[0] - x2[0]) ** 2 + (x2h[1] - x2[1]) ** 2)
    if details:
        return x1h, x2h, cost, {"F": Fr, "f": f, "f2": f2, "abcd": (a, b, c, d),
                                "g": g, "roots": cands[:-1], "t": t,
                                "s": cost_s(t, a, b, c, d, f, f2)}
    return x1h, x2h, cost


def triangulate_dlt(P1, P2, x1, x2) -> Vector:
    """The linear (DLT) triangulation of two image points."""
    A = []
    for P, (u, v) in ((P1, x1), (P2, x2)):
        A.append([u * P[2][k] - P[0][k] for k in range(4)])
        A.append([v * P[2][k] - P[1][k] for k in range(4)])
    X = nullvec(A)
    if X[3] == 0.0:
        raise ValueError("optimal triangulation: the point is at infinity")
    return [X[0] / X[3], X[1] / X[3], X[2] / X[3]]


def optimal_triangulation(P1, P2, x1, x2) -> Tuple[Vector, Vector, Vector, float]:
    """The 3D point of least reprojection error for the cameras P1, P2 and
    the image points x1, x2. Returns (X, x1h, x2h, cost)."""
    F = fundamental_from_cameras(P1, P2)
    x1h, x2h, cost = optimal_correction(F, x1, x2)
    X = triangulate_dlt(P1, P2, x1h, x2h)                            # @line L10
    return X, x1h, x2h, cost


def reprojection_cost(P1, P2, X, x1, x2) -> float:
    """The sum of the squared image distances of the projections of X."""
    s = 0.0
    for P, x in ((P1, x1), (P2, x2)):
        q = matvec(P, list(X) + [1.0])
        s += (q[0] / q[2] - x[0]) ** 2 + (q[1] / q[2] - x[1]) ** 2
    return s
