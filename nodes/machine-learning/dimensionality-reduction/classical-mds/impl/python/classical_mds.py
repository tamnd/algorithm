# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/classical-mds/. The authors are listed in prov/H05ZK6.jsonl.

"""Classical (Torgerson-Gower) multidimensional scaling.

D is a symmetric n x n matrix of distances with a zero diagonal, given as a list of
rows. double_center and is_euclidean work with fractions.Fraction entries and are then
exact. The eigenvectors come from a cyclic Jacobi solver in floating point.
"""

import math


def double_center(d):
    """B = -1/2 J D^(2) J for a distance matrix D."""
    n = len(d)
    a = [[d[i][j] * d[i][j] for j in range(n)] for i in range(n)]  # @line L2
    return double_center_squared(a)


def double_center_squared(a):
    """B = -1/2 J A J for the matrix A of squared distances, as -1/2 (a_ij - r_i - r_j + g)."""
    n = len(a)
    r = [sum(a[i]) / n for i in range(n)]  # @line L3
    g = sum(r) / n
    return [[-(a[i][j] - r[i] - r[j] + g) / 2 for j in range(n)] for i in range(n)]  # @line L4


def is_psd(b):
    """Exact test that a symmetric matrix is positive semidefinite.

    Eliminate on a positive diagonal pivot (a Schur complement step). If no diagonal
    entry is positive, the matrix is PSD only if it is zero.
    """
    m = [list(row) for row in b]
    while m:
        k = len(m)
        p = next((i for i in range(k) if m[i][i] > 0), None)
        if p is None:
            return all(m[i][j] == 0 for i in range(k) for j in range(k))
        rest = [i for i in range(k) if i != p]
        m = [[m[i][j] - m[i][p] * m[p][j] / m[p][p] for j in rest] for i in rest]
    return True


def is_euclidean(d):
    """Schoenberg, Young and Householder: D is Euclidean iff B is PSD."""
    return is_psd(double_center(d))


def jacobi_eigh(a, max_sweeps=100):
    """Eigenvalues in descending order and the matching eigenvectors (as lists)."""
    n = len(a)
    a = [[float(x) for x in row] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = sum(x * x for row in a for x in row) or 1.0
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off <= 1e-26 * scale:
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
    order = sorted(range(n), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def classical_mds(d, k):
    """Return (X, eigenvalues): n points in R^k and all eigenvalues of B, descending.

    A negative eigenvalue among the top k means that no k-dimensional Euclidean
    configuration exists; the coordinate is then set to 0 for that axis.
    """
    n = len(d)  # @line L1
    b = double_center(d)
    lam, vecs = jacobi_eigh(b)  # @line L5
    cols = []
    for j in range(k):
        s = math.sqrt(lam[j]) if lam[j] > 0 else 0.0  # @line L6
        cols.append([s * x for x in vecs[j]])
    x = [tuple(cols[j][i] for j in range(k)) for i in range(n)]  # @line L7
    return x, lam  # @line L8


def distances(points):
    return [[math.dist(p, q) for q in points] for p in points]
