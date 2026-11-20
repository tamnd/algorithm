# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geiger-method/. The authors are listed in prov/9PWX4B.jsonl.

import random

import imgla as la
from geiger_method import (
    best_origin_time,
    distance,
    geiger,
    jacobian,
    misfit,
    predicted_times,
)

V = 6000.0
NET5 = [(0.0, 0.0, 0.0), (10000.0, 0.0, 0.0), (0.0, 10000.0, 0.0),
        (10000.0, 10000.0, 0.0), (5000.0, 12000.0, 0.0)]
NET6 = NET5 + [(3000.0, 4000.0, 0.0)]
TRUE = [4000.0, 3000.0, 5000.0, 0.5]
START = [4500.0, 3500.0, 7000.0, 0.4]


def test_page_example_converges_quadratically():
    times = predicted_times(TRUE, NET6, V)
    assert [round(t, 4) for t in times] == [1.6785, 1.8944, 2.0811, 2.248, 2.224, 1.366]
    errs = []
    for k in range(5):
        m, _ = geiger(NET6, times, V, START, iters=k)
        errs.append(distance(m[:3], TRUE[:3]))
    assert 290.0 < errs[1] < 295.0
    assert 4.7 < errs[2] < 4.9
    assert errs[3] < 2e-3
    assert errs[4] < 1e-8


def test_without_the_near_station_the_first_step_overshoots():
    times = predicted_times(TRUE, NET5, V)
    m, _ = geiger(NET5, times, V, START, iters=1)
    assert m[2] < 0.0


def test_safeguards_recover_from_a_far_start():
    times = predicted_times(TRUE, NET5, V)
    for z0 in (2000.0, 8000.0, 15000.0):
        m, _ = geiger(NET5, times, V, [5000.0, 5000.0, z0, 0.0], iters=30,
                      max_step=2000.0, keep_below_surface=True)
        assert distance(m[:3], TRUE[:3]) < 1e-6
        assert abs(m[3] - TRUE[3]) < 1e-9


def test_jacobian_matches_finite_differences():
    rng = random.Random(1)
    for _ in range(10):
        m = [rng.uniform(0.0, 10000.0), rng.uniform(0.0, 10000.0), rng.uniform(1000.0, 20000.0),
             rng.uniform(-1.0, 1.0)]
        g = jacobian(m, NET6, V)
        for c, h in ((0, 0.01), (1, 0.01), (2, 0.01), (3, 1e-6)):
            mp, mm = list(m), list(m)
            mp[c] += h
            mm[c] -= h
            fd = [(a - b) / (2 * h) for a, b in zip(predicted_times(mp, NET6, V), predicted_times(mm, NET6, V))]
            assert max(abs(a - row[c]) for a, row in zip(fd, g)) < 1e-9


def test_noisy_times_reach_the_least_squares_minimum():
    rng = random.Random(2)
    times = [t + rng.gauss(0.0, 0.01) for t in predicted_times(TRUE, NET6, V)]
    m, hist = geiger(NET6, times, V, START, iters=30)
    # The gradient G^T r is zero at the solution.
    r = [t - p for t, p in zip(times, predicted_times(m, NET6, V))]
    gtr = la.rmatvec(jacobian(m, NET6, V), r)
    assert max(abs(c) for c in gtr[:3]) < 1e-12
    assert abs(gtr[3]) < 1e-12
    # A grid search over the hypocenter, with the best origin time, never does better.
    best = float("inf")
    for i in range(-5, 6):
        for j in range(-5, 6):
            for k in range(-5, 6):
                h = [m[0] + 40.0 * i, m[1] + 40.0 * j, m[2] + 80.0 * k]
                t0 = best_origin_time(h, NET6, times, V)
                best = min(best, misfit(h + [t0], NET6, times, V))
    assert hist[-1] <= best + 1e-15
    assert distance(m[:3], TRUE[:3]) < 500.0


def test_best_origin_time_is_the_mean():
    times = predicted_times(TRUE, NET6, V)
    assert abs(best_origin_time(TRUE[:3], NET6, times, V) - TRUE[3]) < 1e-12


def test_small_aperture_couples_depth_and_origin_time():
    # A deep source under a small network: the depth and origin-time columns of G
    # are nearly parallel, so G^T G is badly conditioned.
    def cond(aperture):
        st = [(aperture * c, aperture * s, 0.0) for c, s in ((1, 0), (0, 1), (-1, 0), (0, -1), (0.7, 0.7))]
        g = jacobian([0.0, 0.0, 10000.0, 0.0], st, V)
        scaled = [[row[0] * V, row[1] * V, row[2] * V, row[3]] for row in g]
        w, _ = la.sym_eig(la.matmul(la.transpose(scaled), scaled))
        return w[-1] / w[0]

    assert cond(2000.0) > 50.0 * cond(30000.0)
