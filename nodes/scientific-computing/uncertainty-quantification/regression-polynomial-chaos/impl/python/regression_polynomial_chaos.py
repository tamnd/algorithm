# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-polynomial-chaos/. The authors are listed in prov/MZG7P5.jsonl.
"""Regression-based (least-squares) polynomial chaos with the leave-one-out error.

The input xi = (xi_1..xi_d) has independent components, each "uniform" on
[-1, 1] (orthonormal Legendre basis sqrt(2n+1) P_n) or "normal" (standard
normal, orthonormal Hermite basis He_n / sqrt(n!)). The code draws N random
inputs from the input law, runs the model, and solves the normal equations
(A^T A) c = A^T y by Cholesky, with A[i][a] = Psi_a(x_i). The leave-one-out
error uses the identity e_(-i) = e_i / (1 - h_i), where h_i is the diagonal
of the hat matrix A (A^T A)^(-1) A^T.
"""

import itertools
import math
import random
from typing import Callable

from scimat import cholesky, cholesky_solve

Model = Callable[[list[float]], float]


def recurrence_offdiag(family: str, k: int) -> float:
    """b_k in x psi_(k-1) = b_k psi_k + b_(k-1) psi_(k-2) for the orthonormal family."""
    if family == "uniform":
        return k / math.sqrt((2 * k - 1) * (2 * k + 1))
    if family == "normal":
        return math.sqrt(k)
    raise ValueError("family must be 'uniform' or 'normal'")


def basis_1d(family: str, x: float, p: int) -> list[float]:
    """psi_0(x)..psi_p(x), orthonormal for the law of the family."""
    vals = [1.0]
    if p >= 1:
        vals.append(x / recurrence_offdiag(family, 1))
    for k in range(2, p + 1):
        bk, bk1 = recurrence_offdiag(family, k), recurrence_offdiag(family, k - 1)
        vals.append((x * vals[k - 1] - bk1 * vals[k - 2]) / bk)
    return vals


def total_degree_set(d: int, p: int) -> list[tuple[int, ...]]:
    """All a in N^d with |a| <= p, sorted by total degree; the zero index is first."""
    out = [a for a in itertools.product(range(p + 1), repeat=d) if sum(a) <= p]
    out.sort(key=lambda a: (sum(a), [-v for v in a]))
    return out


def sample(families: list[str], rng: random.Random) -> list[float]:
    """One draw of the input vector from its law."""
    return [rng.uniform(-1.0, 1.0) if f == "uniform" else rng.gauss(0.0, 1.0) for f in families]


def design_row(index: list[tuple[int, ...]], families: list[str], x: list[float]) -> list[float]:
    """The row Psi_a(x), a in index."""
    p = max(sum(a) for a in index)
    tables = [basis_1d(families[k], x[k], p) for k in range(len(x))]
    return [math.prod(tables[k][a[k]] for k in range(len(x))) for a in index]


def gram(rows: list[list[float]]) -> list[list[float]]:
    """A^T A for the matrix with the given rows, using symmetry."""
    n = len(rows[0])
    g = [[0.0] * n for _ in range(n)]
    for r in rows:
        for i in range(n):
            ri = r[i]
            gi = g[i]
            for j in range(i, n):
                gi[j] += ri * r[j]
    for i in range(n):
        for j in range(i):
            g[i][j] = g[j][i]
    return g


def forward(low: list[list[float]], b: list[float]) -> list[float]:
    """Solve L z = b for lower triangular L."""
    z = [0.0] * len(b)
    for i in range(len(b)):
        z[i] = (b[i] - sum(low[i][k] * z[k] for k in range(i))) / low[i][i]
    return z


def least_squares(rows: list[list[float]], y: list[float]) -> tuple[list[float], list[list[float]]]:
    """Coefficients of min ||A c - y|| by the normal equations; also returns the Cholesky factor of A^T A."""
    n = len(rows[0])
    rhs = [sum(r[j] * yi for r, yi in zip(rows, y)) for j in range(n)]
    low = cholesky(gram(rows))
    return cholesky_solve(low, rhs), low


def loo_error(rows: list[list[float]], y: list[float], coeffs: list[float], low: list[list[float]]) -> float:
    """Relative leave-one-out error mean((e_i / (1 - h_i))^2) / var(y)."""
    n = len(y)
    total = 0.0
    for r, yi in zip(rows, y):
        e = yi - sum(a * c for a, c in zip(r, coeffs))
        z = forward(low, r)
        h = sum(v * v for v in z)
        total += (e / (1.0 - h)) ** 2
    mean = sum(y) / n
    var = sum((v - mean) ** 2 for v in y) / (n - 1)
    return (total / n) / var


def regression_pce(q: Model, families: list[str], p: int, n: int, rng: random.Random):
    """Least-squares PCE of total degree p from n random runs; returns (index, coeffs, loo)."""
    index = total_degree_set(len(families), p)  # @line L1
    if n < len(index):
        raise ValueError("need at least as many runs as coefficients")
    xs = [sample(families, rng) for _ in range(n)]  # @line L2
    y = [q(x) for x in xs]  # @line L3
    rows = [design_row(index, families, x) for x in xs]  # @line L4
    coeffs, low = least_squares(rows, y)  # @line L5
    loo = loo_error(rows, y, coeffs, low)  # @line L6
    return index, coeffs, loo  # @line L7


def mean_variance(coeffs: list[float]) -> tuple[float, float]:
    """Mean c_0 and variance sum_{a != 0} c_a^2 of an orthonormal expansion."""
    return coeffs[0], sum(c * c for c in coeffs[1:])


def sobol_from_coefficients(index: list[tuple[int, ...]], coeffs: list[float]) -> tuple[list[float], list[float]]:
    """First order and total Sobol indices of an orthonormal expansion (Sudret 2008)."""
    d = len(index[0])
    _, var = mean_variance(coeffs)
    first = [0.0] * d
    total = [0.0] * d
    for a, c in zip(index, coeffs):
        active = [k for k in range(d) if a[k] > 0]
        if len(active) == 1:
            first[active[0]] += c * c
        for k in active:
            total[k] += c * c
    return [s / var for s in first], [s / var for s in total]


def ishigami(x: list[float], a: float = 7.0, b: float = 0.1) -> float:
    """The Ishigami function with inputs xi_k uniform on [-1, 1], mapped to pi xi_k."""
    x1, x2, x3 = (math.pi * v for v in x)
    return math.sin(x1) + a * math.sin(x2) ** 2 + b * x3**4 * math.sin(x1)
