# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-model-checking/. The authors are listed in prov/HY0E25.jsonl.

import math
import random

import pytest

from statistical_model_checking import (
    bounded_until_sampler,
    estimate,
    hoeffding_samples,
    sprt,
    sprt_parameters,
    sprt_verdict,
)


def bernoulli(p, rng):
    return lambda: rng.random() < p


def exact_sprt(p, params):
    """Exact (Pr[accept H0], Pr[accept H1], E[samples]) of the SPRT when each
    sample is 1 with probability p, by dynamic programming over the number
    of successes. Runs until the mass still undecided is below 1e-15."""
    mass = {0: 1.0}
    h0 = h1 = expected = 0.0
    m = 0
    while sum(mass.values()) > 1e-15:
        m += 1
        new = {}
        for d, w in mass.items():
            for dd, q in ((d + 1, p), (d, 1 - p)):
                if q == 0:
                    continue
                v = sprt_verdict(dd, m, params)
                if v is None:
                    new[dd] = new.get(dd, 0.0) + w * q
                else:
                    expected += m * w * q
                    if v:
                        h0 += w * q
                    else:
                        h1 += w * q
        mass = new
    return h0, h1, expected


def binomial_miss(n, p, eps):
    """Exact Pr[|K/n - p| >= eps] for K ~ Binomial(n, p), 0 < p < 1."""
    total = 0.0
    for k in range(n + 1):
        if abs(k - n * p) >= n * eps - 1e-9:
            logpmf = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            logpmf += k * math.log(p) + (n - k) * math.log(1 - p)
            total += math.exp(logpmf)
    return total


SETTINGS = [
    # theta, eps, alpha, beta
    (0.5, 0.05, 0.05, 0.05),
    (0.3, 0.1, 0.01, 0.1),
    (0.9, 0.05, 0.1, 0.01),
    (0.2, 0.05, 0.05, 0.2),
    (0.75, 0.02, 0.01, 0.01),
]


def test_hoeffding_sample_size() -> None:
    assert hoeffding_samples(0.05, 0.05) == 738
    assert hoeffding_samples(0.05, 0.1) == 600
    assert hoeffding_samples(0.01, 0.05) == 18445
    assert hoeffding_samples(0.01, 0.01) == 26492
    for eps in (0.3, 0.1, 0.05, 0.02, 0.01):
        for delta in (0.5, 0.1, 0.05, 0.01, 1e-6):
            n = hoeffding_samples(eps, delta)
            assert 2 * math.exp(-2 * n * eps * eps) <= delta
            assert n == 1 or 2 * math.exp(-2 * (n - 1) * eps * eps) > delta


def test_hoeffding_guarantee_is_exact_for_the_binomial() -> None:
    # the true miss probability of the estimator, summed from the binomial law
    for eps, delta in ((0.1, 0.1), (0.05, 0.05), (0.05, 0.01), (0.02, 0.1)):
        n = hoeffding_samples(eps, delta)
        for p in (0.01, 0.1, 0.3, 0.5, 0.77, 0.95):
            assert binomial_miss(n, p, eps) <= delta


def test_hoeffding_seeded_runs() -> None:
    eps, delta, runs = 0.05, 0.1, 300
    for seed, p in enumerate((0.03, 0.25, 0.5, 0.8)):
        rng = random.Random(1000 + seed)
        misses = 0
        for _ in range(runs):
            est, n = estimate(bernoulli(p, rng), eps, delta)
            assert n == 600
            misses += abs(est - p) >= eps
        assert misses <= delta * runs


def test_sprt_exact_error_bounds() -> None:
    for theta, eps, alpha, beta in SETTINGS:
        p0, p1 = theta + eps, theta - eps
        params = sprt_parameters(p0, p1, alpha, beta)
        a, b = (1 - beta) / alpha, beta / (1 - alpha)
        alpha_true = exact_sprt(p0, params)[1]
        beta_true = exact_sprt(p1, params)[0]
        # Wald's inequalities, then the three bounds that follow from them
        assert a * alpha_true <= 1 - beta_true + 1e-12
        assert beta_true <= b * (1 - alpha_true) + 1e-12
        assert alpha_true <= alpha / (1 - beta) + 1e-12
        assert beta_true <= beta / (1 - alpha) + 1e-12
        assert alpha_true + beta_true <= alpha + beta + 1e-12
        # the errors are largest at the edges of the indifference region
        for i in range(1, 6):
            above = p0 + (1 - p0) * i / 6
            below = p1 * i / 6
            assert exact_sprt(above, params)[1] <= alpha_true + 1e-12
            assert exact_sprt(below, params)[0] <= beta_true + 1e-12
        # the strict thresholds 1/alpha and beta bound the errors by alpha and beta
        strict = sprt_parameters(p0, p1, alpha, beta, strict=True)
        assert exact_sprt(p0, strict)[1] <= alpha + 1e-12
        assert exact_sprt(p1, strict)[0] <= beta + 1e-12


