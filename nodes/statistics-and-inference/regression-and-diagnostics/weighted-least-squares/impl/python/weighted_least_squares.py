# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-least-squares/. The authors are listed in prov/3EE4N8.jsonl.
"""Weighted least squares with known weights, by a Householder QR of the scaled rows.

The model is y = X b + e with E[e] = 0 and Var(e_i) = sigma^2 / w_i, the w_i known
and positive (only their ratios matter). The estimate minimizes
sum w_i (y_i - x_i^T b)^2. Each row of X and each y_i is multiplied by sqrt(w_i);
ordinary least squares on the scaled rows, done by QR and not by the normal
equations, gives b-hat, the weighted residual sum of squares, s^2 and the
covariance s^2 (X^T W X)^(-1) = s^2 R^(-1) R^(-T). Rows with w_i = 0 drop out and
do not count in the degrees of freedom.
"""

import math
from typing import NamedTuple

from stdist import t_ppf

RANK_TOL = 1e-12


class WLSFit(NamedTuple):
    b: list          # the coefficient estimate, length p
    rss: float       # weighted residual sum of squares, sum w_i e_i^2
    df: int          # residual degrees of freedom, (number of rows with w_i > 0) - p
    s2: float        # rss / df, the estimate of sigma^2 (nan if df = 0)
    cov: list        # s2 (X^T W X)^(-1), p x p
    residuals: list  # e_i = y_i - x_i^T b, unscaled


def householder_qr(a: list, ys: list) -> tuple[list, list]:
    """Householder QR of the n x p matrix a (list of rows, n >= p), applied to each vector in ys.

    Works on copies. Returns (R, cs): R is the p x p upper triangular factor and
    cs[k] = Q^T ys[k]. Raises ValueError if a has rank below p (relative tolerance RANK_TOL).
    """
    n = len(a)
    p = len(a[0]) if n else 0
    if p == 0 or n < p:
        raise ValueError("need a design with n >= p >= 1")
    a = [[float(v) for v in row] for row in a]
    cs = [[float(v) for v in y] for y in ys]
    col = [math.sqrt(math.fsum(a[i][j] ** 2 for i in range(n))) for j in range(p)]
    for j in range(p):
        norm = math.sqrt(math.fsum(a[i][j] ** 2 for i in range(j, n)))
        if norm == 0.0 or norm <= RANK_TOL * col[j]:
            raise ValueError("the design has rank below its number of columns")
        alpha = -norm if a[j][j] >= 0.0 else norm
        v = [a[j][j] - alpha] + [a[i][j] for i in range(j + 1, n)]
        vv = math.fsum(t * t for t in v)
        for k in range(j, p):
            s = 2.0 * math.fsum(v[i - j] * a[i][k] for i in range(j, n)) / vv
            for i in range(j, n):
                a[i][k] -= s * v[i - j]
        for c in cs:
            s = 2.0 * math.fsum(v[i - j] * c[i] for i in range(j, n)) / vv
            for i in range(j, n):
                c[i] -= s * v[i - j]
    r = [[a[i][k] if k >= i else 0.0 for k in range(p)] for i in range(p)]
    return r, cs


def back_substitute(r: list, c: list) -> list:
    """Solve R x = c for upper triangular nonsingular R."""
    p = len(r)
    x = [0.0] * p
    for i in range(p - 1, -1, -1):
        x[i] = (c[i] - math.fsum(r[i][k] * x[k] for k in range(i + 1, p))) / r[i][i]
    return x


def r_inverse(r: list) -> list:
    """The inverse of an upper triangular nonsingular R, column by column."""
    p = len(r)
    cols = [back_substitute(r, [1.0 if i == j else 0.0 for i in range(p)]) for j in range(p)]
    return [[cols[j][i] for j in range(p)] for i in range(p)]


def weighted_least_squares(x: list, y: list, w: list) -> WLSFit:
    """Fit y = X b + e by weighted least squares with known weights w_i >= 0.

    Cost: Theta(n p^2) for the QR and Theta(p^3) for the covariance.
    """
    n = len(x)
    if len(y) != n or len(w) != n:
        raise ValueError("x, y and w must have the same length")
    if any(not math.isfinite(wi) or wi < 0.0 for wi in w):
        raise ValueError("weights must be finite and nonnegative")
    keep = [i for i in range(n) if w[i] > 0.0]
    xs, ys = [], []
    for i in keep:  # @line L1
        r = math.sqrt(w[i])  # @line L2
        xs.append([r * v for v in x[i]])  # @line L2
        ys.append(r * y[i])  # @line L2
    rr, (c,) = householder_qr(xs, [ys])  # @line L3
    p = len(rr)
    b = back_substitute(rr, c[:p])  # @line L4
    rss = math.fsum(v * v for v in c[p:])  # @line L5
    df = len(keep) - p
    s2 = rss / df if df > 0 else math.nan  # @line L6
    ri = r_inverse(rr)
    cov = [[s2 * math.fsum(ri[i][k] * ri[j][k] for k in range(p)) for j in range(p)]
           for i in range(p)]  # @line L7
    res = [y[i] - math.fsum(a * bb for a, bb in zip(x[i], b)) for i in range(n)]
    return WLSFit(b, rss, df, s2, cov, res)  # @line L8


def confidence_intervals(fit: WLSFit, level: float = 0.95) -> list:
    """t intervals b_j +- t_(df, (1 + level)/2) se_j; exact under normal errors with the right weights."""
    q = t_ppf(0.5 + level / 2.0, fit.df)
    out = []
    for j, bj in enumerate(fit.b):
        se = math.sqrt(fit.cov[j][j])
        out.append((bj - q * se, bj + q * se))
    return out
