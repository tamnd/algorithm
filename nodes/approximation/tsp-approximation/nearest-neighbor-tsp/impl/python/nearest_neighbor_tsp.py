# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-tsp/. The authors are listed in prov/F3GHE4.jsonl.

from typing import Sequence


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    """The cost of the closed tour, including the edge from the last city back to the first."""
    n = len(tour)
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def nearest_neighbor_tour(
    cost: Sequence[Sequence[float]], start: int = 0, rank: Sequence[int] | None = None
) -> list[int]:
    """Start at `start` and go to a closest unvisited city until all cities are visited.

    A tie goes to the city with the smaller rank (the city number when `rank` is None).
    Time Theta(n^2) and extra space Theta(n).
    """
    n = len(cost)
    if n == 0:
        return []
    key = list(range(n)) if rank is None else list(rank)
    visited = [False] * n  # @line L1
    visited[start] = True  # @line L2
    tour = [start]
    here = start
    for _ in range(n - 1):  # @line L3
        best = -1
        for v in range(n):  # @line L4
            if visited[v]:
                continue
            if best < 0 or (cost[here][v], key[v]) < (cost[here][best], key[best]):
                best = v
        visited[best] = True  # @line L5
        tour.append(best)
        here = best  # @line L6
    return tour  # @line L7


def leaving_edges(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> dict[int, float]:
    """The value l_p of the proof: the cost of the tour edge that leaves city p."""
    n = len(tour)
    return {tour[i]: cost[tour[i]][tour[(i + 1) % n]] for i in range(n)}


def hougardy_wilde_path(k: int) -> list[tuple[int, int]]:
    """A nearest-neighbor path on the 2 x (8 * 2^k - 3) grid (Hougardy and Wilde 2014).

    The path visits all n = 16 * 2^k - 6 grid points. With the Manhattan metric each step goes
    to a closest unvisited point, and the path has length (12 + 4k) * 2^k - 3.
    """
    path = [(0, 0), (0, 1), (1, 1), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (3, 1), (2, 1)]
    width = 5
    for _ in range(k):
        right = [(x + width + 3, y) for x, y in path]
        middle_low = [(width, 1), (width, 0), (width + 1, 0), (width + 2, 0)]
        path = path + middle_low + right + [(width + 2, 1), (width + 1, 1)]
        width = 2 * width + 3
    return path


def manhattan_matrix(points: Sequence[tuple[int, int]]) -> list[list[int]]:
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]
