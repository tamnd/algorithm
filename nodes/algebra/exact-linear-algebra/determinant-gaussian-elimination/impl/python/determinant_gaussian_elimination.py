# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinant-gaussian-elimination/. The authors are listed in prov/KQ2JBB.jsonl.

from fractions import Fraction
from typing import Any, Sequence


def determinant_gaussian_elimination(a: Sequence[Sequence[Any]]) -> Any:
    """Return det(a) for an n by n matrix over a field, by elimination to triangular form.

    Integers are read as Fractions; other entries (for example elements of Z/pZ) must support
    +, -, *, / and comparison with 0. The input is not changed. The empty matrix has determinant 1.
    Cost: 2n^3/3 + O(n^2) field operations.
    """
    e = [[Fraction(x) if isinstance(x, int) else x for x in row] for row in a]
    n = len(e)
    d = 1  # @line L1
    for k in range(n):  # @line L2
        p = next((i for i in range(k, n) if e[i][k] != 0), None)  # @line L3
        if p is None:  # @line L4
            return 0 * d
        if p != k:  # @line L5
            e[k], e[p] = e[p], e[k]
            d = -d
        d = d * e[k][k]  # @line L6
        for i in range(k + 1, n):  # @line L7
            f = e[i][k] / e[k][k]  # @line L8
            if f != 0:
                row_i, row_k = e[i], e[k]
                for t in range(k + 1, n):  # @line L9
                    row_i[t] = row_i[t] - f * row_k[t]
    return d  # @line L10
