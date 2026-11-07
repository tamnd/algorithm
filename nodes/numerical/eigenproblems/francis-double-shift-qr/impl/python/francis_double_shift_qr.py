# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/francis-double-shift-qr/. The authors are listed in prov/ADBYNC.jsonl.

"""Francis implicit double-shift QR algorithm for a real matrix, in real arithmetic.

francis_step(h, l, hi, s, t, ...) applies one double-shift step to the window l..hi of an upper
Hessenberg matrix, with shifts the roots of z^2 - s z + t. schur(a) reduces a real square matrix
to Hessenberg form and iterates to real Schur form: it returns (t, q, eigenvalues, iterations)
with a = q t q^T, t quasi upper triangular with 1x1 and 2x2 diagonal blocks, and the number of
double-shift steps used. Standard library only; matrices are lists of lists of floats.
"""

import math

U = 2.0 ** -53  # unit roundoff of IEEE double precision


def house3(x):
    """Householder vector v and beta with (I - beta v v^T) x = -sign(x_1) ||x|| e_1."""
    norm = math.sqrt(sum(c * c for c in x))
    if norm == 0.0:
        return None, 0.0
    v = list(x)
    v[0] += norm if x[0] >= 0 else -norm
    vv = sum(c * c for c in v)
    return v, 2.0 / vv


def francis_step(h, l, hi, s, t, q=None, full=True):
    """One implicit double-shift step on rows and columns l..hi, shifts the roots of z^2 - s z + t."""
    n = len(h)
    lo = 0 if full else l
    top = n if full else hi + 1
    x = h[l][l] * h[l][l] + h[l][l + 1] * h[l + 1][l] - s * h[l][l] + t  # @line L1
    y = h[l + 1][l] * (h[l][l] + h[l + 1][l + 1] - s)
    z = h[l + 1][l] * h[l + 2][l + 1]
    for k in range(l, hi - 1):  # @line L2
        v, beta = house3([x, y, z])  # @line L3
        if v is not None:
            # @line L4
            reflect_window(h, q, v, beta, k, max(l, k - 1), min(k + 3, hi), lo, top, n)
        x = h[k + 1][k]  # @line L5
        y = h[k + 2][k]
        z = h[k + 3][k] if k < hi - 2 else 0.0
    v, beta = house3([x, y])  # @line L6
    if v is not None:
        reflect_window(h, q, v, beta, hi - 1, hi - 2, hi, lo, top, n)  # @line L7
    for k in range(l, hi - 1):  # entries below the subdiagonal are zero in exact arithmetic
        for i in range(k + 2, hi + 1):
            h[i][k] = 0.0


def reflect_window(h, q, v, beta, k, col_from, row_to, lo, top, n):
    """Apply P from the left to rows k.. (columns col_from..top-1) and from the right (rows lo..row_to)."""
    r = len(v)
    for j in range(col_from, top):
        d = beta * sum(v[i] * h[k + i][j] for i in range(r))
        if d != 0.0:
            for i in range(r):
                h[k + i][j] -= d * v[i]
    for i in range(lo, row_to + 1):
        d = beta * sum(h[i][k + c] * v[c] for c in range(r))
        if d != 0.0:
            for c in range(r):
                h[i][k + c] -= d * v[c]
    if q is not None:
        for i in range(n):
            d = beta * sum(q[i][k + c] * v[c] for c in range(r))
            if d != 0.0:
                for c in range(r):
                    q[i][k + c] -= d * v[c]


def hessenberg(a, q):
    """Householder reduction to upper Hessenberg form, accumulating into q."""
    n = len(a)
    h = [row[:] for row in a]
    for k in range(n - 2):
        v, beta = house3([h[i][k] for i in range(k + 1, n)])
        if v is None:
            continue
        reflect_window(h, q, v, beta, k + 1, k, n - 1, 0, n, n)
        for i in range(k + 2, n):
            h[i][k] = 0.0
    return h


def standardize(h, q, i, full=True):
    """Split a 2x2 block at rows i, i+1 with real eigenvalues by a rotation; return its eigenvalues."""
    n = len(h)
    a, b, c, d = h[i][i], h[i][i + 1], h[i + 1][i], h[i + 1][i + 1]
    p = 0.5 * (a - d)
    disc = p * p + b * c
    if disc < 0.0:
        root = math.sqrt(-disc)
        mid = 0.5 * (a + d)
        return [complex(mid, root), complex(mid, -root)]
    lam = 0.5 * (a + d) + math.copysign(math.sqrt(disc), p)
    x1, x2 = b, lam - a
    if abs(lam - d) + abs(c) > abs(x1) + abs(x2):
        x1, x2 = lam - d, c
    r = math.hypot(x1, x2)
    if r == 0.0:
        return [a, d]
    cs, sn = x1 / r, x2 / r
    for j in range(i, n if full else i + 2):
        u, w = h[i][j], h[i + 1][j]
        h[i][j], h[i + 1][j] = cs * u + sn * w, -sn * u + cs * w
    for row in range(0 if full else i, i + 2):
        u, w = h[row][i], h[row][i + 1]
        h[row][i], h[row][i + 1] = cs * u + sn * w, -sn * u + cs * w
    if q is not None:
        for row in range(n):
            u, w = q[row][i], q[row][i + 1]
            q[row][i], q[row][i + 1] = cs * u + sn * w, -sn * u + cs * w
    h[i + 1][i] = 0.0
    return [h[i][i], h[i + 1][i + 1]]


def schur(a, want_q=True, max_its_per_eig=30, trace=None):
    """Real Schur form a = q t q^T by Hessenberg reduction and Francis double-shift steps."""
    n = len(a)
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)] if want_q else None
    h = hessenberg(a, q)
    eig = [None] * n
    its_total = 0
    hi = n - 1
    its = 0
    while hi >= 0:
        l = hi
        while l > 0:  # @line L8
            tol = U * (abs(h[l - 1][l - 1]) + abs(h[l][l]))
            if tol == 0.0:
                tol = U * max(abs(h[l][l - 1]), U)
            if abs(h[l][l - 1]) <= tol:
                h[l][l - 1] = 0.0
                break
            l -= 1
        if l == hi:  # @line L9
            eig[hi] = complex(h[hi][hi])
            hi -= 1
            its = 0
            continue
        if l == hi - 1:
            pair = standardize(h, q, hi - 1, full=want_q)
            eig[hi - 1], eig[hi] = complex(pair[0]), complex(pair[1])
            hi -= 2
            its = 0
            continue
        its += 1
        its_total += 1
        if its > max_its_per_eig:
            raise RuntimeError("QR iteration did not converge")
        if its % 10 == 0:  # exceptional shift, as in LAPACK's xLAHQR
            w = abs(h[hi][hi - 1]) + abs(h[hi - 1][hi - 2])
            h11 = 0.75 * w + h[hi][hi]
            s, t = 2 * h11, h11 * h11 + 0.4375 * w * w
        else:
            s = h[hi - 1][hi - 1] + h[hi][hi]  # @line L10
            t = h[hi - 1][hi - 1] * h[hi][hi] - h[hi - 1][hi] * h[hi][hi - 1]
        if trace is not None:
            trace.append((hi, abs(h[hi][hi - 1]), abs(h[hi - 1][hi - 2])))
        francis_step(h, l, hi, s, t, q, full=want_q)  # @line L11
    return h, q, eig, its_total
