# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-tangent-space-alignment/. The authors are listed in prov/8CGP5G.jsonl.

"""Local tangent space alignment (Zhang and Zha, 2004).

For each point, take the neighborhood made of the point and its k nearest neighbors,
find the m top left singular vectors of the centered neighborhood (local PCA), and form
G_i = [1/sqrt(s), U_i] with s = k + 1. The alignment matrix B = sum_i S_i W_i S_i^T with
W_i = I - G_i G_i^T measures how far the global coordinates are from an affine image of
the local tangent coordinates. The embedding is the eigenvectors of B for the 2nd to the
(m+1)-st smallest eigenvalues, with orthonormal rows T T^T = I as in the paper.
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


def alignment_matrix(points, k, m):
    n, dim = len(points), len(points[0])
    b = [[0.0] * n for _ in range(n)]
    for nb in neighborhoods(points, k):  # @line L1
        s = len(nb)
        mean = [sum(points[j][c] for j in nb) / s for c in range(dim)]
        z = [[points[j][c] - mean[c] for c in range(dim)] for j in nb]  # @line L2
        gram = [[sum(x * y for x, y in zip(z[p], z[q])) for q in range(s)] for p in range(s)]
        _, vecs = jacobi_eigh(gram)
        g = [[1.0 / math.sqrt(s)] + [vecs[s - 1 - l][p] for l in range(m)] for p in range(s)]  # @line L3
        for p in range(s):
            for q in range(s):
                w = (1.0 if p == q else 0.0) - sum(x * y for x, y in zip(g[p], g[q]))  # @line L4
                b[nb[p]][nb[q]] += w  # @line L5
    return b


def ltsa(points, k, m):
    """Return (Y, eigenvalues of B on the vectors orthogonal to the constant, ascending).

    The columns of Y are orthonormal and orthogonal to the constant vector. The constant
    is an exact eigenvector of B with eigenvalue 0; adding c (1 1^T) / n with c above all
    eigenvalues moves it to the top, so that it is discarded even when the null space
    of B has a dimension above 1.
    """
    n = len(points)
    if k < m:
        raise ValueError("k must be at least m")
    b = alignment_matrix(points, k, m)
    c = sum(b[i][i] for i in range(n)) + 1.0
    shifted = [[b[i][j] + c / n for j in range(n)] for i in range(n)]
    lam, vecs = jacobi_eigh(shifted)  # @line L6
    y = [tuple(vecs[l][i] for l in range(m)) for i in range(n)]  # @line L7
    return y, lam[:-1]  # @line L8
