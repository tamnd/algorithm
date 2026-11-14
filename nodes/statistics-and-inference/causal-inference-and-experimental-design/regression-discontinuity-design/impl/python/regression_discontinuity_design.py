# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-discontinuity-design/. The authors are listed in prov/QMX934.jsonl.

"""Regression discontinuity by local linear regression with a triangular kernel.

Units with running variable x >= c are treated (sharp design), or have a higher chance of
treatment (fuzzy design). On each side of c, fit y on (1, x - c) by weighted least squares
with weights max(0, 1 - |x - c| / h). The sharp estimate is the right intercept minus the
left intercept. The fuzzy estimate divides that jump by the jump of the treatment.

Each intercept is a linear combination sum(l_i y_i) of the outcomes; local_weights returns
the l_i. The standard error uses the heteroskedasticity-robust (HC0) variance sum(l_i^2 e_i^2).

The bandwidth h is an input. Choosing it (Imbens and Kalyanaraman, Calonico, Cattaneo and
Titiunik) is not done here. Everything except the standard error is exact for Fractions.
"""

import math
from collections.abc import Sequence
from typing import NamedTuple


class RDResult(NamedTuple):
    tau: object  # the jump at the cutoff
    se: float  # HC0 standard error of the jump
    left: tuple  # (intercept, slope) on the left
    right: tuple  # (intercept, slope) on the right
    n_left: int  # units with positive weight on the left
    n_right: int


def triangular(u):
    return max(u * 0, 1 - abs(u))


def local_weights(v: Sequence, w: Sequence) -> list:
    """For WLS of y on (1, v) with weights w, the intercept is sum(l_i y_i). Returns l."""
    sw = sum(w)
    if sw == 0:
        raise ValueError("no unit has positive weight")
    vb = sum(a * b for a, b in zip(w, v)) / sw
    sv = sum(a * (b - vb) * (b - vb) for a, b in zip(w, v))
    if sv == 0:
        raise ValueError("need at least two distinct running-variable values with positive weight on each side")
    # intercept = ybar - slope * vbar, slope = sum w (v - vb) y / sv
    return [a / sw - vb * a * (b - vb) / sv for a, b in zip(w, v)]


def _fit(v, y, w):
    sw = sum(w)
    vb = sum(a * b for a, b in zip(w, v)) / sw
    yb = sum(a * b for a, b in zip(w, y)) / sw
    sv = sum(a * (b - vb) * (b - vb) for a, b in zip(w, v))
    slope = sum(a * (b - vb) * (c - yb) for a, b, c in zip(w, v, y)) / sv
    return yb - slope * vb, slope


def _side(x, y, c, h, right):
    keep = [i for i in range(len(x)) if (x[i] >= c) == right]
    v = [x[i] - c for i in keep]
    w = [triangular(a / h) for a in v]  # @line L1
    pos = [j for j in range(len(keep)) if w[j] > 0]
    return [keep[j] for j in pos], [v[j] for j in pos], [w[j] for j in pos]


def _local_linear(x, y, c, h, right):
    """(intercept, slope), HC0 variance of the intercept, and the number of units used."""
    idx, v, w = _side(x, y, c, h, right)
    yy = [y[i] for i in idx]
    lw = local_weights(v, w)
    a, b = _fit(v, yy, w)
    resid = [q - a - b * p for p, q in zip(v, yy)]
    var = sum(float(l) ** 2 * float(e) ** 2 for l, e in zip(lw, resid))
    return (a, b), var, len(idx)


def rdd(x: Sequence, y: Sequence, c, h) -> RDResult:
    """Sharp design. Cost: Theta(n)."""
    if len(x) != len(y):
        raise ValueError("x and y need the same length")
    if not h > 0:
        raise ValueError("the bandwidth must be positive")
    left, vl, nl = _local_linear(x, y, c, h, False)  # @line L2
    right_fit, vr, nr = _local_linear(x, y, c, h, True)  # @line L3
    tau = right_fit[0] - left[0]  # @line L4
    se = math.sqrt(vl + vr)  # @line L5
    return RDResult(tau, se, left, right_fit, nl, nr)  # @line L6


def rdd_fuzzy(x: Sequence, y: Sequence, d: Sequence, c, h) -> tuple:
    """Fuzzy design: (jump in y / jump in d, se, jump in y, jump in d). The se linearizes
    the ratio: var = sum over both sides of l_i^2 (e_y,i - tau e_d,i)^2 / jump_d^2."""
    ry = rdd(x, y, c, h)
    rd = rdd(x, d, c, h)
    if rd.tau == 0:
        raise ZeroDivisionError("the treatment does not jump at the cutoff")
    tau = ry.tau / rd.tau
    var = 0.0
    for right, fy, fd in ((False, ry.left, rd.left), (True, ry.right, rd.right)):
        idx, v, w = _side(x, y, c, h, right)
        lw = local_weights(v, w)
        for l, i, p in zip(lw, idx, v):
            ey = y[i] - fy[0] - fy[1] * p
            ed = d[i] - fd[0] - fd[1] * p
            var += float(l) ** 2 * float(ey - tau * ed) ** 2
    return tau, math.sqrt(var) / abs(float(rd.tau)), ry.tau, rd.tau


def wls(xm: list[list], y: Sequence, w: Sequence) -> list:
    """Direct weighted least squares by the normal equations (Gauss-Jordan), for checking."""
    k = len(xm[0])
    a = [[sum(wi * r[i] * r[j] for r, wi in zip(xm, w)) for j in range(k)] for i in range(k)]
    b = [sum(wi * r[i] * yi for r, wi, yi in zip(xm, w, y)) for i in range(k)]
    m = [row + [v] for row, v in zip(a, b)]
    for col in range(k):
        p = max(range(col, k), key=lambda r: abs(m[r][col]))
        if m[p][col] == 0:
            raise ValueError("singular matrix")
        m[col], m[p] = m[p], m[col]
        for r in range(k):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                for j in range(col, k + 1):
                    m[r][j] -= f * m[col][j]
    return [m[r][k] / m[r][r] for r in range(k)]


def pooled_fit(x: Sequence, y: Sequence, c, h) -> list:
    """WLS of y on (1, T, x - c, T (x - c)) with the kernel weights, T = [x >= c].
    The coefficient of T equals rdd(...).tau exactly."""
    one = y[0] * 0 + 1
    rows, yy, ww = [], [], []
    for a, b in zip(x, y):
        w = triangular((a - c) / h)
        if w > 0:
            t = one if a >= c else one - one
            rows.append([one, t, (a - c) * one, t * (a - c)])
            yy.append(b)
            ww.append(w)
    return wls(rows, yy, ww)
