# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-power-estimation/. The authors are listed in prov/QFM309.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction
from statistics import NormalDist

from monte_carlo_power_estimation import monte_carlo_power, power_sampler
from netlist import Circuit, transitions


def full_adder(p, a, b, c):
    return [
        (p + "t", "XOR", [a, b]),
        (p + "s", "XOR", [p + "t", c]),
        (p + "g", "AND", [a, b]),
        (p + "h", "AND", [p + "t", c]),
        (p + "co", "OR", [p + "g", p + "h"]),
    ]


# The two-bit ripple-carry adder of the page, unit load on every gate output.
ADD = Circuit(["a0", "b0", "a1", "b1", "ci"], full_adder("f0", "a0", "b0", "ci") + full_adder("f1", "a1", "b1", "f0co"))
CAP = {g: 1 for g, _, _ in ADD.gates}
UP = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 2), Fraction(1, 3), Fraction(1, 5)]
DOWN = [Fraction(1, 2), Fraction(1, 2), Fraction(1, 4), Fraction(1, 3), Fraction(1, 5)]


def exact_mean(c, up, down, cap, model):
    """E[energy per cycle] in the stationary regime, by enumeration of all 4^n vector pairs, in Fraction."""
    n = len(c.inputs)
    tot = Fraction(0)
    for x in itertools.product((0, 1), repeat=n):
        for y in itertools.product((0, 1), repeat=n):
            w = Fraction(1)
            for i in range(n):
                pi1 = up[i] / (up[i] + down[i])
                w *= pi1 if x[i] else 1 - pi1
                f = down[i] if x[i] else up[i]
                w *= f if x[i] != y[i] else 1 - f
            if w == 0:
                continue
            for v, k in transitions(c, x, y, model).items():
                tot += w * Fraction(cap.get(v, 0)) * k / 2
    return tot


def run(model, T, eps, runs, seed):
    mu = float(exact_mean(ADD, UP, DOWN, CAP, model))
    covered = relative_ok = 0
    sizes = []
    for r in range(runs):
        rng = random.Random(seed + r)
        s = power_sampler(ADD, [float(u) for u in UP], [float(d) for d in DOWN], CAP, T, rng, model)
        m, h, n = monte_carlo_power(s, eps, 0.05)
        assert n >= 30 and h < eps * m
        covered += abs(m - mu) <= h
        relative_ok += abs(m - mu) <= eps / (1 - eps) * mu
        sizes.append(n)
    return covered / runs, relative_ok / runs, sizes


def test_exact_means_of_the_page():
    assert exact_mean(ADD, UP, DOWN, CAP, "zero") == Fraction(233, 120)
    assert exact_mean(ADD, UP, DOWN, CAP, "transport") == Fraction(5519, 2160)


def test_welford_matches_statistics():
    rng = random.Random(1)
    data = [rng.expovariate(1.0) for _ in range(200)]
    it = iter(data)
    m, h, n = monte_carlo_power(lambda: next(it), eps=0.0, alpha=0.05, n_max=200)
    assert n == 200
    assert math.isclose(m, statistics.fmean(data), rel_tol=1e-12)
    z = NormalDist().inv_cdf(0.975)
    assert math.isclose(h, z * statistics.stdev(data) / math.sqrt(200), rel_tol=1e-9)


def test_minimum_sample_count_and_cap():
    m, h, n = monte_carlo_power(lambda: 1.0, eps=0.01)
    assert (m, h, n) == (1.0, 0.0, 30)
    m, h, n = monte_carlo_power(lambda: 0.0, eps=0.01, n_max=50)
    assert n == 50


def test_coverage_zero_delay():
    cov, rel, sizes = run("zero", T=4, eps=0.1, runs=300, seed=1000)
    # Nominal level 0.95; the measured coverage must be close to it.
    assert cov >= 0.9
    assert rel >= cov


def test_coverage_transport_delay():
    cov, rel, sizes = run("transport", T=4, eps=0.1, runs=150, seed=5000)
    assert cov >= 0.88
    assert rel >= cov


def test_sample_count_grows_as_one_over_eps_squared():
    _, _, wide = run("zero", T=4, eps=0.2, runs=40, seed=7000)
    _, _, narrow = run("zero", T=4, eps=0.1, runs=40, seed=7000)
    assert statistics.fmean(narrow) > 1.3 * statistics.fmean(wide)
