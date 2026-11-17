# SPDX-License-Identifier: MIT
# Group module of the single-cell pages of https://algorithm.tamnd.com/ (group rq3). The authors are listed in prov/.
"""Small dense linear algebra and neighbor search for the single-cell pages.

The reference copy is in biology/transcriptomics/doublet-detection/impl/python/.
The other rq3 pages hold identical copies. The module holds no algorithm of a
page: no doublet score, no clustering, no batch correction and no pseudotime.

Conventions:
- A vector is a list of floats and a matrix is a list of rows.
- Ties between equal distances are broken by the smaller index, so that every
  result is deterministic.
- Random draws use a random.Random object that the caller passes in.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def sqdist(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def transpose(A: Sequence[Sequence[float]]) -> Matrix:
    return [list(col) for col in zip(*A)]


def matmul(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]]) -> Matrix:
    Bt = transpose(B)
    return [[dot(row, col) for col in Bt] for row in A]


def matvec(A: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    return [dot(row, x) for row in A]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def column_means(X: Sequence[Sequence[float]]) -> Vector:
    n = len(X)
    return [sum(col) / n for col in zip(*X)]


def knn(points: Sequence[Sequence[float]], k: int,
        queries: Optional[Sequence[Sequence[float]]] = None) -> List[List[int]]:
    """The k nearest points (Euclidean) of each query, by brute force.

    With queries=None the queries are the points themselves and each point is
    left out of its own list. Each list is sorted by (distance, index).
    """
    self_query = queries is None
    qs = points if self_query else queries
    limit = len(points) - (1 if self_query else 0)
    if not 0 <= k <= limit:
        raise ValueError("k must be between 0 and the number of candidate points")
    out = []
    for i, q in enumerate(qs):
        cand = [(sqdist(q, p), j) for j, p in enumerate(points) if not (self_query and j == i)]
        cand.sort()
        out.append([j for _, j in cand[:k]])
    return out


def solve(A: Sequence[Sequence[float]], b: Sequence[float]) -> Vector:
    """Solve A x = b by Gaussian elimination with partial pivoting.

    Raises ValueError when a pivot is zero, that is when A is singular in
    floating point.
    """
    n = len(A)
    M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0.0:
            raise ValueError("singular matrix")
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / piv
            if f != 0.0:
                row, top = M[r], M[c]
                for j in range(c, n + 1):
                    row[j] -= f * top[j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / M[i][i]
    return x


def inverse(A: Sequence[Sequence[float]]) -> Matrix:
    """The inverse of A, one column at a time with solve."""
    n = len(A)
    cols = [solve(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return transpose(cols)


def jacobi_eigh(S: Sequence[Sequence[float]], tol: float = 1e-12,
                max_sweeps: int = 100) -> Tuple[Vector, Matrix]:
    """All eigenvalues and eigenvectors of a symmetric matrix by the cyclic Jacobi method.

    Returns (values, vectors): values in decreasing order, and vectors[i] the
    unit eigenvector of values[i]. Each eigenvector is given the sign that
    makes its entry of largest absolute value positive.
    """
    n = len(S)
    A = [list(map(float, row)) for row in S]
    V = identity(n)
    for _ in range(max_sweeps):
        off = sum(A[i][j] * A[i][j] for i in range(n) for j in range(n) if i != j)
        scale = sum(A[i][i] * A[i][i] for i in range(n)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = A[p][q]
                if apq == 0.0:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * apq)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: -A[i][i])
    values = [A[i][i] for i in order]
    vectors = []
    for i in order:
        v = [V[k][i] for k in range(n)]
        big = max(range(n), key=lambda k: abs(v[k]))
        if v[big] < 0:
            v = [-x for x in v]
        vectors.append(v)
    return values, vectors


def pca_fit(X: Sequence[Sequence[float]], r: int) -> Tuple[Vector, Matrix, Vector]:
    """Principal axes of the rows of X: (means, axes, variances), r axes of unit length.

    The covariance uses the divisor n - 1. The axes come from jacobi_eigh, so they
    are deterministic up to the sign rule of that function.
    """
    n, d = len(X), len(X[0])
    if not 1 <= r <= d:
        raise ValueError("r must be between 1 and the number of columns")
    mu = column_means(X)
    C = [[0.0] * d for _ in range(d)]
    for row in X:
        z = [x - m for x, m in zip(row, mu)]
        for a in range(d):
            za = z[a]
            if za != 0.0:
                Ca = C[a]
                for b in range(a, d):
                    Ca[b] += za * z[b]
    for a in range(d):
        for b in range(a, d):
            C[a][b] /= max(n - 1, 1)
            C[b][a] = C[a][b]
    values, vectors = jacobi_eigh(C)
    return mu, vectors[:r], values[:r]


def pca_project(X: Sequence[Sequence[float]], mu: Sequence[float], axes: Sequence[Sequence[float]]) -> Matrix:
    """The coordinates of the rows of X on the axes, after subtracting mu."""
    return [[dot([x - m for x, m in zip(row, mu)], a) for a in axes] for row in X]


def poisson_knuth(rng: random.Random, lam: float) -> int:
    """A Poisson draw by multiplying uniforms (Knuth); for test data with lam up to about 50.

    Draw order: rng.random() until the product falls below exp(-lam).
    """
    if lam < 0:
        raise ValueError("lam must be non-negative")
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1
