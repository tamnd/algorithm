# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-f-test/. The authors are listed in prov/KE7D2K.jsonl.
"""The F-test for nested linear models, by one Householder QR factorization.

X is an n x p design matrix given as a list of rows. Its first p0 columns span
the null model, and all p columns span the full model. One Householder QR of X,
applied to y as well, gives c = Q^T y. Then RSS_1 = c[p]^2 + ... + c[n-1]^2 and
RSS_0 - RSS_1 = c[p0]^2 + ... + c[p-1]^2 (0-based), with no second fit and no
normal equations. The general linear hypothesis R b = r uses the Wald form,
which gives the same F. The code is in this file and not in
regression_f_test.py, because tools treat a file whose name ends in _test.py
as a test file.
"""

import math
from collections.abc import Sequence

from stdist import f_sf, t_sf

RANK_TOL = 1e-10


def householder_qr(X: Sequence[Sequence[float]], y: Sequence[float]):
    """Return (R, c): R is the p x p upper triangular factor of X = Q R and c = Q^T y.

    Raises ValueError if a column is, to RANK_TOL relative accuracy, a linear
    combination of the columns before it.
    """
    n = len(X)
    p = len(X[0]) if n else 0
    if n == 0 or p == 0 or any(len(row) != p for row in X) or len(y) != n:
        raise ValueError("X must be n x p with p >= 1 and y must have n entries")
    A = [[float(v) for v in row] for row in X]
    c = [float(v) for v in y]
    scale = max(math.sqrt(math.fsum(A[i][j] ** 2 for i in range(n))) for j in range(p))
    if p > n:
        raise ValueError("need n >= p")
    for j in range(p):  # @line L1
        norm = math.sqrt(math.fsum(A[i][j] ** 2 for i in range(j, n)))
        if norm <= RANK_TOL * scale:
            raise ValueError("X does not have full column rank")
        alpha = -norm if A[j][j] >= 0.0 else norm  # @line L2
        v = [0.0] * n
        v[j] = A[j][j] - alpha
        for i in range(j + 1, n):
            v[i] = A[i][j]
        vv = math.fsum(v[i] * v[i] for i in range(j, n))
        for k in range(j, p):  # @line L3
            s = 2.0 * math.fsum(v[i] * A[i][k] for i in range(j, n)) / vv
            for i in range(j, n):
                A[i][k] -= s * v[i]
        s = 2.0 * math.fsum(v[i] * c[i] for i in range(j, n)) / vv  # @line L4
        for i in range(j, n):
            c[i] -= s * v[i]
    R = [[A[i][k] if k >= i else 0.0 for k in range(p)] for i in range(p)]
    return R, c


def nested_f_test(X: Sequence[Sequence[float]], y: Sequence[float], p0: int):
    """F-test of the null model (first p0 columns of X) against the full model (all p columns).

    Returns (F, q, nu, p_value, rss0, rss1) with q = p - p0 and nu = n - p.
    """
    n = len(X)
    p = len(X[0]) if n else 0
    if not 0 <= p0 < p:
        raise ValueError("need 0 <= p0 < p, so that q = p - p0 >= 1")
    if n <= p:
        raise ValueError("need n > p, so that nu = n - p >= 1")
    _, c = householder_qr(X, y)  # lines L1 to L4
    rss1 = math.fsum(v * v for v in c[p:])  # @line L5
    extra = math.fsum(v * v for v in c[p0:p])  # @line L6
    q, nu = p - p0, n - p  # @line L7
    if rss1 == 0.0:
        if extra == 0.0:
            raise ValueError("both sums of squares are 0; F is undefined")
        return math.inf, q, nu, 0.0, extra, 0.0
    f = (extra / q) / (rss1 / nu)  # @line L8
    return f, q, nu, f_sf(f, q, nu), rss1 + extra, rss1  # @line L9


def overall_f_test(X: Sequence[Sequence[float]], y: Sequence[float]):
    """The overall F-test: all columns but the first (the intercept) have zero coefficients."""
    return nested_f_test(X, y, 1)


