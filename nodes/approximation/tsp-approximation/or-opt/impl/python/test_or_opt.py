# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/or-opt/. The authors are listed in prov/WJY5MZ.jsonl.

import itertools
import math
import random

from or_opt import apply_or_move, is_or_optimal, or_gain, or_moves, or_opt, tour_cost

SEVEN = [(1, 2), (0, 5), (3, 3), (1, 0), (0, 0), (3, 4), (2, 6)]  # A to G of the page


def euclid(points):
    return [[math.dist(a, b) for b in points] for a in points]


def all_tours(n):
    return [[0, *q] for q in itertools.permutations(range(1, n)) if q[0] < q[-1]]


def edges(tour):
    n = len(tour)
    return {frozenset((tour[i], tour[(i + 1) % n])) for i in range(n)}


def is_two_optimal(cost, tour):
    n = len(tour)
    for i in range(n - 2):
        for j in range(i + 2, n if i > 0 else n - 1):
            a, b, c, e = tour[i], tour[i + 1], tour[j], tour[(j + 1) % n]
            if cost[a][b] + cost[c][e] - cost[a][c] - cost[b][e] > 1e-12:
                return False
    return True


def test_moves_are_tours_with_exact_gains() -> None:
    rng = random.Random(1976)
    for n in (5, 6, 9):
        cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
        tour = list(range(n))
        rng.shuffle(tour)
        count = 0
        for move in or_moves(n):
            new = apply_or_move(tour, *move)
            assert sorted(new) == list(range(n))
            assert abs(tour_cost(cost, tour) - tour_cost(cost, new) - or_gain(cost, tour, *move)) < 1e-9
            # A move changes at most three edges, so it is a 3-opt move.
            assert len(edges(tour) - edges(new)) <= 3
            count += 1
        assert count > 0


def test_example() -> None:
    cost = euclid(SEVEN)
    start = [0, 2, 5, 6, 1, 4, 3]  # A C F G B E D
    # Move the segment E D (positions 5 and 6) between A and C (position 0).
    assert abs(or_gain(cost, start, 5, 2, 0, False) - 0.2322) < 1e-3
    assert apply_or_move(start, 5, 2, 0, False) == [0, 4, 3, 2, 5, 6, 1]
    assert is_two_optimal(cost, start) and not is_or_optimal(cost, start)
    tour, _ = or_opt(cost, start)
    assert is_or_optimal(cost, tour)
    assert abs(tour_cost(cost, tour) - 15.4760) < 1e-3  # OPT


def test_two_rows_with_a_crossing() -> None:
    """Two rows of m points, toured row after row with two long diagonals: Or-opt removes the crossing."""
    for m in range(3, 8):
        points = [(x, 1) for x in range(m)] + [(x, 0) for x in range(m)]
        cost = euclid(points)
        start = list(range(2 * m))
        assert not is_two_optimal(cost, start)
        tour, _ = or_opt(cost, start)
        assert abs(tour_cost(cost, tour) - 2 * m) < 1e-9  # OPT is the rectangle, 2(m - 1) + 2


def test_or_optimal_but_not_two_optimal() -> None:
    """Two far rows of 8 points with two long crossing diagonals: no segment move of 1 to 3 cities gains."""
    m, h = 8, 10
    points = [(x, h) for x in range(m)] + [(x, 0) for x in range(m)]
    cost = euclid(points)
    tour = list(range(2 * m))
    assert is_or_optimal(cost, tour)
    assert not is_two_optimal(cost, tour)
    assert abs(tour_cost(cost, tour) - 38.4126) < 1e-3
    assert abs(2 * (m - 1) + 2 * h - 34) < 1e-12  # OPT: the points are on the boundary of a rectangle


def test_local_optima_against_brute_force() -> None:
    rng = random.Random(1980)
    worst = 1.0
    for n in range(5, 9):
        for _ in range(4):
            cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
            tours = all_tours(n)
            opt = min(tour_cost(cost, t) for t in tours)
            for t in tours:
                if is_or_optimal(cost, t):
                    worst = max(worst, tour_cost(cost, t) / opt)
            start = list(range(n))
            rng.shuffle(start)
            tour, _ = or_opt(cost, start)
            assert sorted(tour) == list(range(n))
            assert is_or_optimal(cost, tour)
            assert tour_cost(cost, tour) >= opt - 1e-9
    # Measured on these instances, not a proved bound.
    assert worst < 2.0


def test_small_inputs() -> None:
    assert or_opt([[0]], [0]) == ([0], 0)
    cost = euclid([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert list(or_moves(4)) != []
    assert sorted(or_opt(cost, [0, 2, 1, 3])[0]) == [0, 1, 2, 3]
