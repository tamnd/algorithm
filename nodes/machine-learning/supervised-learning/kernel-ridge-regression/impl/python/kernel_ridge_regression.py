# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-ridge-regression/. The authors are listed in prov/EBABAD.jsonl.

"""Kernel ridge regression.

It minimizes sum_i (f(x_i) - y_i)^2 + lam ||f||_H^2 over the reproducing
kernel Hilbert space of k. The minimizer is f(x) = sum_i alpha_i k(x_i, x)
with alpha = (K + lam I)^{-1} y. The penalty lam multiplies the plain sum of
squared errors, not the mean; the objective with the mean uses n lam instead.
"""

import math
from typing import Callable, Sequence

Vec = Sequence[float]
Kernel = Callable[[Vec, Vec], float]


def cholesky(a: Sequence[Sequence[float]]) -> list[list[float]]:
    """Lower triangular L with L L^T = a, for a symmetric positive definite a."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(low[j][t] ** 2 for t in range(j))
        if s <= 0:
            raise ValueError("matrix is not positive definite")
        low[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][t] * low[j][t] for t in range(j))) / low[j][j]
    return low


def krr_fit(xs: Sequence[Vec], ys: Sequence[float], k: Kernel, lam: float) -> list[float]:
    """Return alpha = (K + lam I)^{-1} y. Needs lam > 0, or a positive definite K."""
    n = len(xs)
    gram = [[k(xs[i], xs[j]) for j in range(n)] for i in range(n)]  # @line L1
    a = [[gram[i][j] + (lam if i == j else 0.0) for j in range(n)] for i in range(n)]  # @line L2
    low = cholesky(a)  # @line L3
    u = [0.0] * n
    for i in range(n):  # @line L4 (forward substitution, L u = y)
        u[i] = (ys[i] - sum(low[i][t] * u[t] for t in range(i))) / low[i][i]
    alpha = [0.0] * n
    for i in range(n - 1, -1, -1):  # @line L5 (back substitution, L^T alpha = u)
        alpha[i] = (u[i] - sum(low[t][i] * alpha[t] for t in range(i + 1, n))) / low[i][i]
    return alpha  # @line L6


def krr_predict(xs: Sequence[Vec], alpha: Sequence[float], k: Kernel, x: Vec) -> float:
    return sum(a * k(xi, x) for a, xi in zip(alpha, xs))  # @line L7


def loo_residuals(xs: Sequence[Vec], ys: Sequence[float], k: Kernel, lam: float) -> list[float]:
    """Leave-one-out residuals y_i - f_{-i}(x_i) = alpha_i / [(K + lam I)^{-1}]_ii.

    One fit and one inverse give all n residuals; no refit is needed.
    """
    n = len(xs)
    alpha = krr_fit(xs, ys, k, lam)
    a = [[k(xs[i], xs[j]) + (lam if i == j else 0.0) for j in range(n)] for i in range(n)]
    low = cholesky(a)
    out = []
    for i in range(n):
        e = [1.0 if t == i else 0.0 for t in range(n)]
        u = [0.0] * n
        for r in range(n):
            u[r] = (e[r] - sum(low[r][t] * u[t] for t in range(r))) / low[r][r]
        # [(L L^T)^{-1}]_ii = |L^{-1} e_i|^2
        out.append(alpha[i] / sum(v * v for v in u))
    return out


# ----- references for the tests ----------------------------------------------


def poly2_features(x: Vec) -> list[float]:
    """phi(x) . phi(z) = (x . z + 1)^2 for x, z in R^2."""
    r2 = math.sqrt(2)
    x1, x2 = x
    return [1.0, r2 * x1, r2 * x2, x1 * x1, r2 * x1 * x2, x2 * x2]


def primal_ridge(features: Sequence[Vec], ys: Sequence[float], lam: float) -> list[float]:
    """w = (Phi^T Phi + lam I)^{-1} Phi^T y, with every weight penalized."""
    d = len(features[0])
    a = [[sum(f[i] * f[j] for f in features) + (lam if i == j else 0.0) for j in range(d)] for i in range(d)]
    b = [sum(f[i] * y for f, y in zip(features, ys)) for i in range(d)]
    low = cholesky(a)
    u = [0.0] * d
    for i in range(d):
        u[i] = (b[i] - sum(low[i][t] * u[t] for t in range(i))) / low[i][i]
    w = [0.0] * d
    for i in range(d - 1, -1, -1):
        w[i] = (u[i] - sum(low[t][i] * w[t] for t in range(i + 1, d))) / low[i][i]
    return w
