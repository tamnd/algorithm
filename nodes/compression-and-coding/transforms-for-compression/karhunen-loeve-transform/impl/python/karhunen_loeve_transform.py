# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karhunen-loeve-transform/. The authors are listed in prov/PSR8K0.jsonl.

"""The Karhunen-Loeve transform (KLT) of blocks of real data, in pure Python.

The basis is the set of eigenvectors of the covariance matrix of the blocks.
The eigenvectors come from the classical Jacobi method: each step applies a
plane rotation that sets the largest off-diagonal entry to zero.
"""

import math
from typing import List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def mean_and_covariance(blocks: Sequence[Sequence[float]]) -> Tuple[Vector, Matrix]:
    """Return the sample mean and the covariance (1/M) sum (x - mu)(x - mu)^T.

    Precondition: at least one block, and all blocks have the same length n.
    Cost: Theta(M n^2) arithmetic operations for M blocks.
    """
    m = len(blocks)
    n = len(blocks[0])
    mu = [sum(b[i] for b in blocks) / m for i in range(n)]  # @line L1
    r = [[0.0] * n for _ in range(n)]
    for b in blocks:  # @line L2
        d = [b[i] - mu[i] for i in range(n)]
        for i in range(n):
            di = d[i]
            row = r[i]
            for j in range(n):
                row[j] += di * d[j]
    for i in range(n):
        for j in range(n):
            r[i][j] /= m
    return mu, r


def off_norm(a: Matrix) -> float:
    """Return the Frobenius norm of the off-diagonal part of a square matrix."""
    n = len(a)
    return math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))


def jacobi_eigen(r: Matrix, tol: float = 1e-13) -> Tuple[Vector, Matrix]:
    """Eigenvalues and eigenvectors of a real symmetric matrix by classical Jacobi.

    Returns (lam, v): lam[k] is an eigenvalue and column k of v is a unit
    eigenvector, so that r = v diag(lam) v^T. The order is not sorted.
    Precondition: r is square and symmetric. The input is not changed.
    Cost: each rotation is Theta(n) work for the update and Theta(n^2) for the
    search of the pivot. The off-diagonal mass drops by the factor
    1 - 2 / (n (n - 1)) or more at each rotation.
    """
    n = len(r)
    a = [list(map(float, row)) for row in r]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]  # @line L3
    scale = math.sqrt(sum(x * x for row in a for x in row))
    if n < 2 or scale == 0.0:
        return [a[i][i] for i in range(n)], v
    limit = tol * scale
    while off_norm(a) > limit:  # @line L4
        p, q, best = 0, 1, -1.0
        for i in range(n):  # @line L5
            for j in range(i + 1, n):
                if abs(a[i][j]) > best:
                    best, p, q = abs(a[i][j]), i, j
        apq = a[p][q]
        if apq == 0.0:
            break
        theta = (a[q][q] - a[p][p]) / (2.0 * apq)  # @line L6
        sgn = 1.0 if theta >= 0.0 else -1.0
        t = sgn / (abs(theta) + math.sqrt(theta * theta + 1.0))  # @line L7
        c = 1.0 / math.sqrt(t * t + 1.0)
        s = t * c
        # A <- J^T A J, where J is the identity except J[p][p] = J[q][q] = c,
        # J[p][q] = s and J[q][p] = -s.
        for k in range(n):  # @line L8
            akp, akq = a[k][p], a[k][q]
            a[k][p] = c * akp - s * akq
            a[k][q] = s * akp + c * akq
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k] = c * apk - s * aqk
            a[q][k] = s * apk + c * aqk
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            vkp, vkq = v[k][p], v[k][q]
            v[k][p] = c * vkp - s * vkq
            v[k][q] = s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


def klt_from_covariance(r: Matrix) -> Tuple[Vector, Matrix]:
    """Return (lam, t): eigenvalues in decreasing order and the KLT matrix t.

    Row k of t is a unit eigenvector of r for lam[k], so t r t^T = diag(lam).
    The sign of each row is fixed so that its entry of largest magnitude is
    positive (the first such entry on a tie), which makes the output unique
    when the eigenvalues are distinct.
    """
    lam, v = jacobi_eigen(r)
    n = len(r)
    order = sorted(range(n), key=lambda k: -lam[k])  # @line L9
    t = []
    for k in order:
        row = [v[i][k] for i in range(n)]
        big = max(range(n), key=lambda i: (abs(row[i]), -i))
        if row[big] < 0:
            row = [-x for x in row]
        t.append(row)
    return [lam[k] for k in order], t  # @line L10


def karhunen_loeve_transform(blocks: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector, Vector]:
    """Fit the KLT to data blocks. Return (t, mu, lam).

    t is the n x n orthogonal KLT matrix (rows are eigenvectors of the sample
    covariance, by decreasing eigenvalue), mu the sample mean and lam the
    eigenvalues, which are the variances of the transform coefficients.
    Cost: Theta(M n^2) for the covariance plus the Jacobi rotations.
    """
    mu, r = mean_and_covariance(blocks)
    lam, t = klt_from_covariance(r)
    return t, mu, lam


def klt_forward(t: Matrix, mu: Sequence[float], x: Sequence[float]) -> Vector:
    """Coefficients y = t (x - mu). Cost Theta(n^2)."""
    d = [x[i] - mu[i] for i in range(len(x))]
    return [sum(row[i] * d[i] for i in range(len(d))) for row in t]  # @line L11


def klt_inverse(t: Matrix, mu: Sequence[float], y: Sequence[float]) -> Vector:
    """Block x = t^T y + mu. Cost Theta(n^2)."""
    n = len(mu)
    return [sum(t[k][i] * y[k] for k in range(len(y))) + mu[i] for i in range(n)]  # @line L12
