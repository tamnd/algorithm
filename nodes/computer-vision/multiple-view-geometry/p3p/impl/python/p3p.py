# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/p3p/. The authors are listed in prov/E145BQ.jsonl.
"""P3P by Grunert's elimination.

Given three world points X1, X2, X3 and their images y1, y2, y3 in
normalized image coordinates (y = K^-1 x, two entries each), find every
pose (R, t) with Xc = R Xw + t that maps each Xi onto its ray with a
positive depth. There are at most four such poses.

The unknowns are the distances s1, s2, s3 from the camera center to the
three points. With s2 = u s1 and s3 = v s1, the law of cosines in the
three triangles (center, Xi, Xj) gives a quartic in v and a rational
expression for u. Each positive root gives the three points in the
camera frame, and the pose is the rigid motion that maps the world
triangle onto the camera triangle.

Cost: O(1). The quartic is solved by cvla.polyroots_real; the rest is a
fixed number of arithmetic operations.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from cvla import cross, dot, matvec, mul, norm, polyroots_real, sub, transpose

Matrix = List[List[float]]
Vector = List[float]


# ------------------------------------------------- polynomials in v
# A polynomial is a list of coefficients, highest power first.

def _padd(p: Sequence[float], q: Sequence[float]) -> Vector:
    n = max(len(p), len(q))
    p = [0.0] * (n - len(p)) + list(p)
    q = [0.0] * (n - len(q)) + list(q)
    return [a + b for a, b in zip(p, q)]


def _pmul(p: Sequence[float], q: Sequence[float]) -> Vector:
    r = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def _pscale(p: Sequence[float], c: float) -> Vector:
    return [c * a for a in p]


def _peval(p: Sequence[float], x: float) -> float:
    s = 0.0
    for a in p:
        s = s * x + a
    return s


# ------------------------------------------------------------ the solver

def bearing(y: Sequence[float]) -> Vector:
    """The unit vector along the ray of the normalized image point y."""
    f = [float(y[0]), float(y[1]), 1.0]
    n = norm(f)
    return [c / n for c in f]


def grunert_polynomials(ca: float, cb: float, cg: float, a: float, b: float,
                        c: float) -> Tuple[Vector, Vector, Vector]:
    """The quartic G(v) and the polynomials N(v), D(v) with u = N(v) / D(v).

    ca, cb, cg are the cosines of the angles at the center between the rays
    (2, 3), (1, 3) and (1, 2); a, b, c are the side lengths |X2 X3|,
    |X1 X3| and |X1 X2|. G = N^2 - 2 cg N D + (1 - (c/b)^2 Q) D^2 with
    Q(v) = v^2 - 2 cb v + 1."""
    p = (a * a - c * c) / (b * b)
    q = [1.0, -2.0 * cb, 1.0]                                  # Q(v)
    num = [p - 1.0, -2.0 * p * cb, 1.0 + p]                    # N(v)
    den = [-2.0 * ca, 2.0 * cg]                                # D(v)
    g = _padd(_pmul(num, num), _pscale(_pmul(num, den), -2.0 * cg))
    g = _padd(g, _pmul(_padd([1.0], _pscale(q, -(c * c) / (b * b))), _pmul(den, den)))
    return g, num, den


def _laws_of_cosines_hold(s: Sequence[float], ca: float, cb: float, cg: float,
                          a: float, b: float, c: float, rel: float = 1e-3) -> bool:
    """True if the distances s satisfy the three equations of the page
    within rel times the squared side length. A root of G that is not a
    true solution (a common root of N and D) misses by far more than
    rel; a true root near a double root can miss by about 1e-5."""
    s1, s2, s3 = s
    return (abs(s2 * s2 + s3 * s3 - 2.0 * s2 * s3 * ca - a * a) <= rel * a * a and
            abs(s1 * s1 + s3 * s3 - 2.0 * s1 * s3 * cb - b * b) <= rel * b * b and
            abs(s1 * s1 + s2 * s2 - 2.0 * s1 * s2 * cg - c * c) <= rel * c * c)


def rigid_from_triangles(X: Sequence[Sequence[float]],
                         Y: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector]:
    """The rotation R and translation t with Y_i = R X_i + t for two
    congruent triangles, from an orthonormal frame built on each one."""
    def frame(P):
        e1 = sub(P[1], P[0])
        e1 = [c / norm(e1) for c in e1]
        e3 = cross(sub(P[1], P[0]), sub(P[2], P[0]))
        e3 = [c / norm(e3) for c in e3]
        e2 = cross(e3, e1)
        return transpose([e1, e2, e3])            # columns e1, e2, e3
    R = mul(frame(Y), transpose(frame(X)))
    RX = matvec(R, X[0])
    t = [Y[0][i] - RX[i] for i in range(3)]
    return R, t


def p3p(Xw: Sequence[Sequence[float]], y: Sequence[Sequence[float]],
        eps_d: float = 1e-6) -> List[Tuple[Matrix, Vector]]:
    """All poses (R, t) for three world points Xw and their normalized
    image points y. Each pose puts the three points on their rays with a
    positive depth. Raises ValueError if the world points are collinear.

    If |D(v)| is below eps_d times its scale, u is not fixed by u = N / D;
    then both positive roots of the quadratic (A) in u are tried. Poses
    that agree within 1e-7 (a root found twice) are kept once."""
    X = [[float(c) for c in p] for p in Xw]
    if norm(cross(sub(X[1], X[0]), sub(X[2], X[0]))) == 0.0:
        raise ValueError("p3p: the world points are collinear")
    f = [bearing(yi) for yi in y]                                    # @line L1
    ca, cb, cg = dot(f[1], f[2]), dot(f[0], f[2]), dot(f[0], f[1])   # @line L2
    a = norm(sub(X[1], X[2]))                                        # @line L3
    b = norm(sub(X[0], X[2]))                                        # @line L3
    c = norm(sub(X[0], X[1]))                                        # @line L3
    g, num, den = grunert_polynomials(ca, cb, cg, a, b, c)           # @line L4
    sols: List[Tuple[Matrix, Vector]] = []
    for v in polyroots_real(g):                                      # @line L5
        if v <= 0.0:
            continue
        d = _peval(den, v)
        if abs(d) > eps_d * (abs(ca) * v + abs(cg)):                 # @line L6
            us = [_peval(num, v) / d]                                # @line L6
        else:                                                        # @line L7
            disc = cg * cg - 1.0 + (c * c) / (b * b) * (v * v - 2.0 * cb * v + 1.0)
            if disc < -1e-9:                                         # @line L7
                continue
            r = math.sqrt(max(disc, 0.0))                            # @line L7
            us = [cg - r, cg + r] if r > 0.0 else [cg]               # @line L7
        for u in us:
            if u <= 0.0:                                             # @line L8
                continue
            s1 = b / math.sqrt(1.0 + v * v - 2.0 * v * cb)          # @line L9
            s = [s1, u * s1, v * s1]                                 # @line L9
            if not _laws_of_cosines_hold(s, ca, cb, cg, a, b, c):    # @line L9
                continue
            Y = [[s[i] * f[i][k] for k in range(3)] for i in range(3)]  # @line L10
            R, t = rigid_from_triangles(X, Y)                        # @line L11
            if all(norm(sub(R, R2)) + norm(sub(t, t2)) > 1e-7 * (1.0 + norm(t))
                   for R2, t2 in sols):                              # @line L12
                sols.append((R, t))                                  # @line L12
    return sols                                                      # @line L13


def reprojection_error(R: Sequence[Sequence[float]], t: Sequence[float],
                       Xw: Sequence[float], y: Sequence[float]) -> float:
    """Distance in normalized coordinates between y and the image of Xw.
    A point behind the camera gets an infinite error."""
    Xc = [a + b for a, b in zip(matvec(R, Xw), t)]
    if Xc[2] <= 0.0:
        return math.inf
    return math.hypot(Xc[0] / Xc[2] - y[0], Xc[1] / Xc[2] - y[1])


def p3p_select(Xw: Sequence[Sequence[float]], y: Sequence[Sequence[float]]
               ) -> Tuple[Matrix, Vector]:
    """Solve with the first three points and keep the pose with the
    smallest reprojection error on the remaining points (at least one)."""
    sols = p3p(Xw[:3], y[:3])                                        # @line L14
    if not sols:
        raise ValueError("p3p_select: no pose with positive depths")
    def err(sol):
        R, t = sol
        return sum(reprojection_error(R, t, Xw[i], y[i]) ** 2 for i in range(3, len(Xw)))
    return min(sols, key=err)                                        # @line L15
