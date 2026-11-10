# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-edge-heuristic/. The authors are listed in prov/D6Y1F9.jsonl.

from typing import Sequence


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    """The cost of the closed tour, including the edge from the last city back to the first."""
    n = len(tour)
    if n < 2:
        return 0
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def greedy_edges(cost: Sequence[Sequence[float]]) -> list[tuple[int, int]]:
    """Scan the pairs by cost and keep a pair when both ends have degree < 2 and no short cycle forms.

    Return the n kept edges in the order of the scan; the last one closes the tour. Ties go to the
    smaller pair (u, v). Time Theta(n^2 log n) for the sort; extra space Theta(n^2) for the list.
    """
    n = len(cost)
    if n < 3:
        return [(0, 1), (1, 0)] if n == 2 else []
    pairs = sorted((cost[u][v], u, v) for u in range(n) for v in range(u + 1, n))  # @line L1
    degree = [0] * n  # @line L2
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    kept: list[tuple[int, int]] = []
    for _, u, v in pairs:  # @line L3
        if degree[u] == 2 or degree[v] == 2:  # @line L4
            continue
        ru, rv = find(u), find(v)
        if ru == rv and len(kept) < n - 1:  # @line L5
            continue
        kept.append((u, v))  # @line L6
        degree[u] += 1
        degree[v] += 1
        parent[ru] = rv
        if len(kept) == n:  # @line L7
            break
    return kept


def edges_to_tour(n: int, edges: Sequence[tuple[int, int]]) -> list[int]:
    """Walk the cycle formed by the edges, from city 0."""
    if n < 3:
        return list(range(n))
    nbr: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    tour = [0]
    prev, here = -1, 0
    for _ in range(n - 1):
        a, b = nbr[here]
        nxt = a if a != prev else b
        tour.append(nxt)
        prev, here = here, nxt
    return tour  # @line L8


def greedy_edge_tour(cost: Sequence[Sequence[float]]) -> list[int]:
    return edges_to_tour(len(cost), greedy_edges(cost))
