# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/innovations-algorithm/. The authors are listed in prov/1XEA6P.jsonl.

"""The innovations algorithm (Brockwell and Davis 1991, section 5.2).

For a zero-mean series X_1, ..., X_n with covariances kappa(i, j) = E[X_i X_j], it returns the
coefficients theta[m][j] (1 <= j <= m) and the mean squared errors v[m] of the one-step
predictors

    Xhat_1 = 0,   Xhat_(m+1) = sum_(j=1..m) theta[m][j] (X_(m+1-j) - Xhat_(m+1-j)).

The recursion uses only +, -, * and /, so it runs unchanged on fractions.Fraction values.
Indices follow the book: kappa is called with 1-based arguments.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence


def innovations(kappa: Callable[[int, int], object], n: int, q: int | None = None):
    """Return (theta, v). theta[m] is a list with theta[m][j] at index j (index 0 unused).

    If q is given, kappa(i, j) must be 0 whenever |i - j| > q (an MA(q) process). Then
    theta[m][j] = 0 for j > q and the loops skip those zeros, so the cost is O(n q^2).
    """
    if n < 1:
        raise ValueError("need n >= 1")
    theta: list[list] = [[0]]
    v = [kappa(1, 1)]  # @line L1
    if not v[0] > 0:
        raise ValueError("kappa(1, 1) must be positive")
    for m in range(1, n):  # @line L2
        row = [0] * (m + 1)
        k_lo = 0 if q is None else max(0, m - q)
        for k in range(k_lo, m):  # @line L3
            s = kappa(m + 1, k + 1)
            for j in range(k_lo, k):
                s -= theta[k][k - j] * row[m - j] * v[j]  # @line L4
            row[m - k] = s / v[k]  # @line L5
        theta.append(row)
        vm = kappa(m + 1, m + 1) - sum(row[m - j] * row[m - j] * v[j] for j in range(k_lo, m))  # @line L6
        if not vm > 0:
            raise ValueError("the covariance matrix is not positive definite")
        v.append(vm)
    return theta, v  # @line L7


def one_step_predictors(x: Sequence, theta: list[list]) -> list:
    """Return Xhat_1, ..., Xhat_n (and Xhat_(n+1) if theta has n rows past row 0)."""
    n = len(x)
    xhat = [0 * x[0] if n else 0]
    for m in range(1, min(n, len(theta) - 1) + 1):
        xhat.append(sum(theta[m][j] * (x[m - j] - xhat[m - j]) for j in range(1, m + 1)))
    return xhat


def gaussian_neg2_loglik(x: Sequence[float], kappa: Callable[[int, int], float],
                         q: int | None = None) -> float:
    """-2 log L of a zero-mean Gaussian vector with covariance kappa, by the innovations.

    -2 log L = n log(2 pi) + sum_j log v_(j-1) + sum_j (X_j - Xhat_j)^2 / v_(j-1).
    """
    n = len(x)
    theta, v = innovations(kappa, n, q)
    xhat = one_step_predictors(list(x), theta)
    total = n * math.log(2 * math.pi)
    total += math.fsum(math.log(v[j]) for j in range(n))
    total += math.fsum((x[j] - xhat[j]) ** 2 / v[j] for j in range(n))
    return total


def ma_autocovariance(theta: Sequence, sigma2, max_lag: int) -> list:
    """gamma(h) of X_t = e_t + theta_1 e_(t-1) + ... + theta_q e_(t-q), e ~ WN(0, sigma2)."""
    c = [1] + list(theta)
    q = len(c) - 1
    return [sigma2 * sum(c[j] * c[j + h] for j in range(q - h + 1)) if h <= q else 0 * sigma2
            for h in range(max_lag + 1)]


def stationary_kappa(gamma: Sequence) -> Callable[[int, int], object]:
    """kappa(i, j) = gamma(|i - j|) for a stationary series, with gamma(h) = 0 past the list."""
    zero = 0 * gamma[0]

    def kappa(i: int, j: int):
        h = abs(i - j)
        return gamma[h] if h < len(gamma) else zero

    return kappa


def ma_preliminary_estimate(x: Sequence[float], q: int, m: int) -> tuple[list[float], float]:
    """Preliminary MA(q) estimate (Brockwell and Davis 1991, section 8.3).

    Run the recursion on the sample autocovariances (divisor n) up to step m and return
    (theta_hat[m][1..q], v_hat[m]).
    """
    n = len(x)
    if not q <= m < n:
        raise ValueError("need q <= m < n")
    mean = math.fsum(x) / n
    d = [xi - mean for xi in x]
    gamma = [math.fsum(d[t + h] * d[t] for t in range(n - h)) / n for h in range(m + 1)]
    theta, v = innovations(stationary_kappa(gamma), m + 1)
    return [theta[m][j] for j in range(1, q + 1)], v[m]
