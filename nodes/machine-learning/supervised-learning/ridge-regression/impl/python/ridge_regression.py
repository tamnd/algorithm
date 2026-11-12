# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ridge-regression/. The authors are listed in prov/29H0AF.jsonl.

import math
from typing import Sequence


def ridge_regression(
    X: Sequence[Sequence[float]], y: Sequence[float], lam: float, fit_intercept: bool = True
) -> tuple[list[float], float]:
    """Return (w, b) that minimize ||y - X w - b 1||^2 + lam ||w||^2.

    The intercept b is not penalized. The method centers the columns of X
    and y, solves (Xc^T Xc + lam I) w = Xc^T yc by Cholesky, and sets
    b = mean(y) - mean(X) . w. With fit_intercept=False, b = 0 and there is
    no centering. Needs lam > 0, or lam = 0 with Xc of full column rank.
    Cost: n d^2 flops for the Gram matrix and d^3 / 3 for Cholesky.
    """
    n, d = len(X), len(X[0])
    if lam < 0:
        raise ValueError("lam must be >= 0")
    if fit_intercept:  # @line L1
        xbar = [sum(row[j] for row in X) / n for j in range(d)]
        ybar = sum(y) / n
    else:
        xbar, ybar = [0.0] * d, 0.0
    Xc = [[row[j] - xbar[j] for j in range(d)] for row in X]  # @line L2
    yc = [t - ybar for t in y]
    G = [[sum(r[a] * r[c] for r in Xc) for c in range(d)] for a in range(d)]  # @line L3
    for j in range(d):
        G[j][j] += lam
    h = [sum(r[a] * t for r, t in zip(Xc, yc)) for a in range(d)]  # @line L4
    L = [[0.0] * d for _ in range(d)]  # @line L5
    for j in range(d):
        s = G[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if s <= 0.0:
            raise ArithmeticError("Xc^T Xc + lam I is not numerically positive definite")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, d):
            L[i][j] = (G[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    z = [0.0] * d  # @line L6
    for i in range(d):
        z[i] = (h[i] - sum(L[i][k] * z[k] for k in range(i))) / L[i][i]
    w = [0.0] * d  # @line L7
    for i in range(d - 1, -1, -1):
        w[i] = (z[i] - sum(L[k][i] * w[k] for k in range(i + 1, d))) / L[i][i]
    b = ybar - sum(a * c for a, c in zip(xbar, w))  # @line L8
    return w, b  # @line L9
