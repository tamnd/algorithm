# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/softmax-regression/. The authors are listed in prov/789V98.jsonl.

import math
from typing import Sequence


def softmax(z: Sequence[float]) -> list[float]:
    """exp(z_k) / sum_j exp(z_j), computed with the max subtracted (log-sum-exp trick)."""
    m = max(z)
    e = [math.exp(t - m) for t in z]
    s = sum(e)
    return [t / s for t in e]


def log_sum_exp(z: Sequence[float]) -> float:
    m = max(z)
    return m + math.log(sum(math.exp(t - m) for t in z))


def scores(W: Sequence[Sequence[float]], x: Sequence[float]) -> list[float]:
    """z_k = b_k + w_k . x, where row k of W is (b_k, w_k)."""
    return [row[0] + sum(a * c for a, c in zip(row[1:], x)) for row in W]


def objective(X: Sequence[Sequence[float]], y: Sequence[int], W: Sequence[Sequence[float]], lam: float) -> float:
    """(1/n) sum_i [log sum_k exp(z_ik) - z_{i, y_i}] + (lam/2) sum_k ||w_k||^2 (biases not penalized)."""
    n = len(X)
    total = 0.0
    for xi, yi in zip(X, y):
        z = scores(W, xi)
        total += log_sum_exp(z) - z[yi]
    return total / n + 0.5 * lam * sum(c * c for row in W for c in row[1:])


def gradient(X: Sequence[Sequence[float]], y: Sequence[int], W: Sequence[Sequence[float]], lam: float) -> list[list[float]]:
    """(1/n) (P - Y)^T X~ + lam [0 | w], one row per class."""
    n, K, m = len(X), len(W), len(W[0])
    G = [[0.0] * m for _ in range(K)]
    for xi, yi in zip(X, y):
        p = softmax(scores(W, xi))
        for k in range(K):
            e = (p[k] - (1.0 if k == yi else 0.0)) / n
            G[k][0] += e
            for j in range(1, m):
                G[k][j] += e * xi[j - 1]
    for k in range(K):
        for j in range(1, m):
            G[k][j] += lam * W[k][j]
    return G


def softmax_regression(
    X: Sequence[Sequence[float]],
    y: Sequence[int],
    K: int,
    lam: float,
    tol: float = 1e-9,
    max_iter: int = 200000,
) -> tuple[list[list[float]], int]:
    """Fit P(y = k | x) = softmax(W x~)_k by gradient descent with step 1/L.

    Row k of the returned K x (d + 1) matrix is (b_k, w_k). L = ||X~||_F^2 / (2n)
    + lam bounds the Lipschitz constant of the gradient, because the Hessian of
    log-sum-exp is diag(p) - p p^T, whose eigenvalues are at most 1/2. Starting
    from 0 keeps sum_k W[k] = 0, so the iterates stay in the subspace that
    removes the overparameterization. Returns (W, iterations).
    """
    n, d = len(X), len(X[0])
    W = [[0.0] * (d + 1) for _ in range(K)]  # @line L1
    lip = sum(1.0 + sum(t * t for t in xi) for xi in X) / (2.0 * n) + lam
    eta = 1.0 / lip
    for it in range(1, max_iter + 1):  # @line L2
        G = gradient(X, y, W, lam)  # @line L3
        gnorm = math.sqrt(sum(c * c for row in G for c in row))  # @line L4
        if gnorm <= tol:  # @line L5
            return W, it - 1
        W = [[a - eta * c for a, c in zip(wr, gr)] for wr, gr in zip(W, G)]  # @line L6
    return W, max_iter  # @line L7
