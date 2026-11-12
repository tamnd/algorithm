# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-regression/. The authors are listed in prov/N7DDFT.jsonl.

import math
from typing import Sequence


def sigmoid(z: float) -> float:
    """1 / (1 + exp(-z)) without overflow."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def softplus(z: float) -> float:
    """log(1 + exp(z)) without overflow."""
    return max(z, 0.0) + math.log1p(math.exp(-abs(z)))


def objective(X: Sequence[Sequence[float]], y: Sequence[int], w: Sequence[float], b: float, lam: float) -> float:
    """sum_i [log(1 + e^{z_i}) - y_i z_i] + (lam/2) ||w||^2 with z_i = b + x_i . w."""
    total = 0.0
    for xi, yi in zip(X, y):
        z = b + sum(a * c for a, c in zip(xi, w))
        total += softplus(z) - yi * z
    return total + 0.5 * lam * sum(c * c for c in w)


def _cholesky_solve(H: list[list[float]], g: list[float]) -> list[float]:
    m = len(H)
    L = [[0.0] * m for _ in range(m)]
    for j in range(m):
        s = H[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if s <= 0.0:
            raise ArithmeticError("the Hessian is not numerically positive definite")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, m):
            L[i][j] = (H[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    z = [0.0] * m
    for i in range(m):
        z[i] = (g[i] - sum(L[i][k] * z[k] for k in range(i))) / L[i][i]
    x = [0.0] * m
    for i in range(m - 1, -1, -1):
        x[i] = (z[i] - sum(L[k][i] * x[k] for k in range(i + 1, m))) / L[i][i]
    return x


def logistic_regression(
    X: Sequence[Sequence[float]],
    y: Sequence[int],
    lam: float = 0.0,
    tol: float = 1e-10,
    max_iter: int = 100,
) -> tuple[list[float], float, int]:
    """Fit P(y = 1 | x) = sigmoid(b + x . w) by damped Newton (IRLS).

    Minimizes the negative log-likelihood plus (lam/2) ||w||^2; the bias b
    is not penalized. Each iteration forms the gradient X~^T (p - y) and the
    Hessian X~^T S X~ with S = diag(p_i (1 - p_i)), where X~ = [1, X], and
    takes the Newton step with a backtracking line search. Returns
    (w, b, iterations). On separable data with lam = 0 there is no
    minimizer; the iterates then grow until max_iter or until the Hessian
    is numerically singular (ArithmeticError).
    """
    n, d = len(X), len(X[0])
    Xt = [[1.0] + [float(t) for t in row] for row in X]
    m = d + 1
    theta = [0.0] * m  # @line L1
    for it in range(1, max_iter + 1):  # @line L2
        p = [sigmoid(sum(a * c for a, c in zip(row, theta))) for row in Xt]  # @line L3
        g = [sum(Xt[i][j] * (p[i] - y[i]) for i in range(n)) + (lam * theta[j] if j else 0.0) for j in range(m)]  # @line L4
        s = [pi * (1.0 - pi) for pi in p]  # @line L5
        H = [[sum(s[i] * Xt[i][j] * Xt[i][k] for i in range(n)) + (lam if j == k and j else 0.0) for k in range(m)] for j in range(m)]
        delta = _cholesky_solve(H, g)  # @line L6
        f0 = objective(X, y, theta[1:], theta[0], lam)  # @line L7
        slope = sum(a * c for a, c in zip(g, delta))
        t = 1.0
        while True:
            cand = [a - t * c for a, c in zip(theta, delta)]
            if objective(X, y, cand[1:], cand[0], lam) <= f0 - 0.25 * t * slope or t < 1e-12:
                break
            t *= 0.5
        theta = cand
        if math.sqrt(sum(c * c for c in delta)) * t <= tol * (1.0 + math.sqrt(sum(c * c for c in theta))):  # @line L8
            return theta[1:], theta[0], it
    return theta[1:], theta[0], max_iter  # @line L9
