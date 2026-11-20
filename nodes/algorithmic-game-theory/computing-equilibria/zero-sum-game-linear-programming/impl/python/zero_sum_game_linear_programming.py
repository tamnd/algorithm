# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-sum-game-linear-programming/. The authors are listed in prov/6NAYNS.jsonl.
"""Solve a two-player zero-sum matrix game by one linear program and its dual.

The game is a matrix M with m rows and n columns: when the row player plays i and the
column player plays j, the column player pays M[i][j] to the row player. The row player
maximizes and the column player minimizes. All arithmetic is exact, in Fraction.
"""

from fractions import Fraction

from agtlp import lp_max, lp_min


def _shift(M):
    M = [[Fraction(v) for v in row] for row in M]
    if not M or not M[0] or any(len(row) != len(M[0]) for row in M):
        raise ValueError("M must be a nonempty m by n matrix")
    k = 1 - min(min(row) for row in M)  # @line L1
    Mp = [[v + k for v in row] for row in M]  # @line L2
    return M, k, Mp


def zero_sum_lp(M):
    """Return (value, x, y): the value of the game, an optimal mixed strategy x of the row
    player and an optimal mixed strategy y of the column player.

    x comes from the primal LP of the row player and y from its dual.
    """
    M, k, Mp = _shift(M)
    m, n = len(M), len(M[0])
    # The variables are x_0, ..., x_(m-1) and v, in this order.
    c = [0] * m + [1]  # @line L3
    A_ub = [[-Mp[i][j] for i in range(m)] + [1] for j in range(n)]  # @line L4
    b_ub = [0] * n
    A_eq = [[1] * m + [0]]  # @line L5
    b_eq = [1]
    status, z, v, dual = lp_max(c, A_ub, b_ub, A_eq, b_eq)  # @line L6
    if status != "optimal":
        raise AssertionError("the LP of a matrix game is always feasible and bounded")
    x, y = z[:m], dual[:n]
    return v - k, x, y  # @line L7


def column_player_lp(M):
    """Return (value, y) from the LP of the column player, solved on its own.

    This minimizes w subject to sum_j M'[i][j] y_j <= w for each row i, sum_j y_j = 1 and
    y >= 0, where M' is the shifted matrix. It is the dual of the LP of zero_sum_lp, and
    serves as a second way to get y.
    """
    M, k, Mp = _shift(M)
    m, n = len(M), len(M[0])
    c = [0] * n + [1]
    A_ub = [Mp[i] + [-1] for i in range(m)]
    A_eq = [[1] * n + [0]]
    status, z, w, _ = lp_min(c, A_ub, [0] * m, A_eq, [1])
    if status != "optimal":
        raise AssertionError("the LP of a matrix game is always feasible and bounded")
    return w - k, z[:n]


def guarantees(M, x, y):
    """Return (lo, hi): the least payoff that x guarantees against every column, and the
    largest payoff that y concedes against every row. x and y are optimal if and only if
    lo == hi, and then lo is the value."""
    m, n = len(M), len(M[0])
    lo = min(sum((x[i] * M[i][j] for i in range(m)), Fraction(0)) for j in range(n))
    hi = max(sum((M[i][j] * y[j] for j in range(n)), Fraction(0)) for i in range(m))
    return lo, hi
