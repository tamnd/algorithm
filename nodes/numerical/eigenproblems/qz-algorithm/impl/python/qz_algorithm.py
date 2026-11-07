# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qz-algorithm/. The authors are listed in prov/WCHJ4Y.jsonl.

"""The QZ algorithm for the generalized eigenproblem A x = lambda B x.

qz(a, b) computes unitary Q and Z and upper triangular S and T with
Q* A Z = S and Q* B Z = T, the complex generalized Schur form. The
generalized eigenvalues are the pairs (alpha_i, beta_i) = (s_ii, t_ii):
lambda_i = alpha_i / beta_i when beta_i != 0, and an infinite eigenvalue when
beta_i = 0. The method first reduces (A, B) to Hessenberg-triangular form by
Givens rotations, then runs single-shift complex QZ steps with a shift from
the trailing 2 by 2 pencil, and deflates infinite eigenvalues by chasing a
zero diagonal entry of T to the top of the active block.

Matrices are lists of rows of Python numbers (real or complex); all work is in
complex arithmetic. Standard library only.
"""

import cmath
import math
from typing import NamedTuple

EPS = 2.0**-52


class QZResult(NamedTuple):
    s: list  # upper triangular, Q* A Z
    t: list  # upper triangular, Q* B Z
    q: list  # unitary
    z: list  # unitary
    alpha: list  # s_ii
    beta: list  # t_ii
    iterations: int  # the number of QZ steps
    converged: bool
    history: list  # (hi, |h_(hi,hi-1)|) after each QZ step, for rate measurements


def identity(n):
    return [[complex(i == j) for j in range(n)] for i in range(n)]


def frob(m):
    return math.sqrt(sum(abs(x) ** 2 for row in m for x in row))


def givens(f, g):
    """(c, s, r) with c real, [[c, s], [-conj(s), c]] (f, g)^T = (r, 0)^T."""
    if g == 0:
        return 1.0, 0j, f
    if f == 0:
        return 0.0, 1 + 0j, g
    af = abs(f)
    nrm = math.hypot(af, abs(g))
    ph = f / af
    return af / nrm, ph * g.conjugate() / nrm, ph * nrm


def rot_rows(m, i, j, c, s, cols):
    """Rows i, j of m <- G (rows i, j), G = [[c, s], [-conj(s), c]]."""
    sc = s.conjugate()
    ri, rj = m[i], m[j]
    for k in cols:
        x, y = ri[k], rj[k]
        ri[k] = c * x + s * y
        rj[k] = -sc * x + c * y


def rot_cols(m, i, j, c, s, rows):
    """Columns i, j of m <- (columns i, j) G, G = [[c, s], [-conj(s), c]]."""
    sc = s.conjugate()
    for k in rows:
        row = m[k]
        x, y = row[i], row[j]
        row[i] = c * x - sc * y
        row[j] = s * x + c * y


class _Pencil:
    """H, T, Q, Z with Q* A Z = H and Q* B Z = T; every rotation keeps this invariant."""

    def __init__(self, a, b):
        n = len(a)
        self.n = n
        self.h = [[complex(x) for x in row] for row in a]
        self.t = [[complex(x) for x in row] for row in b]
        self.q = identity(n)
        self.z = identity(n)
        self.all = range(n)

    def left(self, i, j, f, g):
        """Rotate rows i, j of H and T so that the pair (f, g) becomes (r, 0); Q <- Q G*."""
        c, s, _ = givens(f, g)
        rot_rows(self.h, i, j, c, s, self.all)
        rot_rows(self.t, i, j, c, s, self.all)
        # Q G*: columns i, j of Q times [[c, -s], [conj(s), c]]
        sc = s.conjugate()
        for row in self.q:
            x, y = row[i], row[j]
            row[i] = c * x + sc * y
            row[j] = -s * x + c * y

    def right(self, i, j, x, y):
        """Rotate columns i < j of H and T so that a row with entries (x, y) in them becomes (0, r); Z <- Z R."""
        c, s, _ = givens(y, x)
        rot_cols(self.h, i, j, c, s, self.all)
        rot_cols(self.t, i, j, c, s, self.all)
        rot_cols(self.z, i, j, c, s, self.all)


def hessenberg_triangular(p):
    """Reduce H to upper Hessenberg and T to upper triangular form (GVL Algorithm 7.7.1, with Givens)."""
    n, h, t = p.n, p.h, p.t
    for j in range(n - 1):  # T upper triangular by left rotations (a Givens QR of B)
        for i in range(n - 1, j, -1):
            if t[i][j] != 0:
                p.left(i - 1, i, t[i - 1][j], t[i][j])
                t[i][j] = 0j
    for j in range(n - 2):
        for i in range(n - 1, j + 1, -1):
            if h[i][j] == 0:
                continue
            p.left(i - 1, i, h[i - 1][j], h[i][j])  # zero h_ij; fills t_(i, i-1)
            h[i][j] = 0j
            p.right(i - 1, i, t[i][i - 1], t[i][i])  # zero t_(i, i-1); keeps h_ij = 0
            t[i][i - 1] = 0j


