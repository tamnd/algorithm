# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-process/. The authors are listed in prov/6GME91.jsonl.

"""Gaussian process regression by Algorithm 2.1 of Rasmussen and Williams (2006)."""

import math
import random


def rbf(a, b, length=1.0, var=1.0):
    """Squared exponential covariance var * exp(-|a - b|^2 / (2 length^2)) for vectors or numbers."""
    if isinstance(a, (int, float)):
        a, b = [a], [b]
    d2 = sum((x - y) ** 2 for x, y in zip(a, b))
    return var * math.exp(-d2 / (2 * length * length))


def gram(xs, zs, k):
    return [[k(x, z) for z in zs] for x in xs]


def cholesky(a):
    """Lower triangular L with L L^T = a, for a symmetric positive definite a."""
    n = len(a)
    L = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(L[j][t] ** 2 for t in range(j))
        if s <= 0:
            raise ValueError("the matrix is not positive definite")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            L[i][j] = (a[i][j] - sum(L[i][t] * L[j][t] for t in range(j))) / L[j][j]
    return L


def solve_lower(L, b):
    """Forward substitution for L x = b."""
    x = []
    for i in range(len(b)):
        x.append((b[i] - sum(L[i][t] * x[t] for t in range(i))) / L[i][i])
    return x


def solve_upper_t(L, b):
    """Back substitution for L^T x = b, with L lower triangular."""
    n = len(b)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(L[t][i] * x[t] for t in range(i + 1, n))) / L[i][i]
    return x


def gp_regression(xs, y, k, noise, xstar):
    """Algorithm 2.1. Return (the posterior means, the posterior variances of f at xstar, log p(y | X))."""
    n = len(xs)
    K = gram(xs, xs, k)
    A = [[K[i][j] + (noise if i == j else 0.0) for j in range(n)] for i in range(n)]
    L = cholesky(A)  # @line L1
    alpha = solve_upper_t(L, solve_lower(L, y))  # @line L2
    means, variances = [], []
    for xs_ in xstar:
        ks = [k(x, xs_) for x in xs]
        means.append(sum(a * b for a, b in zip(ks, alpha)))  # @line L3
        v = solve_lower(L, ks)  # @line L4
        variances.append(k(xs_, xs_) - sum(t * t for t in v))  # @line L5
    logml = (-0.5 * sum(a * b for a, b in zip(y, alpha))  # @line L6
             - sum(math.log(L[i][i]) for i in range(n)) - 0.5 * n * math.log(2 * math.pi))
    return means, variances, logml  # @line L7


def gp_posterior_covariance(xs, k, noise, xstar):
    """The full posterior covariance K** - V^T V of f at xstar, with V = L \\ K*."""
    n = len(xs)
    A = [[k(xs[i], xs[j]) + (noise if i == j else 0.0) for j in range(n)] for i in range(n)]
    L = cholesky(A)
    V = [solve_lower(L, [k(x, s) for x in xs]) for s in xstar]
    return [[k(a, b) - sum(p * q for p, q in zip(V[i], V[j])) for j, b in enumerate(xstar)]
            for i, a in enumerate(xstar)]


def sample_prior(xs, k, rng: random.Random, jitter=1e-10):
    """One draw of (f(x_1), ..., f(x_m)) from the prior GP(0, k)."""
    m = len(xs)
    K = [[k(xs[i], xs[j]) + (jitter if i == j else 0.0) for j in range(m)] for i in range(m)]
    L = cholesky(K)
    u = [rng.gauss(0.0, 1.0) for _ in range(m)]
    return [sum(L[i][t] * u[t] for t in range(i + 1)) for i in range(m)]
