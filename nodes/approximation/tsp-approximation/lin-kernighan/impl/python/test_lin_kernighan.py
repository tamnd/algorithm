# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lin-kernighan/. The authors are listed in prov/TAC0AY.jsonl.

import itertools
import math
import random

from lin_kernighan import lin_kernighan, lk_search, nearest_lists, tour_cost

SEVEN = [(1, 2), (0, 5), (3, 3), (1, 0), (0, 0), (3, 4), (2, 6)]  # A to G of the page


def euclid(points):
    return [[math.dist(a, b) for b in points] for a in points]


def random_metric(n, rng):
    w = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = rng.choice([1, 2, 3, 5, 8, 13])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                w[i][j] = min(w[i][j], w[i][k] + w[k][j])
    return w


def brute_force(cost):
    n = len(cost)
    return min(tour_cost(cost, [0, *q]) for q in itertools.permutations(range(1, n)))


def is_two_optimal(cost, tour):
    n = len(tour)
    for i in range(n - 2):
        for j in range(i + 2, n if i > 0 else n - 1):
            a, b, c, e = tour[i], tour[i + 1], tour[j], tour[(j + 1) % n]
            if cost[a][b] + cost[c][e] - cost[a][c] - cost[b][e] > 1e-12:
                return False
    return True


def test_example_trace() -> None:
    cost = euclid(SEVEN)
    names = "ABCDEFG"
    start = [0, 2, 5, 6, 1, 4, 3]  # A C F G B E D, a 2-optimal tour
    assert is_two_optimal(cost, start)
    path = [1, 6, 5, 2, 0, 3, 4]  # remove the edge B E: the path from t1 = B to the free end E
    trace = []
    gain, tour = lk_search(cost, path, nearest_lists(cost, 6), (7, 7), trace=trace)
    steps = [(names[y], names[z], names[w], round(g, 3), round(c, 3)) for _, y, z, w, g, c in trace]
    assert steps[:2] == [("E", "A", "D", 4.764, -0.335), ("D", "C", "A", 3.394, 0.232)]
    assert abs(gain - 0.2322) < 1e-3
    assert "".join(names[i] for i in tour) == "BGFCDEA"
    assert abs(tour_cost(cost, tour) - 15.4760) < 1e-3


def test_result_is_a_local_optimum() -> None:
    rng = random.Random(1973)
    for n in range(4, 12):
        cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
        start = list(range(n))
        rng.shuffle(start)
        candidates = nearest_lists(cost, min(8, n - 1))
        tour, _ = lin_kernighan(cost, start, candidates)
        assert sorted(tour) == list(range(n))
        assert tour_cost(cost, tour) <= tour_cost(cost, start) + 1e-9
        for i in range(n):  # no search from any city and either edge gains
            ring = tour[i:] + tour[:i]
            for path in (ring[:1] + ring[1:][::-1], ring):
                assert lk_search(cost, path, candidates) is None


def test_full_lists_give_two_optimal_tours_within_the_bound() -> None:
    rng = random.Random(1999)
    for n in range(5, 9):
        for trial in range(6):
            cost = random_metric(n, rng) if trial % 2 else euclid([(rng.random(), rng.random()) for _ in range(n)])
            start = list(range(n))
            rng.shuffle(start)
            tour, _ = lin_kernighan(cost, start, nearest_lists(cost, n - 1), (n, 1))
            assert is_two_optimal(cost, tour)
            opt = brute_force(cost)
            bound = 2 * math.sqrt(2) * sum(1 / math.sqrt(i) for i in range(1, n + 1))
            assert opt - 1e-9 <= tour_cost(cost, tour) <= bound * opt


def test_measured_quality_small() -> None:
    rng = random.Random(2024)
    hits = 0
    for _ in range(30):
        points = [(rng.random(), rng.random()) for _ in range(8)]
        cost = euclid(points)
        start = list(range(8))
        rng.shuffle(start)
        tour, _ = lin_kernighan(cost, start)
        hits += abs(tour_cost(cost, tour) - brute_force(cost)) < 1e-9
    assert hits >= 27  # measured on these seeds, not a bound


def test_small_inputs() -> None:
    assert lin_kernighan([[0]], [0]) == ([0], 0)
    cost = euclid([(0, 0), (1, 0), (1, 1)])
    assert lin_kernighan(cost, [0, 1, 2]) == ([0, 1, 2], 0)
