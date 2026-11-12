# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locality-preserving-projections/. The authors are listed in prov/3ZFNH0.jsonl.

"""Locality preserving projections (He and Niyogi, 2003).

Build a neighbor graph with heat kernel weights (or unit weights when t is None),
form L = D - W, and solve the generalized problem

    X^T L X a = lambda X^T D X a

for the m smallest eigenvalues. The rows of X are the points, so this is the
equation X L X^T a = lambda X D X^T a of the paper, where the points are columns.
A point x maps to (a_1 . x, ..., a_m . x).

The generalized problem is solved with a Cholesky factor Q = R R^T of
Q = X^T D X: if (R^-1 P R^-T) z = lambda z, then a = R^-T z solves P a = lambda Q a,
and a^T Q a = z^T z.
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


def heat_kernel_graph(points, k=None, eps=None, t=None):
    """Symmetric weight matrix. Join i and j if either is a k-nearest neighbor of the
    other (or if their distance is at most eps). Weight exp(-|xi - xj|^2 / t), or 1 if t is None."""
    n = len(points)
    w = [[0.0] * n for _ in range(n)]
    for i in range(n):
        dist = sorted((math.dist(points[i], points[j]), j) for j in range(n) if j != i)
        chosen = dist[:k] if k is not None else [(d, j) for d, j in dist if d <= eps]  # @line L1
        for d, j in chosen:
            val = 1.0 if t is None else math.exp(-d * d / t)  # @line L2
            w[i][j] = w[j][i] = val
    return w


def cholesky(q):
    """Lower triangular R with q = R R^T. Raise ValueError if q is not positive definite."""
    p = len(q)
    scale = max(abs(q[i][i]) for i in range(p)) or 1.0
    r = [[0.0] * p for _ in range(p)]
    for i in range(p):
        for j in range(i + 1):
            s = q[i][j] - sum(r[i][l] * r[j][l] for l in range(j))
            if i == j:
                if s <= 1e-12 * scale:
                    raise ValueError("X^T D X is singular: reduce the dimension first, for example with PCA")
                r[i][i] = math.sqrt(s)
            else:
                r[i][j] = s / r[j][j]
    return r


def solve_lower(r, b):
    """Solve R x = b for lower triangular R."""
    x = []
    for i in range(len(b)):
        x.append((b[i] - sum(r[i][l] * x[l] for l in range(i))) / r[i][i])
    return x


def solve_lower_transposed(r, b):
    """Solve R^T x = b for lower triangular R."""
    p = len(b)
    x = [0.0] * p
    for i in range(p - 1, -1, -1):
        x[i] = (b[i] - sum(r[l][i] * x[l] for l in range(i + 1, p))) / r[i][i]
    return x


def lpp_from_weights(x, w, m):
    """Return (A, eigenvalues). A is a list of m vectors a_0..a_{m-1} in R^p, the solutions of
    X^T L X a = lambda X^T D X a for the m smallest eigenvalues, with a^T X^T D X a = 1."""
    n, p = len(x), len(x[0])
    deg = [sum(row) for row in w]  # @line L3
    lx = [[deg[i] * x[i][b] - sum(w[i][j] * x[j][b] for j in range(n)) for b in range(p)] for i in range(n)]
    pm = [[sum(x[i][a] * lx[i][b] for i in range(n)) for b in range(p)] for a in range(p)]  # @line L4
    qm = [[sum(deg[i] * x[i][a] * x[i][b] for i in range(n)) for b in range(p)] for a in range(p)]
    r = cholesky(qm)
    s = [solve_lower(r, [pm[a][b] for a in range(p)]) for b in range(p)]  # column b of R^-1 P
    # R^-1 P R^-T = R^-1 (R^-1 P)^T because P is symmetric; its column c is R^-1 times row c of R^-1 P.
    mt = [solve_lower(r, [s[b][c] for b in range(p)]) for c in range(p)]
    sym = [[0.5 * (mt[c][a] + mt[a][c]) for c in range(p)] for a in range(p)]
    lam, vecs = jacobi_eigh(sym)  # @line L5
    a_vectors = [solve_lower_transposed(r, vecs[l]) for l in range(m)]  # @line L6
    return a_vectors, lam[:m]  # @line L7


def project(a_vectors, points):
    """Map each point x to (a_0 . x, ..., a_{m-1} . x). Works for new points too."""
    return [tuple(sum(ai * xi for ai, xi in zip(a, pt)) for a in a_vectors) for pt in points]


def locality_preserving_projections(points, m, k=None, eps=None, t=None):
    """Return (A, Y, eigenvalues) with Y the projections of the input points."""
    w = heat_kernel_graph(points, k, eps, t)
    a_vectors, lam = lpp_from_weights(points, w, m)
    return a_vectors, project(a_vectors, points), lam
