# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-opt/. The authors are listed in prov/F2HNR2.jsonl.

import itertools
import math
import random

from two_opt import is_two_optimal, tour_cost, two_opt, two_opt_gain

POINTS = [(0, 0), (2, 0), (5, 1), (4, 4), (1, 3), (6, 3)]  # A to F of the page


def euclid(points):
    return [[math.dist(a, b) for b in points] for a in points]


def random_metric(n, rng):
    """Shortest-path distances of a complete graph with random weights: a metric."""
    w = [[0 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w[i][j] = w[j][i] = rng.choice([1, 2, 3, 5, 8, 13])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                w[i][j] = min(w[i][j], w[i][k] + w[k][j])
    return w


def all_tours(n):
    return [[0, *q] for q in itertools.permutations(range(1, n)) if n < 3 or q[0] < q[-1]]


def bound(n):
    return 2 * math.sqrt(2) * sum(1 / math.sqrt(i) for i in range(1, n + 1))


def segments_cross(p, q, r, s):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    d1, d2 = orient(p, q, r), orient(p, q, s)
    d3, d4 = orient(r, s, p), orient(r, s, q)
    return d1 * d2 < 0 and d3 * d4 < 0


def test_example() -> None:
    cost = euclid(POINTS)
    start = [0, 3, 1, 4, 2, 5]  # A D B E C F, a tour with crossings
    assert abs(tour_cost(cost, start) - 26.7077) < 1e-3
    assert abs(two_opt_gain(cost, start, 0, 2) - 3.6569) < 1e-3
    tour, moves = two_opt(cost, start)
    assert is_two_optimal(cost, tour)
    assert moves == 3
    assert "".join("ABCDEF"[i] for i in tour) == "AEDFCB"
    assert abs(tour_cost(cost, tour) - 15.9590) < 1e-3  # OPT


def test_local_optimum_and_feasibility() -> None:
    rng = random.Random(1958)
    for n in range(4, 9):
        for _ in range(10):
            points = [(rng.random(), rng.random()) for _ in range(n)]
            cost = euclid(points)
            start = list(range(n))
            rng.shuffle(start)
            tour, _ = two_opt(cost, start)
            assert sorted(tour) == list(range(n))
            assert is_two_optimal(cost, tour)
            assert tour_cost(cost, tour) <= tour_cost(cost, start) + 1e-9


def test_every_two_optimal_tour_obeys_the_bound() -> None:
    rng = random.Random(1999)
    for n in range(4, 9):
        for trial in range(4):
            if trial % 2:
                cost = random_metric(n, rng)
            else:
                cost = euclid([(rng.random(), rng.random()) for _ in range(n)])
            tours = all_tours(n)
            opt = min(tour_cost(cost, t) for t in tours)
            for t in tours:
                if is_two_optimal(cost, t):
                    assert opt - 1e-9 <= tour_cost(cost, t) <= bound(n) * opt


def test_long_edge_count_of_the_proof() -> None:
    """A 2-optimal tour has fewer than 8 (OPT / L)^2 edges longer than L."""
    rng = random.Random(2014)
    for n in range(5, 9):
        cost = random_metric(n, rng)
        tours = all_tours(n)
        opt = min(tour_cost(cost, t) for t in tours)
        for t in tours:
            if not is_two_optimal(cost, t):
                continue
            lengths = sorted((cost[t[i]][t[(i + 1) % n]] for i in range(n)), reverse=True)
            for i, length in enumerate(lengths, start=1):
                assert length <= math.sqrt(8 / i) * opt + 1e-9


def test_no_crossings_in_the_plane() -> None:
    rng = random.Random(1981)
    for n in range(4, 30, 5):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        tour, _ = two_opt(euclid(points), list(range(n)))
        edges = [(points[tour[i]], points[tour[(i + 1) % n]]) for i in range(n)]
        for (p, q), (r, s) in itertools.combinations(edges, 2):
            assert not segments_cross(p, q, r, s)


def test_small_inputs() -> None:
    assert two_opt([[0]], [0]) == ([0], 0)
    cost = euclid([(0, 0), (1, 0), (1, 1)])
    assert two_opt(cost, [0, 1, 2]) == ([0, 1, 2], 0)
