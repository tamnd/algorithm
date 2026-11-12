# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hessian-eigenmaps/. The authors are listed in prov/MMQJ8B.jsonl.

"""Hessian eigenmaps, or Hessian LLE (Donoho and Grimes, 2003).

For each point, take the neighborhood made of the point and its k nearest neighbors,
find m tangent coordinates by local PCA, and build a local Hessian estimator H_i
from the columns [1, U, U_a U_b] by Gram-Schmidt. The quadratic form
H = sum_i H_i^T H_i estimates the integral of the squared Hessian norm. Its null space
holds the constant and the m isometric coordinates.

The function returns an orthonormal basis of that null space, orthogonal to the
constant and scaled by sqrt(n). It does not apply the final normalization of the
paper, so the output equals the isometric coordinates up to an invertible linear map.
"""

import math


def jacobi_eigh(a, max_sweeps=100):
    """Eigenvalues in ascending order and the matching eigenvectors (as lists)."""
    n = len(a)
    a = [[float(x) for x in row] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = sum(x * x for row in a for x in row) or 1.0
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off <= 1e-28 * scale:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                th = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for row in a:
                    x, y = row[p], row[q]
                    row[p], row[q] = c * x - s * y, s * x + c * y
                a[p], a[q] = ([c * x - s * y for x, y in zip(a[p], a[q])],
                              [s * x + c * y for x, y in zip(a[p], a[q])])
                for row in v:
                    x, y = row[p], row[q]
                    row[p], row[q] = c * x - s * y, s * x + c * y
    order = sorted(range(n), key=lambda i: a[i][i])
    return [a[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def neighborhoods(points, k):
    """The point itself followed by its k nearest neighbors."""
    n = len(points)
    out = []
    for i in range(n):
        dist = sorted((math.dist(points[i], points[j]), j) for j in range(n) if j != i)
        out.append([i] + [j for _, j in dist[:k]])
    return out


def tangent_coordinates(points, nb, m):
    """Local PCA: the top m left singular vectors of the centered neighborhood (k+1 x m)."""
    size, dim = len(nb), len(points[0])
    mean = [sum(points[j][c] for j in nb) / size for c in range(dim)]
    z = [[points[j][c] - mean[c] for c in range(dim)] for j in nb]
    gram = [[sum(a * b for a, b in zip(z[s], z[t])) for t in range(size)] for s in range(size)]
    _, vecs = jacobi_eigh(gram)
    return [[vecs[size - 1 - l][s] for l in range(m)] for s in range(size)]


def gram_schmidt(cols):
    """Orthonormalize the columns in order (twice, for stability); drop dependent ones."""
    q = []
    for col in cols:
        v = list(col)
        for _ in range(2):
            for u in q:
                d = sum(a * b for a, b in zip(u, v))
                v = [a - d * b for a, b in zip(v, u)]
        nv = math.sqrt(sum(a * a for a in v))
        if nv > 1e-10:
            q.append([a / nv for a in v])
    return q


def hessian_matrix(points, k, m):
    n = len(points)
    h = [[0.0] * n for _ in range(n)]
    for nb in neighborhoods(points, k):  # @line L1
        size = len(nb)  # @line L2
        u = tangent_coordinates(points, nb, m)  # @line L3
        cols = [[1.0] * size] + [[u[s][a] for s in range(size)] for a in range(m)]  # @line L4
        cols += [[u[s][a] * u[s][b] for s in range(size)] for a in range(m) for b in range(a, m)]
        q = gram_schmidt(cols)  # @line L5
        if len(q) != len(cols):
            raise ValueError("degenerate neighborhood: increase k")
        hi = q[1 + m:]  # rows of H_i, one per pair a <= b
        for s in range(size):
            for t in range(size):
                h[nb[s]][nb[t]] += sum(row[s] * row[t] for row in hi)  # @line L6
    return h


def hessian_eigenmaps(points, k, m):
    """Return (Y, eigenvalues of H on the vectors orthogonal to the constant, ascending)."""
    n = len(points)
    if k + 1 < 1 + m + m * (m + 1) // 2:
        raise ValueError("k must be at least m + m(m+1)/2")
    h = hessian_matrix(points, k, m)
    c = sum(h[i][i] for i in range(n)) + 1.0
    shifted = [[h[i][j] + c / n for j in range(n)] for i in range(n)]
    lam, vecs = jacobi_eigh(shifted)  # @line L7
    s = math.sqrt(n)
    y = [tuple(s * vecs[l][i] for l in range(m)) for i in range(n)]  # @line L8
    return y, lam[:-1]  # @line L9
