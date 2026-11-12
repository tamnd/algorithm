# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-pca/. The authors are listed in prov/JKAB4E.jsonl.

"""Sparse PCA by the truncated power method (TPower) of Yuan and Zhang (2013).

tpower(a, k, x0) approximately solves  max x^T A x  subject to ||x||_2 = 1, ||x||_0 <= k,
for a symmetric positive semidefinite matrix A (a covariance matrix). sparse_pca finds
several components with projection deflation. brute_force solves the problem exactly
by trying every support, for small d.
"""

import math
from itertools import combinations


def covariance(x):
    n, d = len(x), len(x[0])
    mu = [sum(row[j] for row in x) / n for j in range(d)]
    return [[sum((r[i] - mu[i]) * (r[j] - mu[j]) for r in x) / n for j in range(d)] for i in range(d)]


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x) if xj != 0.0) for row in a]


def quad(a, x):
    return sum(xi * yi for xi, yi in zip(x, matvec(a, x)))


def top_k_support(y, k):
    """Indices of the k entries of largest absolute value; ties go to the lower index."""
    return sorted(sorted(range(len(y)), key=lambda i: (-abs(y[i]), i))[:k])


def restrict_normalize(y, support):
    keep = set(support)
    z = [yi if i in keep else 0.0 for i, yi in enumerate(y)]
    norm = math.sqrt(sum(t * t for t in z))
    return [t / norm for t in z] if norm > 0 else z


def truncate(y, k):
    return restrict_normalize(y, top_k_support(y, k))


def tpower(a, k, x0, tol=1e-12, max_iter=1000):
    """Returns (x, value, history) where history lists x^T A x after each iteration."""
    x = truncate(x0, k)  # @line L1
    history = [quad(a, x)]
    for _ in range(max_iter):  # @line L2
        y = matvec(a, x)  # @line L3
        support = top_k_support(y, k)  # @line L4
        nxt = restrict_normalize(y, support)  # @line L5
        if all(t == 0.0 for t in nxt):  # A x = 0, so x^T A x = 0 is the optimum
            break
        stop = math.sqrt(sum((s - t) ** 2 for s, t in zip(nxt, x))) < tol  # @line L6
        x = nxt  # @line L7
        history.append(quad(a, x))
        if stop:
            break
    return x, quad(a, x), history  # @line L8


def default_start(a, k):
    """The unit vector on the largest diagonal entry, the start used for the examples."""
    d = len(a)
    i = max(range(d), key=lambda j: (a[j][j], -j))
    return [1.0 if j == i else 0.0 for j in range(d)]


def best_of_starts(a, k):
    """Run TPower from every coordinate vector e_i and keep the best result."""
    d = len(a)
    best = None
    for i in range(d):
        x, val, _ = tpower(a, k, [1.0 if j == i else 0.0 for j in range(d)])
        if best is None or val > best[1] + 1e-12:
            best = (x, val)
    return best


def deflate(a, x):
    """Projection deflation (I - x x^T) A (I - x x^T)."""
    d = len(a)
    p = [[(1.0 if i == j else 0.0) - x[i] * x[j] for j in range(d)] for i in range(d)]
    pa = [[sum(p[i][t] * a[t][j] for t in range(d)) for j in range(d)] for i in range(d)]
    return [[sum(pa[i][t] * p[t][j] for t in range(d)) for j in range(d)] for i in range(d)]


def sparse_pca(a, k, m):
    """m sparse components of cardinality at most k, with projection deflation."""
    comps, values = [], []
    for _ in range(m):
        x, val = best_of_starts(a, k)
        comps.append(x)
        values.append(val)
        a = deflate(a, x)
    return comps, values


def jacobi_eigen(a, tol=1e-14, max_sweeps=100):
    """Eigenvalues and eigenvectors (columns of v) of a small symmetric matrix."""
    n = len(a)
    a = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol * tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for r in range(n):
                    arp, arq = a[r][p], a[r][q]
                    a[r][p], a[r][q] = c * arp - s * arq, s * arp + c * arq
                for r in range(n):
                    apr, aqr = a[p][r], a[q][r]
                    a[p][r], a[q][r] = c * apr - s * aqr, s * apr + c * aqr
                for r in range(n):
                    vrp, vrq = v[r][p], v[r][q]
                    v[r][p], v[r][q] = c * vrp - s * vrq, s * vrp + c * vrq
    return [a[i][i] for i in range(n)], v


def brute_force(a, k):
    """Exact optimum: the largest eigenvalue of A[S, S] over all supports S of size k."""
    d = len(a)
    best = (-math.inf, None)
    for s in combinations(range(d), k):
        vals, vecs = jacobi_eigen([[a[i][j] for j in s] for i in s])
        j = max(range(k), key=lambda t: vals[t])
        if vals[j] > best[0]:
            x = [0.0] * d
            for pos, i in enumerate(s):
                x[i] = vecs[pos][j]
            best = (vals[j], x)
    return best[1], best[0]
