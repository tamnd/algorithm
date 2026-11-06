# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/babai-rounding/. The authors are listed in prov/24ANYQ.jsonl.

from fractions import Fraction
from math import floor
from typing import Sequence, Union

Number = Union[int, Fraction]


def _dot(u: Sequence[Number], v: Sequence[Number]) -> Fraction:
    return Fraction(sum((a * b for a, b in zip(u, v)), 0))


def _nearest(x: Fraction) -> int:
    """The integer nearest to x; a half is rounded up, so -1/2 <= x - result < 1/2."""
    return floor(x + Fraction(1, 2))


def _solve(g: list[list[Fraction]], r: list[Fraction]) -> list[Fraction]:
    """Solve g y = r for a nonsingular square matrix g by exact Gauss-Jordan elimination."""
    n = len(g)
    a = [row[:] + [r[i]] for i, row in enumerate(g)]
    for c in range(n):
        p = next((i for i in range(c, n) if a[i][c] != 0), None)
        if p is None:
            raise ValueError("the basis vectors are linearly dependent")
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [x / piv for x in a[c]]
        for i in range(n):
            if i != c and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return [a[i][n] for i in range(n)]


def babai_rounding(basis: Sequence[Sequence[Number]], target: Sequence[Number]) -> tuple[list[int], list[Fraction]]:
    """Babai's rounding method for the closest vector problem.

    Input: n >= 1 linearly independent rows b_1..b_n of length m (int or Fraction
    entries, exact arithmetic) and a target t of length m. Output: (x, v) with x an
    integer vector and v = x_1 b_1 + ... + x_n b_n, where x_i is the nearest
    integer to the coordinate y_i of the projection of t onto the span.
    If t = u + e with u in the lattice and |<e, d_i>| < 1/2 for every dual basis
    row d_i, then v = u.
    Cost: O(n^2 m + n^3) arithmetic operations on rationals for the Gram matrix
    and the solve, then O(n m) for the rounding and the combination.
    Raises ValueError for dependent rows or mismatched lengths.
    """
    b = [[Fraction(c) for c in row] for row in basis]
    t = [Fraction(c) for c in target]
    n = len(b)
    if n == 0 or any(len(row) != len(t) for row in b):
        raise ValueError("need at least one basis row, all of the target's length")
    g = [[_dot(bi, bj) for bj in b] for bi in b]  # @line L1
    y = _solve(g, [_dot(bi, t) for bi in b])  # @line L2
    x = [_nearest(yi) for yi in y]  # @line L3
    v = [sum((xi * row[j] for xi, row in zip(x, b)), Fraction(0)) for j in range(len(t))]  # @line L4
    return x, v  # @line L5
