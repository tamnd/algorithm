# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-integration/. The authors are listed in prov/2FTF47.jsonl.

import math
import random
import statistics

import pytest

from monte_carlo_integration import monte_carlo


def disc(x):
    return 4.0 if x[0] * x[0] + x[1] * x[1] <= 1.0 else 0.0


SIGMA_DISC = math.sqrt(math.pi * (4 - math.pi))


def test_example_quarter_disc() -> None:
    est, se = monte_carlo(disc, [0.0, 0.0], [1.0, 1.0], 1000, random.Random(1))
    assert est == pytest.approx(3.112, abs=1e-12)
    assert se == pytest.approx(0.0525949, abs=1e-6)


def test_matches_two_pass_oracle_on_random_cases() -> None:
    # Same seed, same points: compare with statistics.fmean and statistics.stdev.
    rng = random.Random(77)
    for case in range(500):
        s = rng.randint(1, 4)
        lo = [rng.uniform(-3, 3) for _ in range(s)]
        hi = [a + rng.uniform(-2, 4) for a in lo]
        c = [rng.uniform(-2, 2) for _ in range(s + 1)]
        f = lambda x, c=c: c[0] + sum(ck * xk * xk for ck, xk in zip(c[1:], x))
        n = rng.randint(2, 40)
        est, se = monte_carlo(f, lo, hi, n, random.Random(case))
        g = random.Random(case)
        ys = []
        for _ in range(n):
            ys.append(f([a + (b - a) * g.random() for a, b in zip(lo, hi)]))
        vol = math.prod(b - a for a, b in zip(lo, hi))
        assert est == pytest.approx(vol * statistics.fmean(ys), rel=1e-9, abs=1e-9)
        assert se == pytest.approx(abs(vol) * statistics.stdev(ys) / math.sqrt(n), rel=1e-7, abs=1e-9)


def test_rms_error_matches_sigma_over_sqrt_n() -> None:
    # f = x1^2 + ... + xs^2 on [0,1]^s: I = s/3, sigma^2 = s (1/5 - 1/9) = 4s/45.
    s, n, reps = 3, 1000, 300
    f = lambda x: sum(t * t for t in x)
    sigma = math.sqrt(4 * s / 45)
    errs = [monte_carlo(f, [0.0] * s, [1.0] * s, n, random.Random(1000 + r))[0] - s / 3 for r in range(reps)]
    rms = math.sqrt(sum(e * e for e in errs) / reps)
    # the squared RMS of 300 replications has relative sd about sqrt(2/300) = 0.08
    assert 0.85 < rms / (sigma / math.sqrt(n)) < 1.15
    assert abs(statistics.fmean(errs)) < 4 * sigma / math.sqrt(n * reps)  # unbiased


def test_rate_is_n_to_the_minus_one_half() -> None:
    f = lambda x: math.exp(x[0])
    exact = math.e - 1
    rms = []
    for n in (100, 1600):
        errs = [monte_carlo(f, [0.0], [1.0], n, random.Random(5000 + r))[0] - exact for r in range(200)]
        rms.append(math.sqrt(sum(e * e for e in errs) / len(errs)))
    assert 3.2 < rms[0] / rms[1] < 4.8  # the predicted factor is sqrt(16) = 4


def test_confidence_interval_coverage_and_standard_error() -> None:
    hits = 0
    reps = 400
    for r in range(reps):
        est, se = monte_carlo(disc, [0.0, 0.0], [1.0, 1.0], 400, random.Random(9000 + r))
        assert 0.7 < se / (SIGMA_DISC / 20) < 1.3
        hits += abs(est - math.pi) <= 1.96 * se
    assert 0.91 <= hits / reps <= 0.99


def test_dimension_does_not_enter_the_rate() -> None:
    # mean of s uniforms: I = 1/2, sigma^2 = 1/(12 s), for s = 1 and s = 20
    for s in (1, 20):
        f = lambda x: sum(x) / len(x)
        sigma = math.sqrt(1 / (12 * s))
        errs = [monte_carlo(f, [0.0] * s, [1.0] * s, 200, random.Random(300 + r))[0] - 0.5 for r in range(150)]
        rms = math.sqrt(sum(e * e for e in errs) / len(errs))
        assert 0.75 < rms / (sigma / math.sqrt(200)) < 1.25


def test_jump_and_endpoint_singularity() -> None:
    est, se = monte_carlo(lambda x: 1.0 if x[0] < 1 / 3 else 0.0, [0.0], [1.0], 20000, random.Random(3))
    assert abs(est - 1 / 3) < 4 * math.sqrt(2 / 9 / 20000)
    # x^(-1/2): finite integral 2, infinite variance; the estimate still converges
    est, _ = monte_carlo(lambda x: 1 / math.sqrt(1.0 - x[0]), [0.0], [1.0], 100000, random.Random(4))
    assert abs(est - 2.0) < 0.05


def test_edge_cases() -> None:
    est, se = monte_carlo(disc, [0.0, 0.5], [1.0, 0.5], 10, random.Random(0))
    assert est == 0.0 and se == 0.0
    e1, s1 = monte_carlo(lambda x: x[0] ** 2, [0.0], [2.0], 50, random.Random(8))
    e2, s2 = monte_carlo(lambda x: x[0] ** 2, [2.0], [0.0], 50, random.Random(8))
    assert e2 < 0 and s2 > 0 and abs(e1 - 8 / 3) < 5 * s1 and abs(e2 + 8 / 3) < 5 * s2
    assert monte_carlo(lambda x: 7.0, [0.0, 0.0], [2.0, 3.0], 5, random.Random(1)) == (42.0, 0.0)
    with pytest.raises(ValueError):
        monte_carlo(disc, [0.0, 0.0], [1.0, 1.0], 1, random.Random(0))
    with pytest.raises(ValueError):
        monte_carlo(disc, [0.0], [1.0, 1.0], 10, random.Random(0))
