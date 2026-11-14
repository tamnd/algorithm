# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heteroscedasticity-consistent-standard-errors/. The authors are listed in prov/PTWW7S.jsonl.
"""Heteroscedasticity-consistent covariance of the least squares estimate, HC0 to HC3.

With X = Q1 R (thin QR, Q1 = X R^(-1)) the sandwich
(X^T X)^(-1) X^T diag(omega_i) X (X^T X)^(-1) equals R^(-1) (sum omega_i q_i q_i^T) R^(-T),
where q_i^T is row i of Q1 and h_ii = |q_i|^2 is the leverage. The weights are
  HC0: e_i^2                    HC1: e_i^2 n / (n - p)
  HC2: e_i^2 / (1 - h_ii)       HC3: e_i^2 / (1 - h_ii)^2
Nothing of size n x n is formed.
"""

import math
from typing import NamedTuple

from stdist import t_ppf

RANK_TOL = 1e-12
KINDS = ("HC0", "HC1", "HC2", "HC3")


class HCFit(NamedTuple):
    b: list          # least squares coefficients
    cov: list        # the HC covariance estimate, p x p
    se: list         # square roots of its diagonal
    residuals: list  # e_i
    leverage: list   # h_ii
    df: int          # n - p


def householder_r(a: list, y: list) -> tuple[list, list]:
    """R of a Householder QR of the n x p matrix a, and Q^T y. Raises ValueError if rank < p."""
    n = len(a)
    p = len(a[0]) if n else 0
    if p == 0 or n < p:
        raise ValueError("need a design with n >= p >= 1")
    a = [[float(v) for v in row] for row in a]
    c = [float(v) for v in y]
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
        s = 2.0 * math.fsum(v[i - j] * c[i] for i in range(j, n)) / vv
        for i in range(j, n):
            c[i] -= s * v[i - j]
    return [[a[i][k] if k >= i else 0.0 for k in range(p)] for i in range(p)], c


def back_substitute(r: list, c: list) -> list:
    p = len(r)
    x = [0.0] * p
    for i in range(p - 1, -1, -1):
        x[i] = (c[i] - math.fsum(r[i][k] * x[k] for k in range(i + 1, p))) / r[i][i]
    return x


def forward_substitute_rt(r: list, c: list) -> list:
    """Solve R^T q = c for upper triangular R (R^T is lower triangular)."""
    p = len(r)
    q = [0.0] * p
    for i in range(p):
        q[i] = (c[i] - math.fsum(r[k][i] * q[k] for k in range(i))) / r[i][i]
    return q


def sandwich(r: list, q: list, omega: list) -> list:
    """R^(-1) (sum_i omega_i q_i q_i^T) R^(-T) for upper triangular R."""
    p = len(r)
    m = [[math.fsum(o * qi[a] * qi[b] for o, qi in zip(omega, q)) for b in range(p)] for a in range(p)]
    t = [back_substitute(r, [m[a][b] for a in range(p)]) for b in range(p)]   # columns of R^(-1) M
    rows = [back_substitute(r, [t[b][a] for b in range(p)]) for a in range(p)]  # rows of (R^(-1) M) R^(-T)
    return [[rows[a][b] for b in range(p)] for a in range(p)]


def hc_covariance(x: list, y: list, kind: str = "HC3") -> HCFit:
    """Least squares fit with the heteroscedasticity-consistent covariance of the given kind.

    Cost: Theta(n p^2) time, Theta(n p) space.
    """
    if kind not in KINDS:
        raise ValueError("kind must be one of " + ", ".join(KINDS))
    n = len(x)
    if len(y) != n:
        raise ValueError("x and y must have the same length")
    r, c = householder_r(x, y)  # @line L1
    p = len(r)
    if n <= p:
        raise ValueError("need n > p")
    b = back_substitute(r, c[:p])  # @line L2
    e = [yi - math.fsum(a * bb for a, bb in zip(xi, b)) for xi, yi in zip(x, y)]  # @line L3
    q = [forward_substitute_rt(r, xi) for xi in x]  # @line L4
    h = [math.fsum(t * t for t in qi) for qi in q]  # @line L4
    if kind == "HC0":  # @line L5
        omega = [ei * ei for ei in e]
    elif kind == "HC1":
        omega = [ei * ei * n / (n - p) for ei in e]
    elif kind == "HC2":
        if max(h) >= 1.0 - 1e-12:
            raise ValueError("a leverage equals 1; HC2 and HC3 are undefined")
        omega = [ei * ei / (1.0 - hi) for ei, hi in zip(e, h)]
    else:
        if max(h) >= 1.0 - 1e-12:
            raise ValueError("a leverage equals 1; HC2 and HC3 are undefined")
        omega = [ei * ei / (1.0 - hi) ** 2 for ei, hi in zip(e, h)]
    cov = sandwich(r, q, omega)  # @line L6
    se = [math.sqrt(max(cov[j][j], 0.0)) for j in range(p)]  # @line L7
    return HCFit(b, cov, se, e, h, n - p)  # @line L8


def confidence_intervals(fit: HCFit, level: float = 0.95) -> list:
    """b_j +- t_(n-p, (1 + level)/2) se_j. The level is only approximate: HC inference is asymptotic."""
    qt = t_ppf(0.5 + level / 2.0, fit.df)
    return [(bj - qt * s, bj + qt * s) for bj, s in zip(fit.b, fit.se)]
