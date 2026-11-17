# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genetic-principal-components/. The authors are listed in prov/HDK5SD.jsonl.
"""Principal components of a genotype matrix, as in smartpca (Patterson,
Price and Reich 2006) and EIGENSTRAT (Price and coauthors 2006).

Input: a genotype matrix G with n rows (individuals) and m columns (sites).
G[i][j] in {0, 1, 2} is the number of copies of allele 1.

Steps:
1. For each site j, mu_j = the mean of column j and p_j = mu_j / 2. Drop
   the sites with p_j = 0 or 1. Set M[i][j] = (G[i][j] - mu_j) / sqrt(p_j (1 - p_j)).
2. X = M M^T / m', with m' the number of kept sites (an n by n matrix).
3. The top k eigenvectors of X, by orthogonal (subspace) iteration from a
   random start. Their entries are the coordinates of the individuals.

EIGENSTRAT: regress the top k axes out of each genotype column and out of
the phenotype, and use (n - k - 1) r^2 as an approximate chi-square
statistic with 1 degree of freedom, where r is the correlation of the two
residual vectors.

A dense symmetric Jacobi eigenvalue method is included as an independent
reference for the tests.
"""

from __future__ import annotations

import math
import random

Matrix = list[list[float]]


def normalize(g: list[list[int]]) -> tuple[Matrix, list[int]]:
    """Center each site and divide by sqrt(p (1 - p)). Return M and the kept site indices."""
    n = len(g)
    m = len(g[0]) if n else 0
    kept = []
    cols = []
    for j in range(m):  # @line L1
        mu = sum(row[j] for row in g) / n
        p = mu / 2.0
        if p <= 0.0 or p >= 1.0:
            continue  # @line L2
        s = math.sqrt(p * (1.0 - p))
        cols.append([(row[j] - mu) / s for row in g])  # @line L3
        kept.append(j)
    mat = [[cols[c][i] for c in range(len(cols))] for i in range(n)]
    return mat, kept


def covariance(mat: Matrix) -> Matrix:
    """X = M M^T / m for an n by m matrix M."""
    n = len(mat)
    m = len(mat[0]) if n else 0
    if m == 0:
        raise ValueError("no polymorphic site")
    x = [[0.0] * n for _ in range(n)]
    for a in range(n):  # @line L4
        ra = mat[a]
        for b in range(a, n):
            rb = mat[b]
            v = sum(u * w for u, w in zip(ra, rb)) / m
            x[a][b] = v
            x[b][a] = v
    return x


def _matvec(x: Matrix, v: list[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, v)) for row in x]


def _dot(u: list[float], v: list[float]) -> float:
    return sum(a * b for a, b in zip(u, v))


def _orthonormalize(vs: list[list[float]]) -> list[list[float]]:
    """Modified Gram-Schmidt. A vector that is dependent on the earlier ones is replaced by 0."""
    out: list[list[float]] = []
    for v in vs:
        w = list(v)
        for q in out:
            c = _dot(q, w)
            w = [a - c * b for a, b in zip(w, q)]
        norm = math.sqrt(_dot(w, w))
        out.append([a / norm for a in w] if norm > 1e-300 else [0.0] * len(w))
    return out


def top_eigenvectors(x: Matrix, k: int, rng: random.Random, max_iter: int = 5000,
                     tol: float = 1e-12) -> tuple[list[float], list[list[float]]]:
    """The k largest eigenvalues of a symmetric positive semidefinite matrix
    and their unit eigenvectors, by orthogonal iteration.

    The start vectors have entries rng.gauss(0, 1), drawn vector by vector
    and entry by entry. The sign of each vector is fixed so that its entry
    of largest absolute value is positive.
    """
    n = len(x)
    if not 1 <= k <= n:
        raise ValueError("need 1 <= k <= n")
    q = _orthonormalize([[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(k)])  # @line L5
    lam = [0.0] * k
    for _ in range(max_iter):  # @line L6
        z = [_matvec(x, v) for v in q]  # @line L7
        new_lam = [_dot(v, w) for v, w in zip(q, z)]  # @line L8
        q_new = _orthonormalize(z)  # @line L9
        change = max(abs(a - b) for a, b in zip(new_lam, lam))
        lam = new_lam
        q = q_new
        if change <= tol * max(1.0, abs(lam[0])):  # @line L10
            break
    # Rayleigh-Ritz on the final subspace, so that the vectors are sorted
    # eigenvectors even when two eigenvalues are close.
    z = [_matvec(x, v) for v in q]
    small = [[_dot(q[a], z[b]) for b in range(k)] for a in range(k)]
    vals, vecs = jacobi_eigen(small)
    lam_out = []
    q_out = []
    for c in range(k):
        y = [sum(vecs[r][c] * q[r][i] for r in range(k)) for i in range(n)]
        big = max(range(n), key=lambda i: abs(y[i]))
        if y[big] < 0:
            y = [-a for a in y]
        lam_out.append(vals[c])
        q_out.append(y)
    return lam_out, q_out  # @line L11


def jacobi_eigen(a: Matrix, tol: float = 1e-14, max_sweeps: int = 100) -> tuple[list[float], Matrix]:
    """All eigenvalues (in decreasing order) and eigenvectors (as columns) of a
    symmetric matrix, by the cyclic Jacobi rotation method."""
    n = len(a)
    s = [list(row) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(s[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        scale = sum(s[i][i] ** 2 for i in range(n)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                if abs(s[p][r]) < 1e-300:
                    continue
                theta = (s[r][r] - s[p][p]) / (2.0 * s[p][r])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for i in range(n):
                    sip, sir = s[i][p], s[i][r]
                    s[i][p] = c * sip - sn * sir
                    s[i][r] = sn * sip + c * sir
                for i in range(n):
                    spi, sri = s[p][i], s[r][i]
                    s[p][i] = c * spi - sn * sri
                    s[r][i] = sn * spi + c * sri
                for i in range(n):
                    vip, vir = v[i][p], v[i][r]
                    v[i][p] = c * vip - sn * vir
                    v[i][r] = sn * vip + c * vir
    order = sorted(range(n), key=lambda i: -s[i][i])
    vals = [s[i][i] for i in order]
    vecs = [[v[r][i] for i in order] for r in range(n)]
    return vals, vecs


def principal_components(g: list[list[int]], k: int, rng: random.Random
                         ) -> tuple[list[float], list[list[float]], list[int]]:
    """The smartpca pipeline: normalize, form X, take the top k eigenpairs."""
    mat, kept = normalize(g)
    x = covariance(mat)
    vals, vecs = top_eigenvectors(x, k, rng)
    return vals, vecs, kept


def residualize(y: list[float], axes: list[list[float]]) -> list[float]:
    """Remove the mean and the projection on each axis (the axes are orthonormal
    and orthogonal to the all-ones vector)."""
    n = len(y)
    mean = sum(y) / n
    r = [a - mean for a in y]
    for q in axes:
        c = _dot(q, r)
        r = [a - c * b for a, b in zip(r, q)]
    return r


def eigenstrat_statistic(genotype: list[float], phenotype: list[float], axes: list[list[float]]) -> float:
    """(n - k - 1) r^2 for the residual genotype and phenotype after removing k axes."""
    n = len(genotype)
    k = len(axes)
    a = residualize(genotype, axes)
    b = residualize(phenotype, axes)
    saa, sbb, sab = _dot(a, a), _dot(b, b), _dot(a, b)
    if saa <= 0 or sbb <= 0:
        return 0.0
    r2 = sab * sab / (saa * sbb)
    return (n - k - 1) * r2
