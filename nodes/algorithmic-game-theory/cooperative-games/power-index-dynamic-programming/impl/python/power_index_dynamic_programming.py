# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-index-dynamic-programming/. The authors are listed in prov/MQFKCA.jsonl.
"""Banzhaf and Shapley-Shubik indices of a weighted voting game by dynamic programming.

The game [q; w_1, ..., w_n] has nonnegative integer weights and an integer quota q with
1 <= q <= sum(w). A coalition S wins if w(S) >= q. Players are 0 to n - 1. The counts are
exact integers and the indices are Fractions.
"""

from fractions import Fraction
from math import factorial


def check_game(weights: list[int], q: int) -> None:
    """Raise ValueError unless the weights are nonnegative integers and 1 <= q <= sum(weights)."""
    if any(not isinstance(x, int) or x < 0 for x in weights):
        raise ValueError("weights must be nonnegative integers")
    if not isinstance(q, int) or q < 1 or q > sum(weights):
        raise ValueError("the quota must satisfy 1 <= q <= sum of the weights")


def swings_by_size(weights: list[int], q: int, i: int) -> list[int]:
    """c[s] = the number of coalitions S of the other players with |S| = s and q - w_i <= w(S) <= q - 1.

    These are the coalitions that player i turns from losing into winning (the swings of i).
    """
    n = len(weights)
    table = [[0] * q for _ in range(n)]  # @line L1: table[s][k] counts sets of size s and weight k < q
    table[0][0] = 1
    for j in range(n):  # @line L2
        if j == i:
            continue
        wj = weights[j]
        for s in range(n - 2, -1, -1):  # @line L3: downward, so row s is still the old row
            row, up = table[s], table[s + 1]
            for k in range(q - 1 - wj, -1, -1):  # @line L4: a set of weight >= q is never counted
                if row[k]:
                    up[k + wj] += row[k]  # @line L5
    lo = max(0, q - weights[i])
    return [sum(table[s][lo:q]) for s in range(n)]  # @line L6


def player_indices(weights: list[int], q: int, i: int) -> tuple[int, Fraction, Fraction]:
    """Return (swings of i, raw Banzhaf index of i, Shapley-Shubik index of i)."""
    check_game(weights, q)
    n = len(weights)
    c = swings_by_size(weights, q, i)
    swings = sum(c)
    beta = Fraction(swings, 2 ** (n - 1))  # @line L7
    nf = factorial(n)
    phi = sum((Fraction(factorial(s) * factorial(n - 1 - s), nf) * c[s] for s in range(n)), Fraction(0))  # @line L8
    return swings, beta, phi  # @line L9


def power_indices(weights: list[int], q: int) -> dict[str, list]:
    """All indices of all players: swings, raw Banzhaf, normalized Banzhaf and Shapley-Shubik."""
    check_game(weights, q)
    rows = [player_indices(weights, q, i) for i in range(len(weights))]
    swings = [r[0] for r in rows]
    total = sum(swings)  # positive, because some player is pivotal in every order
    return {
        "swings": swings,
        "banzhaf_raw": [r[1] for r in rows],
        "banzhaf_normalized": [Fraction(x, total) for x in swings],
        "shapley_shubik": [r[2] for r in rows],
    }
