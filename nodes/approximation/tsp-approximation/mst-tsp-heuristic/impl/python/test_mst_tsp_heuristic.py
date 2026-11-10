# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-tsp-heuristic/. The authors are listed in prov/HM8R8X.jsonl.

import itertools
import random

import pytest

from mst_tsp_heuristic import improving_two_opt_move, minimum_spanning_tree, mst_tsp, tour_cost

POINTS = [(5, 1), (6, 5), (0, 0), (8, 0), (5, 4), (0, 4), (3, 0)]
NAMES = "ABCDEFG"


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def random_metric(rng):
    n = rng.randrange(1, 8)
    if rng.random() < 0.6:
        return manhattan([(rng.randrange(12), rng.randrange(12)) for _ in range(n)])
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c[i][j] = c[j][i] = rng.choice((1, 2))
    return c


def name(tour):
    return "".join(NAMES[v] for v in tour)


def test_example() -> None:
    cost = manhattan(POINTS)
    assert sum(cost[u][v] for u, v in minimum_spanning_tree(cost)) == 19
    assert name(mst_tsp(cost, "double")) == "AEBGCFD"
    assert tour_cost(cost, mst_tsp(cost, "double")) == 36
    assert tour_cost(cost, mst_tsp(cost, "double", improve=True)) == 28
    assert name(mst_tsp(cost, "matching")) == "AEBFCGD"
    assert tour_cost(cost, mst_tsp(cost, "matching")) == 28
    assert brute_force_opt(cost) == 28


def test_edges() -> None:
    for aug in ("double", "matching"):
        for imp in (False, True):
            assert mst_tsp([], aug, imp) == []
            assert mst_tsp([[0]], aug, imp) == [0]
            assert mst_tsp([[0, 2], [2, 0]], aug, imp) == [0, 1]
            assert sorted(mst_tsp([[0, 1, 1], [1, 0, 1], [1, 1, 0]], aug, imp)) == [0, 1, 2]
    with pytest.raises(ValueError):
        mst_tsp([[0]], "triple")


def test_against_brute_force() -> None:
    rng = random.Random(99)
    for _ in range(500):
        cost = random_metric(rng)
        n = len(cost)
        opt = brute_force_opt(cost)
        mst = sum(cost[u][v] for u, v in minimum_spanning_tree(cost))
        assert mst <= opt
        for aug, num, den in (("double", 2, 1), ("matching", 3, 2)):
            plain = mst_tsp(cost, aug)
            better = mst_tsp(cost, aug, improve=True)
            assert sorted(plain) == sorted(better) == list(range(n))
            a, b = tour_cost(cost, plain), tour_cost(cost, better)
            assert opt <= b <= a
            assert den * a <= num * opt
            assert improving_two_opt_move(cost, better) is None


def test_tight_examples() -> None:
    k = 7
    n = k + 1
    wheel = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            rim = i > 0 and (j - i) % k in (2, k - 2)
            wheel[i][j] = wheel[j][i] = 1 if i == 0 or rim else 2
    assert tour_cost(wheel, mst_tsp(wheel, "double")) == 2 * k
    assert tour_cost(wheel, mst_tsp(wheel, "double", improve=True)) < 2 * k
    assert brute_force_opt(wheel) == n
    # The path example of Christofides with eps = 1/10, scaled by 10 to keep integers.
    m = 7
    line = [[abs(i - j) // 2 * 11 + abs(i - j) % 2 * 10 for j in range(m)] for i in range(m)]
    assert tour_cost(line, mst_tsp(line, "matching")) == 10 * (m - 1) + 11 * (m - 1) // 2
    assert brute_force_opt(line) == 11 * (m - 2) + 20
