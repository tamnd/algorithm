# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-tree-algorithm/. The authors are listed in prov/K3DBM0.jsonl.

import itertools
import random
from fractions import Fraction

from double_tree_algorithm import double_tree, euler_circuit, minimum_spanning_tree, tour_cost

# The seven cities A to G of the page, with the Manhattan distance.
POINTS = [(5, 1), (6, 5), (0, 0), (8, 0), (5, 4), (0, 4), (3, 0)]


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def tree_weight(cost, edges):
    return sum(cost[u][v] for u, v in edges)


def graph_metric(n, rng):
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for v in range(1, n):
        u = rng.randrange(v)
        d[u][v] = d[v][u] = rng.randrange(1, 10)
    for _ in range(n):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            w = rng.randrange(1, 10)
            d[u][v] = d[v][u] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def random_metric(rng):
    n = rng.randrange(1, 8)
    kind = rng.randrange(3)
    if kind == 0:
        return manhattan([(rng.randrange(10), rng.randrange(10)) for _ in range(n)])
    if kind == 1:
        return graph_metric(n, rng)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c[i][j] = c[j][i] = rng.choice((1, 2))
    return c


def test_example() -> None:
    cost = manhattan(POINTS)
    tree = minimum_spanning_tree(cost)
    assert tree_weight(cost, tree) == 19
    walk = euler_circuit(7, tree + tree, 0)
    assert "".join("ABCDEFG"[v] for v in walk) == "AEBEAGCFCGADA"
    tour = double_tree(cost)
    assert "".join("ABCDEFG"[v] for v in tour) == "AEBGCFD"
    assert tour_cost(cost, tour) == 36
    assert brute_force_opt(cost) == 28


def test_edges() -> None:
    assert double_tree([]) == []
    assert double_tree([[0]]) == [0]
    assert double_tree([[0, 3], [3, 0]]) == [0, 1]
    zero = [[0] * 5 for _ in range(5)]
    assert sorted(double_tree(zero)) == list(range(5))
    assert tour_cost(zero, double_tree(zero)) == 0


def test_against_brute_force() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        cost = random_metric(rng)
        n = len(cost)
        tour = double_tree(cost)
        assert sorted(tour) == list(range(n))
        opt = brute_force_opt(cost)
        mst = tree_weight(cost, minimum_spanning_tree(cost))
        alg = tour_cost(cost, tour)
        assert mst <= opt
        assert opt <= alg <= 2 * mst <= 2 * opt


def wheel(k):
    """Center 0, leaves 1..k (k odd, k >= 5). Cost 1 on the spokes and on the rim, cost 2 elsewhere.

    The rim joins the leaves whose numbers differ by 2 modulo k, so leaves with consecutive
    numbers are never joined by a rim edge.
    """
    n = k + 1
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            rim = i > 0 and (j - i) % k in (2, k - 2)
            c[i][j] = c[j][i] = 1 if i == 0 or rim else 2
    return c


def test_tight_example() -> None:
    for k in (5, 7):
        c = wheel(k)
        assert brute_force_opt(c) == k + 1
        assert minimum_spanning_tree(c) == [(0, v) for v in range(1, k + 1)]
        assert tour_cost(c, double_tree(c)) == 2 * k
    for k in (101, 1001):
        c = wheel(k)
        n = k + 1
        alg = tour_cost(c, double_tree(c))
        assert alg == 2 * k
        assert Fraction(alg, n) == 2 - Fraction(2, n)
