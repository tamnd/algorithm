# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cheapest-insertion/. The authors are listed in prov/ZCN8SR.jsonl.

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


def cheapest_insertion(cost: Sequence[Sequence[float]], start: int = 0) -> list[int]:
    """Grow a cycle; at each step add the pair (city, position) with the least extra cost.

    Ties go to the smaller city and then to the earlier position. This plain version takes
    Theta(n^3) time; extra space Theta(n).
    """
    n = len(cost)
    if n == 0:
        return []
    tour = [start]  # @line L1
    inside = [False] * n
    inside[start] = True
    while len(tour) < n:  # @line L2
        best = None
        for k in range(n):  # @line L3
            if inside[k]:
                continue
            for i in range(len(tour)):
                inc = insertion_increase(cost, tour, k, i)
                if best is None or inc < best[0]:
                    best = (inc, k, i)  # @line L4
        assert best is not None
        _, k, i = best
        tour.insert(i + 1, k)  # @line L5
        inside[k] = True
    return tour  # @line L6


def replay(cost: Sequence[Sequence[float]], start: int, steps: Sequence[tuple[int, int]]) -> list[int]:
    """Apply the steps (city k, position i) and check that each one is a legal cheapest-insertion step.

    A legal step has the least extra cost over all cities outside the cycle and all positions.
    Raise ValueError at the first step that is not legal.
    """
    n = len(cost)
    tour = [start]
    for k, i in steps:
        if k in tour:
            raise ValueError(f"city {k} is already in the cycle")
        least = min(
            insertion_increase(cost, tour, v, j) for v in range(n) if v not in tour for j in range(len(tour))
        )
        if insertion_increase(cost, tour, k, i) != least:
            raise ValueError(f"city {k} at position {i} is not a cheapest pair")
        tour.insert(i + 1, k)
    return tour


def cycle_metric(n: int) -> list[list[int]]:
    """The shortest path metric of the cycle graph 0, 1, ..., n - 1 with unit edges."""
    return [[min(abs(i - j), n - abs(i - j)) for j in range(n)] for i in range(n)]


def bad_steps(n: int) -> list[tuple[int, int]]:
    """Tie choices on the cycle metric with even n >= 6 that give a tour of cost 2(n - 1)."""
    h = n // 2 - 1
    tour = [0]
    steps = []
    for k in range(1, n):
        anchor = 0 if (k <= h or k == n - 1) else h
        i = tour.index(anchor)
        steps.append((k, i))
        tour.insert(i + 1, k)
    return steps
