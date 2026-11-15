# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-mode-decomposition/. The authors are listed in prov/BZWTTE.jsonl.

"""Exact dynamic mode decomposition (Schmid, 2010; Tu et al., 2014).

Input: snapshots x_0, ..., x_M (real vectors of length q, the state or a
measurement of it at equally spaced times) and the rank r (or None to pick
the rank of X from the singular values with the relative threshold tol).

With X = [x_0 ... x_(M-1)], X' = [x_1 ... x_M] and the truncated SVD
X = U_r S_r V_r^T, the method computes the r by r matrix

    A_tilde = U_r^T X' V_r S_r^-1,

the eigenpairs A_tilde w = lambda w, and the exact DMD modes

    phi = X' V_r S_r^-1 w / lambda    (lambda nonzero).

Each (lambda, phi) with lambda nonzero is an eigenpair of X' X^+ (Tu et al.).
If the data come from x_(k+1) = A x_k and the range of X is invariant under A,
then each pair is an eigenpair of A.

The SVD is a one-sided Jacobi (Hestenes) method. The eigenvalues of A_tilde
are the roots of its characteristic polynomial; each eigenvector comes from
two steps of inverse iteration. All in floating point.
"""

import cmath
import math

from ctlmat import charpoly, mul, polyroots, solve, transpose

__all__ = ["jacobi_svd", "dmd", "amplitudes", "eigenvector"]


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


def eigenvector(a, lam):
    """Return a unit eigenvector of a for the eigenvalue lam, by two steps of inverse iteration."""
    n = len(a)
    shift = lam + 1e-10 * (1.0 + abs(lam))
    m = [[complex(a[i][j]) - (shift if i == j else 0.0) for j in range(n)] for i in range(n)]
    w = [complex(1.0, 0.1 * (k + 1)) for k in range(n)]
    for _ in range(2):
        w = solve(m, w)
        size = math.sqrt(sum(abs(v) ** 2 for v in w))
        w = [v / size for v in w]
    return w


def dmd(snapshots, r=None, tol=1e-10):
    """Return (eigenvalues, modes, s): the DMD eigenvalues, the modes as columns, and the singular values of X."""
    X = transpose(snapshots[:-1])  # @line L1
    Xp = transpose(snapshots[1:])
    U, s, V = jacobi_svd(X)  # @line L2
    if r is None:  # @line L3
        r = sum(1 for v in s if v > tol * s[0])
    if r < 1 or s[r - 1] <= 0.0:
        raise ValueError("dmd: the rank r must be at least 1 and at most the rank of X")
    Ur = [row[:r] for row in U]
    W = [[V[k][j] / s[j] for j in range(r)] for k in range(len(V))]  # V_r S_r^-1
    XpW = mul(Xp, W)
    At = mul(transpose(Ur), XpW)  # @line L4
    lams = polyroots(charpoly(At))  # @line L5
    modes = []
    for lam in lams:
        w = eigenvector(At, lam)
        if abs(lam) == 0.0:
            raise ValueError("dmd: a zero eigenvalue has no exact DMD mode")
        modes.append([sum(XpW[i][t] * w[t] for t in range(r)) / lam for i in range(len(XpW))])  # @line L6
    return lams, transpose(modes), s  # @line L7


def amplitudes(modes, x0):
    """Return b with modes b closest to x0 in the least squares sense (normal equations)."""
    r = len(modes[0])
    gram = [[sum(modes[i][a].conjugate() * modes[i][b] for i in range(len(modes))) for b in range(r)]
            for a in range(r)]
    rhs = [sum(modes[i][a].conjugate() * x0[i] for i in range(len(modes))) for a in range(r)]
    return solve(gram, rhs)


def continuous_eigenvalues(lams, h):
    """Return omega = ln(lambda) / h for snapshots taken every h time units."""
    return [cmath.log(complex(z)) / h for z in lams]
