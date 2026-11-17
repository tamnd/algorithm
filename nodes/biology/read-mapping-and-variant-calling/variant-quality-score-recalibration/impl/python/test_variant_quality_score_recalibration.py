# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variant-quality-score-recalibration/. The authors are listed in prov/DTZA1Z.jsonl.

import math
import os
import random

import pytest

from variant_quality_score_recalibration import (fit_gmm, log_density, tranche_threshold, vqsr)


def test_tranche_threshold_against_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        s = [rng.choice((-2.0, -1.0, 0.0, 0.5, 1.0, 3.0)) for _ in range(rng.randint(1, 12))]
        sens = rng.choice((0.5, 0.9, 0.99, 1.0, 1 / 3))
        need = math.ceil(sens * len(s) - 1e-12)
        best = max(t for t in s if sum(v >= t for v in s) >= need)
        assert tranche_threshold(s, sens) == best
    assert tranche_threshold([5.0, 1.0, 3.0, 2.0], 0.75) == 2.0
    with pytest.raises(ValueError):
        tranche_threshold([], 0.9)


def test_one_component_is_the_sample_mean_and_variance():
    rng = random.Random(2)
    data = [(rng.gauss(4, 2), rng.gauss(-1, 0.5)) for _ in range(300)]
    w, mu, var = fit_gmm(data, 1, random.Random(0))
    for j in range(2):
        m = sum(x[j] for x in data) / len(data)
        v = sum((x[j] - m) ** 2 for x in data) / len(data)
        assert abs(mu[0][j] - m) < 1e-9 and abs(var[0][j] - v) < 1e-9
    assert w == [1.0]


def test_density_matches_direct_sum():
    mix = ([0.3, 0.7], [[0.0, 1.0], [2.0, -1.0]], [[1.0, 4.0], [0.5, 0.25]])
    x = (0.7, 0.2)
    direct = 0.0
    for w, m, v in zip(*mix):
        dens = 1.0
        for a, mm, vv in zip(x, m, v):
            dens *= math.exp(-(a - mm) ** 2 / (2 * vv)) / math.sqrt(2 * math.pi * vv)
        direct += w * dens
    assert abs(log_density(mix, x) - math.log(direct)) < 1e-12


def test_em_never_lowers_the_likelihood():
    rng = random.Random(3)
    data = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(150)] + \
           [(rng.gauss(5, 0.5), rng.gauss(3, 2)) for _ in range(100)]
    for seed in range(4):
        trace = []
        fit_gmm(data, 3, random.Random(seed), iters=40, trace=trace)
        assert all(b >= a - 1e-7 * abs(a) for a, b in zip(trace, trace[1:]))


def simulate(rng):
    """True variants in two clusters of high QD and low FS; artifacts at low QD and high FS."""
    calls, real = [], []
    for _ in range(700):
        c = rng.random() < 0.6
        calls.append((rng.gauss(12 if c else 25, 2), abs(rng.gauss(1, 1))))
        real.append(True)
    for _ in range(200):
        calls.append((rng.gauss(4, 2), rng.gauss(18, 5)))
        real.append(False)
    return calls, real


def test_filters_artifacts_at_the_target_sensitivity():
    rng = random.Random(4)
    calls, real = simulate(rng)
    training = [r and rng.random() < 0.5 for r in real]
    scores, threshold, passed = vqsr(calls, training, training, 0.99, seed=1)
    truth_kept = sum(p for p, t in zip(passed, training) if t) / sum(training)
    assert truth_kept >= 0.99
    real_kept = sum(p for p, r in zip(passed, real) if r) / sum(real)
    junk_kept = sum(p for p, r in zip(passed, real) if not r) / (len(real) - sum(real))
    assert real_kept > 0.97 and junk_kept < 0.05
    assert all((s >= threshold) == p for s, p in zip(scores, passed))


if __name__ == "__main__":
    raise SystemExit(pytest.main([os.path.abspath(__file__), "-q"]))
