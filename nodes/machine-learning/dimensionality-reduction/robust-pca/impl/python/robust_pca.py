# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-pca/. The authors are listed in prov/4W6RMP.jsonl.

"""Robust PCA by principal component pursuit,
    minimize ||L||_* + lam ||S||_1  subject to  L + S = M,
solved with the inexact augmented Lagrange multiplier method (Lin, Chen and Ma, Algorithm 5).
The singular value thresholding step uses a one-sided Jacobi SVD. Matrices are lists of rows.
"""

import math


def dot(a, b):
    return sum(s * t for s, t in zip(a, b))


def transpose(m):
    return [list(col) for col in zip(*m)]


def one_sided_jacobi(m, tol=1e-14, max_sweeps=40):
    """Hestenes one-sided Jacobi on the columns of m. Returns (a, s, v): the columns a_j of
    m V are mutually orthogonal, s_j = ||a_j||, and v holds the columns of the orthogonal V.
    So m = sum_j a_j v_j^T, and a_j / s_j are the left singular vectors."""
    a = transpose(m)
    c = len(a)
    v = [[1.0 if i == j else 0.0 for i in range(c)] for j in range(c)]
    for _ in range(max_sweeps):
        rotated = False
        for p in range(c - 1):
            for q in range(p + 1, c):
                alpha, beta, gamma = dot(a[p], a[p]), dot(a[q], a[q]), dot(a[p], a[q])
                if gamma == 0.0 or abs(gamma) <= tol * math.sqrt(alpha * beta):
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                cs = 1.0 / math.sqrt(1.0 + t * t)
                sn = cs * t
                for vec in (a, v):
                    xp, xq = vec[p], vec[q]
                    vec[p] = [cs * s - sn * u for s, u in zip(xp, xq)]
                    vec[q] = [sn * s + cs * u for s, u in zip(xp, xq)]
        if not rotated:
            break
    return a, [math.sqrt(dot(col, col)) for col in a], v


def singular_values(m):
    return sorted(one_sided_jacobi(m)[1], reverse=True)


def svt(m, tau):
    """Singular value thresholding: U diag(max(s - tau, 0)) V^T, the prox of tau ||.||_*.
    Returns the matrix and its rank."""
    a, s, v = one_sided_jacobi(m)
    rows, cols = len(m), len(m[0])
    out = [[0.0] * cols for _ in range(rows)]
    rank = 0
    for aj, sj, vj in zip(a, s, v):
        if sj > tau:
            rank += 1
            f = (sj - tau) / sj  # (s_j - tau) u_j v_j^T with u_j = a_j / s_j
            for i in range(rows):
                c = f * aj[i]
                if c != 0.0:
                    row = out[i]
                    for j in range(cols):
                        row[j] += c * vj[j]
    return out, rank


def shrink(m, tau):
    """Entrywise soft thresholding, the prox of tau ||.||_1."""
    return [[math.copysign(max(abs(x) - tau, 0.0), x) for x in row] for row in m]


def fro(m):
    return math.sqrt(sum(x * x for row in m for x in row))


def add(a, b, cb=1.0):
    return [[x + cb * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def rpca(m, lam=None, tol=1e-7, rho=1.2, mu_max_factor=1e7, max_iter=1000, trace=None):
    """Returns (L, S, Y, iterations, rank history). mu starts at 1.25 / ||M||_2 as in Lin, Chen
    and Ma; their experiments use rho = 1.6, but on small matrices that growth can stop at a
    feasible pair that is not optimal, so the default here is the slower rho = 1.2. If trace is
    a list, (rank of L, nonzeros of S, ||M - L - S||_F / ||M||_F) is appended per iteration."""
    n1, n2 = len(m), len(m[0])
    if lam is None:
        lam = 1.0 / math.sqrt(max(n1, n2))
    norm2 = singular_values(m)[0]
    norm_inf = max(abs(x) for row in m for x in row)
    j = max(norm2, norm_inf / lam)
    y = [[x / j for x in row] for row in m]  # @line L1
    s = [[0.0] * n2 for _ in range(n1)]
    mu = 1.25 / norm2
    mu_max = mu * mu_max_factor
    norm_m = fro(m)
    ranks = []
    for it in range(1, max_iter + 1):  # @line L2
        low, r = svt(add(add(m, s, -1.0), y, 1.0 / mu), 1.0 / mu)  # @line L3
        ranks.append(r)
        s = shrink(add(add(m, low, -1.0), y, 1.0 / mu), lam / mu)  # @line L4
        z = add(add(m, low, -1.0), s, -1.0)  # @line L5
        y = add(y, z, mu)
        mu = min(rho * mu, mu_max)  # @line L6
        if trace is not None:
            trace.append((r, sum(1 for row in s for x in row if x != 0.0), fro(z) / norm_m))
        if fro(z) <= tol * norm_m:  # @line L7
            break
    return low, s, y, it, ranks  # @line L8
