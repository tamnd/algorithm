# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semidefinite-embedding/. The authors are listed in prov/6YS5CD.jsonl.

"""Semidefinite embedding, or maximum variance unfolding (Weinberger and Saul, 2004 and 2006).

Solve the semidefinite program

    maximize    trace(K)
    subject to  K is positive semidefinite,
                sum_ij K_ij = 0,
                K_ii + K_jj - 2 K_ij = |x_i - x_j|^2 for each constrained pair (i, j),

where the constrained pairs are the k-nearest-neighbor pairs and the pairs of points that
are neighbors of a common point. Then embed with the top eigenvectors of K, as in
classical MDS.

The paper uses an interior point SDP solver. This file uses a simple solver instead: an
augmented Lagrangian method whose inner steps are projected gradient steps. The projection
onto {K PSD, K 1 = 0} is J K J followed by setting the negative eigenvalues to 0, with a
Jacobi eigensolver. It is slow and only meant for small inputs, but it solves the same SDP.
"""

import math


def jacobi_eigh(a, v0=None, max_sweeps=100):
    """Eigenvalues in ascending order and the matching eigenvectors (as lists).

    If v0 is an orthogonal matrix (as rows of columns: v0[r][c]), start from v0^T a v0. A good
    v0, such as the eigenvectors of a nearby matrix, makes the method converge in few sweeps."""
    n = len(a)
    if v0 is None:
        v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        a = [[float(x) for x in row] for row in a]
    else:
        v = [row[:] for row in v0]
        av = [[sum(a[i][l] * v[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        a = [[sum(v[l][i] * av[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
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
    return [a[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order], v


def constraint_pairs(points, k):
    """The k-nearest-neighbor pairs, and the pairs of points that are neighbors of a common point."""
    n = len(points)
    pairs = set()
    for i in range(n):
        nbrs = sorted(range(n), key=lambda j: (math.dist(points[i], points[j]), j))[1:k + 1]
        for a in nbrs:
            pairs.add((min(i, a), max(i, a)))
            for b in nbrs:
                if a < b:
                    pairs.add((a, b))
    return sorted(pairs)


def centered_gram(points):
    n, d = len(points), len(points[0])
    mean = [sum(p[c] for p in points) / n for c in range(d)]
    z = [[p[c] - mean[c] for c in range(d)] for p in points]
    return [[sum(zi[c] * zj[c] for c in range(d)) for zj in z] for zi in z]


def project_psd_centered(k, v0=None):
    """The nearest matrix to k (in the Frobenius norm) that is PSD with rows summing to 0."""
    n = len(k)
    rmean = [sum(row) / n for row in k]
    cmean = [sum(k[i][j] for i in range(n)) / n for j in range(n)]
    tmean = sum(rmean) / n
    jkj = [[0.5 * (k[i][j] + k[j][i]) - 0.5 * (rmean[i] + cmean[i] + rmean[j] + cmean[j]) + tmean
            for j in range(n)] for i in range(n)]
    lam, vecs, v = jacobi_eigh(jkj, v0)
    out = [[0.0] * n for _ in range(n)]
    for l in range(n):
        if lam[l] > 0:
            u = vecs[l]
            for i in range(n):
                ui = lam[l] * u[i]
                row = out[i]
                for j in range(n):
                    row[j] += ui * u[j]
    return out, v


def solve_mvu_sdp(n, pairs, targets, k0, rho=10.0, inner=20, max_outer=2000, tol=1e-6):
    """Augmented Lagrangian method for max trace(K) under the MVU constraints.

    Each inner step is a projected gradient step on
        -trace(K) + sum_c mu_c g_c(K) + (rho / 2) sum_c g_c(K)^2,
    with g_c(K) = K_ii + K_jj - 2 K_ij - target_c, and after each inner loop the
    multipliers are updated by mu_c += rho g_c(K)."""
    # Step size 1 / (rho * L), with L a Gershgorin bound on the norm of the constraint map.
    touch = [0] * n
    for i, j in pairs:
        touch[i] += 1
        touch[j] += 1
    # <A_c, A_c> = 4, and two constraints that share one point have <A_c, A_c'> = 1.
    lips = max(4 + (touch[i] - 1) + (touch[j] - 1) for i, j in pairs)
    step = 1.0 / (rho * lips)
    mu = [0.0] * len(pairs)
    k, v = project_psd_centered(k0)
    for _ in range(max_outer):
        start = k
        for _ in range(inner):
            grad = [[-1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
            for c, (i, j) in enumerate(pairs):
                coef = mu[c] + rho * (k[i][i] + k[j][j] - 2 * k[i][j] - targets[c])
                grad[i][i] += coef
                grad[j][j] += coef
                grad[i][j] -= coef
                grad[j][i] -= coef
            moved = [[k[i][j] - step * grad[i][j] for j in range(n)] for i in range(n)]
            k, v = project_psd_centered(moved, v)
        g = [k[i][i] + k[j][j] - 2 * k[i][j] - targets[c] for c, (i, j) in enumerate(pairs)]
        mu = [m + rho * gc for m, gc in zip(mu, g)]
        # Stop when K is feasible within tol and the inner loop no longer moves it.
        moved_by = max(abs(k[i][j] - start[i][j]) for i in range(n) for j in range(n))
        if max(abs(x) for x in g) < tol and moved_by < tol:
            break
    return k, mu


def semidefinite_embedding(points, k, m, pairs=None, **solver_options):
    """Return (Y, eigenvalues of K in decreasing order, K)."""
    n = len(points)
    if pairs is None:
        pairs = constraint_pairs(points, k)  # @line L1
    targets = [math.dist(points[i], points[j]) ** 2 for i, j in pairs]  # @line L2
    big, _ = solve_mvu_sdp(n, pairs, targets, centered_gram(points), **solver_options)  # @line L3
    lam, vecs, _ = jacobi_eigh(big)  # @line L4
    lam, vecs = lam[::-1], vecs[::-1]
    y = [tuple(math.sqrt(max(lam[l], 0.0)) * vecs[l][i] for l in range(m)) for i in range(n)]  # @line L5
    return y, lam, big  # @line L6
