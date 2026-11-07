# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lup-solve/. The authors are listed in prov/XY7DX3.jsonl.

"""Solve A x = b from the factorization P A = L U by forward and back substitution.

Matrices are lists of rows of floats (or fractions.Fraction for exact work).
The factorization helper lup_factor is included so that the file stands alone.
"""

from fractions import Fraction
from typing import TypeVar

T = TypeVar("T", float, Fraction)


class SingularMatrix(ValueError):
    """Raised when a pivot column (in lup_factor) or a diagonal entry of U (in lup_solve) is zero."""


def lup_factor(a: list[list[T]]) -> tuple[list[list[T]], list[int]]:
    """Gaussian elimination with partial pivoting: return (lu, perm) with row k of P A = row perm[k] of A.

    L (unit lower triangular) is stored below the diagonal of lu, U on and above it.
    Cost: 2n^3/3 - n^2/2 - n/6 flops.
    """
    n = len(a)
    lu = [list(row) for row in a]
    perm = list(range(n))
    for k in range(n):
        p = k
        for i in range(k + 1, n):
            if abs(lu[i][k]) > abs(lu[p][k]):
                p = i
        if lu[p][k] == 0:
            raise SingularMatrix("zero pivot column at step %d" % k)
        if p != k:
            perm[k], perm[p] = perm[p], perm[k]
            lu[k], lu[p] = lu[p], lu[k]
        for i in range(k + 1, n):
            lik = lu[i][k] / lu[k][k]
            lu[i][k] = lik
            for j in range(k + 1, n):
                lu[i][j] = lu[i][j] - lik * lu[k][j]
    return lu, perm


def lup_solve(lu: list[list[T]], perm: list[int], b: list[T]) -> list[T]:
    """Return x with L U x = P b, that is A x = b when P A = L U.

    Precondition: lu and perm come from lup_factor (or any compact LU with unit L),
    and len(b) == n. Raises SingularMatrix if a diagonal entry of U is zero.
    Cost: 2n^2 - n flops, Theta(n) extra space.
    In floating point (A + dA) x = b with |dA| <= gamma_(3n) P^T |L| |U| (Higham, Theorem 9.4).
    """
    n = len(b)
    y = [b[0]] * n
    for i in range(n):  # @line L1
        s = b[perm[i]]
        row = lu[i]
        for j in range(i):
            s = s - row[j] * y[j]
        y[i] = s  # @line L2: forward substitution with the unit lower triangular L
    x = [b[0]] * n
    for i in range(n - 1, -1, -1):  # @line L3
        s = y[i]
        row = lu[i]
        for j in range(i + 1, n):
            s = s - row[j] * x[j]
        if row[i] == 0:
            raise SingularMatrix("u_%d%d is zero" % (i, i))
        x[i] = s / row[i]  # @line L4: back substitution with U
    return x  # @line L5


def solve(a: list[list[T]], b: list[T]) -> list[T]:
    """Factor A once and solve A x = b."""
    lu, perm = lup_factor(a)
    return lup_solve(lu, perm, b)
