# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tridiagonalization/. The authors are listed in prov/9W3V78.jsonl.

"""Householder tridiagonalization of a real symmetric matrix.

tridiagonalize(a) returns (d, e, q, flops) with A = Q T Q^T, where T is the
symmetric tridiagonal matrix with diagonal d and off-diagonal e, and Q is
orthogonal. Each step uses one Householder reflector and the symmetric rank-2
update A22 <- A22 - v w^T - w v^T, computed on the lower triangle only. Q is
formed afterwards by backward accumulation. flops counts the floating-point
operations of the two phases from the loop lengths, so that tests can compare
it with 4 n^3 / 3 for each phase.
Standard library only.
"""

import math
from typing import NamedTuple


class TridiagResult(NamedTuple):
    d: list  # diagonal of T, length n
    e: list  # off-diagonal of T, length n - 1
    q: list  # orthogonal Q with A = Q T Q^T (None if want_q is False)
    flops: tuple  # (reduction flops, accumulation flops)


def house(x):
    """Return (v, beta, alpha) with (I - beta v v^T) x = alpha e_1 and beta = 0 if x is already a multiple of e_1."""
    sigma = sum(t * t for t in x[1:])
    if sigma == 0.0:
        return [1.0] + [0.0] * (len(x) - 1), 0.0, x[0]
    alpha = -math.copysign(math.sqrt(x[0] * x[0] + sigma), x[0])
    v = x[:]
    v[0] -= alpha  # no cancellation: x[0] and -alpha have the same sign
    beta = 2.0 / (v[0] * v[0] + sigma)
    return v, beta, alpha


def tridiagonalize(a, want_q=True):
    n = len(a)
    if n == 0 or any(len(row) != n for row in a):
        raise ValueError("a must be a nonempty square matrix")
    # work on the lower triangle of a copy; the upper triangle is never read
    w_ = [[float(a[i][j]) for j in range(i + 1)] for i in range(n)]

    def get(i, j):
        return w_[i][j] if i >= j else w_[j][i]

    q = [[float(i == j) for j in range(n)] for i in range(n)]  # @line L1
    reflectors = []
    e = []
    f_red = 0
    for k in range(n - 2):  # @line L2
        m = n - k - 1
        x = [w_[k + 1 + i][k] for i in range(m)]  # @line L3
        v, beta, alpha = house(x)  # @line L4
        reflectors.append((v, beta))
        e.append(alpha)
        if beta == 0.0:
            continue
        # p = beta * A22 v, using the symmetric lower triangle
        p = [beta * sum(get(k + 1 + i, k + 1 + j) * v[j] for j in range(m)) for i in range(m)]  # @line L5
        c = beta * sum(p[i] * v[i] for i in range(m)) / 2.0
        w = [p[i] - c * v[i] for i in range(m)]  # @line L6
        for i in range(m):  # @line L7
            row = w_[k + 1 + i]
            for j in range(i + 1):
                row[k + 1 + j] -= v[i] * w[j] + w[i] * v[j]
        w_[k + 1][k] = alpha  # @line L8
        for i in range(1, m):
            w_[k + 1 + i][k] = 0.0
        f_red += 2 * m * m + 4 * m + 4 * (m * (m + 1) // 2)
    if n >= 2:
        e.append(w_[n - 1][n - 2])
    d = [w_[i][i] for i in range(n)]
    f_acc = 0
    if not want_q:
        return TridiagResult(d, e, None, (f_red, 0))
    for k in range(n - 3, -1, -1):  # @line L9
        v, beta = reflectors[k]
        if beta == 0.0:
            continue
        m = n - k - 1
        # Q[k+1:, k+1:] <- (I - beta v v^T) Q[k+1:, k+1:]; columns <= k of these rows are still zero
        for j in range(k + 1, n):  # @line L10
            s = beta * sum(v[i] * q[k + 1 + i][j] for i in range(m))
            if s != 0.0:
                for i in range(m):
                    q[k + 1 + i][j] -= s * v[i]
        f_acc += 4 * m * m
    return TridiagResult(d, e, q, (f_red, f_acc))  # @line L11
