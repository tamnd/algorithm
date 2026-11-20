# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-related-multiple-elimination/. The authors are listed in prov/JC2TNG.jsonl.
"""Surface-related multiple elimination (SRME) in the data-matrix form.

For one frequency, the data form a square matrix P: row = receiver
position, column = source position, on the same grid. The data without
surface multiples are P0, and the free surface links them by

    P = P0 + a P0 P,

where the surface operator a = r / S folds the free-surface reflection
coefficient r (-1 for water over air), the inverse of the source spectrum S
and the spatial step of the sum into one number per frequency. Then
P0 = P (I + a P)^(-1). The iteration P0 <- P - a P0 P converges to it when
the spectral radius of a P is below 1. All matrices are complex lists of rows.
"""

import imgkit as ik
import imgla as la


def _sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def _scale(a, s):
    return [[s * x for x in row] for row in a]


def srme_iterative(p, a, iters):
    """Iterate P0 <- P - a P0 P, starting from P0 = P, for one frequency."""
    p0 = [list(row) for row in p]  # @line L2
    for _ in range(iters):  # @line L3
        p0 = _sub(p, _scale(la.matmul(p0, p), a))  # @line L4
    return p0


def srme_direct(p, a):
    """P0 = P (I + a P)^(-1) for one frequency, by one linear solve."""
    n = len(p)
    m = [[(1.0 if i == j else 0.0) + a * p[i][j] for j in range(n)] for i in range(n)]
    # X (I + a P) = P is the same as (I + a P)^T X^T = P^T.
    xt = la.solve(la.transpose(m), la.transpose(p))
    return la.transpose(xt)


def srme(data, surface, iters=None):
    """Apply SRME at every frequency.

    data is a list of matrices P(w_k), surface a list of the scalars a(w_k).
    With iters=None the direct form is used, otherwise the iteration.
    """
    out = []
    for p, a in zip(data, surface):  # @line L1
        if iters is None:
            out.append(srme_direct(p, a))
        else:
            out.append(srme_iterative(p, a, iters))  # @line L5
    return out  # @line L6


def add_surface_multiples(p0, a):
    """The data with surface multiples: P = (I - a P0)^(-1) P0, the inverse map of SRME."""
    n = len(p0)
    m = [[(1.0 if i == j else 0.0) - a * p0[i][j] for j in range(n)] for i in range(n)]
    return la.solve(m, p0)


def estimate_surface_scalar(data, predicted):
    """The least-squares scalar s minimizing sum_k ||P_k - s M_k||^2 (Frobenius).

    This is the minimum-energy rule of adaptive subtraction with one
    complex scalar for the whole data set; it is a heuristic, not part of the
    exact relation.
    """
    num = 0j
    den = 0.0
    for p, m in zip(data, predicted):
        for rp, rm in zip(p, m):
            for x, y in zip(rp, rm):
                num += y.conjugate() * x
                den += abs(y) ** 2
    return num / den


def srme_trace(trace, a=-1.0, iters=None):
    """SRME for one zero-offset trace of a 1D earth (each P is a 1 x 1 matrix).

    The trace is periodic with n samples; a is the surface operator, -1 for
    a unit impulse source under a free surface with r = -1. Returns the trace
    without surface multiples.
    """
    spec = ik.dft(trace)
    data = [[[v]] for v in spec]
    out = srme(data, [a] * len(spec), iters)
    return [v.real for v in ik.idft([m[0][0] for m in out])]
