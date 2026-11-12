# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sammon-mapping/. The authors are listed in prov/HP4B32.jsonl.

import math
import random

from sammon_mapping import derivatives, sammon, sammon_step, sammon_stress


def euclid(points):
    return [[math.dist(p, q) for q in points] for p in points]


def test_derivatives_match_finite_differences():
    rng = random.Random(2)
    x = [tuple(rng.uniform(0, 3) for _ in range(3)) for _ in range(6)]
    delta = euclid(x)
    y = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(6)]
    g, h = derivatives(y, delta)
    eps = 1e-5
    for p in range(6):
        for q in range(2):
            yp = [list(r) for r in y]
            ym = [list(r) for r in y]
            yp[p][q] += eps
            ym[p][q] -= eps
            e0, ep, em = sammon_stress(y, delta), sammon_stress(yp, delta), sammon_stress(ym, delta)
            assert abs((ep - em) / (2 * eps) - g[p][q]) < 1e-6
            assert abs((ep - 2 * e0 + em) / eps ** 2 - h[p][q]) < 1e-3


def test_zero_stress_and_fixed_point_for_representable_input():
    rng = random.Random(4)
    y = [(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(7)]
    delta = euclid(y)
    assert sammon_stress(y, delta) == 0.0
    y2 = sammon_step(y, delta)
    assert max(abs(a - b) for p, q in zip(y, y2) for a, b in zip(p, q)) < 1e-12


def test_stress_decreases_on_average():
    starts, ends = [], []
    for seed in range(8):
        rng = random.Random(seed)
        x = [tuple(rng.uniform(0, 1) for _ in range(4)) for _ in range(10)]
        delta = euclid(x)
        y0 = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(10)]
        _, hist = sammon(delta, y0, iters=60)
        starts.append(hist[0])
        ends.append(hist[-1])
        assert hist[-1] < hist[0]
    assert sum(ends) / len(ends) < 0.5 * sum(starts) / len(starts)


def test_recovers_planar_data():
    rng = random.Random(6)
    x = [(rng.uniform(0, 4), rng.uniform(0, 4)) for _ in range(8)]
    delta = euclid(x)
    y0 = [(a + rng.gauss(0, 0.3), b + rng.gauss(0, 0.3)) for a, b in x]
    _, hist = sammon(delta, y0, iters=300)
    assert hist[-1] < 1e-8
