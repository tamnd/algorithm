# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farthest-insertion/. The authors are listed in prov/AVDTNJ.jsonl.

from typing import Sequence


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    """The cost of the closed tour, including the edge from the last city back to the first."""
    n = len(tour)
    if n < 2:
        return 0
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def insertion_increase(cost: Sequence[Sequence[float]], tour: Sequence[int], k: int, i: int) -> float:
    """The extra cost when city k goes between tour[i] and the next city of the tour."""
    if len(tour) == 1:
        return 2 * cost[tour[0]][k]
    a, b = tour[i], tour[(i + 1) % len(tour)]
    return cost[a][k] + cost[k][b] - cost[a][b]


def farthest_insertion(cost: Sequence[Sequence[float]], start: int = 0) -> list[int]:
    """Grow a cycle; add the city farthest from the cycle at its cheapest position.

    The distance of a city to the cycle is its distance to the closest city of the cycle.
    Ties go to the smaller city and the earlier position. Time Theta(n^2), extra space Theta(n).
    """
    n = len(cost)
    if n == 0:
        return []
    tour = [start]  # @line L1
    inside = [False] * n
    inside[start] = True
    near = [cost[start][v] for v in range(n)]  # @line L2
    while len(tour) < n:  # @line L3
        k = -1
        for v in range(n):  # @line L4
            if not inside[v] and (k < 0 or near[v] > near[k]):
                k = v
        best_i = 0
        best = insertion_increase(cost, tour, k, 0)
        for i in range(1, len(tour)):  # @line L5
            inc = insertion_increase(cost, tour, k, i)
            if inc < best:
                best, best_i = inc, i
        tour.insert(best_i + 1, k)  # @line L6
        inside[k] = True
        for v in range(n):  # @line L7
            if cost[k][v] < near[v]:
                near[v] = cost[k][v]
    return tour  # @line L8
