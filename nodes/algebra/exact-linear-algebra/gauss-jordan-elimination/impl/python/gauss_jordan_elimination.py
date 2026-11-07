# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-jordan-elimination/. The authors are listed in prov/NK577G.jsonl.

from fractions import Fraction
from typing import Sequence


def gauss_jordan_elimination(a: Sequence[Sequence[int | Fraction]], n: int | None = None) -> tuple[list[list[Fraction]], int, list[int]]:
    """Return (e, r, pivots): the reduced row echelon form e of the m by n matrix a over Q,
    its rank r and its pivot columns (0-based). The input is not changed. Pass n when a has no rows.
    Cost: O(m n min(m, n)) field operations.
    """
    e = [[Fraction(x) for x in row] for row in a]
    m = len(e)
    if n is None:
        n = len(e[0]) if m else 0
    r, pivots = 0, []  # @line L1
    for j in range(n):  # @line L2
        p = next((i for i in range(r, m) if e[i][j] != 0), None)  # @line L3
        if p is None:  # @line L4
            continue
        e[r], e[p] = e[p], e[r]  # @line L5
        c = e[r][j]  # @line L6
        row_r = e[r]
        for t in range(j, n):
            row_r[t] /= c
        for i in range(m):  # @line L7
            if i == r:
                continue
            f = e[i][j]  # @line L8
            if f != 0:
                row_i = e[i]
                for t in range(j, n):  # @line L9
                    row_i[t] -= f * row_r[t]
        pivots.append(j)  # @line L10
        r += 1
    return e, r, pivots  # @line L11


def inverse(a: Sequence[Sequence[int | Fraction]]) -> list[list[Fraction]] | None:
    """Return the inverse of the n by n matrix a over Q, or None when a is singular.

    Runs Gauss-Jordan on [a | I]; a is invertible exactly when the pivots are the columns 0..n-1.
    Cost: O(n^3) field operations.
    """
    n = len(a)
    aug = [list(a[i]) + [int(i == j) for j in range(n)] for i in range(n)]
    e, r, pivots = gauss_jordan_elimination(aug, 2 * n)
    if pivots != list(range(n)):
        return None
    return [row[n:] for row in e]


def solve(a: Sequence[Sequence[int | Fraction]], b: Sequence[int | Fraction]) -> list[Fraction] | None:
    """Return one solution x of a x = b over Q (free variables set to 0), or None when there is none.

    Runs Gauss-Jordan on [a | b]; the system is inconsistent exactly when the last column is a pivot.
    Cost: O(m n min(m, n)) field operations for an m by n matrix a.
    """
    m = len(a)
    n = len(a[0]) if m else 0
    e, r, pivots = gauss_jordan_elimination([list(a[i]) + [b[i]] for i in range(m)], n + 1)
    if pivots and pivots[-1] == n:
        return None
    x = [Fraction(0)] * n
    for i, j in enumerate(pivots):
        x[j] = e[i][n]
    return x
