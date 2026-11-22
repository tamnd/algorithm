# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-signatures-defense/. The authors are listed in prov/DEFG9T.jsonl.

"""The spectral signatures filter of Tran, Li and Madry (2018), on feature vectors of one label.

The tests build the feature vectors from a fixed seed (Gaussian clean points and a shifted
Gaussian for the poisoned ones); nothing here reads a real data set or a real model.
"""

import math
from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]


def covariance_sum(rows: Sequence[Sequence[float]], mu: Sequence[float]) -> Matrix:
    """The d by d matrix M^T M, where the rows of M are the centered rows r - mu. Cost O(n d^2)."""
    d = len(mu)
    c = [[0.0] * d for _ in range(d)]
    for r in rows:
        z = [a - m for a, m in zip(r, mu, strict=True)]
        for p in range(d):
            for q in range(d):
                c[p][q] += z[p] * z[q]
    return c


def _power(c: Matrix, v: Vector, iters: int, tol: float) -> Vector:
    """Power iteration on c from the unit vector v. Cost O(iters d^2)."""
    for _ in range(iters):
        w = [sum(a * b for a, b in zip(row, v)) for row in c]
        norm = math.sqrt(sum(a * a for a in w))
        if norm == 0.0:
            return v
        w = [a / norm for a in w]
        if sum((a - b) * (a - b) for a, b in zip(w, v)) < tol * tol:
            return w
        v = w
    return v


def top_eigenvector(c: Matrix, iters: int = 5000, tol: float = 1e-15, squarings: int = 8) -> Vector:
    """A unit eigenvector of the largest eigenvalue of a symmetric positive semidefinite matrix, by power iteration.

    First p = c^(2^squarings), scaled, by repeated squaring, so that each column of p is
    a start that has already had 2^squarings power steps. One column of p may be
    orthogonal to the top eigenvector, but not all of them, since the columns span the
    range of p. So the iteration runs from each nonzero column, and the result with the
    largest Rayleigh quotient on c is kept. Precondition: the largest eigenvalue is simple,
    or the answer is any unit vector of its eigenspace. Cost O(squarings d^3 + iters d^3).
    """
    d = len(c)
    p = [row[:] for row in c]
    for _ in range(squarings):
        q = [[sum(p[i][k] * p[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
        f = math.sqrt(sum(x * x for row in q for x in row))
        if f == 0.0:
            break
        p = [[x / f for x in row] for row in q]
    best: Vector = [1.0] + [0.0] * (d - 1)
    best_q = -1.0
    for start in range(d):
        v = [p[i][start] for i in range(d)]
        norm = math.sqrt(math.fsum(a * a for a in v))
        if norm == 0.0:
            continue
        v = _power(c, [a / norm for a in v], iters, tol)
        q = math.fsum(v[i] * c[i][j] * v[j] for i in range(d) for j in range(d))
        if q > best_q:
            best, best_q = v, q
    return best


def spectral_scores(rows: Sequence[Sequence[float]]) -> list[float]:
    """The score tau_i = ((R_i - mu) . v)^2 of each row, for the top right singular vector v of the centered rows.

    Precondition: n >= 1 rows of the same length d. Cost O(n d^2 + iters d^3).
    """
    n, d = len(rows), len(rows[0])
    mu = [math.fsum(r[j] for r in rows) / n for j in range(d)]  # @line L1
    c = covariance_sum(rows, mu)  # @line L2
    v = top_eigenvector(c)  # @line L3
    return [math.fsum((r[j] - mu[j]) * v[j] for j in range(d)) ** 2 for r in rows]  # @line L4


def spectral_filter(rows: Sequence[Sequence[float]], epsilon: float, factor: float = 1.5) -> tuple[list[int], list[int]]:
    """Split the indices of the rows into (kept, removed), removing the floor(factor epsilon n) largest scores.

    epsilon is the assumed upper bound on the poisoned fraction, and factor = 1.5 is the
    value of Tran et al., a tuned choice. Ties in the score go to the larger index first,
    so the order is fixed. Precondition: n >= 1 and epsilon >= 0. Cost O(n d^2 + iters d^3 + n log n).
    """
    n = len(rows)
    tau = spectral_scores(rows)
    k = min(n, math.floor(factor * epsilon * n + 1e-9))
    order = sorted(range(n), key=lambda i: (tau[i], i), reverse=True)  # @line L5
    removed = sorted(order[:k])
    kept = sorted(order[k:])
    return kept, removed  # @line L6
