# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial-chaos/. The authors are listed in prov/NEQJ8H.jsonl.
"""Sparse polynomial chaos by l1 minimization (compressive sampling).

The input xi = (xi_1..xi_d) has independent components, each "uniform" on
[-1, 1] (orthonormal Legendre basis) or "normal" (orthonormal Hermite basis).
The code draws N random inputs, possibly fewer than the number of terms P,
and solves the LASSO form of basis pursuit denoising

    min_c  (1/2) ||A c - y||^2 + lam ||c||_1,   A[i][a] = Psi_a(x_i) / sqrt(N),
    y_i = q(x_i) / sqrt(N),

by ISTA (proximal gradient with the constant step 1/L, L = ||A||_2^2).
It then refits the coefficients on the support that ISTA found by least
squares, which removes the shrinkage bias of the l1 penalty.
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


def apply(rows: list[list[float]], c: list[float]) -> list[float]:
    """A c."""
    return [sum(a * b for a, b in zip(r, c)) for r in rows]


def apply_t(rows: list[list[float]], v: list[float]) -> list[float]:
    """A^T v."""
    out = [0.0] * len(rows[0])
    for r, vi in zip(rows, v):
        if vi != 0.0:
            for j, a in enumerate(r):
                out[j] += a * vi
    return out


def lipschitz(rows: list[list[float]], iters: int = 200) -> float:
    """An upper bound on ||A||_2^2: power iteration on A^T A, enlarged by 1 percent."""
    v = [1.0] * len(rows[0])
    lam = 0.0
    for _ in range(iters):
        w = apply_t(rows, apply(rows, v))
        lam = math.sqrt(sum(t * t for t in w))
        if lam == 0.0:
            return 1.0
        v = [t / lam for t in w]
    return 1.01 * lam


def soft(t: float, tau: float) -> float:
    """The soft thresholding S_tau(t) = sign(t) max(|t| - tau, 0), the prox of tau |.|."""
    if t > tau:
        return t - tau
    if t < -tau:
        return t + tau
    return 0.0


def objective(rows: list[list[float]], y: list[float], c: list[float], lam: float) -> float:
    """(1/2) ||A c - y||^2 + lam ||c||_1."""
    r = [a - b for a, b in zip(apply(rows, c), y)]
    return 0.5 * sum(t * t for t in r) + lam * sum(abs(t) for t in c)


def ista(rows: list[list[float]], y: list[float], lam: float, iters: int, lip: float | None = None) -> list[float]:
    """ISTA with the constant step 1/L from c = 0."""
    lip = lipschitz(rows) if lip is None else lip  # @line L3
    c = [0.0] * len(rows[0])
    for _ in range(iters):  # @line L4
        g = apply_t(rows, [a - b for a, b in zip(apply(rows, c), y)])
        c = [soft(cj - gj / lip, lam / lip) for cj, gj in zip(c, g)]
    return c


def debias(rows: list[list[float]], y: list[float], support: list[int]) -> list[float]:
    """Least-squares refit on the given support; the other coefficients are 0."""
    c = [0.0] * len(rows[0])
    if not support:
        return c
    sub = [[r[j] for j in support] for r in rows]
    g = [[sum(r[i] * r[j] for r in sub) for j in range(len(support))] for i in range(len(support))]
    rhs = [sum(r[i] * yi for r, yi in zip(sub, y)) for i in range(len(support))]
    for j, v in zip(support, cholesky_solve(cholesky(g), rhs)):
        c[j] = v
    return c


def sparse_pce(q: Model, families: list[str], p: int, n: int, lam_ratio: float, iters: int, rng: random.Random):
    """Sparse PCE of total degree p from n runs; lam = lam_ratio * ||A^T y||_inf. Returns (index, coeffs, support)."""
    index = total_degree_set(len(families), p)  # @line L1
    xs = [sample(families, rng) for _ in range(n)]
    s = 1.0 / math.sqrt(n)
    y = [s * q(x) for x in xs]  # @line L2
    rows = [[s * v for v in design_row(index, families, x)] for x in xs]
    lam = lam_ratio * max(abs(t) for t in apply_t(rows, y))
    c = ista(rows, y, lam, iters)
    support = [j for j, v in enumerate(c) if v != 0.0]  # @line L5
    if len(support) < n:
        c = debias(rows, y, support)  # @line L6
    return index, c, support  # @line L7


def mean_variance(coeffs: list[float]) -> tuple[float, float]:
    """Mean c_0 and variance sum_{a != 0} c_a^2 of an orthonormal expansion."""
    return coeffs[0], sum(c * c for c in coeffs[1:])


def ishigami(x: list[float], a: float = 7.0, b: float = 0.1) -> float:
    """The Ishigami function with inputs xi_k uniform on [-1, 1], mapped to pi xi_k."""
    x1, x2, x3 = (math.pi * v for v in x)
    return math.sin(x1) + a * math.sin(x2) ** 2 + b * x3**4 * math.sin(x1)
