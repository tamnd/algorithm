# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locally-linear-embedding/. The authors are listed in prov/QVE4K5.jsonl.

"""Locally linear embedding (Roweis and Saul, 2000).

Step 1 finds the k nearest neighbors of each point. Step 2 finds the weights that
reconstruct each point from its neighbors with the weights summing to one. Step 3
finds the coordinates from the bottom eigenvectors of M = (I - W)^T (I - W).

The weights are the solution of the bordered system [[C + r I, 1], [1^T, 0]], with C
the local Gram matrix and r = reg * trace(C). With reg = 0 and fractions.Fraction
coordinates, the weights and M are exact.
"""

import math


def nearest_neighbors(points, k):
    n = len(points)
    out = []
    for i in range(n):
        dist = sorted((sum((a - b) ** 2 for a, b in zip(points[i], points[j])), j) for j in range(n) if j != i)
        out.append([j for _, j in dist[:k]])
    return out


def solve(a, b):
    """Gaussian elimination with pivoting on the largest entry. Exact for Fractions."""
    n = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular local system: use reg > 0")
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f != 0:
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    x = [0] * n
    for c in range(n - 1, -1, -1):
        x[c] = (m[c][n] - sum(m[c][j] * x[j] for j in range(c + 1, n))) / m[c][c]
    return x


def reconstruction_weights(points, nbrs, reg=0):
    """Return W as a list of dicts {j: w_ij}; each row sums to one."""
    w = []
    for i, nb in enumerate(nbrs):  # @line L2
        k = len(nb)
        z = [[a - b for a, b in zip(points[j], points[i])] for j in nb]
        c = [[sum(p * q for p, q in zip(z[s], z[t])) for t in range(k)] for s in range(k)]  # @line L3
        r = reg * sum(c[s][s] for s in range(k))
        for s in range(k):
            c[s][s] += r  # @line L4
        kkt = [c[s] + [1] for s in range(k)] + [[1] * k + [0]]
        sol = solve(kkt, [0] * k + [1])  # @line L5
        w.append(dict(zip(nb, sol[:k])))
    return w


def cost_matrix(w):
    """M = (I - W)^T (I - W)."""
    n = len(w)
    a = [[(1 if i == j else 0) - w[i].get(j, 0) for j in range(n)] for i in range(n)]
    return [[sum(a[r][i] * a[r][j] for r in range(n)) for j in range(n)] for i in range(n)]  # @line L6


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


def lle(points, k, m, reg=1e-3):
    """Return (Y, eigenvalues). Y has n rows in R^m, centered, with (1/n) Y^T Y = I.

    The eigenvalues are those of M on the vectors orthogonal to the constant, ascending.
    The constant vector is an exact eigenvector of M with eigenvalue 0. To discard it
    even when the null space of M has a dimension above 1, the code adds c (1 1^T) / n
    with c above every eigenvalue of M. This moves the constant to the top of the
    spectrum and leaves the other eigenvectors unchanged.
    """
    n = len(points)
    nbrs = nearest_neighbors(points, k)  # @line L1
    w = reconstruction_weights(points, nbrs, reg)
    mm = cost_matrix(w)
    c = sum(mm[i][i] for i in range(n)) + 1.0
    shifted = [[mm[i][j] + c / n for j in range(n)] for i in range(n)]
    lam, vecs = jacobi_eigh(shifted)  # @line L7
    s = math.sqrt(n)
    y = [tuple(s * vecs[l][i] for l in range(m)) for i in range(n)]  # @line L8
    return y, lam[:-1]  # @line L9
