# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lu-decomposition/. The authors are listed in prov/EH2SQ6.jsonl.

"""Exact LU decomposition with row swaps, P A = L U, over Q or over Z/pZ."""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Matrix = list[list[Number]]


def _norm(x: Number, p: Optional[int]) -> Number:
    return Fraction(x) if p is None else int(x) % p


def _div(x: Number, y: Number, p: Optional[int]) -> Number:
    if p is None:
        return Fraction(x) / Fraction(y)
    return int(x) * pow(int(y), -1, p) % p


def lu_decomposition(a: Matrix, p: Optional[int] = None) -> tuple[list[int], Matrix, Matrix]:
    """Return (perm, L, U) with P A = L U.

    a is an m by n matrix (a list of m rows of length n) over Q (p is None,
    entries are int or Fraction) or over Z/pZ for a prime p. Row r of P A is
    row perm[r] of A. L is m by m unit lower triangular, U is m by n in row
    echelon form, and its number of nonzero rows is the rank of A. The first
    nonzero entry of a column is the pivot, so the result is deterministic.
    Cost: O(m n min(m, n)) field operations.
    """
    m = len(a)
    n = len(a[0]) if m else 0
    u = [[_norm(x, p) for x in row] for row in a]  # @line L1
    one, zero = _norm(1, p), _norm(0, p)
    low = [[one if i == j else zero for j in range(m)] for i in range(m)]
    perm = list(range(m))
    r = 0
    for c in range(n):  # @line L2
        if r >= m:  # @line L3
            break
        piv = next((i for i in range(r, m) if u[i][c] != 0), None)  # @line L4
        if piv is None:
            continue
        if piv != r:  # @line L5
            u[r], u[piv] = u[piv], u[r]
            perm[r], perm[piv] = perm[piv], perm[r]
            for k in range(r):
                low[r][k], low[piv][k] = low[piv][k], low[r][k]
        for i in range(r + 1, m):  # @line L6
            if u[i][c] == 0:
                continue
            f = _div(u[i][c], u[r][c], p)  # @line L7
            low[i][r] = f
            row_i, row_r = u[i], u[r]
            row_i[c] = zero  # @line L8
            for j in range(c + 1, n):
                if p is None:
                    row_i[j] = row_i[j] - f * row_r[j]
                else:
                    row_i[j] = (row_i[j] - f * row_r[j]) % p
        r += 1  # @line L9
    return perm, low, u  # @line L10


def lu_solve(perm: list[int], low: Matrix, u: Matrix, b: list[Number], p: Optional[int] = None) -> list[Number]:
    """Solve A x = b from P A = L U, for a square nonsingular A.

    Forward substitution gives y with L y = P b, and back substitution gives
    x with U x = y. Raises ZeroDivisionError or ValueError when U has a zero
    diagonal entry, that is when A is singular. Cost: O(n^2) field operations.
    """
    n = len(perm)
    y: list[Number] = []
    for i in range(n):  # @line L11
        s = _norm(b[perm[i]], p)
        for k in range(i):
            s -= low[i][k] * y[k]
        y.append(_norm(s, p))
    x: list[Number] = [_norm(0, p)] * n
    for i in range(n - 1, -1, -1):  # @line L12
        s = y[i]
        for k in range(i + 1, n):
            s -= u[i][k] * x[k]
        x[i] = _div(s, u[i][i], p)
    return x  # @line L13


def lu_determinant(a: Matrix, p: Optional[int] = None) -> Number:
    """Return det A for a square matrix, as sign(P) times the product of the diagonal of U."""
    perm, _, u = lu_decomposition(a, p)
    sign = 1
    seen = [False] * len(perm)
    for i in range(len(perm)):
        if not seen[i]:
            j, length = i, 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                length += 1
            if length % 2 == 0:
                sign = -sign
    d = _norm(sign, p)
    for i in range(len(u)):
        d = _norm(d * u[i][i], p)
    return d
