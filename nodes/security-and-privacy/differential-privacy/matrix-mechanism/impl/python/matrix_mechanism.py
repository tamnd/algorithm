# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-mechanism/. The authors are listed in prov/73DA32.jsonl.
"""The matrix mechanism for a workload of linear counting queries
(Li, Hay, Rastogi, Miklau and McGregor 2010), with Laplace noise.

The data is a histogram x in N^n (one count per cell). The workload is an
m x n matrix W; the true answers are W x. The analyst picks a strategy, a
p x n matrix A of full column rank. The mechanism answers A x with Laplace
noise, finds the least squares estimate of x, and outputs W times it.

Neighbors are add/remove: x' = x + e_j or x - e_j for one cell j. Then the
l1 sensitivity of x -> A x is the largest l1 norm of a column of A.

The linear algebra works over any field type: pass Fraction entries for
exact results, or floats. The code uses random.Random so that the tests can
be repeated, and float noise. A real release needs a cryptographic source
of randomness and an exact sampler (Mironov 2012; Canonne, Kamath and
Steinke 2020).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Sequence

Matrix = list[list]


def laplace_noise(b: float, rng: random.Random) -> float:
    """One draw of Lap(b), the density (1/(2b)) exp(-|z|/b), by the inverse CDF.

    Precondition: b > 0. Cost: one uniform draw and O(1) time.
    """
    u = rng.random() - 0.5
    while u == -0.5:
        u = rng.random() - 0.5
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def transpose(A: Sequence[Sequence]) -> Matrix:
    """The transpose of A. Cost: O(pn)."""
    return [list(col) for col in zip(*A)]


def matmul(A: Sequence[Sequence], B: Sequence[Sequence]) -> Matrix:
    """The product A B. Precondition: the inner sizes agree. Cost: O(m k n)."""
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def matvec(A: Sequence[Sequence], x: Sequence) -> list:
    """The product A x. Cost: O(p n)."""
    return [sum(a * v for a, v in zip(row, x)) for row in A]


def inverse(M: Sequence[Sequence]) -> Matrix:
    """The inverse of a square matrix by Gauss-Jordan elimination with partial pivoting.

    Raises ValueError if M is singular (exactly for Fraction entries, to a
    tolerance of 1e-12 times the largest entry for floats). Cost: O(n^3).
    """
    n = len(M)
    exact = not any(isinstance(v, float) for row in M for v in row)
    one, zero = (Fraction(1), Fraction(0)) if exact else (1.0, 0.0)
    aug = [
        [Fraction(v) if exact else v for v in row] + [one if i == j else zero for j in range(n)]
        for i, row in enumerate(M)
    ]
    scale = max((abs(v) for row in M for v in row), default=0)
    tol = 0 if exact else 1e-12 * scale
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aug[r][c]))
        if abs(aug[p][c]) <= tol:
            raise ValueError("matrix is singular")
        aug[c], aug[p] = aug[p], aug[c]
        piv = aug[c][c]
        aug[c] = [v / piv for v in aug[c]]
        for r in range(n):
            if r != c and aug[r][c] != 0:
                f = aug[r][c]
                aug[r] = [a - f * b for a, b in zip(aug[r], aug[c])]
    return [row[n:] for row in aug]


def pseudoinverse(A: Sequence[Sequence]) -> Matrix:
    """The left inverse A^+ = (A^T A)^(-1) A^T of a matrix of full column rank.

    A^+ y is the least squares solution of A x = y. Raises ValueError if A
    does not have full column rank. Cost: O(p n^2 + n^3).
    """
    At = transpose(A)
    return matmul(inverse(matmul(At, A)), At)


def sensitivity(A: Sequence[Sequence]) -> float:
    """The l1 sensitivity of x -> A x under add/remove: the largest column l1 norm. Cost: O(p n)."""
    return max(sum(abs(v) for v in col) for col in zip(*A))


def matrix_mechanism(
    W: Sequence[Sequence],
    A: Sequence[Sequence],
    x: Sequence[int],
    epsilon: float,
    rng: random.Random,
) -> list[float]:
    """Answer the workload W on the histogram x through the strategy A, with epsilon-DP.

    Precondition: epsilon > 0, A has full column rank, and W and A have
    len(x) columns. Cost: O(p n^2 + n^3 + m n) arithmetic and p Laplace draws.
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    delta_a = sensitivity(A)  # @line L1
    b = delta_a / epsilon
    y = [v + laplace_noise(b, rng) for v in matvec(A, x)]  # @line L2
    A_plus = pseudoinverse([[float(v) for v in row] for row in A])  # @line L3
    x_hat = matvec(A_plus, y)  # @line L4
    return matvec(W, x_hat)  # @line L5


def total_squared_error(W: Sequence[Sequence], A: Sequence[Sequence], epsilon: float):
    """The expected total squared error 2 (Delta_A / epsilon)^2 trace(W (A^T A)^(-1) W^T).

    Exact if the entries are Fraction and epsilon is 1. Cost: O(p n^2 + n^3 + m n^2).
    """
    At = transpose(A)
    G = inverse(matmul(At, A))
    WG = matmul(W, G)
    tr = sum(sum(a * b for a, b in zip(WG[i], W[i])) for i in range(len(W)))
    d = sensitivity(A)
    return 2 * d * d * tr / (epsilon * epsilon)


def identity(n: int) -> Matrix:
    """The n x n identity strategy: one noisy count per cell."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def all_range_queries(n: int) -> Matrix:
    """The workload of all n(n+1)/2 range queries x[i] + ... + x[j] over n cells."""
    return [[1 if i <= k <= j else 0 for k in range(n)] for i in range(n) for j in range(i, n)]


def hierarchical_strategy(n: int) -> Matrix:
    """The binary hierarchical strategy: the sum over each dyadic block of cells.

    Precondition: n is a power of two. It has 2n - 1 rows and each cell lies
    in log2(n) + 1 of them, so its sensitivity is log2(n) + 1.
    """
    if n < 1 or n & (n - 1):
        raise ValueError("n must be a power of two")
    rows = []
    size = 1
    while size <= n:
        for start in range(0, n, size):
            rows.append([1 if start <= k < start + size else 0 for k in range(n)])
        size *= 2
    return rows
