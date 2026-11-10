# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-tsp/. The authors are listed in prov/F3GHE4.jsonl.

import itertools
import math
import random
from fractions import Fraction

from nearest_neighbor_tsp import (
    hougardy_wilde_path,
    leaving_edges,
    manhattan_matrix,
    nearest_neighbor_tour,
    tour_cost,
)


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def graph_metric(n, rng):
    """Shortest path costs of a random connected graph with integer edge costs."""
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for i in range(1, n):
        j = rng.randrange(i)
        d[i][j] = d[j][i] = min(d[i][j], rng.randint(1, 9))
    for _ in range(n):
        i, j = rng.sample(range(n), 2)
        d[i][j] = d[j][i] = min(d[i][j], rng.randint(1, 9))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def euclidean_points(n, rng):
    return [(rng.random(), rng.random()) for _ in range(n)]


def euclid(points):
    return [[math.dist(p, q) for q in points] for p in points]


def instances():
    rng = random.Random(1977)
    for n in range(2, 9):
        for _ in range(6):
            yield graph_metric(n, rng)
            yield euclid(euclidean_points(n, rng))


def test_example() -> None:
    points = hougardy_wilde_path(0)
    cost = manhattan_matrix(points)
    tour = nearest_neighbor_tour(cost, 0, list(range(10)))
    assert tour == list(range(10))
    assert tour_cost(cost, tour) == 12
    assert brute_force_opt(cost) == 10


def test_edges() -> None:
    assert nearest_neighbor_tour([]) == []
    assert nearest_neighbor_tour([[0]]) == [0]
    assert nearest_neighbor_tour([[0, 4], [4, 0]], start=1) == [1, 0]
    cost = [[0, 2, 2], [2, 0, 2], [2, 2, 0]]
    assert nearest_neighbor_tour(cost) == [0, 1, 2]
    assert nearest_neighbor_tour(cost, rank=[0, 5, 1]) == [0, 2, 1]


def test_tour_is_a_permutation() -> None:
    for cost in instances():
        n = len(cost)
        for s in range(n):
            assert sorted(nearest_neighbor_tour(cost, s)) == list(range(n))


def test_ratio_bound_against_brute_force() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        bound = (math.ceil(math.log2(n)) + 1) / 2
        for s in range(n):
            alg = tour_cost(cost, nearest_neighbor_tour(cost, s))
            assert alg >= opt - 1e-9
            assert alg <= bound * opt + 1e-9


def test_the_two_lemmas() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        tour = nearest_neighbor_tour(cost, 0)
        ell = leaving_edges(cost, tour)
        for p in range(n):
            assert ell[p] <= opt / 2 + 1e-9
            for q in range(p + 1, n):
                assert cost[p][q] >= min(ell[p], ell[q]) - 1e-9


def test_charging_inequality() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        ell = sorted(leaving_edges(cost, nearest_neighbor_tour(cost, 0)).values(), reverse=True)
        for k in range(1, n):
            assert opt >= 2 * sum(ell[k:min(2 * k, n)]) - 1e-9


def test_hougardy_wilde_family() -> None:
    for k in range(6):
        points = hougardy_wilde_path(k)
        n = len(points)
        width = 8 * 2**k - 3
        assert n == 16 * 2**k - 6 == 2 * width
        assert sorted(points) == [(x, y) for x in range(width) for y in range(2)]
        cost = manhattan_matrix(points)
        tour = nearest_neighbor_tour(cost, 0, list(range(n)))
        assert tour == list(range(n))
        path = sum(cost[i][i + 1] for i in range(n - 1))
        assert path == (12 + 4 * k) * 2**k - 3
        alg = tour_cost(cost, tour)
        assert alg == (16 + 4 * k) * 2**k - 4
        # OPT = n: all costs are at least 1, and the boundary of the grid is a tour of n unit steps.
        boundary = [(x, 0) for x in range(width)] + [(x, 1) for x in reversed(range(width))]
        index = {p: i for i, p in enumerate(points)}
        assert tour_cost(cost, [index[p] for p in boundary]) == n
        assert Fraction(alg, n) >= Fraction(k + 4, 4)
        assert alg <= (math.ceil(math.log2(n)) + 1) * n / 2
