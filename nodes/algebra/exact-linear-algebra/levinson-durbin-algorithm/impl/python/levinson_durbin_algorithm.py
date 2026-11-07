# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levinson-durbin-algorithm/. The authors are listed in prov/44KZ70.jsonl.

"""Exact Levinson-Durbin recursion for Toeplitz systems T x = c over Q or Z/pZ."""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]


class LeadingMinorZero(ValueError):
    """Raised when a leading principal minor of T is zero, so the recursion cannot continue."""


def _norm(x: Number, p: Optional[int]) -> Number:
    return Fraction(x) if p is None else int(x) % p


def _inv(x: Number, p: Optional[int]) -> Number:
    return 1 / Fraction(x) if p is None else pow(int(x), -1, p)


def levinson_durbin(col: list[Number], row: list[Number], c: list[Number], p: Optional[int] = None) -> list[Number]:
    """Solve T x = c for the n by n Toeplitz matrix T with T[i][j] = t_(i-j).

    col = (t_0, t_1, ..., t_(n-1)) is the first column and row = (t_0, t_-1, ...,
    t_-(n-1)) the first row, so col[0] must equal row[0]. Arithmetic is exact
    over Q (p is None) or over Z/pZ for a prime p. Every leading principal minor
    of T must be nonzero; otherwise LeadingMinorZero is raised, also when T itself
    is nonsingular. Cost: 7 n^2 + O(n) field operations and O(n) extra space.
    """
    n = len(c)
    if len(col) != n or len(row) != n:
        raise ValueError("col, row and c must have the same length")
    if n == 0:  # @line L1
        return []
    if _norm(col[0], p) != _norm(row[0], p):
        raise ValueError("col[0] and row[0] are both t_0 and must be equal")

    def t(k: int) -> Number:
        return _norm(col[k], p) if k >= 0 else _norm(row[-k], p)

    def red(x: Number) -> Number:
        return x if p is None else x % p

    if t(0) == 0:  # @line L2
        raise LeadingMinorZero("the leading 1 by 1 minor t_0 is zero")
    inv0 = _inv(t(0), p)
    f = [inv0]  # @line L3
    g = [inv0]
    x = [red(_norm(c[0], p) * inv0)]
    for k in range(1, n):  # @line L4
        ef = red(sum((t(k - j) * f[j] for j in range(k)), _norm(0, p)))  # @line L5
        eg = red(sum((t(-1 - j) * g[j] for j in range(k)), _norm(0, p)))
        ex = red(sum((t(k - j) * x[j] for j in range(k)), _norm(0, p)))
        d = red(1 - ef * eg)  # @line L6
        if d == 0:
            raise LeadingMinorZero(f"the leading {k + 1} by {k + 1} minor is zero")
        dinv = _inv(d, p)
        fe = f + [_norm(0, p)]  # @line L7
        ge = [_norm(0, p)] + g
        f = [red((a - ef * b) * dinv) for a, b in zip(fe, ge)]
        g = [red((b - eg * a) * dinv) for a, b in zip(fe, ge)]
        mu = red(_norm(c[k], p) - ex)  # @line L8
        x = [red(a + mu * b) for a, b in zip(x + [_norm(0, p)], g)]
    return x  # @line L9


def toeplitz_matrix(col: list[Number], row: list[Number]) -> list[list[Number]]:
    """Return the dense n by n Toeplitz matrix with first column col and first row row."""
    n = len(col)
    return [[col[i - j] if i >= j else row[j - i] for j in range(n)] for i in range(n)]
