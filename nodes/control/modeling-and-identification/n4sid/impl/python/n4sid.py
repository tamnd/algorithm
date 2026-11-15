# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/n4sid/. The authors are listed in prov/0NXMFM.jsonl.

"""N4SID (Van Overschee and De Moor, 1994), the version that uses two state sequences.

Input: an input sequence u_0, ..., u_(N-1) (vectors of length m) and an
output sequence y_0, ..., y_(N-1) (vectors of length p) of a discrete-time
system in innovation form x_(k+1) = A x_k + B u_k + K e_k,
y_k = C x_k + D u_k + e_k, the number i of block rows (i > n), and the order
n (or None to pick it from the singular values with the relative threshold
tol).

Steps: block Hankel matrices U and Y with 2i block rows and j = N - 2i + 1
columns; one LQ factorization of [U; Y] = L Q; the oblique projections
O_i = Y_f /_(U_f) W_p and O_(i-1) = Y_f^- /_(U_f^-) W_p^+; an SVD of O_i that
gives Gamma_i and the order; the state sequences X_i = Gamma_i^+ O_i and
X_(i+1) = Gamma_(i-1)^+ O_(i-1); and one linear least squares problem for
A, B, C and D. The residuals give the noise covariances.

Every row of the data matrix is the matching row of L times Q, and Q has
orthonormal rows. So every projection and every least squares problem is
computed on the rows of L (vectors of length 2 i (m + p)), not on rows of
length j.

The LQ factorization uses Householder reflections. The SVD is a one-sided
Jacobi (Hestenes) method. Both are in floating point.
"""

import math

from ctlmat import mul, sub, transpose

__all__ = ["block_hankel", "householder_lq", "jacobi_svd", "pinv", "oblique_projection", "n4sid", "simulate"]


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


def pinv(a, rtol=1e-10):
    """Return the Moore-Penrose pseudoinverse; singular values below rtol s_max count as zero."""
    U, s, V = jacobi_svd(a)
    keep = [k for k in range(len(s)) if s[k] > rtol * s[0]] if s and s[0] > 0.0 else []
    return [[sum(V[r][k] * U[c][k] / s[k] for k in keep) for c in range(len(U))] for r in range(len(V))]


def oblique_projection(a, b, c):
    """Return a /_b c = (a / b_perp) (c / b_perp)^+ c, for matrices with the same row length.

    x / b_perp = x - x b^T (b b^T)^+ b removes the part of each row of x that
    lies in the row space of b.
    """
    def perp(x):
        return sub(x, mul(mul(mul(x, transpose(b)), pinv(mul(b, transpose(b)))), b))
    return mul(mul(perp(a), pinv(perp(c))), c)


def simulate(A, B, C, D, u, x0, K=None, e=None):
    """Return y_0, ..., y_(N-1) of x_(k+1) = A x_k + B u_k + K e_k, y_k = C x_k + D u_k + e_k."""
    x = list(x0)
    n, out = len(x), []
    for k, uk in enumerate(u):
        ek = e[k] if e is not None else [0.0] * len(C)
        out.append([sum(C[a][t] * x[t] for t in range(n)) + sum(D[a][c] * uk[c] for c in range(len(uk))) + ek[a]
                    for a in range(len(C))])
        x = [sum(A[r][t] * x[t] for t in range(n)) + sum(B[r][c] * uk[c] for c in range(len(uk)))
             + (sum(K[r][a] * ek[a] for a in range(len(ek))) if K is not None else 0.0)
             for r in range(n)]
    return out


def n4sid(u, y, i, n=None, tol=1e-8):
    """Return (A, B, C, D, cov, s): the model, the residual covariance [[Q, S], [S^T, R]], and the singular values of O_i."""
    m, p, N = len(u[0]), len(y[0]), len(u)
    j = N - 2 * i + 1
    if j < 2 * i * (m + p):
        raise ValueError("n4sid: too few samples for i block rows")
    U = block_hankel(u, 2 * i, j)  # @line L1
    Y = block_hankel(y, 2 * i, j)
    L = householder_lq(U + Y)  # @line L2
    Lu, Ly = L[:2 * i * m], L[2 * i * m:]
    Up, Uf = Lu[:i * m], Lu[i * m:]
    Yp, Yf = Ly[:i * p], Ly[i * p:]
    Oi = oblique_projection(Yf, Uf, Up + Yp)  # @line L3
    Up1, Uf1 = Lu[:(i + 1) * m], Lu[(i + 1) * m:]
    Yp1, Yf1 = Ly[:(i + 1) * p], Ly[(i + 1) * p:]
    Oi1 = oblique_projection(Yf1, Uf1, Up1 + Yp1)  # @line L4
    Us, s, _ = jacobi_svd(Oi)  # @line L5
    if n is None:
        n = sum(1 for v in s if v > tol * s[0])
    if n < 1 or n >= i or s[n - 1] <= 0.0:
        raise ValueError("n4sid: need 1 <= n < i and n at most the rank of O_i")
    G = [[Us[r][k] * math.sqrt(s[k]) for k in range(n)] for r in range(i * p)]  # @line L6
    G1 = G[:-p]
    Xi = mul(pinv(G), Oi)  # @line L7
    Xi1 = mul(pinv(G1), Oi1)
    lhs = Xi1 + Ly[i * p:(i + 1) * p]
    rhs = Xi + Lu[i * m:(i + 1) * m]
    theta = mul(lhs, pinv(rhs))  # @line L8
    A = [row[:n] for row in theta[:n]]
    B = [row[n:] for row in theta[:n]]
    C = [row[:n] for row in theta[n:]]
    D = [row[n:] for row in theta[n:]]
    res = sub(lhs, mul(theta, rhs))  # @line L9
    cov = [[v / j for v in row] for row in mul(res, transpose(res))]
    return A, B, C, D, cov, s  # @line L10
