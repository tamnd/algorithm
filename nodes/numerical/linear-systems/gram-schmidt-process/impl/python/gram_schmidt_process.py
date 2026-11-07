# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gram-schmidt-process/. The authors are listed in prov/5JCA6Q.jsonl.

"""Gram-Schmidt QR of an m by n matrix with full column rank: modified (MGS), classical (CGS),
and classical with one reorthogonalization (CGS2).

Matrices are lists of rows. Each function returns (Q, R) with Q an m by n list of rows with
orthonormal columns (in exact arithmetic) and R an n by n upper triangular list of rows.
A zero column after orthogonalization raises RankDeficient.
"""

import math


class RankDeficient(ValueError):
    pass


def _columns(a):
    if not a or not a[0]:
        raise ValueError("empty matrix")
    m, n = len(a), len(a[0])
    if n > m:
        raise RankDeficient("more columns than rows")
    return m, n, [[float(a[i][j]) for i in range(m)] for j in range(n)]


def _dot(u, v):
    s = 0.0
    for x, y in zip(u, v):
        s += x * y
    return s


def _rows(cols, m):
    return [[c[i] for c in cols] for i in range(m)]


def mgs(a):
    """Modified Gram-Schmidt: each new q_j is removed from all later columns at once."""
    m, n, v = _columns(a)
    r = [[0.0] * n for _ in range(n)]
    q = []
    for j in range(n):  # @line L1
        r[j][j] = math.sqrt(_dot(v[j], v[j]))  # @line L2
        if r[j][j] == 0.0:  # @line L3
            raise RankDeficient(f"column {j} is in the span of the previous columns")
        qj = [x / r[j][j] for x in v[j]]  # @line L4
        q.append(qj)
        for k in range(j + 1, n):  # @line L5
            r[j][k] = _dot(qj, v[k])  # @line L6
            v[k] = [x - r[j][k] * y for x, y in zip(v[k], qj)]  # @line L7
    return _rows(q, m), r  # @line L8


def cgs(a, reorthogonalize=False):
    """Classical Gram-Schmidt: all coefficients of column j come from the original a_j.

    With reorthogonalize=True the projection is repeated once (CGS2, "twice is enough").
    """
    m, n, cols = _columns(a)
    r = [[0.0] * n for _ in range(n)]
    q = []
    for j in range(n):
        v = list(cols[j])
        for _ in range(2 if reorthogonalize else 1):
            coef = [_dot(q[i], v) for i in range(j)]
            for i in range(j):
                r[i][j] += coef[i]
                v = [x - coef[i] * y for x, y in zip(v, q[i])]
        r[j][j] = math.sqrt(_dot(v, v))
        if r[j][j] == 0.0:
            raise RankDeficient(f"column {j} is in the span of the previous columns")
        q.append([x / r[j][j] for x in v])
    return _rows(q, m), r


def least_squares(a, b):
    """Minimize ||b - A x||_2 by MGS on the augmented matrix [A b] (Bjorck 1967)."""
    m, n = len(a), len(a[0])
    aug = [list(map(float, a[i])) + [float(b[i])] for i in range(m)]
    # Orthogonalize the first n columns only; b is treated as one more column to be reduced.
    v = [[aug[i][j] for i in range(m)] for j in range(n + 1)]
    r = [[0.0] * (n + 1) for _ in range(n)]
    for j in range(n):
        r[j][j] = math.sqrt(_dot(v[j], v[j]))
        if r[j][j] == 0.0:
            raise RankDeficient(f"column {j} is in the span of the previous columns")
        qj = [x / r[j][j] for x in v[j]]
        for k in range(j + 1, n + 1):
            r[j][k] = _dot(qj, v[k])
            v[k] = [x - r[j][k] * y for x, y in zip(v[k], qj)]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = r[i][n]
        for j in range(i + 1, n):
            s -= r[i][j] * x[j]
        x[i] = s / r[i][i]
    return x, v[n]  # v[n] is the computed residual vector b - A x
