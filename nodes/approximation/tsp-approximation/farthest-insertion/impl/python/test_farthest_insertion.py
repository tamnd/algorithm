# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farthest-insertion/. The authors are listed in prov/AVDTNJ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from farthest_insertion import farthest_insertion, insertion_increase, tour_cost

# The six cities A to F of the page, with the Manhattan distance.
POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]

# A small instance from a seeded search on a 7 x 7 grid, with ratio 14/9 from city 3.
BAD = [(2, 5), (0, 3), (2, 0), (4, 2), (4, 5), (4, 1), (0, 2), (0, 4)]


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


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


def increases(cost, start):
    """Replay the run and return the order of the cities and the increase of each insertion."""
    tour = farthest_insertion(cost, start)
    n = len(cost)
    cycle = [start]
    inside = {start}
    order, incs = [start], {start: 0}
    while len(cycle) < n:
        far = {v: min(cost[v][u] for u in cycle) for v in range(n) if v not in inside}
        k = min(far, key=lambda v: (-far[v], v))
        row = [insertion_increase(cost, cycle, k, i) for i in range(len(cycle))]
        i = row.index(min(row))
        cycle.insert(i + 1, k)
        inside.add(k)
        order.append(k)
        incs[k] = row[i]
    assert cycle == tour
    return order, incs


def test_example() -> None:
    cost = manhattan(POINTS)
    tour = farthest_insertion(cost, 0)
    assert tour == [0, 4, 3, 5, 2, 1]
    order, incs = increases(cost, 0)
    assert order == [0, 5, 4, 2, 3, 1]
    assert [incs[v] for v in order] == [0, 18, 0, 0, 2, 0]
    assert tour_cost(cost, tour) == 20 == brute_force_opt(cost)


def test_edges() -> None:
    assert farthest_insertion([]) == []
    assert farthest_insertion([[0]]) == [0]
    assert farthest_insertion([[0, 5], [5, 0]]) == [0, 1]
    cost = [[0, 1, 9], [1, 0, 9], [9, 9, 0]]
    assert increases(cost, 0)[0] == [0, 2, 1]
    assert farthest_insertion(cost) == [0, 1, 2]


def test_tour_is_a_permutation() -> None:
    for cost in instances():
        n = len(cost)
        for s in range(n):
            assert sorted(farthest_insertion(cost, s)) == list(range(n))


def test_log_bound_against_brute_force() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        for s in range(n):
            alg = tour_cost(cost, farthest_insertion(cost, s))
            assert opt - 1e-9 <= alg <= (math.ceil(math.log2(n)) + 1) * opt + 1e-9


def test_the_half_increases_satisfy_the_two_lemmas() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        order, incs = increases(cost, 0)
        ell = {v: incs[v] / 2 for v in order}
        for p in range(n):
            assert ell[p] <= opt / 2 + 1e-9
            for q in range(p + 1, n):
                assert cost[p][q] >= min(ell[p], ell[q]) - 1e-9


def test_small_bad_instance() -> None:
    cost = manhattan(BAD)
    opt = brute_force_opt(cost)
    alg = tour_cost(cost, farthest_insertion(cost, 3))
    assert (alg, opt) == (28, 18)
    assert Fraction(alg, opt) == Fraction(14, 9)
