# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qr-decomposition/. The authors are listed in prov/H9XW97.jsonl.

"""Householder QR factorization A = Q R and its use for least squares.

A is m by n with m >= n, given as a list of m rows of floats. Q is kept in factored
form as the Householder vectors v_k and scalars beta_k, with H_k = I - beta_k v_k v_k^T
acting on rows k..m-1, and Q = H_0 H_1 ... H_{n-1}.
"""

import math


class RankDeficient(ValueError):
    """Raised when R has a zero diagonal entry, so the least squares solution is not unique."""


def householder_qr(a: list[list[float]]) -> tuple[list[list[float]], list[float], list[list[float]]]:
    """Return (vs, betas, r): Householder vectors, their scalars, and the n by n upper triangular R.

    vs[k] has length m - k and acts on rows k..m-1. A zero column gives beta = 0
    (no reflection) and a zero diagonal entry of R.
    Precondition: m >= n >= 1. Cost: 2 m n^2 - 2 n^3/3 flops.
    """
    m, n = len(a), len(a[0])
    if m < n:
        raise ValueError("need m >= n")
    w = [list(map(float, row)) for row in a]
    vs: list[list[float]] = []
    betas: list[float] = []
    for k in range(n):  # @line L1
        col = [w[i][k] for i in range(k, m)]
        scale = max(abs(t) for t in col)
        if scale == 0.0:
            vs.append([0.0] * (m - k))
            betas.append(0.0)
            continue
        nrm = scale * math.sqrt(sum((t / scale) ** 2 for t in col))
        alpha = -nrm if col[0] >= 0 else nrm  # @line L2
        v = col[:]
        v[0] = col[0] - alpha  # @line L3
        vtv = sum(t * t for t in v)
        beta = 2.0 / vtv
        w[k][k] = alpha
        for i in range(k + 1, m):
            w[i][k] = 0.0
        for j in range(k + 1, n):  # @line L4
            s = sum(v[i - k] * w[i][j] for i in range(k, m)) * beta
            for i in range(k, m):
                w[i][j] -= s * v[i - k]
        vs.append(v)  # @line L5
        betas.append(beta)
    r = [[w[i][j] if j >= i else 0.0 for j in range(n)] for i in range(n)]
    return vs, betas, r  # @line L6


def apply_qt(vs: list[list[float]], betas: list[float], b: list[float]) -> list[float]:
    """Return Q^T b = H_{n-1} ... H_0 b. Cost: 4 m n - 2 n^2 flops."""
    y = list(map(float, b))
    for k, (v, beta) in enumerate(zip(vs, betas)):
        if beta == 0.0:
            continue
        s = beta * sum(v[i] * y[k + i] for i in range(len(v)))
        for i in range(len(v)):
            y[k + i] -= s * v[i]
    return y


def form_q(vs: list[list[float]], betas: list[float], m: int) -> list[list[float]]:
    """Return the thin Q (m by n) by applying H_0 ... H_{n-1} to the first n columns of I, last reflector first."""
    n = len(vs)
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(m)]
    for k in range(n - 1, -1, -1):
        v, beta = vs[k], betas[k]
        if beta == 0.0:
            continue
        for j in range(n):
            s = beta * sum(v[i] * q[k + i][j] for i in range(len(v)))
            for i in range(len(v)):
                q[k + i][j] -= s * v[i]
    return q


def qr_least_squares(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve min ||b - A x||_2 by Householder QR: R x = (Q^T b)[0:n].

    Raises RankDeficient if some r_kk is exactly zero. A tiny but nonzero r_kk is
    not caught; use numerical_rank for that.
    Cost: 2 m n^2 - 2 n^3/3 + O(m n) flops.
    """
    vs, betas, r = householder_qr(a)
    n = len(r)
    y = apply_qt(vs, betas, b)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if r[i][i] == 0.0:
            raise RankDeficient("r[%d][%d] is zero" % (i, i))
        s = y[i]
        for j in range(i + 1, n):
            s -= r[i][j] * x[j]
        x[i] = s / r[i][i]
    return x


def numerical_rank(r: list[list[float]], tol: float) -> int:
    """Number of diagonal entries of R with |r_kk| > tol. Without column pivoting this is only a heuristic."""
    return sum(1 for i in range(len(r)) if abs(r[i][i]) > tol)
