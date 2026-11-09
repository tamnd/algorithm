# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-heuristic/. The authors are listed in prov/0YM2MN.jsonl.

from typing import Sequence


def nearest_neighbor_tour(dist: Sequence[Sequence[int]], start: int = 0) -> list[int]:
    """Build a TSP tour by always moving to the closest unvisited city.

    dist is an n by n matrix of non-negative costs. Ties go to the city with
    the smallest index. The returned list is a permutation of range(n) that
    starts at `start`. The tour closes with the edge from the last city back
    to `start`.

    Cost: Theta(n^2) time and Theta(n) extra space.
    """
    n = len(dist)
    if n == 0:
        return []
    if not 0 <= start < n:
        raise ValueError("start must be a city index")
    tour = [start]  # @line L1
    visited = [False] * n
    visited[start] = True
    cur = start  # @line L2
    for _ in range(n - 1):  # @line L3
        nxt = -1  # @line L4
        row = dist[cur]
        for j in range(n):  # @line L5
            if not visited[j] and (nxt == -1 or row[j] < row[nxt]):  # @line L6
                nxt = j
        tour.append(nxt)  # @line L7
        visited[nxt] = True
        cur = nxt  # @line L8
    return tour  # @line L9


def tour_cost(dist: Sequence[Sequence[int]], tour: Sequence[int]) -> int:
    """Total cost of the closed tour, including the edge back to the start."""
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n)) if n > 1 else 0


def repeated_nearest_neighbor(dist: Sequence[Sequence[int]]) -> list[int]:
    """Run the heuristic from every start city and keep the cheapest tour.

    Cost: Theta(n^3) time.
    """
    best: list[int] = []
    best_cost = None
    for s in range(len(dist)):
        t = nearest_neighbor_tour(dist, s)
        c = tour_cost(dist, t)
        if best_cost is None or c < best_cost:
            best, best_cost = t, c
    return best