def pencil_shift(h, t, k):
    """The eigenvalue of the 2 by 2 pencil in rows and columns k-1, k nearer to h_kk / t_kk."""
    h11, h12, h21, h22 = h[k - 1][k - 1], h[k - 1][k], h[k][k - 1], h[k][k]
    t11, t12, t22 = t[k - 1][k - 1], t[k - 1][k], t[k][k]
    # det(H2 - x T2) = qa x^2 + qb x + qc
    qa = t11 * t22
    qb = -(h11 * t22 + h22 * t11 - h21 * t12)
    qc = h11 * h22 - h12 * h21
    target = h22 / t22
    if qa == 0:
        return target
    disc = cmath.sqrt(qb * qb - 4 * qa * qc)
    den = -qb + disc if abs(-qb + disc) >= abs(-qb - disc) else -qb - disc
    r1 = den / (2 * qa)
    r2 = (2 * qc) / den if den != 0 else r1
    return r1 if abs(r1 - target) <= abs(r2 - target) else r2


def qz(a, b, maxit_per_eig=30):
    """Return a QZResult for the pencil (A, B) of square matrices of equal order."""
    n = len(a)
    if len(b) != n or any(len(r) != n for r in a) or any(len(r) != n for r in b):
        raise ValueError("A and B must be square of the same order")
    p = _Pencil(a, b)
    hessenberg_triangular(p)  # @line L1
    h, t = p.h, p.t
    hnorm = max(frob(h), 1e-300)
    tnorm = max(frob(t), 1e-300)
    iters, since, history = 0, 0, []
    maxit = maxit_per_eig * max(n, 1)
    hi = n - 1  # @line L2
    converged = True
    while hi > 0:  # @line L3
        for k in range(1, hi + 1):  # @line L4
            scale = abs(h[k][k]) + abs(h[k - 1][k - 1]) or hnorm
            if abs(h[k][k - 1]) <= EPS * scale:
                h[k][k - 1] = 0j
        if h[hi][hi - 1] == 0:  # @line L5
            hi -= 1
            since = 0
            continue
        lo = hi - 1  # @line L6
        while lo > 0 and h[lo][lo - 1] != 0:
            lo -= 1
        for k in range(lo, hi + 1):  # negligible diagonal entries of T in the active block
            if abs(t[k][k]) <= EPS * tnorm:
                t[k][k] = 0j
        zero = next((k for k in range(lo, hi + 1) if t[k][k] == 0), None)
        if zero is not None:  # @line L7
            for j in range(zero, lo, -1):  # chase the zero of T up to t_(lo, lo)
                p.right(j - 1, j, t[j - 1][j - 1], t[j - 1][j])
                t[j - 1][j - 1] = 0j
                if j + 1 <= hi:
                    p.left(j, j + 1, h[j][j - 1], h[j + 1][j - 1])
                    h[j + 1][j - 1] = 0j
                    t[j + 1][j] = 0j
            p.left(lo, lo + 1, h[lo][lo], h[lo + 1][lo])  # deflate an infinite eigenvalue at the top
            h[lo + 1][lo] = 0j
            t[lo + 1][lo] = 0j
            since = 0
            continue
        if iters >= maxit:
            converged = False
            break
        iters += 1
        since += 1
        if since % 11 == 0:  # an exceptional shift breaks rare cycles
            mu = h[hi][hi] / t[hi][hi] + 0.75 * abs(h[hi][hi - 1]) / abs(t[hi][hi])
        else:
            mu = pencil_shift(h, t, hi)  # @line L8
        p.left(lo, lo + 1, h[lo][lo] - mu * t[lo][lo], h[lo + 1][lo])  # @line L9
        for k in range(lo, hi):  # @line L10
            p.right(k, k + 1, t[k + 1][k], t[k + 1][k + 1])  # zero the bulge t_(k+1, k)
            t[k + 1][k] = 0j
            if k + 2 <= hi:
                p.left(k + 1, k + 2, h[k + 1][k], h[k + 2][k])  # zero the bulge h_(k+2, k)
                h[k + 2][k] = 0j
        history.append((hi, abs(h[hi][hi - 1])))
    for i in range(n):  # clean the strictly lower parts, which are zero up to rounding
        for j in range(i):
            h[i][j] = 0j
            t[i][j] = 0j
    alpha = [h[i][i] for i in range(n)]
    beta = [t[i][i] for i in range(n)]
    return QZResult(h, t, p.q, p.z, alpha, beta, iters, converged, history)  # @line L11


def eigenvalues(res):
    """The generalized eigenvalues alpha / beta, with math.inf for beta = 0."""
    out = []
    for a, b in zip(res.alpha, res.beta):
        out.append(a / b if b != 0 else complex(math.inf))
    return out
