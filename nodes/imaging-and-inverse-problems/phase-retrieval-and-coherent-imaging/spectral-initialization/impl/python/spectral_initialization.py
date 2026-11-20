# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-initialization/. The authors are listed in prov/5K2MNA.jsonl.

"""Spectral initialization for phase retrieval.

The data are y_r = |<a_r, x>|^2 = |a_r^H x|^2 for r = 1 .. m, with known
sampling vectors a_r in C^n (lists of numbers). The estimate of x, up to a
global phase, is lambda v, where v is a unit leading eigenvector of

    Y = (1/m) sum_r y_r a_r a_r^H

and lambda^2 = n sum_r y_r / sum_r ||a_r||^2 estimates ||x||^2. This is the
initialization of Candes, Li and Soltanolkotabi (2015). With alpha_y set, the
terms with y_r > alpha_y^2 mean(y) are left out (the truncated version of
Chen and Candes (2017)). The eigenvector is found by power iteration: Y is
positive semidefinite, so its largest eigenvalue is also the largest in
absolute value.
"""

import math
import random


def gaussian_design(rng, m, n, complex_valued=True):
    """m sampling vectors with entries N(0, 1/2) + i N(0, 1/2), or N(0, 1) if real."""
    if complex_valued:
        s = math.sqrt(0.5)
        return [[complex(rng.gauss(0.0, s), rng.gauss(0.0, s)) for _ in range(n)] for _ in range(m)]
    return [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(m)]


def inner(a, v):
    """<a, v> = a^H v = sum conj(a_i) v_i."""
    return sum(complex(u).conjugate() * w for u, w in zip(a, v))


def measure(a_rows, x):
    """The phaseless data y_r = |a_r^H x|^2."""
    return [abs(inner(a, x)) ** 2 for a in a_rows]


def kept_terms(y, alpha_y=None):
    """The indices r used in Y: all of them, or those with y_r <= alpha_y^2 mean(y)."""
    if alpha_y is None:
        return list(range(len(y)))
    cut = alpha_y * alpha_y * sum(y) / len(y)
    return [r for r, v in enumerate(y) if v <= cut]


def apply_y(a_rows, y, v, keep=None):
    """Y v = (1/m) sum_r y_r a_r (a_r^H v), over the kept indices."""
    idx = range(len(y)) if keep is None else keep
    out = [0j] * len(v)
    for r in idx:
        c = y[r] * inner(a_rows[r], v)
        for i, ai in enumerate(a_rows[r]):
            out[i] += c * ai
    m = len(y)
    return [w / m for w in out]


def spectral_matrix(a_rows, y, keep=None):
    """The n x n matrix Y, built term by term."""
    n = len(a_rows[0])
    idx = range(len(y)) if keep is None else keep
    mat = [[0j] * n for _ in range(n)]
    for r in idx:
        a = a_rows[r]
        for i in range(n):
            for j in range(n):
                mat[i][j] += y[r] * a[i] * complex(a[j]).conjugate()
    return [[v / len(y) for v in row] for row in mat]


def norm(v):
    """The Euclidean norm."""
    return math.sqrt(sum(abs(w) ** 2 for w in v))


def spectral_init(a_rows, y, iters=100, seed=0, alpha_y=None):
    """Return (z0, eig): z0 = lambda v and the Rayleigh quotient eig = v^H Y v."""
    n = len(a_rows[0])
    lam = math.sqrt(n * sum(y) / sum(norm(a) ** 2 for a in a_rows))  # @line L1
    keep = kept_terms(y, alpha_y)  # @line L2
    rng = random.Random(seed)
    v = [complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)) for _ in range(n)]  # @line L3
    s = norm(v)
    v = [w / s for w in v]
    for _ in range(iters):  # @line L4
        w = apply_y(a_rows, y, v, keep)  # @line L5
        s = norm(w)
        if s == 0.0:
            break
        v = [u / s for u in w]  # @line L6
    eig = inner(v, apply_y(a_rows, y, v, keep)).real
    return [lam * w for w in v], eig  # @line L7


def dist(z, x):
    """min over phi of ||z - e^{i phi} x|| = sqrt(||z||^2 + ||x||^2 - 2 |x^H z|)."""
    d2 = norm(z) ** 2 + norm(x) ** 2 - 2.0 * abs(inner(x, z))
    return math.sqrt(max(d2, 0.0))
