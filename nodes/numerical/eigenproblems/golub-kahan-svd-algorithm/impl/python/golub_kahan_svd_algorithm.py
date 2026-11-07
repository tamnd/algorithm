# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golub-kahan-svd-algorithm/. The authors are listed in prov/K72EMJ.jsonl.
"""Golub-Kahan SVD: Householder bidiagonalization, then implicit QR steps on
the bidiagonal matrix with a Wilkinson shift. Python standard library only.

svd(a) returns (u, sigma, v, steps) with a = u diag(sigma) v^T, u of size
m by r and v of size n by r, r = min(m, n), sigma[0] >= ... >= sigma[r-1] >= 0.
"""
import math

U = 2.0 ** -53


def _house(x):
    """Return (v, beta) with (I - beta v v^T) x = -sign(x0) ||x|| e1."""
    alpha = math.sqrt(sum(t * t for t in x))
    v = list(x)
    if alpha == 0.0:
        return v, 0.0
    v[0] += alpha if x[0] >= 0 else -alpha
    vv = sum(t * t for t in v)
    return v, 2.0 / vv


def bidiagonalize(a):
    """For m >= n, return (b, uq, vq) with a = uq b vq^T and b upper bidiagonal.
    b is n by n (dense list), uq is m by n with orthonormal columns, vq is n by n."""
    m, n = len(a), len(a[0])
    b = [row[:] for row in a]
    uq = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    vq = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(n):
        v, beta = _house([b[i][k] for i in range(k, m)])
        if beta:
            for j in range(k, n):
                s = beta * sum(v[i - k] * b[i][j] for i in range(k, m))
                for i in range(k, m):
                    b[i][j] -= s * v[i - k]
            for i in range(m):
                s = beta * sum(uq[i][r] * v[r - k] for r in range(k, m))
                for r in range(k, m):
                    uq[i][r] -= s * v[r - k]
        for i in range(k + 1, m):
            b[i][k] = 0.0
        if k < n - 2:
            v, beta = _house([b[k][j] for j in range(k + 1, n)])
            if beta:
                for i in range(k, m):
                    s = beta * sum(b[i][j] * v[j - k - 1] for j in range(k + 1, n))
                    for j in range(k + 1, n):
                        b[i][j] -= s * v[j - k - 1]
                for i in range(n):
                    s = beta * sum(vq[i][j] * v[j - k - 1] for j in range(k + 1, n))
                    for j in range(k + 1, n):
                        vq[i][j] -= s * v[j - k - 1]
            for j in range(k + 2, n):
                b[k][j] = 0.0
    sq = [row[:n] for row in b[:n]]
    return sq, [row[:n] for row in uq], vq


def _givens(f, g):
    """Return (c, s, r) with c f + s g = r and -s f + c g = 0."""
    if g == 0.0:
        return 1.0, 0.0, f
    r = math.hypot(f, g)
    return f / r, g / r, r


def _rot_cols(x, i, j, c, s, rows):
    for r in rows:
        p, q = x[r][i], x[r][j]
        x[r][i] = c * p + s * q
        x[r][j] = -s * p + c * q


def _rot_rows(x, i, j, c, s, cols):
    for t in cols:
        p, q = x[i][t], x[j][t]
        x[i][t] = c * p + s * q
        x[j][t] = -s * p + c * q


def _wilkinson_shift(b, p, q):
    """Eigenvalue of the trailing 2 by 2 block of B^T B (block p..q) closer to its last entry."""
    t11 = b[q - 1][q - 1] ** 2 + (b[q - 2][q - 1] ** 2 if q - 1 > p else 0.0)
    t12 = b[q - 1][q - 1] * b[q - 1][q]
    t22 = b[q][q] ** 2 + b[q - 1][q] ** 2
    d = (t11 - t22) / 2.0
    if d == 0.0 and t12 == 0.0:
        return t22
    return t22 - t12 * t12 / (d + math.copysign(math.hypot(d, t12), d if d != 0 else 1.0))


