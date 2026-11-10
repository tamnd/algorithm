# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cheapest-insertion/. The authors are listed in prov/ZCN8SR.jsonl.

import itertools
import math
import random
from fractions import Fraction

from cheapest_insertion import (
    bad_steps,
    cheapest_insertion,
    cycle_metric,
    insertion_increase,
    replay,
    tour_cost,
)

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


def cut_sum(cost, order):
    """The sum over t of d(S_t, V - S_t), where S_t holds the first t cities of the order."""
    total = 0
    for t in range(1, len(order)):
        inside, outside = order[:t], order[t:]
        total += min(cost[u][v] for u in inside for v in outside)
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
    tour = cheapest_insertion(cost, 0)
    assert tour == [0, 4, 3, 5, 2, 1]
    assert tour_cost(cost, tour) == 20 == brute_force_opt(cost)
    assert mst_weight(cost) == 16
    # The order of the run is A, B, E, C, D, F.
    assert cut_sum(cost, [0, 1, 4, 2, 3, 5]) == 16


def test_edges() -> None:
    assert cheapest_insertion([]) == []
    assert cheapest_insertion([[0]]) == [0]
    assert cheapest_insertion([[0, 3], [3, 0]], start=1) == [1, 0]
    assert insertion_increase([[0, 3], [3, 0]], [0], 1, 0) == 6


def test_tour_is_a_permutation() -> None:
    for cost in instances():
        n = len(cost)
        for s in range(n):
            assert sorted(cheapest_insertion(cost, s)) == list(range(n))


def test_ratio_bound_against_brute_force() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        tree = mst_weight(cost)
        for s in range(n):
            alg = tour_cost(cost, cheapest_insertion(cost, s))
            assert opt - 1e-9 <= alg <= 2 * tree + 1e-9
            assert alg <= 2 * (1 - 1 / n) * opt + 1e-9


def test_cut_lemma_for_each_order() -> None:
    rng = random.Random(7)
    for cost in instances():
        n = len(cost)
        tree = mst_weight(cost)
        for _ in range(5):
            order = list(range(n))
            rng.shuffle(order)
            assert cut_sum(cost, order) <= tree + 1e-9


def test_tight_family_on_cycles() -> None:
    for n in range(6, 31, 2):
        cost = cycle_metric(n)
        tour = replay(cost, 0, bad_steps(n))
        alg = tour_cost(cost, tour)
        assert alg == 2 * (n - 1)
        assert tour_cost(cost, list(range(n))) == n
        assert Fraction(alg, n) == 2 * (1 - Fraction(1, n))


def test_replay_rejects_a_wrong_step() -> None:
    cost = cycle_metric(6)
    try:
        replay(cost, 0, [(1, 0), (3, 0)])
    except ValueError:
        return
    raise AssertionError("an increase of 4 was accepted when 2 was possible")
