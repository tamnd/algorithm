# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-median-problem/. The authors are listed in prov/D8T8TZ.jsonl.

import random

from k_median_problem import (
    brute_force_discrete,
    kmedian_cost,
    l1_continuous_brute,
    line_kmedian,
)


def line(a, b):
    return abs(a - b)


def l1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def test_worked_example():
    xs = [1, 2, 3, 4, 40, 41, 42]
    assert line_kmedian(xs, 1) == (117, [4])
    assert line_kmedian(xs, 2) == (6, [2, 41])
    assert brute_force_discrete(xs, 2, line)[0] == 6


def test_line_dp_matches_brute_force():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 8)
        xs = [rng.randint(-20, 20) for _ in range(n)]
        for k in range(1, n + 1):
            cost, centers = line_kmedian(xs, k)
            assert cost == brute_force_discrete(xs, k, line)[0]
            assert len(centers) == k
            assert kmedian_cost(xs, centers, line) == cost


def test_line_discrete_equals_continuous():
    # on a line, a median of each run is a data point, so the best centers
    # anywhere on the line cost no less than the best data points
    rng = random.Random(2)
    grid = [x / 2 for x in range(-2, 23)]
    for _ in range(50):
        xs = [rng.randint(0, 10) for _ in range(rng.randint(1, 6))]
        k = rng.randint(1, min(2, len(xs)))
        cont = brute_force_discrete(xs, k, line, candidates=grid)[0]
        assert line_kmedian(xs, k)[0] == cont


def test_discrete_within_twice_continuous():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(2, 6)
        pts = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)]
        k = rng.randint(1, min(3, n))
        cont = l1_continuous_brute(pts, k)
        disc = brute_force_discrete(pts, k, l1)[0]
        assert cont <= disc <= 2 * cont


def test_star_shows_factor_two():
    # leaves at pairwise distance 2, all at distance 1 from a hub that is
    # not a data point: discrete cost 2 (n - 1), cost with the hub n
    n = 6
    pts = list(range(n))

    def d(a, b):
        if a == b:
            return 0
        if "hub" in (a, b):
            return 1
        return 2

    assert brute_force_discrete(pts, 1, d)[0] == 2 * (n - 1)
    assert kmedian_cost(pts, ["hub"], d) == n
