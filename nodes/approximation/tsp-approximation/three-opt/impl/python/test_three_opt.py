# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-opt/. The authors are listed in prov/ADCC0B.jsonl.

import itertools
import math
import random

from three_opt import RECONNECTIONS, apply_move, is_three_optimal, three_opt, three_opt_gain, tour_cost, triples

POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]  # A to F of the page


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


def all_tours(n):
    return [[0, *q] for q in itertools.permutations(range(1, n)) if q[0] < q[-1]]


def is_two_optimal(cost, tour):
    n = len(tour)
    for i in range(n - 2):
        for j in range(i + 2, n if i > 0 else n - 1):
            a, b, c, e = tour[i], tour[i + 1], tour[j], tour[(j + 1) % n]
            if cost[a][b] + cost[c][e] - cost[a][c] - cost[b][e] > 1e-12:
                return False
    return True


def test_moves_are_tours_and_gains_are_exact() -> None:
    rng = random.Random(1965)
    n = 8
    cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
    tour = list(range(n))
    rng.shuffle(tour)
    for i, j, k in triples(n):
        for kind in RECONNECTIONS:
            new = apply_move(tour, i, j, k, kind)
            assert sorted(new) == list(range(n))
            gain = three_opt_gain(cost, tour, i, j, k, kind)
            assert abs(tour_cost(cost, tour) - tour_cost(cost, new) - gain) < 1e-9


def test_pure_moves_are_not_two_opt_moves() -> None:
    """The four pure reconnections change three edges; the first three change only two."""
    tour = list(range(9))
    for kind in RECONNECTIONS:
        new = apply_move(tour, 1, 4, 6, kind)
        old_edges = {frozenset((tour[i], tour[(i + 1) % 9])) for i in range(9)}
        new_edges = {frozenset((new[i], new[(i + 1) % 9])) for i in range(9)}
        assert len(old_edges - new_edges) == (2 if kind in RECONNECTIONS[:3] else 3)


def test_six_city_trace() -> None:
    cost = euclid(POINTS)
    start = [0, 3, 1, 4, 2, 5]  # A D B E C F
    tour, moves = three_opt(cost, start)
    assert is_three_optimal(cost, tour)
    assert moves == 4
    assert abs(tour_cost(cost, tour) - 15.9590) < 1e-3


SEVEN = [(1, 2), (0, 5), (3, 3), (1, 0), (0, 0), (3, 4), (2, 6)]  # A to G of the page


def test_example_two_optimal_but_not_three_optimal() -> None:
    cost = euclid(SEVEN)
    start = [0, 2, 5, 6, 1, 4, 3]  # A C F G B E D
    assert is_two_optimal(cost, start)
    assert not is_three_optimal(cost, start)
    assert abs(tour_cost(cost, start) - 15.7082) < 1e-3
    assert abs(three_opt_gain(cost, start, 0, 4, 6, "Y X") - 0.2322) < 1e-3
    assert apply_move(start, 0, 4, 6, "Y X") == [0, 4, 3, 2, 5, 6, 1]  # A E D C F G B
    opt = min(tour_cost(cost, t) for t in all_tours(7))
    assert abs(opt - 15.4760) < 1e-3
    tour, _ = three_opt(cost, start)
    assert abs(tour_cost(cost, tour) - opt) < 1e-9


def test_three_optimal_implies_two_optimal_and_obeys_bound() -> None:
    rng = random.Random(1973)
    for n in range(5, 9):
        for trial in range(4):
            if trial % 2:
                cost = random_metric(n, rng)
            else:
                cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
            tours = all_tours(n)
            opt = min(tour_cost(cost, t) for t in tours)
            bound = 2 * math.sqrt(2) * sum(1 / math.sqrt(i) for i in range(1, n + 1))
            for t in tours:
                if is_three_optimal(cost, t):
                    assert is_two_optimal(cost, t)
                    assert opt - 1e-9 <= tour_cost(cost, t) <= bound * opt


def test_search_from_random_starts() -> None:
    rng = random.Random(3)
    for n in range(5, 12):
        cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
        start = list(range(n))
        rng.shuffle(start)
        tour, _ = three_opt(cost, start)
        assert sorted(tour) == list(range(n))
        assert is_three_optimal(cost, tour)
        assert tour_cost(cost, tour) <= tour_cost(cost, start) + 1e-9
