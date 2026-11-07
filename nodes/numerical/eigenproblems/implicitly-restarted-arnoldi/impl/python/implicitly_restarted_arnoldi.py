# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicitly-restarted-arnoldi/. The authors are listed in prov/PAMN7C.jsonl.

"""Implicitly restarted Arnoldi method (Sorensen 1992) with exact shifts, in complex arithmetic.

iram(matvec, b, k, m) returns (theta, x, est, restarts, matvecs, converged): the k wanted Ritz
values, their Ritz vectors, residual norm estimates, the number of implicit restarts, the number
of products with A and whether every wanted pair met the tolerance. which="LM" wants largest
modulus, "LR" largest real part. Standard library only; vectors are lists of numbers.
"""

import cmath
import math

U = 2.0 ** -53  # unit roundoff of IEEE double precision
EPS23 = (2 * U) ** (2.0 / 3.0)  # ARPACK's floor for the relative test


def dot(x, y):
    """Inner product x* y (conjugate-linear in x)."""
    return sum(complex(a).conjugate() * b for a, b in zip(x, y))


def norm2(x):
    return math.sqrt(sum(abs(a) ** 2 for a in x))


def extend(matvec, v, h, f, j0, m, counter):
    """Extend A V_j0 = V_j0 H_j0 + f e_j0^T to m steps. Returns (f, j): j < m on breakdown."""
    n = len(f)
    for j in range(j0, m):
        beta = norm2(f)
        if j > 0:
            if beta <= 10.0 * n * U * counter["scale"]:
                return [0j] * n, j
            h[j][j - 1] = beta
        v.append([x / beta for x in f])
        w = [complex(x) for x in matvec(v[j])]
        counter["matvecs"] += 1
        counter["scale"] = max(counter["scale"], norm2(w))
        for _ in range(2):  # classical Gram-Schmidt run twice
            c = [dot(v[i], w) for i in range(j + 1)]
            for i in range(j + 1):
                h[i][j] += c[i]
            for i in range(j + 1):
                ci, vi = c[i], v[i]
                w = [wv - ci * qv for wv, qv in zip(w, vi)]
        f = w
    return f, m


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




def ritz_pairs(hm, beta):
    """Ritz values of the Hessenberg matrix hm, with eigenvectors y and estimates beta |e_m^* y|."""
    m = len(hm)
    out = []
    for theta in hessenberg_eigvals(hm):
        shifted = [[hm[i][j] - (theta if i == j else 0) for j in range(m)] for i in range(m)]
        y = [1.0 + 0j] * m
        for _ in range(3):
            y = _solve(shifted, y)
            ny = norm2(y)
            y = [val / ny for val in y]
        out.append((theta, y, beta * abs(y[m - 1])))
    return out


def order_key(which):
    if which == "LM":
        return lambda t: (-abs(t), -t.real, -t.imag)
    if which == "LR":
        return lambda t: (-t.real, -abs(t.imag), -t.imag)
    raise ValueError("which must be LM or LR")


def shifted_qr(h, mu, qacc):
    """One explicit shifted QR step H - mu I = Q R, H <- R Q + mu I, on the full m x m H."""
    m = len(h)
    for i in range(m):
        h[i][i] -= mu
    rots = []
    for p in range(m - 1):
        x, y = h[p][p], h[p + 1][p]
        r = math.hypot(abs(x), abs(y))
        c, s = (1.0 + 0j, 0j) if r == 0.0 else (x / r, y / r)
        rots.append((c, s))
        for col in range(p, m):
            a1, a2 = h[p][col], h[p + 1][col]
            h[p][col] = c.conjugate() * a1 + s.conjugate() * a2
            h[p + 1][col] = -s * a1 + c * a2
    for p, (c, s) in enumerate(rots):
        for row in range(0, min(p + 2, m - 1) + 1):
            a1, a2 = h[row][p], h[row][p + 1]
            h[row][p] = a1 * c + a2 * s
            h[row][p + 1] = -a1 * s.conjugate() + a2 * c.conjugate()
        for row in range(m):
            a1, a2 = qacc[row][p], qacc[row][p + 1]
            qacc[row][p] = a1 * c + a2 * s
            qacc[row][p + 1] = -a1 * s.conjugate() + a2 * c.conjugate()
    for i in range(m):
        h[i][i] += mu


def iram(matvec, b, k, m, which="LM", tol=1e-10, max_restarts=300):
    """Compute k wanted eigenvalues with a basis of at most m vectors (k < m)."""
    n = len(b)
    nb = norm2(b)
    if nb == 0.0:
        raise ValueError("start vector is zero")
    m = min(m, n)
    if not 0 < k < m:
        raise ValueError("need 0 < k < m <= n")
    key = order_key(which)
    counter = {"matvecs": 0, "scale": 0.0}
    v = []
    h = [[0j] * m for _ in range(m)]
    f, j = extend(matvec, v, h, [complex(x) for x in b], 0, k, counter)  # @line L1
    restarts = 0
    while True:  # @line L2
        f, j = extend(matvec, v, h, f, j, m, counter)  # @line L3
        hm = [row[:j] for row in h[:j]]
        beta = norm2(f)
        pairs = ritz_pairs(hm, beta)  # @line L4
        pairs.sort(key=lambda t: key(t[0]))
        kk = min(k, j)
        wanted = pairs[:kk]
        done = all(est <= tol * max(abs(th), EPS23) for th, _, est in wanted)
        if done or j < m or restarts >= max_restarts:  # @line L5
            x = [[sum(v[c][i] * y[c] for c in range(j)) for i in range(n)] for _, y, _ in wanted]
            return ([t[0] for t in wanted], x, [t[2] for t in wanted], restarts,
                    counter["matvecs"], done or j < m)
        restarts += 1
        qacc = [[1.0 + 0j if r == c else 0j for c in range(m)] for r in range(m)]  # @line L6
        for mu, _, _ in pairs[k:]:  # @line L7
            shifted_qr(h, mu, qacc)  # @line L8
        sigma = qacc[m - 1][k - 1]
        vnew = [[sum(v[c][i] * qacc[c][col] for c in range(m)) for i in range(n)]
                for col in range(k + 1)]
        hk1 = h[k][k - 1]
        f = [hk1 * a + sigma * fv for a, fv in zip(vnew[k], f)]  # @line L9
        v = vnew[:k]  # @line L10
        for r in range(m):
            for c in range(m):
                if r >= k or c >= k:
                    h[r][c] = 0j
        j = k
