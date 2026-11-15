# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moesp/. The authors are listed in prov/7ZZDNB.jsonl.

"""Ordinary MOESP (Verhaegen and Dewilde, 1992).

Input: an input sequence u_0, ..., u_(N-1) (vectors of length m) and an
output sequence y_0, ..., y_(N-1) (vectors of length p) of a discrete-time
system x_(k+1) = A x_k + B u_k, y_k = C x_k + D u_k (+ white output noise),
the number i of block rows (i > n), and the order n (or None to pick it from
the singular values with the relative threshold tol).

Steps: block Hankel matrices U and Y with i block rows and j = N - i + 1
columns; the LQ factorization [U; Y] = L Q; the SVD of the block L22; the
extended observability matrix Gamma = U_n (left singular vectors); C from the
first block row of Gamma; A from its shift structure; then x_0, B and D by
linear least squares on the data.

The LQ factorization uses Householder reflections. The SVD is a one-sided
Jacobi (Hestenes) method. Both are in floating point.
"""

import math

from ctlmat import mul, transpose

__all__ = ["block_hankel", "householder_lq", "jacobi_svd", "pinv", "moesp", "estimate_x0_b_d", "simulate"]


def block_hankel(w, i, j):
    """Return the i q by j matrix whose block (r, c) is the vector w[r + c] as a column."""
    q = len(w[0])
    return [[float(w[r + c][a]) for c in range(j)] for r in range(i) for a in range(q)]


def householder_lq(a):
    """Return the d by d lower triangular L with a = L Q, Q with orthonormal rows.

    a is d by N with d <= N. Each step applies a Householder reflection from
    the right that sets the entries to the right of the diagonal in one row
    to zero. Cost: O(d^2 N).
    """
    d, ncol = len(a), len(a[0])
    if d > ncol:
        raise ValueError("householder_lq: need at least as many columns as rows")
    w = [[float(v) for v in row] for row in a]
    for k in range(d):
        v = w[k][k:]
        normx = math.sqrt(sum(t * t for t in v))
        if normx == 0.0:
            continue
        alpha = -math.copysign(normx, v[0])
        v[0] -= alpha
        vv = sum(t * t for t in v)
        for r in range(k, d):
            row = w[r]
            f = 2.0 * sum(row[k + t] * v[t] for t in range(len(v))) / vv
            if f != 0.0:
                for t in range(len(v)):
                    row[k + t] -= f * v[t]
    return [[w[r][c] if c <= r else 0.0 for c in range(d)] for r in range(d)]


def jacobi_svd(a, tol=1e-15, max_sweeps=80):
    """Return (U, s, V) with a = U diag(s) V^T and s sorted in decreasing order.

    a is r by c. U is r by k and V is c by k, with k = min(r, c), as lists of
    rows. A column of U that belongs to a zero singular value is zero. A
    column whose squared norm is below 1e-30 times the squared Frobenius norm
    of a counts as zero and is not rotated.
    """
    r, c = len(a), len(a[0])
    if r < c:
        v, s, u = jacobi_svd(transpose(a), tol, max_sweeps)
        return u, s, v
    cols = [[float(a[i][j]) for i in range(r)] for j in range(c)]
    vcols = [[1.0 if i == j else 0.0 for i in range(c)] for j in range(c)]
    tiny = 1e-30 * sum(t * t for col in cols for t in col)
    for _ in range(max_sweeps):
        rotated = False
        for p in range(c - 1):
            for q in range(p + 1, c):
                x, y = cols[p], cols[q]
                alpha = sum(t * t for t in x)
                beta = sum(t * t for t in y)
                gamma = sum(s * t for s, t in zip(x, y))
                if min(alpha, beta) <= tiny or abs(gamma) <= tol * math.sqrt(alpha * beta):
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                cs = 1.0 / math.sqrt(1.0 + t * t)
                sn = cs * t
                cols[p] = [cs * xi - sn * yi for xi, yi in zip(x, y)]
                cols[q] = [sn * xi + cs * yi for xi, yi in zip(x, y)]
                vx, vy = vcols[p], vcols[q]
                vcols[p] = [cs * xi - sn * yi for xi, yi in zip(vx, vy)]
                vcols[q] = [sn * xi + cs * yi for xi, yi in zip(vx, vy)]
        if not rotated:
            break
    sv = [math.sqrt(sum(t * t for t in col)) for col in cols]
    order = sorted(range(c), key=lambda j: -sv[j])
    s = [sv[j] for j in order]
    ucols = [[t / sv[j] for t in cols[j]] if sv[j] > 0.0 else [0.0] * r for j in order]
    return transpose(ucols), s, transpose([vcols[j] for j in order])


