# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascade-click-model/. The authors are listed in prov/F0GVXM.jsonl.

import math
import random

from cascade_click_model import click_distribution, examination_counts, fit, log_likelihood, simulate

TOL = 1e-12
DOCS = list(range(10))
TRUE_ALPHA = {d: 0.05 + 0.05 * d for d in DOCS}  # 0.05, 0.10, ..., 0.50


def hoeffding(n, delta):
    """Half width of a two-sided Hoeffding interval for a mean of n coins."""
    return math.sqrt(math.log(2.0 / delta) / (2.0 * n))


def random_rankings(rng, sessions, depth):
    return [rng.sample(DOCS, depth) for _ in range(sessions)]


def test_distribution_sums_to_one():
    rng = random.Random(1)
    for _ in range(100):
        alpha = {d: rng.random() for d in DOCS}
        ranking = rng.sample(DOCS, rng.randint(1, 10))
        probs, miss = click_distribution(ranking, alpha)
        assert math.isclose(sum(probs) + miss, 1.0, rel_tol=0, abs_tol=TOL)
        assert all(p >= 0.0 for p in probs)


def test_example_of_the_page():
    alpha = {"a": 0.5, "b": 0.4, "c": 0.2}
    probs, miss = click_distribution(["a", "b", "c"], alpha)
    for got, want in zip(probs + [miss], [0.5, 0.2, 0.06, 0.24]):
        assert math.isclose(got, want, rel_tol=1e-12)
    rankings = [["a", "b", "c"]] * 4
    clicks = [0, 1, None, 0]
    examined, clicked = examination_counts(rankings, clicks)
    assert examined == {"a": 4, "b": 2, "c": 1} and clicked == {"a": 2, "b": 1}
    assert fit(rankings, clicks) == {"a": 0.5, "b": 0.5, "c": 0.0}


def test_monte_carlo_frequencies_match_the_formula():
    rng = random.Random(2)
    ranking = [9, 3, 6, 0, 5]
    n = 40000
    clicks = simulate([ranking] * n, TRUE_ALPHA, rng)
    probs, miss = click_distribution(ranking, TRUE_ALPHA)
    tol = hoeffding(n, 1e-6)
    for i, p in enumerate(probs):
        assert abs(clicks.count(i) / n - p) <= tol
    assert abs(clicks.count(None) / n - miss) <= tol


def test_estimates_are_close_to_the_true_parameters():
    # The examinations of d depend only on the coins of the documents above d,
    # so given their number, the clicks of d are independent Bernoulli(alpha[d])
    # coins and Hoeffding's bound applies. With delta = 1e-6 per document the
    # test fails with probability at most 1e-5 for a fresh seed.
    rng = random.Random(3)
    rankings = random_rankings(rng, 50000, 5)
    clicks = simulate(rankings, TRUE_ALPHA, rng)
    assert all(c is None or 0 <= c < 5 for c in clicks)
    examined, _ = examination_counts(rankings, clicks)
    est = fit(rankings, clicks)
    for d in DOCS:
        assert examined[d] >= 5000
        assert abs(est[d] - TRUE_ALPHA[d]) <= hoeffding(examined[d], 1e-6)


def test_estimate_maximizes_the_likelihood():
    rng = random.Random(4)
    rankings = random_rankings(rng, 3000, 4)
    clicks = simulate(rankings, TRUE_ALPHA, rng)
    est = fit(rankings, clicks)
    best = log_likelihood(rankings, clicks, est)
    for d in DOCS:
        for step in (-0.02, -0.001, 0.001, 0.02):
            moved = dict(est)
            moved[d] = min(1.0, max(0.0, est[d] + step))
            assert log_likelihood(rankings, clicks, moved) <= best + 1e-9
