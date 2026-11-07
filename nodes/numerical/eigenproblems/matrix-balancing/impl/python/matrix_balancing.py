# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-balancing/. The authors are listed in prov/T97X37.jsonl.

"""Parlett-Reinsch balancing of a square matrix by a diagonal similarity.

balance(a, radix, maxsweeps) returns B = D^-1 A D with D diagonal, whose
entries are powers of the radix, so that every scaling is exact in binary
floating point (barring overflow and underflow) and B has exactly the same
eigenvalues as A. For each index i in turn it compares the off-diagonal
1-norms c of column i and r of row i, and scales column i by f and row i by
1/f, with f the power of the radix that makes c f and r / f closest, when this
lowers c + r by at least 5 percent. Standard library only.
"""

from typing import NamedTuple


class BalanceResult(NamedTuple):
    b: list  # the balanced matrix D^-1 A D, a new list of rows
    d: list  # the diagonal of D, powers of the radix
    sweeps: int  # the number of sweeps over the indices
    converged: bool  # True if the last sweep changed nothing
    updates: int  # the number of accepted scalings


def offdiag_norms(b, i):
    """(c, r): the off-diagonal 1-norms of column i and row i."""
    n = len(b)
    c = sum(abs(b[j][i]) for j in range(n) if j != i)
    r = sum(abs(b[i][j]) for j in range(n) if j != i)
    return c, r


def offdiag_sum(b):
    n = len(b)
    return sum(abs(b[i][j]) for i in range(n) for j in range(n) if i != j)


def balance(a, radix=2.0, maxsweeps=100, factor=0.95):
    """Return a BalanceResult for the square matrix a (a list of rows of floats)."""
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("the matrix must be square")
    if radix < 2:
        raise ValueError("the radix must be at least 2")
    b = [list(map(float, row)) for row in a]
    d = [1.0] * n  # @line L1
    radix2 = radix * radix
    updates = 0
    for sweep in range(1, maxsweeps + 1):  # @line L2
        done = True  # @line L3
        for i in range(n):  # @line L4
            c, r = offdiag_norms(b, i)  # @line L5
            if c == 0.0 or r == 0.0:  # @line L6
                continue
            s = c + r
            f = 1.0  # @line L7
            g = r / radix
            while c < g:
                f *= radix
                c *= radix2
            g = r * radix
            while c >= g:
                f /= radix
                c /= radix2
            # now c holds c_old * f^2, with r / radix <= c < r * radix
            if (c + r) / f < factor * s:  # @line L8
                done = False  # @line L9
                updates += 1
                d[i] *= f
                for j in range(n):
                    b[j][i] *= f  # column i times f
                for j in range(n):
                    b[i][j] /= f  # row i over f (the diagonal entry is unchanged)
        if done:  # @line L10
            return BalanceResult(b, d, sweep, True, updates)
    return BalanceResult(b, d, maxsweeps, False, updates)  # @line L11