def gk_step(b, p, q, uq, vq, mu):
    """One implicit-shift Golub-Kahan step on the block p..q of the bidiagonal b."""
    n, m = len(b), len(uq)
    y = b[p][p] ** 2 - mu  # @line L6
    z = b[p][p] * b[p][p + 1]
    for k in range(p, q):  # @line L7
        c, s, _ = _givens(y, z)  # @line L8
        _rot_cols(b, k, k + 1, c, s, range(max(p, k - 1), k + 2))
        _rot_cols(vq, k, k + 1, c, s, range(len(vq)))
        if k > p:
            b[k - 1][k + 1] = 0.0
        y, z = b[k][k], b[k + 1][k]  # @line L9
        c, s, _ = _givens(y, z)
        _rot_rows(b, k, k + 1, c, s, range(k, min(q, k + 2) + 1))
        _rot_cols(uq, k, k + 1, c, s, range(m))
        b[k + 1][k] = 0.0
        if k < q - 1:  # @line L10
            y, z = b[k][k + 1], b[k][k + 2]


def _chase_zero_diagonal(b, p, q, k, uq, vq):
    """b[k][k] is zero: rotate the block so that row k (or column q) becomes zero."""
    m, n = len(uq), len(b)
    if k < q:
        for j in range(k + 1, q + 1):
            c, s, _ = _givens(b[j][j], b[k][j])
            _rot_rows(b, j, k, c, s, range(j, min(q, j + 1) + 1))
            _rot_cols(uq, j, k, c, s, range(m))
            b[k][j] = 0.0
    else:
        for j in range(q - 1, p - 1, -1):
            c, s, _ = _givens(b[j][j], b[j][q])
            _rot_cols(b, j, q, c, s, range(max(p, j - 1), j + 1))
            _rot_cols(vq, j, q, c, s, range(n))
            b[j][q] = 0.0


def svd_bidiagonal(b, uq, vq, max_steps_per_value=40, trace=None):
    """Diagonalize the upper bidiagonal b in place; returns the number of GK steps."""
    n = len(b)
    anorm = max([abs(b[i][i]) for i in range(n)] + [abs(b[i][i + 1]) for i in range(n - 1)] + [0.0])
    steps, q = 0, n - 1
    limit = max_steps_per_value * max(n, 1)
    while q > 0:
        for i in range(n - 1):  # @line L2
            if abs(b[i][i + 1]) <= U * (abs(b[i][i]) + abs(b[i + 1][i + 1])):
                b[i][i + 1] = 0.0
        while q > 0 and b[q - 1][q] == 0.0:  # @line L3
            q -= 1
        if q == 0:
            break
        p = q - 1
        while p > 0 and b[p - 1][p] != 0.0:
            p -= 1
        zero = [k for k in range(p, q + 1) if abs(b[k][k]) <= U * anorm]
        if zero:  # @line L4
            b[zero[0]][zero[0]] = 0.0
            _chase_zero_diagonal(b, p, q, zero[0], uq, vq)
            continue
        if steps >= limit:
            raise ArithmeticError("Golub-Kahan iteration did not converge")
        if trace is not None:
            trace.append([abs(b[i][i + 1]) for i in range(n - 1)])
        mu = _wilkinson_shift(b, p, q)  # @line L5
        gk_step(b, p, q, uq, vq, mu)
        steps += 1
    return steps


def transpose(a):
    return [list(col) for col in zip(*a)]


def svd(a, trace=None):
    """Return (u, sigma, v, steps) with a = u diag(sigma) v^T and sigma sorted descending."""
    m, n = len(a), len(a[0])
    if m < n:
        v, sigma, u, steps = svd(transpose(a), trace)
        return u, sigma, v, steps
    b, uq, vq = bidiagonalize(a)  # @line L1
    steps = svd_bidiagonal(b, uq, vq, trace=trace)
    sigma = [b[i][i] for i in range(n)]
    for i in range(n):  # @line L11
        if sigma[i] < 0:
            sigma[i] = -sigma[i]
            for r in range(n):
                vq[r][i] = -vq[r][i]
    order = sorted(range(n), key=lambda i: -sigma[i])
    sigma = [sigma[i] for i in order]
    u = [[row[i] for i in order] for row in uq]
    v = [[row[i] for i in order] for row in vq]
    return u, sigma, v, steps