def pinv(a, rtol=1e-12):
    """Return the Moore-Penrose pseudoinverse; singular values below rtol s_max count as zero."""
    U, s, V = jacobi_svd(a)
    keep = [k for k in range(len(s)) if s[k] > rtol * s[0]] if s and s[0] > 0.0 else []
    return [[sum(V[r][k] * U[c][k] / s[k] for k in keep) for c in range(len(U))] for r in range(len(V))]


def simulate(A, B, C, D, u, x0):
    """Return y_0, ..., y_(N-1) of x_(k+1) = A x_k + B u_k, y_k = C x_k + D u_k."""
    x = list(x0)
    out = []
    for uk in u:
        out.append([sum(C[a][t] * x[t] for t in range(len(x))) + sum(D[a][c] * uk[c] for c in range(len(uk)))
                    for a in range(len(C))])
        x = [sum(A[r][t] * x[t] for t in range(len(x))) + sum(B[r][c] * uk[c] for c in range(len(uk)))
             for r in range(len(x))]
    return out


def estimate_x0_b_d(A, C, u, y):
    """Fit x_0, B and D by linear least squares, with A and C fixed.

    y_k = C A^k x_0 + sum_(t<k) C A^(k-1-t) B u_t + D u_k is linear in the
    entries of x_0, B and D. Each regressor column is the output of a small
    simulation, so the cost is O(N n^3 m + N p m) to build the columns and
    O(N p q^2) per SVD sweep for the q = n + n m + p m unknowns.
    """
    n, p, m, N = len(A), len(C), len(u[0]), len(u)
    columns = []
    for r in range(n):  # x_0 entries: free response C A^k e_r
        e = [1.0 if t == r else 0.0 for t in range(n)]
        columns.append([v for yk in simulate(A, [[0.0] * m for _ in range(n)], C, [[0.0] * m for _ in range(p)], u, e)
                        for v in yk])
    for r in range(n):  # B entries
        for c in range(m):
            E = [[1.0 if (t == r and s == c) else 0.0 for s in range(m)] for t in range(n)]
            columns.append([v for yk in simulate(A, E, C, [[0.0] * m for _ in range(p)], u, [0.0] * n) for v in yk])
    for a in range(p):  # D entries
        for c in range(m):
            columns.append([float(u[k][c]) if b == a else 0.0 for k in range(N) for b in range(p)])
    phi = transpose(columns)
    theta = mul(pinv(phi), [[float(v)] for yk in y for v in yk])
    theta = [row[0] for row in theta]
    x0 = theta[:n]
    B = [[theta[n + r * m + c] for c in range(m)] for r in range(n)]
    D = [[theta[n + n * m + a * m + c] for c in range(m)] for a in range(p)]
    return x0, B, D


def moesp(u, y, i, n=None, tol=1e-8):
    """Return (A, B, C, D, x0, s): an order n model and the singular values of L22."""
    m, p, N = len(u[0]), len(y[0]), len(u)
    j = N - i + 1
    if j < i * (m + p):
        raise ValueError("moesp: too few samples for i block rows")
    U = block_hankel(u, i, j)  # @line L1
    Y = block_hankel(y, i, j)
    L = householder_lq(U + Y)  # @line L2
    L22 = [row[i * m:] for row in L[i * m:]]
    Ul, s, _ = jacobi_svd(L22)  # @line L3
    if n is None:  # @line L4
        n = sum(1 for v in s if v > tol * s[0])
    if n < 1 or n >= i or s[n - 1] <= 0.0:
        raise ValueError("moesp: need 1 <= n < i and n at most the rank of L22")
    G = [row[:n] for row in Ul]  # @line L5
    C = [list(row) for row in G[:p]]  # @line L6
    A = mul(pinv(G[:-p]), G[p:])  # @line L7
    x0, B, D = estimate_x0_b_d(A, C, u, y)  # @line L8
    return A, B, C, D, x0, s  # @line L9
