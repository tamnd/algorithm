# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-edge-heuristic/. The authors are listed in prov/D6Y1F9.jsonl.

import itertools
import math
import random
from fractions import Fraction

from greedy_edge_heuristic import edges_to_tour, greedy_edge_tour, greedy_edges, tour_cost

# The six cities A to F of the page, with the Manhattan distance.
POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]

# A small instance from a seeded search on a 7 x 7 grid, with ratio 13/9.
BAD = [(2, 5), (6, 3), (1, 2), (2, 2), (1, 5), (6, 1), (4, 2), (3, 3)]


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
    rng = random.Random(1984)
    for n in range(3, 9):
        for _ in range(6):
            yield graph_metric(n, rng)
            points = [(rng.random(), rng.random()) for _ in range(n)]
            yield [[math.dist(p, q) for q in points] for p in points]


def test_example() -> None:
    cost = manhattan(POINTS)
    names = "ABCDEF"
    kept = ["".join(names[x] for x in e) for e in greedy_edges(cost)]
    assert kept == ["AB", "CF", "DF", "AE", "BC", "DE"]
    tour = greedy_edge_tour(cost)
    assert tour_cost(cost, tour) == 20 == brute_force_opt(cost)


def test_edges() -> None:
    assert greedy_edge_tour([]) == []
    assert greedy_edge_tour([[0]]) == [0]
    assert greedy_edge_tour([[0, 1], [1, 0]]) == [0, 1]
    assert sorted(greedy_edge_tour([[0, 1, 1], [1, 0, 1], [1, 1, 0]])) == [0, 1, 2]


def test_result_is_a_tour() -> None:
    for cost in instances():
        n = len(cost)
        edges = greedy_edges(cost)
        assert len(edges) == n
        degree = [0] * n
        for u, v in edges:
            degree[u] += 1
            degree[v] += 1
        assert degree == [2] * n
        assert sorted(edges_to_tour(n, edges)) == list(range(n))


def test_log_bound_against_brute_force() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        alg = tour_cost(cost, greedy_edge_tour(cost))
        assert opt - 1e-9 <= alg <= (math.ceil(math.log2(n)) + 1) / 2 * opt + 1e-9


def test_oriented_edges_satisfy_the_two_lemmas() -> None:
    for cost in instances():
        n = len(cost)
        opt = brute_force_opt(cost)
        tour = greedy_edge_tour(cost)
        for order in (tour, tour[::-1]):
            ell = {order[i]: cost[order[i]][order[(i + 1) % n]] for i in range(n)}
            assert abs(sum(ell.values()) - tour_cost(cost, tour)) <= 1e-9
            for p in range(n):
                assert ell[p] <= opt / 2 + 1e-9
                for q in range(p + 1, n):
                    assert cost[p][q] >= min(ell[p], ell[q]) - 1e-9


def test_small_bad_instance() -> None:
    cost = manhattan(BAD)
    alg = tour_cost(cost, greedy_edge_tour(cost))
    opt = brute_force_opt(cost)
    assert (alg, opt) == (26, 18)
    assert Fraction(alg, opt) == Fraction(13, 9)
