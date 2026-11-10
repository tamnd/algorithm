# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-insertion/. The authors are listed in prov/F86NNE.jsonl.

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


def nearest_insertion(cost: Sequence[Sequence[float]], start: int = 0) -> tuple[list[int], list[float]]:
    """Grow a cycle; add the city closest to the cycle at its cheapest position.

    Return the tour and the list of the distances d(S_t, V - S_t) of the chosen cities, which is
    the list of edge costs of a Prim tree. Ties go to the smaller city and the earlier position.
    Time Theta(n^2) and extra space Theta(n).
    """
    n = len(cost)
    if n == 0:
        return [], []
    tour = [start]  # @line L1
    inside = [False] * n
    inside[start] = True
    near = [cost[start][v] for v in range(n)]  # @line L2
    gaps: list[float] = []
    while len(tour) < n:  # @line L3
        k = -1
        for v in range(n):  # @line L4
            if not inside[v] and (k < 0 or near[v] < near[k]):
                k = v
        gaps.append(near[k])
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
    return tour, gaps  # @line L8


def replay(cost: Sequence[Sequence[float]], start: int, steps: Sequence[tuple[int, int]]) -> list[int]:
    """Apply the steps (city k, position i) and check that each one is a legal nearest-insertion step.

    A legal step takes a city at the least distance from the cycle and puts it at one of its
    cheapest positions. This lets a test follow any tie rule, also a rule that works against the
    algorithm. Raise ValueError at the first step that is not legal.
    """
    n = len(cost)
    tour = [start]
    for k, i in steps:
        out = [v for v in range(n) if v not in tour]
        dist = {v: min(cost[v][u] for u in tour) for v in out}
        if k not in dist or dist[k] != min(dist.values()):
            raise ValueError(f"city {k} is not a closest city")
        incs = [insertion_increase(cost, tour, k, j) for j in range(len(tour))]
        if incs[i] != min(incs):
            raise ValueError(f"position {i} is not a cheapest position for city {k}")
        tour.insert(i + 1, k)
    return tour


def cycle_metric(n: int) -> list[list[int]]:
    """The shortest path metric of the cycle graph 0, 1, ..., n - 1 with unit edges."""
    return [[min(abs(i - j), n - abs(i - j)) for j in range(n)] for i in range(n)]


def bad_steps(n: int) -> list[tuple[int, int]]:
    """Tie choices on the cycle metric with even n >= 6 that give a tour of cost 2(n - 1).

    The cities 1, ..., n - 1 come in this order. City k goes right after city 0 when k <= h or
    k = n - 1, and right after city h otherwise, with h = n/2 - 1. The positions are tour indices.
    """
    h = n // 2 - 1
    tour = [0]
    steps = []
    for k in range(1, n):
        anchor = 0 if (k <= h or k == n - 1) else h
        i = tour.index(anchor)
        steps.append((k, i))
        tour.insert(i + 1, k)
    return steps
