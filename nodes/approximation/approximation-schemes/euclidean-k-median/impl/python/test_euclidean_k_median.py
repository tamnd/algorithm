# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euclidean-k-median/. The authors are listed in prov/3ZK1AD.jsonl.

import random
from math import dist, sqrt

from euclidean_k_median import cost, discrete_k_median, line_k_median, weiszfeld


def test_examples() -> None:
    xs = [1, 2, 3, 10, 11, 20]
    assert line_k_median(xs, 1) == (35, [3])
    assert line_k_median(xs, 2) == (12, [2, 11])
    assert line_k_median(xs, 3) == (3, [2, 10, 20])
    # an equilateral triangle of side 1: the best input point costs 2, the Fermat point costs sqrt(3)
    tri = [(0.0, 0.0), (1.0, 0.0), (0.5, sqrt(3) / 2)]
    assert abs(discrete_k_median(tri, 1)[0] - 2) < 1e-12
    y = weiszfeld(tri)
    assert abs(cost(tri, [y]) - sqrt(3)) < 1e-9


def test_line_dp_against_brute_force() -> None:
    rng = random.Random(1984)
    for _ in range(300):
        n = rng.randint(1, 9)
        xs = [float(rng.randint(0, 30)) for _ in range(n)]
        k = rng.randint(1, n)
        val, centres = line_k_median(xs, k)
        pts = [(x,) for x in xs]
        assert abs(val - discrete_k_median(pts, k)[0]) < 1e-9
        assert abs(cost(pts, [(c,) for c in centres]) - val) < 1e-9
        # a centre between two points can be moved to a point without loss, so the input points suffice
        if k <= 2:
            grid = [(t / 2,) for t in range(61)]
            assert abs(val - discrete_k_median(pts, k, grid)[0]) < 1e-9


def test_input_points_lose_at_most_a_factor_two() -> None:
    rng = random.Random(1988)
    for _ in range(300):
        pts = [(rng.random(), rng.random()) for _ in range(rng.randint(1, 8))]
        best_point = discrete_k_median(pts, 1)[0]
        for c in [weiszfeld(pts), (rng.random(), rng.random()), (rng.uniform(-3, 3), rng.uniform(-3, 3))]:
            assert best_point <= 2 * cost(pts, [c]) + 1e-12


def test_more_centres_cost_less() -> None:
    rng = random.Random(1998)
    for _ in range(50):
        pts = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(rng.randint(2, 8))]
        values = [discrete_k_median(pts, k)[0] for k in range(1, len(pts) + 1)]
        assert all(a >= b - 1e-12 for a, b in zip(values, values[1:])) and values[-1] == 0
        # one centre serves the two farthest points p and q at a total distance of at least |pq|
        far = max(dist(p, q) for p in pts for q in pts)
        assert values[0] >= far - 1e-12
