# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qr-algorithm/. The authors are listed in prov/9ACH0R.jsonl.

"""The shifted Hessenberg QR algorithm for the complex Schur form.

qr_algorithm(a) returns T upper triangular and Q unitary with A ~ Q T Q*,
so the eigenvalues of A are the diagonal of T. It reduces A to Hessenberg
form by Householder reflectors, then runs explicitly shifted QR steps made of
Givens rotations on the active window, with the Wilkinson shift (the
eigenvalue of the trailing 2 by 2 block nearer its last entry), deflation of
negligible subdiagonal entries, an exceptional shift after every 10 steps
without deflation (not for shift="none", the plain unshifted algorithm),
and a cap of maxit steps per eigenvalue. Arithmetic is complex, so real
matrices with complex eigenvalues are handled directly.
Standard library only.
"""

import cmath
import math
from typing import NamedTuple

U = 2.0**-53


class QRResult(NamedTuple):
    t: list  # upper triangular Schur factor (strict lower part exactly zero)
    q: list  # unitary Schur vectors, A = Q T Q*
    eigenvalues: list  # diag(T), in the order of the Schur form
    iterations: int  # total number of QR steps
    converged: bool
    history: list  # (hi, |h[hi][hi-1]|) after each QR step, for rate measurements


def identity(n):
    return [[complex(i == j) for j in range(n)] for i in range(n)]


def hessenberg(a):
    """Return (H, Q) with A = Q H Q*, H upper Hessenberg, by Householder reflectors."""
    n = len(a)
    h = [[complex(t) for t in row] for row in a]
    q = identity(n)
    for k in range(n - 2):
        x = [h[i][k] for i in range(k + 1, n)]
        nx = math.sqrt(sum(abs(t) ** 2 for t in x[1:]))
        if nx == 0.0:
            continue  # already zero below the subdiagonal
        alpha = -cmath.exp(1j * cmath.phase(x[0])) * math.sqrt(abs(x[0]) ** 2 + nx * nx)
        v = x[:]
        v[0] -= alpha
        vv = sum(abs(t) ** 2 for t in v)
        # H <- P H with P = I - 2 v v* / v*v acting on rows k+1..n-1
        for j in range(n):
            s = 2 * sum(v[i].conjugate() * h[k + 1 + i][j] for i in range(len(v))) / vv
            for i in range(len(v)):
                h[k + 1 + i][j] -= s * v[i]
        # H <- H P and Q <- Q P acting on columns k+1..n-1
        for m in (h, q):
            for i in range(n):
                s = 2 * sum(m[i][k + 1 + j] * v[j] for j in range(len(v))) / vv
                for j in range(len(v)):
                    m[i][k + 1 + j] -= s * v[j].conjugate()
        for i in range(k + 2, n):
            h[i][k] = 0j
    return h, q


def givens(f, g):
    """Return (c, s, r) with c real, |c|^2 + |s|^2 = 1, [[c, s], [-conj(s), c]] (f, g)^T = (r, 0)^T."""
    if g == 0:
        return 1.0, 0j, f
    if f == 0:
        return 0.0, g.conjugate() / abs(g), abs(g)
    nf, ng = abs(f), abs(g)
    r = math.hypot(nf, ng)
    c = nf / r
    phase = f / nf
    s = phase * g.conjugate() / r
    return c, s, phase * r


def wilkinson_shift(a, b, c, d):
    """The eigenvalue of [[a, b], [c, d]] nearer d."""
    tr2 = (a + d) / 2
    disc = cmath.sqrt(((a - d) / 2) ** 2 + b * c)
    l1, l2 = tr2 + disc, tr2 - disc
    return l1 if abs(l1 - d) <= abs(l2 - d) else l2


def qr_algorithm(a, maxit=100, shift="wilkinson", want_q=True):
    """Return a QRResult. shift is "wilkinson", "rayleigh" (mu = h_nn) or "none" (mu = 0)."""
    n = len(a)
    if n == 0:
        raise ValueError("empty matrix")
    h, q = hessenberg(a)  # @line L1
    scale = math.sqrt(sum(abs(t) ** 2 for row in h for t in row))
    hi = n - 1  # @line L2
    its, total, history = 0, 0, []
    while hi > 0:  # @line L3
        lo = hi  # @line L4
        while lo > 0:
            tiny = U * (abs(h[lo - 1][lo - 1]) + abs(h[lo][lo]))
            if tiny == 0.0:
                tiny = U * scale
            if abs(h[lo][lo - 1]) <= tiny:
                h[lo][lo - 1] = 0j
                break
            lo -= 1
        if lo == hi:  # @line L5
            hi -= 1
            its = 0
            continue
        its += 1  # @line L6
        if its > maxit:
            return QRResult(h, q, [h[i][i] for i in range(n)], total, False, history)
        if its % 10 == 0 and shift != "none":  # @line L7
            mu = h[hi][hi] + 1.5 * abs(h[hi][hi - 1])  # exceptional shift
        elif shift == "wilkinson":
            mu = wilkinson_shift(h[hi - 1][hi - 1], h[hi - 1][hi], h[hi][hi - 1], h[hi][hi])
        elif shift == "rayleigh":
            mu = h[hi][hi]
        else:
            mu = 0j
        for i in range(lo, hi + 1):  # @line L8
            h[i][i] -= mu
        rots = []
        for k in range(lo, hi):  # left rotations: H - mu I = G R
            c, s, r = givens(h[k][k], h[k + 1][k])
            rots.append((c, s))
            for j in range(k, n):
                x, y = h[k][j], h[k + 1][j]
                h[k][j] = c * x + s * y
                h[k + 1][j] = -s.conjugate() * x + c * y
            h[k][k], h[k + 1][k] = r, 0j
        for k, (c, s) in zip(range(lo, hi), rots):  # @line L9
            for i in range(min(k + 2, hi) + 1):  # right rotations: R G + mu I
                x, y = h[i][k], h[i][k + 1]
                h[i][k] = c * x + s.conjugate() * y
                h[i][k + 1] = -s * x + c * y
            if want_q:
                for i in range(n):
                    x, y = q[i][k], q[i][k + 1]
                    q[i][k] = c * x + s.conjugate() * y
                    q[i][k + 1] = -s * x + c * y
        for i in range(lo, hi + 1):
            h[i][i] += mu
        total += 1
        history.append((hi, abs(h[hi][hi - 1])))
    return QRResult(h, q, [h[i][i] for i in range(n)], total, True, history)  # @line L10
