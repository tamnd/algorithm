# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eigensystem-realization-algorithm/. The authors are listed in prov/8Q2BQ4.jsonl.

"""The eigensystem realization algorithm (ERA) of Juang and Pappa (1985).

Input: measured Markov parameters h_0, ..., h_(2N) (the impulse response
samples of a discrete-time system, p by m matrices as lists of rows), the
number N of block rows and block columns, and the order n (or None to pick
the order from the singular values with a relative threshold tol).

With H the N p by N m block Hankel matrix with blocks h_(i+j-1), Hs the
shifted one with blocks h_(i+j), and H = U S V^T a singular value
decomposition truncated to the n largest singular values:

    A = S^(-1/2) U^T Hs V S^(-1/2),  B = (S^(1/2) V^T)[:, 0:m],
    C = (U S^(1/2))[0:p, :],         D = h_0.

On exact data of a system of order at most N, with n the rank of H, the
result is a minimal realization. On noisy data it is an approximation whose
error is governed by the singular values that are dropped.

The SVD is a one-sided Jacobi (Hestenes) method in floating point. Each sweep
costs O(a b^2) for an a by b matrix with a >= b; the sweeps stop when every
pair of columns is orthogonal to a relative tolerance of 1e-15.
"""

import cmath
import math

from ctlmat import mat_power, mul, transpose

__all__ = ["hankel", "jacobi_svd", "era", "markov_parameters", "continuous_poles"]


def hankel(h, rows, cols, shift=0):
    """Return the block Hankel matrix whose block (i, j) is h[i + j + 1 + shift]."""
    p = len(h[0])
    out = []
    for i in range(rows):
        for a in range(p):
            line = []
            for j in range(cols):
                line.extend(float(v) for v in h[i + j + 1 + shift][a])
            out.append(line)
    return out


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
    vsorted = [vcols[j] for j in order]
    return transpose(ucols), s, transpose(vsorted)


def era(h, N, n=None, tol=1e-8):
    """Return (A, B, C, D, s): an order n realization and the singular values of H."""
    if len(h) < 2 * N + 1:
        raise ValueError("era: need h_0, ..., h_(2N)")
    p, m = len(h[0]), len(h[0][0])
    H = hankel(h, N, N)  # @line L1
    Hs = hankel(h, N, N, shift=1)  # @line L2
    U, s, V = jacobi_svd(H)  # @line L3
    if n is None:  # @line L4
        n = sum(1 for v in s if v > tol * s[0])
    if n < 1 or s[n - 1] <= 0.0:
        raise ValueError("era: the order must be at most the rank of H")
    Un = [row[:n] for row in U]  # @line L5
    Vn = [row[:n] for row in V]
    root = [math.sqrt(v) for v in s[:n]]
    core = mul(mul(transpose(Un), Hs), Vn)
    A = [[core[i][j] / (root[i] * root[j]) for j in range(n)] for i in range(n)]  # @line L6
    B = [[root[i] * Vn[c][i] for c in range(m)] for i in range(n)]  # @line L7
    C = [[Un[a][j] * root[j] for j in range(n)] for a in range(p)]  # @line L8
    D = [[float(v) for v in row] for row in h[0]]  # @line L9
    return A, B, C, D, s  # @line L10


def markov_parameters(A, B, C, D, K):
    """Return [D, C B, C A B, ..., C A^(K-1) B]."""
    out = [[list(row) for row in D]]
    for k in range(1, K + 1):
        out.append(mul(mul(C, mat_power(A, k - 1)), B))
    return out


def continuous_poles(eigs, h_period):
    """Map discrete poles lambda to s = ln(lambda) / h, with the principal branch."""
    return [cmath.log(complex(z)) / h_period for z in eigs]
