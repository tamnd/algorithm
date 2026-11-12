# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-maps/. The authors are listed in prov/T8KPAP.jsonl.

"""Diffusion maps (Coifman and Lafon, 2006).

Build a Gaussian kernel K, apply the alpha normalization K_ij / (q_i^alpha q_j^alpha)
with q_i = sum_j K_ij, normalize the rows to get the random walk P = D^-1 K,
and map point i to (lambda_1^t psi_1(i), ..., lambda_m^t psi_m(i)), where
P psi_l = lambda_l psi_l and the constant psi_0 with lambda_0 = 1 is left out.

P is similar to the symmetric matrix S = D^-1/2 K D^-1/2. If S v = lambda v with
|v| = 1, then psi = v / sqrt(pi) solves P psi = lambda psi, where pi_i = d_i / sum(d) is
the stationary distribution, and sum_i pi_i psi(i)^2 = 1. With this normalization the
Euclidean distance between the full maps equals the diffusion distance
D_t(x, y)^2 = sum_z (p_t(x, z) - p_t(y, z))^2 / pi(z).
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


def gaussian_kernel(points, eps):
    """K_ij = exp(-|x_i - x_j|^2 / eps), including K_ii = 1."""
    return [[math.exp(-math.dist(p, q) ** 2 / eps) for q in points] for p in points]  # @line L1


def is_connected(k):
    n = len(k)
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for v in range(n):
            if k[u][v] > 0 and v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def diffusion_map_from_kernel(k, m, t=1, alpha=1.0):
    """Return (Psi_t, eigenvalues, stationary distribution).

    k is a symmetric matrix with nonnegative entries whose graph is connected.
    Psi_t has n rows in R^m; the eigenvalues are lambda_1..lambda_m of P, after lambda_0 = 1,
    ordered by decreasing absolute value."""
    n = len(k)
    if not is_connected(k):
        raise ValueError("the kernel graph is not connected: P has the eigenvalue 1 more than once")
    q = [sum(row) for row in k]
    ka = [[k[i][j] / (q[i] ** alpha * q[j] ** alpha) for j in range(n)] for i in range(n)]  # @line L2
    d = [sum(row) for row in ka]  # @line L3
    vol = sum(d)
    pi = [x / vol for x in d]
    sym = [[ka[i][j] / math.sqrt(d[i] * d[j]) for j in range(n)] for i in range(n)]
    lam, vecs = jacobi_eigh(sym)  # @line L4
    # lambda_0 = 1 is the largest eigenvalue, with v_0 = sqrt(pi); leave it out.
    rest = sorted(range(n - 1), key=lambda l: -abs(lam[l]))[:m]  # @line L5
    psi = [[vecs[l][i] / math.sqrt(pi[i]) for i in range(n)] for l in rest]
    emb = [tuple(lam[l] ** t * psi[c][i] for c, l in enumerate(rest)) for i in range(n)]  # @line L6
    return emb, [lam[l] for l in rest], pi  # @line L7


def diffusion_map(points, m, eps, t=1, alpha=1.0):
    return diffusion_map_from_kernel(gaussian_kernel(points, eps), m, t, alpha)
