# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kraut-determinant/. The authors are listed in prov/VFMNY1.jsonl.

from fractions import Fraction
from typing import Any, Sequence


def crout(a: Sequence[Sequence[Any]]) -> tuple[list[list[Any]], list[int], int] | None:
    """Crout (Kraut) factorization with row swaps over a field.

    Returns (w, perm, s) such that, with P the rows of a in the order perm, P = L U, where L is
    the lower triangle of w (with its diagonal) and U is the strict upper triangle of w with a unit
    diagonal; s = +1 or -1 is the sign of the permutation. Returns None when a is singular.
    Integers are converted to Fraction; other field elements are used as they are.
    Cost: 2n^3/3 + O(n^2) field operations.
    """
    w = [[Fraction(x) if isinstance(x, int) else x for x in row] for row in a]
    n = len(w)
    perm = list(range(n))
    s = 1  # @line L1
    for j in range(n):  # @line L2
        for i in range(j, n):  # @line L3
            acc = w[i][j]
            for k in range(j):
                acc = acc - w[i][k] * w[k][j]
            w[i][j] = acc
        p = next((i for i in range(j, n) if w[i][j] != 0), None)  # @line L4
        if p is None:  # @line L5
            return None
        if p != j:  # @line L6
            w[j], w[p] = w[p], w[j]
            perm[j], perm[p] = perm[p], perm[j]
            s = -s
        piv = w[j][j]
        for t in range(j + 1, n):  # @line L7
            acc = w[j][t]
            for k in range(j):
                acc = acc - w[j][k] * w[k][t]
            w[j][t] = acc / piv
    return w, perm, s


def kraut_determinant(a: Sequence[Sequence[Any]]) -> Any:
    """Return det a for a square matrix over a field (ints become Fraction), by Crout's method.

    Cost: 2n^3/3 + O(n^2) field operations.
    """
    if not a:
        return Fraction(1)
    res = crout(a)
    if res is None:
        z = Fraction(a[0][0]) if isinstance(a[0][0], int) else a[0][0]
        return z - z
    w, _, s = res
    d = w[0][0] if s == 1 else -w[0][0]  # @line L8
    for j in range(1, len(w)):  # @line L9
        d = d * w[j][j]
    return d  # @line L10
