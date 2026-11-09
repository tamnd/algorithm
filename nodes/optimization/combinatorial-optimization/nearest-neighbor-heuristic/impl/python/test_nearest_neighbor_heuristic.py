# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-heuristic/. The authors are listed in prov/0YM2MN.jsonl.

import random
from itertools import permutations

from nearest_neighbor_heuristic import nearest_neighbor_tour, repeated_nearest_neighbor, tour_cost


def optimum(dist: list[list[int]]) -> int:
    n = len(dist)
    if n <= 1:
        return 0
    return min(tour_cost(dist, (0,) + p) for p in permutations(range(1, n)))


def ceil_lg(n: int) -> int:
    return (n - 1).bit_length()


def manhattan(points: list[tuple[int, int]]) -> list[list[int]]:
    return [[abs(a - c) + abs(b - d) for (c, d) in points] for (a, b) in points]


def random_metric(rng: random.Random, n: int) -> list[list[int]]:
    """Shortest-path closure of a random complete graph: always a metric."""
    d = [[0 if i == j else rng.randint(1, 30) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):
            d[i][j] = d[j][i]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def check_greedy_steps(dist: list[list[int]], tour: list[int], start: int) -> None:
    n = len(dist)
    assert sorted(tour) == list(range(n))
    assert tour[0] == start
    for i in range(1, n):
        cur, chosen = tour[i - 1], tour[i]
        left = tour[i:]
        assert dist[cur][chosen] == min(dist[cur][j] for j in left)
        ties = [j for j in left if dist[cur][j] == dist[cur][chosen]]
        assert chosen == min(ties)


def out_lengths(dist: list[list[int]], tour: list[int]) -> dict[int, int]:
    n = len(tour)
    return {tour[i]: dist[tour[i]][tour[(i + 1) % n]] for i in range(n)}


def test_line_example() -> None:
    xs = [0, 1, -2, 5, -10]
    dist = [[abs(a - b) for b in xs] for a in xs]
    tour = nearest_neighbor_tour(dist, 0)
    assert [xs[i] for i in tour] == [0, 1, -2, 5, -10]
    assert tour_cost(dist, tour) == 36
    assert optimum(dist) == 30


def test_grid_example() -> None:
    pts = [(0, 0), (4, 0), (4, 3), (1, 3), (2, 1)]
    dist = manhattan(pts)
    tour = nearest_neighbor_tour(dist, 0)
    assert tour == [0, 4, 1, 2, 3]
    assert tour_cost(dist, tour) == 16 == optimum(dist)


def test_small_cases() -> None:
    assert nearest_neighbor_tour([], 0) == []
    assert nearest_neighbor_tour([[0]], 0) == [0]
    assert nearest_neighbor_tour([[0, 5], [5, 0]], 1) == [1, 0]
    assert tour_cost([[0, 5], [5, 0]], [1, 0]) == 10


def test_non_metric_can_be_arbitrarily_bad() -> None:
    for big in (10, 1000, 10**9):
        dist = [[0, 1, 2, big], [1, 0, 1, 2], [2, 1, 0, 1], [big, 2, 1, 0]]
        tour = nearest_neighbor_tour(dist, 0)
        assert tour == [0, 1, 2, 3]
        assert tour_cost(dist, tour) == 3 + big
        assert optimum(dist) == 6


def test_random_metric_invariants_and_bound() -> None:
    rng = random.Random(9137)
    for trial in range(600):
        n = rng.randint(2, 7)
        if trial % 2:
            dist = random_metric(rng, n)
        else:
            dist = manhattan([(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)])
        start = rng.randrange(n)
        tour = nearest_neighbor_tour(dist, start)
        check_greedy_steps(dist, tour, start)
        cost = tour_cost(dist, tour)
        opt = optimum(dist)
        assert opt <= cost
        # Rosenkrantz, Stearns and Lewis: cost <= (ceil(lg n) + 1) / 2 * OPT.
        assert 2 * cost <= (ceil_lg(n) + 1) * opt
        # The two facts of the proof.
        ell = out_lengths(dist, tour)
        assert sum(ell.values()) == cost
        for i in range(n):
            assert 2 * ell[i] <= opt
            for j in range(n):
                if i != j:
                    assert dist[i][j] >= min(ell[i], ell[j])
        best = repeated_nearest_neighbor(dist)
        assert sorted(best) == list(range(n))
        assert opt <= tour_cost(dist, best) <= cost
