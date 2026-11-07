# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-elimination/. The authors are listed in prov/82ZZ65.jsonl.

from fractions import Fraction
from typing import Sequence


def gaussian_elimination(a: Sequence[Sequence[int | Fraction]], n: int | None = None) -> tuple[list[list[Fraction]], int, list[int]]:
    """Bring an m by n matrix over Q to row echelon form by row operations.

    Returns (e, r, pivots): e is an echelon form of a (a new matrix, a is not changed), r is the rank,
    and pivots lists the r pivot columns (0-based, increasing). Pass n when a has no rows.
    Cost: O(m n min(m, n)) field operations; with Fraction the entries stay quotients of minors of a.
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
        for i in range(r + 1, m):  # @line L6
            f = e[i][j] / e[r][j]  # @line L7
            if f != 0:
                row_i, row_r = e[i], e[r]
                for t in range(j, n):  # @line L8
                    row_i[t] -= f * row_r[t]
        pivots.append(j)  # @line L9
        r += 1  # @line L10
    return e, r, pivots  # @line L11


def solve(a: Sequence[Sequence[int | Fraction]], b: Sequence[int | Fraction]) -> list[Fraction] | None:
    """Return one solution x of a x = b over Q, or None when there is none. Free variables are set to 0.

    Cost: the elimination of the m by (n + 1) augmented matrix, then O(n r) for back substitution.
    """
    m = len(a)
    n = len(a[0]) if m else 0
    aug = [list(a[i]) + [b[i]] for i in range(m)]
    e, r, pivots = gaussian_elimination(aug, n + 1)
    if r > 0 and pivots[-1] == n:
        return None  # a row 0 = nonzero
    x = [Fraction(0)] * n
    for k in range(r - 1, -1, -1):
        j = pivots[k]
        s = e[k][n] - sum((e[k][t] * x[t] for t in range(j + 1, n)), Fraction(0))
        x[j] = s / e[k][j]
    return x
