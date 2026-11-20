# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stackelberg-commitment-algorithm/. The authors are listed in prov/3741KV.jsonl.
"""The optimal mixed strategy to commit to in a bimatrix game, by one LP per follower action.

The leader is the row player with payoff matrix A, the follower is the column player with
payoff matrix B, both m x n. The leader commits to a mixed strategy x; the follower sees x
and plays a best response, breaking ties in the leader's favor (the strong Stackelberg
convention). For each column j, an LP finds the best x among those to which j is a best
response; the answer is the best of these LPs.
"""

from fractions import Fraction

from agtlp import lp_max


def best_for_column(A, B, j):
    """Return (value, x) of max x . A[:, j] over the x in the simplex with j a best response to x.

    Return None if no mixed strategy makes j a best response.
    """
    m, n = len(A), len(A[0])
    c = [A[i][j] for i in range(m)]
    # sum_i x_i B[i][k] <= sum_i x_i B[i][j] for every other column k.
    A_ub = [[B[i][k] - B[i][j] for i in range(m)] for k in range(n) if k != j]  # @line L2
    status, x, value, _ = lp_max(c, A_ub, [0] * len(A_ub), [[1] * m], [1])
    if status != "optimal":  # @line L3
        return None
    return value, x


def optimal_commitment(A, B):
    """Return (value, x, j): the leader's optimal commitment x, its value, and the follower's column j."""
    best = None
    for j in range(len(A[0])):  # @line L1
        res = best_for_column(A, B, j)
        if res is not None and (best is None or res[0] > best[0]):  # @line L4
            best = (res[0], res[1], j)
    return best  # @line L5


def follower_response(A, B, x):
    """The follower's best response to x, with ties broken in the leader's favor."""
    m, n = len(A), len(A[0])
    pay = [sum(Fraction(x[i]) * B[i][k] for i in range(m)) for k in range(n)]
    top = max(pay)
    ties = [k for k in range(n) if pay[k] == top]
    return max(ties, key=lambda k: (sum(Fraction(x[i]) * A[i][k] for i in range(m)), -k))