def back_substitute(R: Sequence[Sequence[float]], z: Sequence[float]) -> list[float]:
    """Solve R b = z for upper triangular R."""
    p = len(R)
    b = [0.0] * p
    for i in range(p - 1, -1, -1):
        b[i] = (z[i] - math.fsum(R[i][k] * b[k] for k in range(i + 1, p))) / R[i][i]
    return b


def r_inverse(R: Sequence[Sequence[float]]) -> list[list[float]]:
    """The inverse of an upper triangular R, column by column."""
    p = len(R)
    cols = [back_substitute(R, [1.0 if i == j else 0.0 for i in range(p)]) for j in range(p)]
    return [[cols[j][i] for j in range(p)] for i in range(p)]


def ols_fit(X: Sequence[Sequence[float]], y: Sequence[float]):
    """Return (b, rss, xtx_inv): coefficients, residual sum of squares and (X^T X)^(-1) = R^(-1) R^(-T)."""
    p = len(X[0])
    R, c = householder_qr(X, y)
    b = back_substitute(R, c[:p])
    Ri = r_inverse(R)
    xtx_inv = [[math.fsum(Ri[i][k] * Ri[j][k] for k in range(p)) for j in range(p)] for i in range(p)]
    return b, math.fsum(v * v for v in c[p:]), xtx_inv


def coefficient_t_tests(X: Sequence[Sequence[float]], y: Sequence[float]):
    """For each coefficient: (b_j, standard error, t = b_j / se, two-sided p-value), nu = n - p."""
    n, p = len(X), len(X[0])
    nu = n - p
    if nu < 1:
        raise ValueError("need n > p")
    b, rss, V = ols_fit(X, y)
    s2 = rss / nu
    out = []
    for j in range(p):
        se = math.sqrt(s2 * V[j][j])
        t = b[j] / se
        out.append((b[j], se, t, min(1.0, 2.0 * t_sf(abs(t), nu))))
    return out


def _solve_spd(A: list[list[float]], z: list[float]) -> list[float]:
    """Solve A u = z for a symmetric positive definite A by Cholesky."""
    m = len(A)
    L = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            s = A[i][j] - math.fsum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= RANK_TOL * abs(A[i][i]):
                    raise ValueError("the restriction matrix does not have full row rank")
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    w = [0.0] * m
    for i in range(m):
        w[i] = (z[i] - math.fsum(L[i][k] * w[k] for k in range(i))) / L[i][i]
    u = [0.0] * m
    for i in range(m - 1, -1, -1):
        u[i] = (w[i] - math.fsum(L[k][i] * u[k] for k in range(i + 1, m))) / L[i][i]
    return u


def linear_hypothesis_f_test(X: Sequence[Sequence[float]], y: Sequence[float],
                             Rm: Sequence[Sequence[float]], r: Sequence[float]):
    """Wald form of the F-test of H_0: Rm b = r, with Rm a q x p matrix of full row rank.

    F = (Rm b - r)^T [Rm (X^T X)^(-1) Rm^T]^(-1) (Rm b - r) / (q s^2).
    Returns (F, q, nu, p_value).
    """
    n, p = len(X), len(X[0])
    q, nu = len(Rm), n - p
    if q < 1 or nu < 1:
        raise ValueError("need at least one restriction and n > p")
    if any(len(row) != p for row in Rm) or len(r) != q:
        raise ValueError("Rm must be q x p and r must have q entries")
    b, rss, V = ols_fit(X, y)
    d = [math.fsum(Rm[i][j] * b[j] for j in range(p)) - r[i] for i in range(q)]
    RV = [[math.fsum(Rm[i][k] * V[k][j] for k in range(p)) for j in range(p)] for i in range(q)]
    M = [[math.fsum(RV[i][k] * Rm[j][k] for k in range(p)) for j in range(q)] for i in range(q)]
    u = _solve_spd(M, d)
    num = math.fsum(di * ui for di, ui in zip(d, u))
    s2 = rss / nu
    if s2 == 0.0:
        raise ValueError("RSS is 0; F is undefined")
    f = num / (q * s2)
    return f, q, nu, f_sf(f, q, nu)
