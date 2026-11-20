# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dmp-half-approximate-nash/. The authors are listed in prov/F0ZSX8.jsonl.
"""The Daskalakis-Mehta-Papadimitriou algorithm for a 1/2-approximate Nash equilibrium.

The row player gets A[i][j] and the column player gets B[i][j]; both maximize. If all the
payoffs are in [0, 1], the output is a 1/2-Nash equilibrium in the additive sense: no player
gains more than 1/2 by a deviation. The method reads one row of B and one column of A, so
it reads m + n entries. Ties go to the smallest index.
"""

from fractions import Fraction


def dmp(A, B, i=0):
    """Return (x, y): x mixes row i and row k with weight 1/2 each, y is the pure column j."""
    m, n = len(A), len(A[0])
    j = max(range(n), key=lambda c: (B[i][c], -c))  # @line L1
    k = max(range(m), key=lambda r: (A[r][j], -r))  # @line L2
    x = [Fraction(0)] * m  # @line L3
    x[i] += Fraction(1, 2)
    x[k] += Fraction(1, 2)
    y = [Fraction(0)] * n  # @line L4
    y[j] = Fraction(1)
    return x, y  # @line L5


def gains(A, B, x, y):
    """Return the largest gain of the row player and of the column player from a pure deviation."""
    m, n = len(A), len(A[0])
    Ay = [sum((Fraction(A[r][c]) * y[c] for c in range(n)), Fraction(0)) for r in range(m)]
    xB = [sum((x[r] * Fraction(B[r][c]) for r in range(m)), Fraction(0)) for c in range(n)]
    u = sum((x[r] * Ay[r] for r in range(m)), Fraction(0))
    v = sum((xB[c] * y[c] for c in range(n)), Fraction(0))
    return max(Ay) - u, max(xB) - v
