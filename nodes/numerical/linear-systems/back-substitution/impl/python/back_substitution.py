# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/back-substitution/. The authors are listed in prov/4HMP35.jsonl.

"""Forward and back substitution for triangular systems, in floating point.

Matrices are lists of rows (lists of floats). Only the triangle that the
method needs is read, so the other triangle may hold anything.
"""


def back_substitution(u: list[list[float]], b: list[float]) -> list[float]:
    """Solve U x = b for an upper triangular n by n matrix U.

    Precondition: len(u) == len(b) == n >= 1 and each row has n entries.
    Raises ValueError when a diagonal entry is zero (U is singular).
    Cost: n^2 flops and Theta(1) extra space besides the output.
    The computed x satisfies (U + dU) x = b with |dU| <= gamma_n |U|.
    """
    n = len(b)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):  # @line L1
        if u[i][i] == 0.0:  # @line L2
            raise ValueError("singular: zero diagonal entry at row %d" % i)
        s = b[i]  # @line L3
        row = u[i]
        for j in range(i + 1, n):  # @line L4
            s -= row[j] * x[j]  # @line L5
        x[i] = s / row[i]  # @line L6
    return x  # @line L7


def forward_substitution(l: list[list[float]], b: list[float], unit_diagonal: bool = False) -> list[float]:
    """Solve L x = b for a lower triangular n by n matrix L.

    With unit_diagonal=True the diagonal is taken as 1 and is not read.
    Raises ValueError when a diagonal entry is zero. Cost: n^2 flops
    (n^2 - n with a unit diagonal).
    """
    n = len(b)
    x = [0.0] * n
    for i in range(n):  # @line F1
        if not unit_diagonal and l[i][i] == 0.0:  # @line F2
            raise ValueError("singular: zero diagonal entry at row %d" % i)
        s = b[i]  # @line F3
        row = l[i]
        for j in range(i):  # @line F4
            s -= row[j] * x[j]  # @line F5
        x[i] = s if unit_diagonal else s / row[i]  # @line F6
    return x  # @line F7
