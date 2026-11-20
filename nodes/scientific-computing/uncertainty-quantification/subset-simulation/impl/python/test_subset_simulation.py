# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subset-simulation/. The authors are listed in prov/2D3RV8.jsonl.
import math
import random
import statistics

import pytest

from subset_simulation import mm_step, subset_simulation


def phi(t):
    return 0.5 * math.erfc(-t / math.sqrt(2.0))


def run_many(g, d, seeds, **kw):
    return [subset_simulation(g, d, random.Random(s), **kw) for s in seeds]


def test_linear_limit_state_in_twenty_dimensions():
    g = lambda u: 3.0 - sum(u) / math.sqrt(len(u))
    est = [r["pf"] for r in run_many(g, 20, range(20))]
    m = statistics.mean(est)
    se = statistics.stdev(est) / math.sqrt(len(est))
    assert abs(m - phi(-3.0)) < 4.0 * se
    assert abs(m / phi(-3.0) - 1.0) < 0.3


def test_two_design_points_are_both_found():
    est = [r["pf"] for r in run_many(lambda u: 3.0 - abs(u[0]), 5, range(20))]
    m = statistics.mean(est)
    se = statistics.stdev(est) / math.sqrt(len(est))
    assert abs(m - 2.0 * phi(-3.0)) < 4.0 * se
    assert m > 1.5 * phi(-3.0)


def test_estimate_is_the_product_of_the_level_probabilities():
    r = subset_simulation(lambda u: 3.0 - u[0], 3, random.Random(5))
    assert r["pf"] == pytest.approx(math.prod(r["probs"]), rel=1e-15)
    assert all(p == 0.1 for p in r["probs"][:-1])
    assert 0.0 < r["probs"][-1] <= 1.0
    th = r["thresholds"]
    assert th[-1] == 0.0 and all(a > b for a, b in zip(th, th[1:]))
    assert r["calls"] <= 1000 + 900 * (len(r["probs"]) - 1)


def test_large_probability_is_plain_monte_carlo():
    rng = random.Random(3)
    r = subset_simulation(lambda u: 0.5 - u[0], 2, rng)
    assert len(r["probs"]) == 1 and r["calls"] == 1000
    rng2 = random.Random(3)
    us = [[rng2.gauss(0.0, 1.0) for _ in range(2)] for _ in range(1000)]
    assert r["pf"] == sum(1 for u in us if 0.5 - u[0] <= 0.0) / 1000


def test_modified_metropolis_keeps_the_conditional_law():
    rng = random.Random(11)
    g = lambda u: 1.0 - u[0]
    p1 = phi(-1.0)
    us = []
    for _ in range(4000):
        t = rng.random()
        x = -statistics.NormalDist().inv_cdf(p1 * t)
        us.append([x, rng.gauss(0.0, 1.0)])
    gs = [g(u) for u in us]
    for _ in range(3):
        nxt = [mm_step(g, u, gu, 0.0, rng) for u, gu in zip(us, gs)]
        us = [s[0] for s in nxt]
        gs = [s[1] for s in nxt]
    assert all(v <= 0.0 for v in gs)
    mean_x = statistics.mean(u[0] for u in us)
    assert abs(mean_x - math.exp(-0.5) / math.sqrt(2.0 * math.pi) / p1) < 0.04
    assert abs(statistics.mean(u[1] for u in us)) < 0.06
    assert abs(statistics.pvariance([u[1] for u in us]) - 1.0) < 0.08


def test_same_seed_same_result():
    g = lambda u: 3.0 - u[1]
    a = subset_simulation(g, 4, random.Random(9))
    b = subset_simulation(g, 4, random.Random(9))
    assert a == b


def test_bad_sizes_are_rejected():
    with pytest.raises(ValueError):
        subset_simulation(lambda u: 1.0 - u[0], 1, random.Random(0), n=1000, p0=0.15)
    with pytest.raises(ValueError):
        subset_simulation(lambda u: 1.0 - u[0], 1, random.Random(0), n=100, p0=0.003)


def test_unreachable_failure_set_raises():
    with pytest.raises(RuntimeError):
        subset_simulation(lambda u: 50.0 - u[0], 1, random.Random(0), n=100, max_levels=3)
