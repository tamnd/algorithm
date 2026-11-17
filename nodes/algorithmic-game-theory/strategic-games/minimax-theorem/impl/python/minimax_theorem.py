# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimax-theorem/. The authors are listed in prov/C14532.jsonl.

"""Exact value and optimal mixed strategies of a finite matrix game.

The row player picks a row and maximizes, the column player picks a column
and minimizes, and M[i][j] is the payment from the column player to the row
player. The game is solved by one linear program in exact rational
arithmetic: the primal gives an optimal strategy of the column player and
the dual, read from the final objective row, gives one of the row player.
"""

from fractions import Fraction
from typing import Sequence

Number = int | Fraction
Matrix = Sequence[Sequence[Number]]


def solve_matrix_game(m: Matrix) -> tuple[Fraction, list[Fraction], list[Fraction]]:
    """Return (v, x, y): the value, a maximin row strategy and a minimax column strategy.

    Precondition: m is a nonempty list of nonempty rows of equal length, with
    integer or Fraction entries.
    Postcondition: min_j (x^T M)_j = v = max_i (M y)_i.
    Cost: the simplex method with Bland's rule on an r by (c + r) tableau,
    O(r (c + r)) exact operations per pivot. Bland's rule never cycles, but the
    number of pivots can be exponential in the worst case.
    """
    rows = len(m)
    cols = len(m[0])
    if rows == 0 or cols == 0 or any(len(r) != cols for r in m):
        raise ValueError("m must be a nonempty rectangular matrix")
    low = min(min(r) for r in m)
    shift = Fraction(1) - low if low <= 0 else Fraction(0)
    # Tableau rows: sum_j (M[i][j] + shift) u_j + s_i = 1. Variables 0..cols-1
    # are u, variables cols..cols+rows-1 are the slacks s.
    width = cols + rows
    tab = []
    for i in range(rows):
        row = [Fraction(m[i][j]) + shift for j in range(cols)]
        row += [Fraction(1) if k == i else Fraction(0) for k in range(rows)]
        row.append(Fraction(1))
        tab.append(row)
    # Objective row for maximize sum u_j, stored as z - sum u_j = 0.
    obj = [Fraction(-1)] * cols + [Fraction(0)] * rows + [Fraction(0)]
    basis = [cols + i for i in range(rows)]
    while True:
        enter = next((j for j in range(width) if obj[j] < 0), -1)
        if enter < 0:
            break
        best = -1
        for i in range(rows):
            a = tab[i][enter]
            if a > 0:
                if best < 0:
                    best = i
                    continue
                lhs = tab[i][-1] * tab[best][enter]
                rhs = tab[best][-1] * a
                if lhs < rhs or (lhs == rhs and basis[i] < basis[best]):
                    best = i
        # The shifted matrix is positive, so the LP is bounded and best >= 0.
        piv = tab[best][enter]
        tab[best] = [t / piv for t in tab[best]]
        for i in range(rows):
            if i != best and tab[i][enter] != 0:
                f = tab[i][enter]
                tab[i] = [a - f * b for a, b in zip(tab[i], tab[best])]
        f = obj[enter]
        obj = [a - f * b for a, b in zip(obj, tab[best])]
        basis[best] = enter
    u = [Fraction(0)] * cols
    for i, b in enumerate(basis):
        if b < cols:
            u[b] = tab[i][-1]
    w = [obj[cols + i] for i in range(rows)]
    total = obj[-1]
    shifted_value = 1 / total
    y = [uj * shifted_value for uj in u]
    x = [wi * shifted_value for wi in w]
    return shifted_value - shift, x, y


def row_payoffs(m: Matrix, y: Sequence[Number]) -> list[Fraction]:
    """Return the vector M y: the payoff of each pure row against y. Cost O(r c)."""
    return [sum((Fraction(a) * b for a, b in zip(r, y)), Fraction(0)) for r in m]


def column_payoffs(m: Matrix, x: Sequence[Number]) -> list[Fraction]:
    """Return the vector x^T M: the payoff of each pure column against x. Cost O(r c)."""
    cols = len(m[0])
    return [sum((Fraction(m[i][j]) * x[i] for i in range(len(m))), Fraction(0)) for j in range(cols)]


def pure_maximin(m: Matrix) -> Fraction:
    """Return max_i min_j M[i][j], the security level of the row player in pure strategies."""
    return Fraction(max(min(r) for r in m))


def pure_minimax(m: Matrix) -> Fraction:
    """Return min_j max_i M[i][j], the security level of the column player in pure strategies."""
    cols = len(m[0])
    return Fraction(min(max(r[j] for r in m) for j in range(cols)))
