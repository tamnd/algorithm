# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elastic-net/. The authors are listed in prov/DZDDDE.jsonl.

import math
from typing import Sequence


def soft_threshold(z: float, t: float) -> float:
    """S(z, t) = sign(z) max(|z| - t, 0)."""
    if z > t:
        return z - t
    if z < -t:
        return z + t
    return 0.0


def elastic_net(
    X: Sequence[Sequence[float]],
    y: Sequence[float],
    lam1: float,
    lam2: float,
    fit_intercept: bool = True,
    corrected: bool = False,
    tol: float = 1e-12,
    max_sweeps: int = 100000,
) -> tuple[list[float], float]:
    """Return (w, b) for the elastic net by cyclic coordinate descent.

    The naive elastic net minimizes
        (1/(2n)) ||y - X w - b 1||^2 + lam1 ||w||_1 + (lam2/2) ||w||^2,
    with b not penalized. The coordinate update is
        w_j = S((1/n) x_j^T r_(j), lam1) / ((1/n) x_j^T x_j + lam2).
    With corrected=True the weights are multiplied by (1 + lam2), the
    rescaling of Zou and Hastie (2005); it assumes standardized columns,
    (1/n) x_j^T x_j = 1 after centering. One sweep costs O(n d).
    """
    n, d = len(X), len(X[0])
    if lam1 < 0 or lam2 < 0:
        raise ValueError("penalties must be >= 0")
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
            if a[j] + lam2 == 0.0:
                continue
            c = cols[j]
            rho = sum(c[i] * r[i] for i in range(n)) / n + a[j] * w[j]  # @line L5
            new = soft_threshold(rho, lam1) / (a[j] + lam2)  # @line L6
            delta = new - w[j]
            if delta != 0.0:  # @line L7
                for i in range(n):
                    r[i] -= c[i] * delta
                w[j] = new
            biggest = max(biggest, math.sqrt(a[j] + lam2) * abs(delta))
        if biggest <= tol * scale:  # @line L8
            break
    if corrected:  # @line L9
        w = [(1.0 + lam2) * t for t in w]
    b = ybar - sum(p * q for p, q in zip(xbar, w))  # @line L10
    return w, b  # @line L11
