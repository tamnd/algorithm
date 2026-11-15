# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sindy/. The authors are listed in prov/5WMZP5.jsonl.

"""Sparse identification of nonlinear dynamics (SINDy) with sequentially
thresholded least squares (STLSQ), after Brunton, Proctor and Kutz (2016).

Input: states x(t_0), ..., x(t_(M-1)) (vectors of length n), their time
derivatives (measured, or estimated by central differences), a library of
candidate functions (here all monomials of total degree at most d), and a
threshold lam > 0.

Model: x' = Xi^T theta(x), where theta(x) is the vector of the p library
functions and Xi is a sparse p by n matrix. With Theta the M by p matrix of
library values at the samples, each column xi of Xi solves

    xi = argmin ||Theta xi - dx||_2,

then every entry with |xi_k| < lam is set to zero and the least squares fit
is repeated on the remaining columns of Theta, until the set of kept
columns does not change. The kept set never grows, so there are at most
p + 1 fits per column.

Least squares uses a Householder QR factorization in floating point.
"""

import math
from itertools import combinations_with_replacement

__all__ = ["monomials", "library", "lstsq_qr", "stlsq", "sindy", "central_difference"]


def monomials(n, degree):
    """Return the exponent tuples of all monomials in n variables with total degree <= degree."""
    out = []
    for d in range(degree + 1):
        for combo in combinations_with_replacement(range(n), d):
            e = [0] * n
            for v in combo:
                e[v] += 1
            out.append(tuple(e))
    return out


def term_name(e):
    """Return a readable name such as '1', 'x0', 'x0 x2' or 'x1^2'."""
    parts = []
    for v, k in enumerate(e):
        if k == 1:
            parts.append("x%d" % v)
        elif k > 1:
            parts.append("x%d^%d" % (v, k))
    return " ".join(parts) if parts else "1"


def library(xs, exps):
    """Return Theta: one row per sample, one column per exponent tuple."""
    return [[math.prod(x[v] ** k for v, k in enumerate(e)) for e in exps] for x in xs]


def lstsq_qr(a, b):
    """Return x that minimizes ||a x - b||_2 for an M by p matrix a of full column rank (M >= p).

    Householder QR: p reflections reduce a to upper triangular R and turn b
    into Q^T b; then R x = (Q^T b)[0:p] is solved by back substitution.
    Cost: O(M p^2).
    """
    m, p = len(a), len(a[0]) if a else 0
    if p == 0:
        return []
    cols = [[float(a[i][j]) for i in range(m)] for j in range(p)]
    rhs = [float(v) for v in b]
    for k in range(p):
        v = cols[k][k:]
        normx = math.sqrt(sum(t * t for t in v))
        if normx == 0.0:
            raise ValueError("lstsq_qr: the matrix does not have full column rank")
        alpha = -math.copysign(normx, v[0])
        v[0] -= alpha
        vv = sum(t * t for t in v)
        for j in range(k, p):
            col = cols[j]
            f = 2.0 * sum(col[k + t] * v[t] for t in range(len(v))) / vv
            for t in range(len(v)):
                col[k + t] -= f * v[t]
        f = 2.0 * sum(rhs[k + t] * v[t] for t in range(len(v))) / vv
        for t in range(len(v)):
            rhs[k + t] -= f * v[t]
    x = [0.0] * p
    for k in range(p - 1, -1, -1):
        s = rhs[k] - sum(cols[j][k] * x[j] for j in range(k + 1, p))
        if cols[k][k] == 0.0:
            raise ValueError("lstsq_qr: the matrix does not have full column rank")
        x[k] = s / cols[k][k]
    return x


def stlsq(theta, dx, lam, max_iter=None):
    """Return (xi, fits): the STLSQ solution for one state and the number of least squares fits."""
    p = len(theta[0])
    if max_iter is None:
        max_iter = p + 1
    xi = lstsq_qr(theta, dx)  # @line L3
    fits = 1
    keep = list(range(p))
    while fits < max_iter:  # @line L4
        new_keep = [k for k in keep if abs(xi[k]) >= lam]  # @line L5
        if new_keep == keep:  # @line L7
            break
        keep = new_keep
        xi = [0.0] * p  # @line L6
        if keep:
            sol = lstsq_qr([[row[k] for k in keep] for row in theta], dx)
            for k, v in zip(keep, sol):
                xi[k] = v
        fits += 1
    return xi, fits


def sindy(xs, dxs, degree, lam):
    """Return (Xi, exps): the p by n coefficient matrix and the exponent tuples of its rows."""
    n = len(xs[0])
    exps = monomials(n, degree)
    theta = library(xs, exps)  # @line L1
    cols = []
    for j in range(n):  # @line L2
        xi, _ = stlsq(theta, [d[j] for d in dxs], lam)
        cols.append(xi)
    Xi = [[cols[j][k] for j in range(n)] for k in range(len(exps))]
    return Xi, exps  # @line L8


def central_difference(xs, dt):
    """Return (x_k, (x_(k+1) - x_(k-1)) / (2 dt)) for k = 1, ..., M - 2."""
    inner = xs[1:-1]
    d = [[(b - a) / (2.0 * dt) for a, b in zip(xs[k - 1], xs[k + 1])] for k in range(1, len(xs) - 1)]
    return inner, d
