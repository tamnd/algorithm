# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-click-model/. The authors are listed in prov/56VCGX.jsonl.

import math
import random

from position_based_click_model import aggregate, em_step, fit, log_likelihood, simulate

DOCS = list(range(10))
TRUE_ALPHA = {d: 0.1 + 0.07 * d for d in DOCS}  # 0.10 ... 0.73
TRUE_GAMMA = {0: 1.0, 1: 0.7, 2: 0.5, 3: 0.35, 4: 0.25}
# Sampling error and EM convergence together. With about 20000 impressions
# per (document, rank) pair, the standard error of a click rate is below
# 0.004, so 0.03 leaves a wide margin; the fit is a measurement on one seed.
TOL = 0.03
SLACK = 1e-9  # allowed decrease of the log likelihood from rounding


def data(seed, sessions):
    rng = random.Random(seed)
    rankings = [rng.sample(DOCS, 5) for _ in range(sessions)]
    clicks = simulate(rankings, TRUE_ALPHA, TRUE_GAMMA, rng)
    return aggregate(rankings, clicks)


def test_aggregate_counts():
    n, c = aggregate([["a", "b"], ["b", "a"], ["a", "b"]], [[1, 0], [1, 1], [0, 0]])
    assert n == {("a", 0): 2, ("b", 1): 2, ("b", 0): 1, ("a", 1): 1}
    assert c == {("a", 0): 1, ("b", 1): 0, ("b", 0): 1, ("a", 1): 1}


def test_one_em_step_by_hand():
    # One pair, 10 impressions, 4 clicks, start at alpha = gamma = 0.5:
    # a non-click is examined with probability 0.25 / 0.75 = 1/3.
    n, c = {("d", 0): 10}, {("d", 0): 4}
    alpha, gamma = em_step(n, c, {"d": 0.5}, {0: 0.5})
    assert math.isclose(gamma[0], (4 + 6 / 3) / 10, rel_tol=1e-12)
    assert math.isclose(alpha["d"], (4 + 6 / 3) / 10, rel_tol=1e-12)


def test_log_likelihood_never_decreases():
    for seed in range(5):
        n, c = data(100 + seed, 4000)
        _, _, history = fit(n, c, iterations=200)
        for before, after in zip(history, history[1:]):
            assert after >= before - SLACK


def test_em_recovers_the_identifiable_parameters():
    # The likelihood only depends on the products gamma[r] * alpha[d], so
    # (gamma * t, alpha / t) fits equally well. With the true gamma[0] = 1,
    # compare gamma[r] / gamma[0] and alpha[d] * gamma[0] with the truth.
    n, c = data(7, 200000)
    alpha, gamma, history = fit(n, c, iterations=1000)
    for before, after in zip(history, history[1:]):
        assert after >= before - SLACK
    scale = gamma[0]
    for r, g in TRUE_GAMMA.items():
        assert abs(gamma[r] / scale - g) <= TOL
    for d, a in TRUE_ALPHA.items():
        assert abs(alpha[d] * scale - a) <= TOL
    # The fitted model is at least as likely as the truth on these data.
    assert history[-1] >= log_likelihood(n, c, TRUE_ALPHA, TRUE_GAMMA) - 1e-6


def test_raw_click_rates_are_biased():
    # Without the model, the click rate of a document mixes its attraction
    # with the examination of the ranks where it was shown.
    n, c = data(8, 20000)
    for d in DOCS:
        shown = sum(m for (x, _), m in n.items() if x == d)
        clicked = sum(k for (x, _), k in c.items() if x == d)
        assert clicked / shown < TRUE_ALPHA[d] * 0.8
