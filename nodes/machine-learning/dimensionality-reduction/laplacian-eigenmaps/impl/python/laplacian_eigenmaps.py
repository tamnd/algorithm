# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-eigenmaps/. The authors are listed in prov/N1D05V.jsonl.

"""Laplacian eigenmaps (Belkin and Niyogi, 2003).

Build a neighbor graph with heat kernel weights (or unit weights when t is None),
form L = D - W, solve the generalized problem L y = lambda D y, discard the constant
solution with eigenvalue 0, and use the next m solutions as coordinates.

The generalized problem is solved through N = D^(-1/2) L D^(-1/2): if N z = lambda z,
then y = D^(-1/2) z solves L y = lambda D y, and y^T D y = z^T z.
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


def is_connected(w):
    n = len(w)
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for v in range(n):
            if w[u][v] > 0 and v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def laplacian_eigenmaps_from_weights(w, m):
    """Return (Y, eigenvalues). Y has n rows in R^m; the eigenvalues are lambda_1..lambda_{n-1},
    those of L y = lambda D y after the constant solution with lambda_0 = 0."""
    n = len(w)
    if not is_connected(w):
        raise ValueError("the graph is not connected: embed each component separately")
    deg = [sum(row) for row in w]  # @line L3
    r = [1.0 / math.sqrt(x) for x in deg]
    norm = [[((deg[i] if i == j else 0.0) - w[i][j]) * r[i] * r[j] for j in range(n)] for i in range(n)]
    # The constant solution of L y = 0 is z0 = D^(1/2) 1 for N. Shift it to the top.
    vol = sum(deg)
    c = sum(norm[i][i] for i in range(n)) + 1.0
    sq = [math.sqrt(x) for x in deg]
    shifted = [[norm[i][j] + c * sq[i] * sq[j] / vol for j in range(n)] for i in range(n)]
    lam, vecs = jacobi_eigh(shifted)  # @line L4
    y = [tuple(r[i] * vecs[l][i] for l in range(m)) for i in range(n)]  # @line L5
    return y, lam[:-1]  # @line L6


def laplacian_eigenmaps(points, m, k=None, eps=None, t=None):
    w = heat_kernel_graph(points, k, eps, t)
    return laplacian_eigenmaps_from_weights(w, m)
