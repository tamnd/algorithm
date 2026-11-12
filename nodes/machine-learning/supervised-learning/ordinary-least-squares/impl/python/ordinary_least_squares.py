# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordinary-least-squares/. The authors are listed in prov/QBJGD1.jsonl.

import math
from typing import Sequence


def ordinary_least_squares(X: Sequence[Sequence[float]], y: Sequence[float]) -> list[float]:
    """Return w that minimizes ||y - X w||_2, by Householder QR.

    X is n x d (a list of n rows) with n >= d and rank d. The method applies
    d Householder reflections to X and y, which gives R w = (Q^T y)[0:d] with
    R upper triangular, then solves by back substitution. Cost: about
    2 n d^2 - 2 d^3 / 3 flops for the factorization, O(n d) for y, and
    O(n d) extra memory for the working copy.
    """
    n, d = len(X), len(X[0])
    if n < d:
        raise ValueError("need n >= d")
    A = [list(map(float, row)) for row in X]  # @line L1
    b = list(map(float, y))
    tol = 1e-12 * math.sqrt(sum(t * t for row in A for t in row))
    for k in range(d):  # @line L2
        norm = math.sqrt(sum(A[i][k] ** 2 for i in range(k, n)))  # @line L3
        if norm <= tol:
            raise ValueError("X does not have full column rank")
        alpha = -norm if A[k][k] >= 0 else norm
        v = [A[i][k] for i in range(k, n)]
        v[0] -= alpha  # @line L4
        vv = sum(t * t for t in v)
        for j in range(k, d):  # @line L5
            s = 2.0 * sum(v[i - k] * A[i][j] for i in range(k, n)) / vv
            for i in range(k, n):
                A[i][j] -= s * v[i - k]
        s = 2.0 * sum(v[i - k] * b[i] for i in range(k, n)) / vv  # @line L6
        for i in range(k, n):
            b[i] -= s * v[i - k]
    w = [0.0] * d  # @line L7
    for k in range(d - 1, -1, -1):
        w[k] = (b[k] - sum(A[k][j] * w[j] for j in range(k + 1, d))) / A[k][k]
    return w  # @line L8


def normal_equations(X: Sequence[Sequence[float]], y: Sequence[float]) -> list[float]:
    """Return w that solves X^T X w = X^T y, by Cholesky. For comparison only.

    Cost: about n d^2 flops to form X^T X and d^3 / 3 for Cholesky. The
    condition number of X^T X is the square of that of X, so this loses
    twice as many digits as QR. Raises ArithmeticError when the computed
    X^T X is not numerically positive definite.
    """
    n, d = len(X), len(X[0])
    G = [[sum(X[i][a] * X[i][c] for i in range(n)) for c in range(d)] for a in range(d)]
    h = [sum(X[i][a] * y[i] for i in range(n)) for a in range(d)]
    L = [[0.0] * d for _ in range(d)]
    for j in range(d):
        s = G[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if s <= 0.0:
            raise ArithmeticError("X^T X is not numerically positive definite")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, d):
            L[i][j] = (G[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    z = [0.0] * d
    for i in range(d):
        z[i] = (h[i] - sum(L[i][k] * z[k] for k in range(i))) / L[i][i]
    w = [0.0] * d
    for i in range(d - 1, -1, -1):
        w[i] = (z[i] - sum(L[k][i] * w[k] for k in range(i + 1, d))) / L[i][i]
    return w
