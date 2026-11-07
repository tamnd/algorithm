# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cholesky-decomposition/. The authors are listed in prov/4WHW5Y.jsonl.

"""Cholesky decomposition A = R^T R of a symmetric positive definite matrix, in floating point.

Matrices are lists of rows of floats. Only the upper triangle of A is read.
"""

import math


class NotPositiveDefinite(ValueError):
    """Raised when a pivot s <= 0 appears: A is not (numerically) positive definite."""


def cholesky(a: list[list[float]]) -> list[list[float]]:
    """Return the upper triangular R with positive diagonal and R^T R = A.

    Precondition: a is n by n, n >= 1, symmetric (only a[j][i] with i >= j is read).
    Raises NotPositiveDefinite when line L3 finds s <= 0.
    Cost: n^3/3 + n^2/2 - 5n/6 flops and n square roots; Theta(n^2) space for R.
    In floating point R^T R = A + dA with |dA| <= gamma_(n+1) |R^T| |R|.
    """
    n = len(a)
    r = [[0.0] * n for _ in range(n)]
    for j in range(n):  # @line L1
        s = a[j][j]
        for k in range(j):
            s -= r[k][j] * r[k][j]  # @line L2
        if s <= 0.0:  # @line L3
            raise NotPositiveDefinite("pivot %r at column %d" % (s, j))
        rjj = math.sqrt(s)  # @line L4
        r[j][j] = rjj
        for i in range(j + 1, n):  # @line L5
            t = a[j][i]
            for k in range(j):
                t -= r[k][j] * r[k][i]
            r[j][i] = t / rjj  # @line L6
    return r  # @line L7


def cholesky_solve(r: list[list[float]], b: list[float]) -> list[float]:
    """Solve R^T R x = b by forward substitution with R^T, then back substitution with R.

    Cost: 2n^2 flops. The result satisfies (A + dA) x = b with |dA| <= gamma_(3n+1) |R^T| |R|.
    """
    n = len(b)
    y = [0.0] * n
    for i in range(n):  # @line S1: R^T y = b, column i of R is row i of R^T
        s = b[i]
        for k in range(i):
            s -= r[k][i] * y[k]
        y[i] = s / r[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):  # @line S2: R x = y
        s = y[i]
        row = r[i]
        for k in range(i + 1, n):
            s -= row[k] * x[k]
        x[i] = s / row[i]
    return x  # @line S3
