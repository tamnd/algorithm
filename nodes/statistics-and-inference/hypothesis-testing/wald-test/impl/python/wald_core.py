# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wald-test/. The authors are listed in prov/QP1T8S.jsonl.
"""The Wald test, in matrix form and for common models.

wald_test takes an estimate theta_hat of r parameters, the null values theta_0
and an estimate V of the covariance matrix of theta_hat, and returns
(W, p) with W = d^T V^(-1) d, d = theta_hat - theta_0, and p the upper
chi-squared tail with r degrees of freedom. The p-value is only asymptotic.
The linear system V y = d is solved by Gaussian elimination with partial
pivoting, in the arithmetic of the inputs, so Fraction inputs give an exact W.
The code is in this file and not in wald_test.py, because tools treat a file
whose name ends in _test.py as a test file.
"""

import math
from collections.abc import Sequence

from stdist import chi2_sf


def solve(a: Sequence[Sequence], b: Sequence) -> list:
    """Solve a y = b by Gaussian elimination with partial pivoting."""
    n = len(a)
    if n == 0 or any(len(row) != n for row in a) or len(b) != n:
        raise ValueError("need a square nonempty matrix and a vector of the same size")
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda i: abs(m[i][col]))
        if m[piv][col] == 0:
            raise ValueError("the covariance matrix is singular")
        m[col], m[piv] = m[piv], m[col]
        for i in range(col + 1, n):
            f = m[i][col] / m[col][col]
            if f:
                for j in range(col, n + 1):
                    m[i][j] -= f * m[col][j]
    y = [0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n] - sum(m[i][j] * y[j] for j in range(i + 1, n))
        y[i] = s / m[i][i]
    return y


def wald_test(theta_hat: Sequence, theta0: Sequence, cov: Sequence[Sequence]):
    """Wald test of H_0: theta = theta0 for r = len(theta0) parameters; returns (W, p)."""
    r = len(theta0)
    if r < 1 or len(theta_hat) != r:
        raise ValueError("theta_hat and theta0 must have the same length r >= 1")
    d = [theta_hat[i] - theta0[i] for i in range(r)]  # @line L1
    y = solve(cov, d)  # @line L2
    w = sum(d[i] * y[i] for i in range(r))  # @line L3
    if w < 0:
        raise ValueError("the covariance matrix is not positive definite")
    p = chi2_sf(float(w), r)  # @line L4
    return w, p  # @line L5


def binomial_wald(k: int, n: int, p0: float) -> tuple[float, float]:
    """W = (p_hat - p0)^2 / (p_hat (1 - p_hat) / n); infinite when p_hat is 0 or 1."""
    if n < 1 or not 0 <= k <= n or not 0.0 < p0 < 1.0:
        raise ValueError("need n >= 1, 0 <= k <= n and 0 < p0 < 1")
    if k in (0, n):
        return math.inf, 0.0
    ph = k / n
    w = n * (ph - p0) ** 2 / (ph * (1.0 - ph))
    return w, chi2_sf(w, 1)


def logit_binomial_wald(k: int, n: int, p0: float) -> tuple[float, float]:
    """Wald test of the log odds: W = (logit p_hat - logit p0)^2 n p_hat (1 - p_hat)."""
    if n < 1 or not 0 <= k <= n or not 0.0 < p0 < 1.0:
        raise ValueError("need n >= 1, 0 <= k <= n and 0 < p0 < 1")
    if k in (0, n):
        raise ValueError("the MLE of the log odds does not exist when k is 0 or n")
    ph = k / n
    beta = math.log(k / (n - k))
    beta0 = math.log(p0 / (1.0 - p0))
    w = (beta - beta0) ** 2 * n * ph * (1.0 - ph)
    return w, chi2_sf(w, 1)


def poisson_wald(total: int, n: int, lam0: float) -> tuple[float, float]:
    """W = n (lam_hat - lam0)^2 / lam_hat with lam_hat = total / n; infinite when total = 0."""
    if n < 1 or total < 0 or lam0 <= 0.0:
        raise ValueError("need n >= 1, total >= 0 and lam0 > 0")
    if total == 0:
        return math.inf, 0.0
    lh = total / n
    w = n * (lh - lam0) ** 2 / lh
    return w, chi2_sf(w, 1)


def normal_mean_wald(x: Sequence[float], mu0: float,
                     sigma: float | None = None) -> tuple[float, float]:
    """W = n (xbar - mu0)^2 / sigma^2, with sigma^2 = SS / n (the MLE) when sigma is None."""
    n = len(x)
    if n < 1 or (sigma is None and n < 2):
        raise ValueError("need n >= 1, and n >= 2 when sigma is unknown")
    mean = math.fsum(x) / n
    if sigma is None:
        var = math.fsum((v - mean) ** 2 for v in x) / n
        if var == 0.0:
            raise ValueError("all observations are equal")
    else:
        if sigma <= 0.0:
            raise ValueError("sigma must be positive")
        var = sigma * sigma
    w = n * (mean - mu0) ** 2 / var
    return w, chi2_sf(w, 1)
