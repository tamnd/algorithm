# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-a-posteriori-estimation/. The authors are listed in prov/WXKGVJ.jsonl.

"""Maximum a posteriori estimation.

MAP maximizes log p(D | theta) + log p(theta). The module gives the
beta-Bernoulli and Dirichlet-multinomial modes, a grid search for the
mode of a posterior density in any parameterization (with the Jacobian),
ridge regression as the MAP estimate under a Gaussian prior, and lasso
as the MAP estimate under a Laplace prior, solved by coordinate descent.
"""

import math
from fractions import Fraction
from typing import Callable, List, Sequence


def beta_bernoulli_map(a: Fraction, b: Fraction, s: int, f: int) -> Fraction:
    """Mode of Beta(a + s, b + f); needs a + s > 1 and b + f > 1."""
    return Fraction(a + s - 1) / (a + b + s + f - 2)


def dirichlet_map(alpha: Sequence[Fraction], counts: Sequence[int]) -> List[Fraction]:
    """Mode of Dirichlet(alpha + counts); needs every alpha_k + N_k > 1."""
    tot = sum(alpha) + sum(counts) - len(alpha)
    return [Fraction(a + c - 1) / tot for a, c in zip(alpha, counts)]


def grid_mode(log_density: Callable[[float], float], lo: float, hi: float, m: int = 200000) -> float:
    """Argmax of a log density on the midpoints of m cells of (lo, hi)."""
    h = (hi - lo) / m
    best, arg = -math.inf, lo
    for i in range(m):
        t = lo + (i + 0.5) * h
        v = log_density(t)
        if v > best:
            best, arg = v, t
    return arg


def beta_log_density_theta(a: float, b: float) -> Callable[[float], float]:
    return lambda t: (a - 1) * math.log(t) + (b - 1) * math.log(1 - t)


def beta_log_density_logit(a: float, b: float) -> Callable[[float], float]:
    """Log density of eta = logit(theta) when theta ~ Beta(a, b).

    p(eta) = p(theta(eta)) * dtheta/deta and dtheta/deta = theta (1 - theta).
    """
    def f(eta: float) -> float:
        t = 1 / (1 + math.exp(-eta))
        return a * math.log(t) + b * math.log(1 - t)
    return f


def solve(A: List[List[float]], y: List[float]) -> List[float]:
    """Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] + [y[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n + 1):
                M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))) / M[r][r]
    return x


def ridge_map(X: Sequence[Sequence[float]], y: Sequence[float], noise_var: float, prior_var: float) -> List[float]:
    """MAP weights for y = X w + N(0, noise_var), w ~ N(0, prior_var I).

    Equals ridge regression with lambda = noise_var / prior_var:
    w = (X^T X + lambda I)^{-1} X^T y.
    """
    d = len(X[0])
    lam = noise_var / prior_var
    A = [[sum(r[i] * r[j] for r in X) + (lam if i == j else 0.0) for j in range(d)] for i in range(d)]
    b = [sum(r[i] * t for r, t in zip(X, y)) for i in range(d)]
    return solve(A, b)


def lasso_map(X: Sequence[Sequence[float]], y: Sequence[float], noise_var: float, scale: float, sweeps: int = 500) -> List[float]:
    """MAP weights for y = X w + N(0, noise_var), w_j i.i.d. Laplace(0, scale).

    The negative log posterior is |y - X w|^2 / (2 noise_var) + sum |w_j| / scale,
    which is the lasso objective with lambda = 2 noise_var / scale. Solved by
    cyclic coordinate descent with soft thresholding.
    """
    n, d = len(X), len(X[0])
    lam = 2 * noise_var / scale
    w = [0.0] * d
    for _ in range(sweeps):
        for j in range(d):
            r = [y[i] - sum(X[i][k] * w[k] for k in range(d) if k != j) for i in range(n)]
            rho = sum(X[i][j] * r[i] for i in range(n))
            z = sum(X[i][j] ** 2 for i in range(n))
            w[j] = math.copysign(max(abs(rho) - lam / 2, 0.0), rho) / z
    return w


def neg_log_posterior(X, y, w, noise_var: float, prior: str, scale: float) -> float:
    rss = sum((t - sum(a * b for a, b in zip(r, w))) ** 2 for r, t in zip(X, y))
    if prior == "gauss":
        pen = sum(v * v for v in w) / (2 * scale)
    else:
        pen = sum(abs(v) for v in w) / scale
    return rss / (2 * noise_var) + pen
