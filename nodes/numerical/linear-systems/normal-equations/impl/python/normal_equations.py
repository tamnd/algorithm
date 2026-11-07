# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-equations/. The authors are listed in prov/FJBYRZ.jsonl.

"""Solve the least squares problem min ||b - A x||_2 through the normal equations A^T A x = A^T b.

A is m by n with m >= n and full column rank, given as a list of m rows.
Entries may be floats or fractions.Fraction; with Fraction the result is the exact
least squares solution, which the tests use as a reference.
"""

import math
from fractions import Fraction
from typing import TypeVar

T = TypeVar("T", float, Fraction)


class NotFullRank(ValueError):
    """Raised when the Cholesky factorization of A^T A meets a pivot that is not positive."""


def _sqrt(v: T) -> T:
    """Square root; for a Fraction it must be a perfect square, otherwise the float root is used."""
    if isinstance(v, Fraction):
        rn, rd = math.isqrt(v.numerator), math.isqrt(v.denominator)
        if rn * rn == v.numerator and rd * rd == v.denominator:
            return Fraction(rn, rd)
        raise ValueError("exact square root not available")
    return math.sqrt(v)


def gram(a: list[list[T]], b: list[T]) -> tuple[list[list[T]], list[T]]:
    """Return C = A^T A (full symmetric array, lower triangle computed) and d = A^T b.

    Cost: m n (n + 1) flops for C using symmetry, plus 2 m n flops for d.
    """
    m, n = len(a), len(a[0])
    c = [[a[0][0] * 0 for _ in range(n)] for _ in range(n)]
    for i in range(n):  # @line L1
        for j in range(i + 1):
            s = a[0][i] * a[0][j]
            for k in range(1, m):
                s += a[k][i] * a[k][j]
            c[i][j] = s
            c[j][i] = s
    d = []
    for i in range(n):  # @line L2
        s = a[0][i] * b[0]
        for k in range(1, m):
            s += a[k][i] * b[k]
        d.append(s)
    return c, d


def cholesky(c: list[list[T]]) -> list[list[T]]:
    """Return upper triangular R with R^T R = C, or raise NotFullRank.

    Column-oriented Cholesky with square roots. Cost: n^3/3 flops.
    Fraction input works only when every pivot is a perfect square; the exact
    reference exact_least_squares uses a square-root-free LDL^T instead.
    """
    n = len(c)
    r = [[c[0][0] * 0 for _ in range(n)] for _ in range(n)]
    for j in range(n):
        s = c[j][j]
        for k in range(j):
            s -= r[k][j] * r[k][j]
        if not s > 0:
            raise NotFullRank("pivot %d of A^T A is %r, not positive" % (j, s))
        rjj = _sqrt(s)
        r[j][j] = rjj
        for i in range(j + 1, n):
            t = c[j][i]
            for k in range(j):
                t -= r[k][j] * r[k][i]
            r[j][i] = t / rjj
    return r


def normal_equations_solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Least squares solution by the normal equations and Cholesky, in floating point.

    Precondition: m >= n >= 1 and A of full column rank. Raises NotFullRank if
    the computed A^T A is not numerically positive definite (for example when
    kappa_2(A) is about u^(-1/2) or larger).
    Cost: m n^2 + n^3/3 flops to leading order.
    """
    m, n = len(a), len(a[0])
    if m < n:
        raise ValueError("need m >= n")
    c, d = gram(a, b)
    r = cholesky(c)  # @line L3
    y = [0.0] * n
    for i in range(n):  # @line L4
        s = d[i]
        for k in range(i):
            s -= r[k][i] * y[k]
        y[i] = s / r[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):  # @line L5
        s = y[i]
        for k in range(i + 1, n):
            s -= r[i][k] * x[k]
        x[i] = s / r[i][i]
    return x


def exact_least_squares(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Exact least squares solution: the same normal equations, solved by rational LDL^T.

    Raises NotFullRank if A does not have full column rank (exactly).
    """
    a = [[Fraction(v) for v in row] for row in a]
    b = [Fraction(v) for v in b]
    c, d = gram(a, b)
    n = len(c)
    # LDL^T without square roots: c = L D L^T
    lmat = [[Fraction(0)] * n for _ in range(n)]
    dg = [Fraction(0)] * n
    for j in range(n):
        s = c[j][j] - sum(lmat[j][k] ** 2 * dg[k] for k in range(j))
        if s <= 0:
            raise NotFullRank("A does not have full column rank")
        dg[j] = s
        lmat[j][j] = Fraction(1)
        for i in range(j + 1, n):
            lmat[i][j] = (c[i][j] - sum(lmat[i][k] * lmat[j][k] * dg[k] for k in range(j))) / s
    y = [Fraction(0)] * n
    for i in range(n):
        y[i] = d[i] - sum(lmat[i][k] * y[k] for k in range(i))
    z = [y[i] / dg[i] for i in range(n)]
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = z[i] - sum(lmat[k][i] * x[k] for k in range(i + 1, n))
    return x
