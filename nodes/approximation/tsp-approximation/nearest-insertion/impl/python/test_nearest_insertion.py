# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-insertion/. The authors are listed in prov/F86NNE.jsonl.

import itertools
import math
import random
from fractions import Fraction

from nearest_insertion import bad_steps, cycle_metric, nearest_insertion, replay, tour_cost

# The six cities A to F of the page, with the Manhattan distance.
POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def mst_weight(cost):
    """Kruskal's algorithm with a plain parent array."""
    n = len(cost)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    for w, u, v in sorted((cost[u][v], u, v) for u in range(n) for v in range(u + 1, n)):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
    return total


def graph_metric(n, rng):
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


def instances():
    rng = random.Random(1977)
    for n in range(2, 9):
        for _ in range(6):
            yield graph_metric(n, rng)
            points = [(rng.random(), rng.random()) for _ in range(n)]
            yield [[math.dist(p, q) for q in points] for p in points]


def test_example() -> None:
    cost = manhattan(POINTS)
    tour, gaps = nearest_insertion(cost, 0)
    assert tour == [0, 4, 3, 5, 2, 1]
    assert gaps == [2, 4, 3, 3, 4]
    assert tour_cost(cost, tour) == 20 == brute_force_opt(cost)
    assert sum(gaps) == mst_weight(cost) == 16


def test_edges() -> None:
    assert nearest_insertion([]) == ([], [])
    assert nearest_insertion([[0]]) == ([0], [])
    tour, gaps = nearest_insertion([[0, 3], [3, 0]])
    assert tour == [0, 1] and gaps == [3]
    assert tour_cost([[0, 3], [3, 0]], tour) == 6


def test_tour_is_a_permutation() -> None:
    for cost in instances():
        n = len(cost)
        for s in range(n):
            assert sorted(nearest_insertion(cost, s)[0]) == list(range(n))


def test_ratio_bound_against_brute_force() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        tree = mst_weight(cost)
        assert tree <= (1 - 1 / n) * opt + 1e-9
        for s in range(n):
            tour, gaps = nearest_insertion(cost, s)
            alg = tour_cost(cost, tour)
            assert opt - 1e-9 <= alg <= 2 * tree + 1e-9
            assert alg <= 2 * (1 - 1 / n) * opt + 1e-9
            # The chosen distances are the edges of a Prim tree, so they sum to the MST weight.
            assert abs(sum(gaps) - tree) <= 1e-9


def test_tight_family_on_cycles() -> None:
    for n in range(6, 41, 2):
        cost = cycle_metric(n)
        tour = replay(cost, 0, bad_steps(n))
        alg = tour_cost(cost, tour)
        assert alg == 2 * (n - 1)
        # The cycle 0, 1, ..., n - 1 has cost n, and each tour has n edges of cost at least 1.
        assert tour_cost(cost, list(range(n))) == n
        assert Fraction(alg, n) == 2 * (1 - Fraction(1, n))


def test_replay_rejects_a_wrong_step() -> None:
    cost = cycle_metric(6)
    try:
        replay(cost, 0, [(3, 0)])
    except ValueError:
        return
    raise AssertionError("a city at distance 3 was accepted")
