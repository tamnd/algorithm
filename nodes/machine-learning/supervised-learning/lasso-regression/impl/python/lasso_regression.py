# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lasso-regression/. The authors are listed in prov/J4MKX9.jsonl.

import math
from typing import Sequence


def soft_threshold(z: float, t: float) -> float:
    """S(z, t) = sign(z) max(|z| - t, 0), the proximal map of t |.|."""
    if z > t:
        return z - t
    if z < -t:
        return z + t
    return 0.0


def lasso_regression(
    X: Sequence[Sequence[float]],
    y: Sequence[float],
    lam: float,
    fit_intercept: bool = True,
    tol: float = 1e-12,
    max_sweeps: int = 100000,
) -> tuple[list[float], float]:
    """Return (w, b) that minimize (1/(2n)) ||y - X w - b 1||^2 + lam ||w||_1.

    This is the glmnet scaling. The intercept b is not penalized: the method
    centers X and y, runs cyclic coordinate descent with soft thresholding
    on the centered data, and sets b = mean(y) - mean(X) . w. It keeps the
    residual r = yc - Xc w up to date, so one sweep costs O(n d). It stops
    when a whole sweep moves no weight by more than tol (in the scale of
    sqrt(a_j)), or after max_sweeps sweeps.
    """
    n, d = len(X), len(X[0])
    if lam < 0:
        raise ValueError("lam must be >= 0")
    if fit_intercept:  # @line L1
        xbar = [sum(row[j] for row in X) / n for j in range(d)]
        ybar = sum(y) / n
    else:
        xbar, ybar = [0.0] * d, 0.0
    cols = [[row[j] - xbar[j] for row in X] for j in range(d)]
    r = [t - ybar for t in y]
    a = [sum(t * t for t in c) / n for c in cols]  # @line L2
    w = [0.0] * d
    scale = 1.0 + math.sqrt(sum(t * t for t in r) / n)
    for _ in range(max_sweeps):  # @line L3
        biggest = 0.0
        for j in range(d):  # @line L4
            if a[j] == 0.0:
                continue
            c = cols[j]
            rho = sum(c[i] * r[i] for i in range(n)) / n + a[j] * w[j]  # @line L5
            new = soft_threshold(rho, lam) / a[j]  # @line L6
            delta = new - w[j]
            if delta != 0.0:  # @line L7
                for i in range(n):
                    r[i] -= c[i] * delta
                w[j] = new
            biggest = max(biggest, math.sqrt(a[j]) * abs(delta))
        if biggest <= tol * scale:  # @line L8
            break
    b = ybar - sum(p * q for p, q in zip(xbar, w))  # @line L9
    return w, b  # @line L10
