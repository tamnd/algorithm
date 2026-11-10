# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-opt/. The authors are listed in prov/ADCC0B.jsonl.

from typing import Sequence

EPS = 1e-12

# The seven ways to put the segments X = tour[i+1..j] and Y = tour[j+1..k] back between
# tour[i] and tour[k+1]. "r" means reversed. The first three remove only two of the three
# edges (2-opt moves); the last four are the pure 3-opt moves.
RECONNECTIONS = ("Xr Y", "X Yr", "Yr Xr", "Xr Yr", "Y X", "Y Xr", "Yr X")


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    n = len(tour)
    if n < 2:
        return 0.0
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def _pieces(tour: Sequence[int], i: int, j: int, k: int, kind: str) -> list[list[int]]:
    x = list(tour[i + 1 : j + 1])
    y = list(tour[j + 1 : k + 1])
    seg = {"X": x, "Xr": x[::-1], "Y": y, "Yr": y[::-1]}
    return [seg[name] for name in kind.split()]


def three_opt_gain(cost: Sequence[Sequence[float]], tour: Sequence[int], i: int, j: int, k: int, kind: str) -> float:
    """The gain of removing the edges after positions i < j < k and reconnecting as kind."""
    n = len(tour)
    a, f = tour[i], tour[(k + 1) % n]
    first, second = _pieces(tour, i, j, k, kind)
    old = cost[a][tour[i + 1]] + cost[tour[j]][tour[j + 1]] + cost[tour[k]][f]
    new = cost[a][first[0]] + cost[first[-1]][second[0]] + cost[second[-1]][f]
    return old - new


def apply_move(tour: Sequence[int], i: int, j: int, k: int, kind: str) -> list[int]:
    first, second = _pieces(tour, i, j, k, kind)
    return list(tour[: i + 1]) + first + second + list(tour[k + 1 :])


def triples(n: int):
    """All i < j < k with nonempty segments; the case i = 0, k = n - 1 removes the edge (tour[n-1], tour[0])."""
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                yield i, j, k


def three_opt(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> tuple[list[int], int]:
    """First-improvement 3-opt over all seven reconnections. Return the 3-optimal tour and the moves."""
    t = list(tour)
    n = len(t)
    moves = 0
    improved = n >= 5
    while improved:  # @line L1
        improved = False
        for i, j, k in triples(n):  # @line L2
            for kind in RECONNECTIONS:  # @line L3
                if three_opt_gain(cost, t, i, j, k, kind) > EPS:  # @line L4
                    t = apply_move(t, i, j, k, kind)  # @line L5
                    moves += 1
                    improved = True
                    break
    return t, moves  # @line L6


def is_three_optimal(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> bool:
    return all(
        three_opt_gain(cost, tour, i, j, k, kind) <= EPS for i, j, k in triples(len(tour)) for kind in RECONNECTIONS
    )
