# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-linear-model/. The authors are listed in prov/KTAMYG.jsonl.

"""Generalized linear models fitted by iteratively reweighted least squares (IRLS).

A family gives the variance function V(mu) and the log-likelihood of one
observation (with the dispersion set to 1). A link gives eta = g(mu), its
inverse and g'(mu). IRLS is Fisher scoring: with eta = X beta and
mu = g^{-1}(eta), it solves the weighted least squares problem with weights
W_i = 1 / (V(mu_i) g'(mu_i)^2) and working response
z_i = eta_i + (y_i - mu_i) g'(mu_i). For the canonical link, W_i = V(mu_i),
and the step is exactly Newton's method.
"""

import math
from typing import Callable, NamedTuple, Sequence


class Link(NamedTuple):
    g: Callable[[float], float]
    inverse: Callable[[float], float]
    derivative: Callable[[float], float]  # g'(mu)


class Family(NamedTuple):
    variance: Callable[[float], float]
    loglik: Callable[[float, float], float]  # log f(y; mu) up to terms free of mu
    canonical: str
    start: Callable[[float], float]  # a starting mu from y


def _sigmoid(t: float) -> float:
    if t >= 0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


LINKS = {
    "identity": Link(lambda m: m, lambda e: e, lambda m: 1.0),
    "log": Link(math.log, math.exp, lambda m: 1.0 / m),
    "logit": Link(lambda m: math.log(m / (1.0 - m)), _sigmoid, lambda m: 1.0 / (m * (1.0 - m))),
    "inverse": Link(lambda m: 1.0 / m, lambda e: 1.0 / e, lambda m: -1.0 / (m * m)),
}

FAMILIES = {
    "gaussian": Family(lambda m: 1.0, lambda y, m: -0.5 * (y - m) ** 2, "identity", lambda y: y),
    "poisson": Family(lambda m: m, lambda y, m: y * math.log(m) - m, "log", lambda y: y + 0.5),
    "binomial": Family(
        lambda m: m * (1.0 - m),
        lambda y, m: y * math.log(m) + (1.0 - y) * math.log(1.0 - m),
        "logit",
        lambda y: (y + 0.5) / 2.0,
    ),
    "gamma": Family(lambda m: m * m, lambda y, m: -y / m - math.log(m), "inverse", lambda y: y),
}


def _weighted_least_squares(X: Sequence[Sequence[float]], w: Sequence[float], z: Sequence[float]) -> list[float]:
    """Solve (X^T W X) beta = X^T W z by Cholesky."""
    n, d = len(X), len(X[0])
    A = [[sum(w[i] * X[i][a] * X[i][c] for i in range(n)) for c in range(d)] for a in range(d)]
    h = [sum(w[i] * X[i][a] * z[i] for i in range(n)) for a in range(d)]
    L = [[0.0] * d for _ in range(d)]
    for j in range(d):
        s = A[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if s <= 0.0:
            raise ArithmeticError("X^T W X is not numerically positive definite")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, d):
            L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    v = [0.0] * d
    for i in range(d):
        v[i] = (h[i] - sum(L[i][k] * v[k] for k in range(i))) / L[i][i]
    beta = [0.0] * d
    for i in range(d - 1, -1, -1):
        beta[i] = (v[i] - sum(L[k][i] * beta[k] for k in range(i + 1, d))) / L[i][i]
    return beta


def log_likelihood(X, y, beta, family: str, link: str) -> float:
    fam, lk = FAMILIES[family], LINKS[link]
    total = 0.0
    for xi, yi in zip(X, y):
        mu = lk.inverse(sum(a * b for a, b in zip(xi, beta)))
        total += fam.loglik(yi, mu)
    return total


def irls(
    X: Sequence[Sequence[float]],
    y: Sequence[float],
    family: str,
    link: str | None = None,
    tol: float = 1e-10,
    max_iter: int = 100,
) -> tuple[list[float], int]:
    """Fit a GLM by IRLS (Fisher scoring) with step halving. Returns (beta, iterations).

    X should contain a column of ones for an intercept. link defaults to the
    canonical link of the family. Stops when no coefficient moves by more
    than tol (relative) in one step.
    """
    fam = FAMILIES[family]
    lk = LINKS[link or fam.canonical]
    mu = [fam.start(t) for t in y]
    eta = [lk.g(m) for m in mu]
    beta = None
    old = -math.inf
    for it in range(1, max_iter + 1):
        gp = [lk.derivative(m) for m in mu]
        w = [1.0 / (fam.variance(m) * g * g) for m, g in zip(mu, gp)]
        z = [e + (yi - m) * g for e, yi, m, g in zip(eta, y, mu, gp)]
        new = _weighted_least_squares(X, w, z)
        if beta is not None:
            # Step halving: keep the likelihood from going down (or out of range).
            for _ in range(60):
                try:
                    ll = log_likelihood(X, y, new, family, link or fam.canonical)
                except (ValueError, ZeroDivisionError, OverflowError):
                    ll = -math.inf
                if ll >= old - 1e-12 * (1 + abs(old)):
                    break
                new = [(a + b) / 2 for a, b in zip(new, beta)]
        step = math.inf if beta is None else max(abs(a - b) for a, b in zip(new, beta))
        beta = new
        if step <= tol * (1 + max(abs(b) for b in beta)):
            return beta, it
        eta = [sum(a * b for a, b in zip(xi, beta)) for xi in X]
        mu = [lk.inverse(e) for e in eta]
        old = log_likelihood(X, y, beta, family, link or fam.canonical)
    return beta, max_iter


def score(X, y, beta, family: str, link: str | None = None) -> list[float]:
    """The gradient of the log-likelihood: X^T [(y - mu) / (V(mu) g'(mu))]."""
    fam = FAMILIES[family]
    lk = LINKS[link or fam.canonical]
    d = len(X[0])
    out = [0.0] * d
    for xi, yi in zip(X, y):
        mu = lk.inverse(sum(a * b for a, b in zip(xi, beta)))
        r = (yi - mu) / (fam.variance(mu) * lk.derivative(mu))
        for j in range(d):
            out[j] += r * xi[j]
    return out
