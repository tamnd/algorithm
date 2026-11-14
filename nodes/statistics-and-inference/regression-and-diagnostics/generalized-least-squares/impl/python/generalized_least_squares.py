# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-least-squares/. The authors are listed in prov/A3NRM4.jsonl.
"""Generalized least squares with a known error covariance, by Cholesky whitening.

The model is y = X b + e with E[e] = 0 and Cov(e) = sigma^2 V, V known and
positive definite, sigma^2 unknown. With V = L L^T (Cholesky), the whitened
model L^(-1) y = L^(-1) X b + L^(-1) e has uncorrelated errors of variance
sigma^2, and ordinary least squares on it, done by Householder QR, gives
b-hat = (X^T V^(-1) X)^(-1) X^T V^(-1) y without forming V^(-1).

feasible_gls_ar1 is the two-step Prais-Winsten estimator for AR(1) errors:
rho is estimated from the OLS residuals and the exact AR(1) whitening is applied.
"""

import math
from typing import NamedTuple

from stdist import t_ppf

RANK_TOL = 1e-12


class GLSFit(NamedTuple):
    b: list          # the coefficient estimate, length p
    rss: float       # whitened residual sum of squares, e^T V^(-1) e
    df: int          # n - p
    s2: float        # rss / df, the estimate of sigma^2
    cov: list        # s2 (X^T V^(-1) X)^(-1), p x p
    residuals: list  # e = y - X b-hat, on the original scale


def cholesky(v: list) -> list:
    """The lower triangular L with positive diagonal and L L^T = V. Raises ValueError if V is not positive definite."""
    n = len(v)
    l = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = v[j][j] - math.fsum(l[j][k] ** 2 for k in range(j))
        if not d > 0.0:
            raise ValueError("V is not positive definite")
        l[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            l[i][j] = (v[i][j] - math.fsum(l[i][k] * l[j][k] for k in range(j))) / l[j][j]
    return l


def forward_substitute(l: list, b: list) -> list:
    """Solve L z = b for lower triangular nonsingular L."""
    z = []
    for i in range(len(l)):
        z.append((b[i] - math.fsum(l[i][k] * z[k] for k in range(i))) / l[i][i])
    return z


def householder_qr(a: list, ys: list) -> tuple[list, list]:
    """Householder QR of the n x p matrix a (rows), applied to each vector in ys.

    Returns (R, cs) with R the p x p triangular factor and cs[k] = Q^T ys[k].
    Raises ValueError if a has rank below p (relative tolerance RANK_TOL).
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


def _ols_whitened(xw: list, yw: list, x: list, y: list) -> GLSFit:
    rr, (c,) = householder_qr(xw, [yw])
    p = len(rr)
    b = back_substitute(rr, c[:p])
    rss = math.fsum(v * v for v in c[p:])
    df = len(xw) - p
    s2 = rss / df if df > 0 else math.nan
    cols = [back_substitute(rr, [1.0 if i == j else 0.0 for i in range(p)]) for j in range(p)]
    # cols[k] is column k of R^(-1), so (R^(-1) R^(-T))_ij = sum_k cols[k][i] cols[k][j].
    cov =[[s2 * math.fsum(cols[k][i] * cols[k][j] for k in range(p)) for j in range(p)]
           for i in range(p)]
    res = [y[i] - math.fsum(a * bb for a, bb in zip(x[i], b)) for i in range(len(x))]
    return GLSFit(b, rss, df, s2, cov, res)


def generalized_least_squares(x: list, y: list, v: list) -> GLSFit:
    """Fit y = X b + e with Cov(e) = sigma^2 V for a known positive definite V.

    Cost: n^3/3 flops for the Cholesky factor, n^2 p for the whitening and
    2 n p^2 for the QR.
    """
    n = len(x)
    if len(y) != n or len(v) != n or any(len(row) != n for row in v):
        raise ValueError("x, y and V must have matching sizes")
    l = cholesky(v)  # @line L1
    cols = [forward_substitute(l, [row[j] for row in x]) for j in range(len(x[0]))]  # @line L2
    xw = [[c[i] for c in cols] for i in range(n)]  # @line L2
    yw = forward_substitute(l, y)  # @line L2
    rr, (c,) = householder_qr(xw, [yw])  # @line L3
    p = len(rr)
    b = back_substitute(rr, c[:p])  # @line L4
    rss = math.fsum(t * t for t in c[p:])  # @line L5
    df = n - p
    s2 = rss / df if df > 0 else math.nan  # @line L6
    rinv_cols = [back_substitute(rr, [1.0 if i == j else 0.0 for i in range(p)]) for j in range(p)]
    cov = [[s2 * math.fsum(rinv_cols[k][i] * rinv_cols[k][j] for k in range(p)) for j in range(p)]
           for i in range(p)]  # @line L7
    res = [y[i] - math.fsum(a * bb for a, bb in zip(x[i], b)) for i in range(n)]
    return GLSFit(b, rss, df, s2, cov, res)  # @line L8


def confidence_intervals(fit: GLSFit, level: float = 0.95) -> list:
    """t intervals b_j +- t_(n-p, (1 + level)/2) se_j; exact under normal errors and the right V."""
    q = t_ppf(0.5 + level / 2.0, fit.df)
    return [(bj - q * math.sqrt(fit.cov[j][j]), bj + q * math.sqrt(fit.cov[j][j]))
            for j, bj in enumerate(fit.b)]


def ar1_covariance(n: int, rho: float) -> list:
    """V with V_ts = rho^|t-s| / (1 - rho^2): the covariance of a stationary AR(1) with unit innovation variance."""
    if not -1.0 < rho < 1.0:
        raise ValueError("need |rho| < 1")
    return [[rho ** abs(t - s) / (1.0 - rho * rho) for s in range(n)] for t in range(n)]


def prais_winsten(rows: list, rho: float) -> list:
    """Apply the AR(1) whitening P to a list of rows (vectors or scalars per time point).

    Row 1 is multiplied by sqrt(1 - rho^2); row t >= 2 becomes row_t - rho row_(t-1).
    P equals L^(-1) for the Cholesky factor L of ar1_covariance(n, rho).
    """
    scalar = not isinstance(rows[0], (list, tuple))
    rs = [[r] for r in rows] if scalar else [list(r) for r in rows]
    out = [[math.sqrt(1.0 - rho * rho) * v for v in rs[0]]]
    for t in range(1, len(rs)):
        out.append([a - rho * b for a, b in zip(rs[t], rs[t - 1])])
    return [r[0] for r in out] if scalar else out


def feasible_gls_ar1(x: list, y: list) -> tuple[GLSFit, float]:
    """Two-step Prais-Winsten feasible GLS for AR(1) errors.

    Step 1: OLS residuals e and rho-hat = sum e_t e_(t-1) / sum e_t^2.
    Step 2: OLS on the rows whitened with rho-hat. Returns (fit, rho-hat).
    The reported covariance treats rho-hat as known, so it is only asymptotically valid.
    """
    n = len(x)
    ols = _ols_whitened(x, y, x, y)
    e = ols.residuals
    rho = math.fsum(e[t] * e[t - 1] for t in range(1, n)) / math.fsum(t * t for t in e)
    rho = max(-0.999, min(0.999, rho))
    fit = _ols_whitened(prais_winsten(x, rho), prais_winsten(y, rho), x, y)
    return fit, rho
