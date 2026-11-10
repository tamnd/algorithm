# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-opt/. The authors are listed in prov/F2HNR2.jsonl.

from typing import Sequence

EPS = 1e-12  # a move must gain more than this, so that rounding cannot make the search cycle


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    n = len(tour)
    if n < 2:
        return 0.0
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def two_opt_gain(cost: Sequence[Sequence[float]], tour: Sequence[int], i: int, j: int) -> float:
    """The gain of the move that removes the edges after positions i and j and reverses tour[i+1..j]."""
    n = len(tour)
    a, b = tour[i], tour[i + 1]
    c, e = tour[j], tour[(j + 1) % n]
    return cost[a][b] + cost[c][e] - cost[a][c] - cost[b][e]


def two_opt(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> tuple[list[int], int]:
    """Apply improving 2-opt moves, first improvement in a fixed scan order, until none is left.

    Return the 2-optimal tour and the number of moves. Each pass costs O(n^2); the number of
    passes is not bounded by a polynomial in the worst case.
    """
    t = list(tour)
    n = len(t)
    moves = 0
    improved = n >= 4
    while improved:  # @line L1
        improved = False  # @line L2
        for i in range(n - 2):  # @line L3
            for j in range(i + 2, n if i > 0 else n - 1):  # @line L4
                if two_opt_gain(cost, t, i, j) > EPS:  # @line L5
                    t[i + 1 : j + 1] = reversed(t[i + 1 : j + 1])  # @line L6
                    moves += 1
                    improved = True
    return t, moves  # @line L7


def is_two_optimal(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> bool:
    n = len(tour)
    return all(
        two_opt_gain(cost, tour, i, j) <= EPS for i in range(n - 2) for j in range(i + 2, n if i > 0 else n - 1)
    )
