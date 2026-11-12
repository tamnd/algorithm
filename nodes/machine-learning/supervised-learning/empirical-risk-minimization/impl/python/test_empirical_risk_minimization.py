# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-risk-minimization/. The authors are listed in prov/CNMDNK.jsonl.

import random
from fractions import Fraction

from empirical_risk_minimization import (
    empirical_risk, erm_finite, erm_threshold, memorizer, threshold,
)


def brute_force_threshold(sample):
    cands = sorted({x for x, _ in sample}) + [float("inf")]
    return min(sum(1 for x, y in sample if threshold(t)(x) != y) for t in cands)


def test_sweep_matches_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 25)
        sample = [(rng.randint(0, 10), rng.randint(0, 1)) for _ in range(n)]
        t, err = erm_threshold(sample)
        assert err == brute_force_threshold(sample)
        assert sum(1 for x, y in sample if threshold(t)(x) != y) == err


def test_realizable_sample_gives_zero_error():
    rng = random.Random(2)
    for _ in range(50):
        xs = [rng.uniform(0, 1) for _ in range(30)]
        sample = [(x, 1 if x >= 0.37 else 0) for x in xs]
        assert erm_threshold(sample)[1] == 0


def test_finite_class_erm_returns_a_minimizer():
    rng = random.Random(3)
    H = [threshold(t / 4) for t in range(-1, 6)]
    for _ in range(50):
        sample = [(rng.uniform(0, 1), rng.randint(0, 1)) for _ in range(15)]
        i, r = erm_finite(H, sample)
        assert r == min(empirical_risk(h, sample) for h in H)
        assert empirical_risk(H[i], sample) == r


def test_memorizer_fits_the_sample_but_not_the_distribution():
    # D uniform on {0..999}, target 1 on x < 500. The memorizer outputs 0 off the sample.
    rng = random.Random(4)
    target = lambda x: 1 if x < 500 else 0
    sample = [(x, target(x)) for x in (rng.randrange(1000) for _ in range(50))]
    h = memorizer(sample)
    assert empirical_risk(h, sample) == 0
    true_risk = Fraction(sum(1 for x in range(1000) if h(x) != target(x)), 1000)
    assert true_risk >= Fraction(45, 100)
    t, err = erm_threshold([(-x, y) for x, y in sample])  # x < 500 means -x > -500
    assert err == 0
