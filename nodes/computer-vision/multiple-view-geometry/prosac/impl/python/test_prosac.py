# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prosac/. The authors are listed in prov/B0M487.jsonl.

import math
import random

from prosac import (choose_n_star, growth_schedule, line_through, min_inliers_table, point_line_distance,
                    prosac, samples_needed)

EXAMPLE = [(0, 0), (0, 3), (2, 2), (5, 5), (4, 1), (1, 1), (3, 3), (2, 5), (4, 4), (5, 2)]


def planted(rng, n_in, n_out, good_order=True):
    true_line = line_through([(0.0, 2.0), (1.0, 2.5)])
    items = []
    for _ in range(n_in):
        x = rng.uniform(0.0, 10.0)
        items.append((rng.uniform(0.0, 0.3) if good_order else rng.random(), (x, 0.5 * x + 2.0), True))
    while len(items) < n_in + n_out:
        q = (rng.uniform(0.0, 10.0), rng.uniform(-5.0, 12.0))
        if point_line_distance(true_line, q) > 1.0:
            items.append((rng.uniform(0.1, 1.0) if good_order else rng.random(), q, False))
    items.sort(key=lambda z: z[0])
    return [p for _, p, _ in items], [i for i, z in enumerate(items) if z[2]]


def test_schedule_counts_subsets():
    for m in (2, 3):
        Tp = growth_schedule(12, m, math.comb(12, m))
        assert all(Tp[n] == math.comb(n, m) for n in range(m, 13))
    Tp = growth_schedule(100, 2, 200000)
    assert Tp[2] == 1 and Tp[3] == 82
    assert all(Tp[n + 1] >= Tp[n] for n in range(2, 100))


def test_samples_follow_eq6():
    data = [(float(i), float(i * i % 7)) for i in range(15)]
    where = {p: i for i, p in enumerate(data)}
    seen = []

    def solver(sample):
        seen.append(sorted(where[p] for p in sample))
        return line_through(sample)

    Tp = growth_schedule(15, 2, 105)
    prosac(data, 1e-9, random.Random(4), T_N=105, max_trials=60, fit_minimal=solver)
    for t, idx in enumerate(seen, start=1):
        g = min(n for n in Tp if Tp[n] >= t)
        assert idx[-1] == g - 1 and idx[0] < g - 1


def test_min_inliers_table():
    imin = min_inliers_table(30, 2, 0.05, 0.05)
    for n in range(2, 31):
        def tail(j):
            return sum(math.comb(n - 2, i - 2) * 0.05 ** (i - 2) * 0.95 ** (n - i) for i in range(j, n + 1))
        j = imin[n]
        assert tail(j) < 0.05 and (j == 2 or tail(j - 1) >= 0.05)


def test_example_stopping():
    flags = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
    imin = min_inliers_table(10, 2, 0.05, 0.05)
    assert [imin[n] for n in range(2, 11)] == [3, 4, 4, 4, 4, 4, 4, 4, 5]
    assert choose_n_star(flags, 2, imin, 0.05, 10000) == (7, 5)
    assert samples_needed(5, 7, 2, 0.05) == 5 and samples_needed(4, 6, 2, 0.05) == 6


def test_example_run():
    model, inl, t, n_star = prosac(EXAMPLE, 0.1, random.Random(0), T_N=45)
    assert inl == [0, 2, 3, 5, 6, 8] and t == 5 and n_star == 7
    assert abs(model[0] - math.sqrt(0.5)) < 1e-12 and abs(model[0] + model[1]) < 1e-12


def test_good_ordering_is_fast():
    for seed in range(3):
        data, true_in = planted(random.Random(seed), 30, 70)
        _, inl, t, _ = prosac(data, 0.05, random.Random(seed), T_N=math.comb(100, 2))
        assert inl == true_in
        assert t < 49  # RANSAC needs 49 samples for p = 0.99 at w = 0.3


def test_random_ordering_still_works():
    for seed in range(3):
        data, true_in = planted(random.Random(10 + seed), 30, 70, good_order=False)
        _, inl, _, _ = prosac(data, 0.05, random.Random(seed), T_N=math.comb(100, 2))
        assert inl == true_in


def test_small_input():
    assert prosac([(0.0, 0.0)], 0.1, random.Random(0)) == (None, [], 0, 1)
