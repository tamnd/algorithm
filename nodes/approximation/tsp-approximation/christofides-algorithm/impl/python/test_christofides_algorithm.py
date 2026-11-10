# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/christofides-algorithm/. The authors are listed in prov/XH4RYS.jsonl.

import itertools
import random
from fractions import Fraction

from christofides_algorithm import (
    christofides,
    euler_circuit,
    min_weight_perfect_matching,
    minimum_spanning_tree,
    tour_cost,
)

POINTS = [(5, 1), (6, 5), (0, 0), (8, 0), (5, 4), (0, 4), (3, 0)]
NAMES = "ABCDEFG"


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def brute_force_matching(cost, vertices):
    if not vertices:
        return 0
    a, rest = vertices[0], vertices[1:]
    return min(cost[a][b] + brute_force_matching(cost, rest[:i] + rest[i + 1 :]) for i, b in enumerate(rest))


def shortest_paths(n, wedges):
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for u, v, w in wedges:
        d[u][v] = d[v][u] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def random_metric(rng):
    n = 8 if rng.random() < 0.05 else rng.randrange(1, 8)
    kind = rng.randrange(3)
    if kind == 0:
        return manhattan([(rng.randrange(10), rng.randrange(10)) for _ in range(n)])
    if kind == 1:
        w = [(v, rng.randrange(v), rng.randrange(1, 10)) for v in range(1, n)]
        w += [(rng.randrange(n), rng.randrange(n), rng.randrange(1, 10)) for _ in range(n)]
        return shortest_paths(n, w)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c[i][j] = c[j][i] = rng.choice((1, 2))
    return c


def test_example() -> None:
    cost = manhattan(POINTS)
    tree = minimum_spanning_tree(cost)
    assert sum(cost[u][v] for u, v in tree) == 19
    degree = [0] * 7
    for u, v in tree:
        degree[u] += 1
        degree[v] += 1
    odd = [v for v in range(7) if degree[v] % 2]
    assert "".join(NAMES[v] for v in odd) == "ABDF"
    matching = min_weight_perfect_matching(cost, odd)
    assert sorted(NAMES[u] + NAMES[v] for u, v in matching) == ["AD", "BF"]
    assert sum(cost[u][v] for u, v in matching) == 11
    walk = euler_circuit(7, tree + matching, 0)
    assert "".join(NAMES[v] for v in walk) == "AEBFCGADA"
    tour = christofides(cost)
    assert "".join(NAMES[v] for v in tour) == "AEBFCGD"
    assert tour_cost(cost, tour) == 28
    assert brute_force_opt(cost) == 28


def test_edges() -> None:
    assert christofides([]) == []
    assert christofides([[0]]) == [0]
    assert christofides([[0, 5], [5, 0]]) == [0, 1]
    assert sorted(christofides([[0, 1, 1], [1, 0, 1], [1, 1, 0]])) == [0, 1, 2]
    zero = [[0] * 6 for _ in range(6)]
    assert tour_cost(zero, christofides(zero)) == 0


def test_against_brute_force() -> None:
    rng = random.Random(1976)
    for _ in range(600):
        cost = random_metric(rng)
        n = len(cost)
        tour = christofides(cost)
        assert sorted(tour) == list(range(n))
        opt = brute_force_opt(cost)
        tree = minimum_spanning_tree(cost)
        mst = sum(cost[u][v] for u, v in tree)
        degree = [0] * n
        for u, v in tree:
            degree[u] += 1
            degree[v] += 1
        odd = [v for v in range(n) if degree[v] % 2]
        assert len(odd) % 2 == 0
        matching = min_weight_perfect_matching(cost, odd)
        m = sum(cost[u][v] for u, v in matching)
        assert m == brute_force_matching(cost, odd)
        assert 2 * m <= opt
        assert mst <= opt
        alg = tour_cost(cost, tour)
        assert opt <= alg <= mst + m
        assert 2 * alg <= 3 * opt


def tight(n, eps):
    """The path 0..n-1 (n odd) with unit edges and edges {i, i+2} of cost 1 + eps, with shortest paths."""
    w = [(i, i + 1, 1) for i in range(n - 1)] + [(i, i + 2, 1 + eps) for i in range(n - 2)]
    return shortest_paths(n, w)


def tight_formula(n, eps):
    """The same metric in closed form: d(i, j) = floor(m / 2) (1 + eps) + (m mod 2) with m = |i - j|."""
    return [[abs(i - j) // 2 * (1 + eps) + abs(i - j) % 2 for j in range(n)] for i in range(n)]


def test_tight_example() -> None:
    eps = Fraction(1, 1000)
    for n in (5, 7):
        c = tight(n, eps)
        assert c == tight_formula(n, eps)
        alg = tour_cost(c, christofides(c))
        assert alg == (n - 1) + Fraction(n - 1, 2) * (1 + eps)
        assert brute_force_opt(c) == (n - 2) * (1 + eps) + 2
    assert tight(31, eps) == tight_formula(31, eps)
    n = 201
    c = tight_formula(n, eps)
    alg = tour_cost(c, christofides(c))
    assert alg == (n - 1) + Fraction(n - 1, 2) * (1 + eps)
    upper_opt = (n - 2) * (1 + eps) + 2
    assert alg / upper_opt > Fraction(148, 100)
