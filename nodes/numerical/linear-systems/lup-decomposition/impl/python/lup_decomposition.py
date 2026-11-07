# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lup-decomposition/. The authors are listed in prov/3B5H9A.jsonl.

"""LUP decomposition PA = LU by Gaussian elimination with partial pivoting.

Matrices are lists of rows. The entries may be floats (floating-point LU) or
fractions.Fraction (exact LU); the code uses only +, -, *, / and abs.
"""

from fractions import Fraction
from typing import TypeVar

T = TypeVar("T", float, Fraction)


class SingularMatrix(ValueError):
    """Raised when a whole pivot column is zero: A is singular (exactly, or after rounding)."""


def lup_decomposition(a: list[list[T]]) -> tuple[list[list[T]], list[int]]:
    """Return (lu, perm) with P A = L U.

    Row k of P A is row perm[k] of A. L is unit lower triangular and is stored in
    lu below the diagonal; U is upper triangular and is stored on and above it.
    Each multiplier satisfies |l_ik| <= 1.

    Precondition: a is n by n with n >= 1. The input is not changed.
    Raises SingularMatrix when line L4 finds a zero pivot column.
    Cost: 2n^3/3 - n^2/2 - n/6 flops, n(n-1)/2 comparisons, Theta(n^2) space.
    In floating point the computed factors satisfy L U = P A + dA with
    |dA| <= gamma_n |L| |U| (Higham, Theorem 9.3).
    """
    n = len(a)
    lu = [list(row) for row in a]
    perm = list(range(n))  # @line L1
    for k in range(n):  # @line L2
        p = k
        big = abs(lu[k][k])
        for i in range(k + 1, n):  # @line L3: the first index of largest modulus
            if abs(lu[i][k]) > big:
                p, big = i, abs(lu[i][k])
        if big == 0:  # @line L4
            raise SingularMatrix("zero pivot column at step %d" % k)
        if p != k:  # @line L5: swap the whole rows, multipliers included
            perm[k], perm[p] = perm[p], perm[k]
            lu[k], lu[p] = lu[p], lu[k]
        pivot_row = lu[k]
        pivot = pivot_row[k]
        for i in range(k + 1, n):  # @line L6
            row = lu[i]
            lik = row[k] / pivot  # @line L7
            row[k] = lik
            for j in range(k + 1, n):  # @line L8
                row[j] = row[j] - lik * pivot_row[j]  # @line L9
    return lu, perm  # @line L10


def unpack(lu: list[list[T]]) -> tuple[list[list[T]], list[list[T]]]:
    """Split the compact array into the unit lower triangular L and the upper triangular U."""
    n = len(lu)
    zero = lu[0][0] * 0
    one = zero + 1
    low = [[lu[i][j] if j < i else (one if j == i else zero) for j in range(n)] for i in range(n)]
    up = [[lu[i][j] if j >= i else zero for j in range(n)] for i in range(n)]
    return low, up


def growth_factor(a: list[list[float]]) -> float:
    """Return max_k max_ij |a_ij^(k)| / max_ij |a_ij| over the stages of elimination with partial pivoting."""
    n = len(a)
    m = [list(row) for row in a]
    base = max(abs(v) for row in m for v in row)
    big = base
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        if m[p][k] == 0:
            raise SingularMatrix("zero pivot column at step %d" % k)
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            lik = m[i][k] / m[k][k]
            for j in range(k + 1, n):
                m[i][j] = m[i][j] - lik * m[k][j]
                big = max(big, abs(m[i][j]))
    return big / base