def test_symmetric_case_is_gamblers_ruin() -> None:
    params = sprt_parameters(0.55, 0.45, 0.05, 0.05)
    for m in range(1, 80):
        for d in range(m + 1):
            v = sprt_verdict(d, m, params)
            gap = (m - d) - d  # failures minus successes
            if abs(gap) < 15:
                assert v is None
            else:
                assert v is (gap < 0)
    h0, h1, expected = exact_sprt(0.55, params)
    assert abs(h1 - 1 / (1 + (11 / 9) ** 15)) < 1e-12
    assert abs(exact_sprt(0.5, params)[2] - 225) < 1e-9


def test_sprt_seeded_runs() -> None:
    theta, eps, alpha, beta = 0.5, 0.05, 0.05, 0.05
    params = sprt_parameters(theta + eps, theta - eps, alpha, beta)
    runs = 2000
    for seed, (p, wrong_answer) in enumerate(((0.55, False), (0.45, True))):
        rng = random.Random(2002 + seed)
        wrong = used = 0
        for _ in range(runs):
            verdict, m = sprt(bernoulli(p, rng), theta, eps, alpha, beta)
            wrong += verdict is wrong_answer
            used += m
        h0, h1, expected = exact_sprt(p, params)
        err = h1 if wrong_answer is False else h0
        sigma = math.sqrt(err * (1 - err) / runs)
        rate = wrong / runs
        assert rate <= alpha / (1 - beta) + 3 * sigma
        assert abs(rate - err) <= 4 * sigma
        assert abs(used / runs - expected) <= 0.05 * expected
    # far outside the indifference region the answer is almost always right
    for seed, (p, right) in enumerate(((0.7, True), (0.3, False), (0.99, True), (0.01, False))):
        rng = random.Random(3000 + seed)
        answers = [sprt(bernoulli(p, rng), theta, eps, alpha, beta)[0] for _ in range(500)]
        assert answers.count(right) >= 499


def knuth_yao():
    t = {0: (1, 2), 1: (3, 4), 2: (5, 6), 3: (1, 7), 4: (8, 9), 5: (10, 11), 6: (12, 2)}
    P = [{t[s][0]: 0.5, t[s][1]: 0.5} if s in t else {s: 1.0} for s in range(13)]
    return {"P": P}


def test_knuth_yao_die_by_simulation() -> None:
    chain = knuth_yao()
    every, done = set(range(13)), set(range(7, 13))
    rng = random.Random(7)
    sample = bounded_until_sampler(chain, 0, every, done, 3, rng)
    # the exact value Pr(F<=3 done) = 3/4 is computed on the PCTL model checking page
    eps, delta, runs = 0.02, 0.05, 60
    misses = 0
    for _ in range(runs):
        est, _ = estimate(sample, eps, delta)
        misses += abs(est - 0.75) >= eps
    assert misses <= delta * runs
    for theta, right in ((0.7, True), (0.8, False)):
        answers = [sprt(sample, theta, 0.02, 0.01, 0.01)[0] for _ in range(40)]
        assert answers.count(right) == 40
    # a one-face property: d6 within 3 flips has probability 1/8
    six = bounded_until_sampler(chain, 0, every, {12}, 3, rng)
    est, n = estimate(six, 0.01, 0.01)
    assert abs(est - 1 / 8) < 0.01


def test_edge_cases() -> None:
    with pytest.raises(ValueError):
        sprt_parameters(1.0, 0.9, 0.05, 0.05)
    with pytest.raises(ValueError):
        sprt_parameters(0.5, 0.5, 0.05, 0.05)
    with pytest.raises(ValueError):
        sprt_parameters(0.6, 0.4, 0.6, 0.5)
    with pytest.raises(ValueError):
        hoeffding_samples(0, 0.1)
    # constant samplers: here each sample moves lambda by ln(11/9), so the
    # test needs 15 equal samples to cross ln 19
    verdict, m = sprt(lambda: False, 0.5, 0.05, 0.05, 0.05)
    assert verdict is False and m == 15
    verdict, m = sprt(lambda: True, 0.5, 0.05, 0.05, 0.05)
    assert verdict is True and m == 15
    verdict, m = sprt(lambda: True, 0.5, 0.05, 0.05, 0.05, max_samples=10)
    assert verdict is None and m == 10
    # the chain stays in a non-phi state: the until fails at once
    chain = {"P": [{1: 1.0}, {1: 1.0}]}
    assert bounded_until_sampler(chain, 0, set(), {1}, 5, random.Random(1))() is False
    assert bounded_until_sampler(chain, 0, {0}, {1}, 0, random.Random(1))() is False
    assert bounded_until_sampler(chain, 0, {0}, {1}, 1, random.Random(1))() is True
