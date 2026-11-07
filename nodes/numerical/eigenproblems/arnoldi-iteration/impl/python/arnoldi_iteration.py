# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arnoldi-iteration/. The authors are listed in prov/1X1DGA.jsonl.

"""Arnoldi iteration with modified Gram-Schmidt and optional reorthogonalization.

arnoldi(matvec, b, k) returns (q, h, m): the orthonormal Arnoldi vectors q_1..q_(m+1) (only
q_1..q_m if the iteration stopped early), the (m+1) x m upper Hessenberg matrix H_bar with
A Q_m = Q_(m+1) H_bar, and the number m of completed steps (m < k means that K_m(A, b) is an
invariant subspace). ritz(h, q, m) returns the Ritz values of H_m with Ritz vectors and the
residual estimates h_(m+1,m) |e_m^* y|. Real or complex lists; standard library only.
"""

import cmath
import math

U = 2.0 ** -53  # unit roundoff of IEEE double precision


def dot(x, y):
    """Inner product x* y (conjugate-linear in x)."""
    return sum(a.conjugate() * b for a, b in zip(x, y))


def norm2(x):
    return math.sqrt(sum(abs(a) ** 2 for a in x))


def arnoldi(matvec, b, k, reorth=True):
    """Run up to k Arnoldi steps on the operator matvec from the start vector b."""
    n = len(b)
    nb = norm2(b)
    if nb == 0.0:
        raise ValueError("start vector is zero")
    k = min(k, n)
    q = [[x / nb for x in b]]  # @line L1
    h = [[0.0] * k for _ in range(k + 1)]
    scale = 0.0
    for j in range(k):  # @line L2
        w = list(matvec(q[j]))  # @line L3
        scale = max(scale, norm2(w))
        passes = 2 if reorth else 1
        for _ in range(passes):  # @line L6
            for i in range(j + 1):  # @line L4
                c = dot(q[i], w)  # @line L5
                h[i][j] += c
                w = [wv - c * qv for wv, qv in zip(w, q[i])]
        beta = norm2(w)  # @line L7
        h[j + 1][j] = beta
        if beta <= 10.0 * n * U * scale:  # @line L8
            h[j + 1][j] = 0.0
            return q, [row[: j + 1] for row in h[: j + 2]], j + 1
        q.append([x / beta for x in w])  # @line L9
    return q, h, k  # @line L10


def _wilkinson_shift(a, b, c, d):
    """Eigenvalue of [[a, b], [c, d]] closer to d."""
    half = (a - d) / 2
    disc = cmath.sqrt(half * half + b * c)
    m1 = (a + d) / 2 + disc
    m2 = (a + d) / 2 - disc
    return m1 if abs(m1 - d) <= abs(m2 - d) else m2


def hessenberg_eigvals(hm):
    """All eigenvalues of a small upper Hessenberg matrix by complex shifted QR with Givens."""
    m = len(hm)
    a = [[complex(hm[i][j]) for j in range(m)] for i in range(m)]
    hnorm = math.sqrt(sum(abs(v) ** 2 for row in a for v in row)) or 1.0
    out = []
    hi = m - 1
    its = 0
    total = 0
    while hi >= 0:
        l = hi
        while l > 0:
            tol = U * (abs(a[l][l]) + abs(a[l - 1][l - 1]))
            if tol == 0.0:
                tol = U * hnorm
            if abs(a[l][l - 1]) <= tol:
                a[l][l - 1] = 0j
                break
            l -= 1
        if l == hi:
            out.append(a[hi][hi])
            hi -= 1
            its = 0
            continue
        its += 1
        total += 1
        if total > 60 * m:
            raise RuntimeError("Hessenberg QR did not converge")
        if its % 11 == 10:
            mu = a[hi][hi] + 1.5 * abs(a[hi][hi - 1])
        else:
            mu = _wilkinson_shift(a[hi - 1][hi - 1], a[hi - 1][hi], a[hi][hi - 1], a[hi][hi])
        for i in range(l, hi + 1):
            a[i][i] -= mu
        rots = []
        for p in range(l, hi):
            x, y = a[p][p], a[p + 1][p]
            r = math.hypot(abs(x), abs(y))
            if r == 0.0:
                c, s = 1.0 + 0j, 0j
            else:
                c, s = x / r, y / r
            rots.append((c, s))
            for col in range(p, hi + 1):
                u, v = a[p][col], a[p + 1][col]
                a[p][col] = c.conjugate() * u + s.conjugate() * v
                a[p + 1][col] = -s * u + c * v
        for p, (c, s) in zip(range(l, hi), rots):
            for row in range(l, min(p + 2, hi) + 1):
                u, v = a[row][p], a[row][p + 1]
                a[row][p] = u * c + v * s
                a[row][p + 1] = -u * s.conjugate() + v * c.conjugate()
        for i in range(l, hi + 1):
            a[i][i] += mu
    return out


def _solve(mat, rhs):
    """Gaussian elimination with partial pivoting; tiny pivots are replaced by U times the norm."""
    m = len(mat)
    a = [row[:] + [rhs[i]] for i, row in enumerate(mat)]
    big = max(abs(v) for row in mat for v in row) or 1.0
    for c in range(m):
        p = max(range(c, m), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        if abs(a[c][c]) < U * big:
            a[c][c] = U * big
        for r in range(c + 1, m):
            f = a[r][c] / a[c][c]
            if f != 0:
                for cc in range(c, m + 1):
                    a[r][cc] -= f * a[c][cc]
    x = [0j] * m
    for r in range(m - 1, -1, -1):
        x[r] = (a[r][m] - sum(a[r][cc] * x[cc] for cc in range(r + 1, m))) / a[r][r]
    return x


def ritz(h, q, m):
    """Ritz values of H_m, ordered by decreasing modulus, with vectors and residual estimates."""
    hm = [[h[i][j] for j in range(m)] for i in range(m)]
    beta = h[m][m - 1] if len(h) > m else 0.0
    out = []
    for theta in hessenberg_eigvals(hm):  # @line L11
        shifted = [[hm[i][j] - (theta if i == j else 0) for j in range(m)] for i in range(m)]
        y = [1.0 + 0j] * m
        for _ in range(3):
            y = _solve(shifted, y)
            ny = norm2(y)
            y = [v / ny for v in y]
        x = [sum(q[j][i] * y[j] for j in range(m)) for i in range(len(q[0]))]  # @line L12
        out.append((theta, x, abs(beta) * abs(y[m - 1])))  # @line L13
    out.sort(key=lambda t: (-abs(t[0]), -t[0].real, -t[0].imag))
    return out
