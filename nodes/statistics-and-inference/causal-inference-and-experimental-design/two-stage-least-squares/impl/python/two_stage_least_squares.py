# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-stage-least-squares/. The authors are listed in prov/2XMPJR.jsonl.

"""Two-stage least squares (2SLS) for the linear model y = X b + u with instruments Z.

X is n x k (a constant column, exogenous regressors and endogenous regressors) and
Z is n x l with l >= k (the constant, the exogenous regressors and the excluded
instruments). The estimate is

    b = (X' P_Z X)^(-1) X' P_Z y,   P_Z = Z (Z'Z)^(-1) Z'.

It is computed as two least squares fits: X_hat = Z (Z'Z)^(-1) Z'X, then
b = (X_hat' X)^(-1) X_hat' y, which equals the regression of y on X_hat because
X_hat' X = X_hat' X_hat. The residuals use the original X, not X_hat.

Matrices are lists of rows. All functions are exact for Fraction inputs, except
the p-values, which come from stdist.
"""

from collections.abc import Sequence
from typing import NamedTuple

from stdist import chi2_sf, f_sf


class TSLSResult(NamedTuple):
    coef: list  # b, one entry per column of X
    resid: list  # u = y - X b, with the original X
    sigma2: object  # u'u / (n - k)
    cov: list  # sigma2 (X_hat' X_hat)^(-1), the variance under homoskedastic errors
    cov_hc0: list  # the sandwich (X_hat' X_hat)^(-1) (sum u_i^2 xh_i xh_i') (X_hat' X_hat)^(-1)
    first_stage: list  # Pi = (Z'Z)^(-1) Z'X, l x k
    x_hat: list  # Z Pi, n x k


def transpose(a):
    return [list(col) for col in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def crossprod(a, b):
    """a' b for matrices with the same number of rows."""
    return matmul(transpose(a), b)


def solve(a: list[list], b: list[list]) -> list[list]:
    """Solve a x = b for a square a and a matrix b, by Gaussian elimination with partial pivoting."""
    k = len(a)
    m = [list(ra) + list(rb) for ra, rb in zip(a, b)]
    w = len(m[0])
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix: the instruments or regressors are collinear")
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                for j in range(c, w):
                    m[r][j] -= f * m[c][j]
    return [[m[r][j] / m[r][r] for j in range(k, w)] for r in range(k)]


def inverse(a):
    k = len(a)
    one = a[0][0] * 0 + 1
    return solve(a, [[one if i == j else one - one for j in range(k)] for i in range(k)])


def column(v):
    return [[x] for x in v]


def tsls(y: Sequence, x: list[list], z: list[list]) -> TSLSResult:
    """2SLS fit. Cost: Theta(n l^2 + l^3) for the first stage and Theta(n k^2 + k^3) for the second."""
    n, k, l = len(y), len(x[0]), len(z[0])
    if len(x) != n or len(z) != n:
        raise ValueError("y, X and Z need the same number of rows")
    if l < k:
        raise ValueError("under-identified: fewer instruments than regressors")
    if n <= k:
        raise ValueError("need more units than regressors")
    pi = solve(crossprod(z, z), crossprod(z, x))  # @line L1
    xh = matmul(z, pi)  # @line L2
    a = crossprod(xh, x)  # @line L3
    b = [r[0] for r in solve(a, crossprod(xh, column(y)))]
    u = [yi - sum(xij * bj for xij, bj in zip(row, b)) for yi, row in zip(y, x)]  # @line L4
    s2 = sum(ui * ui for ui in u) / (n - k)  # @line L5
    bread = inverse(crossprod(xh, xh))
    cov = [[s2 * v for v in row] for row in bread]
    meat = [[sum(ui * ui * r[i] * r[j] for ui, r in zip(u, xh)) for j in range(k)] for i in range(k)]  # @line L6
    hc0 = matmul(matmul(bread, meat), bread)
    return TSLSResult(b, u, s2, cov, hc0, pi, xh)  # @line L7


def ols(y: Sequence, x: list[list]) -> list:
    """Least squares coefficients of y on the columns of x."""
    return [r[0] for r in solve(crossprod(x, x), crossprod(x, column(y)))]


def sargan(res: TSLSResult, z: list[list]) -> tuple[object, int, float]:
    """Sargan's overidentification statistic n R^2 from the regression of the 2SLS residuals on Z.

    Returns (statistic, degrees of freedom l - k, p-value from chi-square). The R^2 is centred,
    so Z must contain a constant column. Valid with homoskedastic errors.
    """
    n, k, l = len(res.resid), len(res.coef), len(z[0])
    if l == k:
        raise ValueError("just-identified: there is nothing to test")
    u = res.resid
    g = ols(u, z)
    fit = [sum(zij * gj for zij, gj in zip(row, g)) for row in z]
    ubar = sum(u) / n
    tss = sum((ui - ubar) ** 2 for ui in u)
    ess = sum((fi - ubar) ** 2 for fi in fit)
    stat = n * ess / tss
    return stat, l - k, chi2_sf(float(stat), l - k)


def first_stage_f(d: Sequence, z_exog: list[list], z_excl: list[list]) -> tuple[object, int, int, float]:
    """F statistic for the excluded instruments in the regression of one endogenous regressor d
    on (z_exog, z_excl). Returns (F, q, n - l, p-value) with q the number of excluded instruments."""
    n = len(d)
    full = [a + b for a, b in zip(z_exog, z_excl)]
    l, q = len(full[0]), len(z_excl[0])

    def rss(cols):
        g = ols(d, cols)
        return sum((di - sum(c * gj for c, gj in zip(row, g))) ** 2 for di, row in zip(d, cols))

    ru, rr = rss(full), rss(z_exog)
    f = ((rr - ru) / q) / (ru / (n - l))
    return f, q, n - l, f_sf(float(f), q, n - l)
