# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marginal-likelihood/. The authors are listed in prov/04WZ19.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

from marginal_likelihood import (
    bayes_factor,
    evidence_chain_rule,
    evidence_exact,
    evidence_point,
    log_evidence,
    log_evidence_bic,
    log_evidence_grid,
    log_evidence_laplace,
)


def test_page_numbers_and_bayes_factors() -> None:
    fair = F(1, 2)
    five = [1, 0] * 5
    assert evidence_exact(1, 1, five) == F(1, 2772)
    assert evidence_point(fair, five) == F(1, 1024)
    assert bayes_factor(evidence_exact(1, 1, five), evidence_point(fair, five)) == F(256, 693)
    nine = [1] * 9 + [0]
    assert evidence_exact(1, 1, nine) == F(1, 110)
    assert bayes_factor(evidence_exact(1, 1, nine), evidence_point(fair, nine)) == F(512, 55)
    ten = [1] * 10
    assert bayes_factor(evidence_exact(1, 1, ten), evidence_point(fair, ten)) == F(1024, 11)


def test_chain_rule_matches_closed_form() -> None:
    rng = random.Random(7)
    for _ in range(200):
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        data = [rng.randint(0, 1) for _ in range(rng.randint(0, 15))]
        assert evidence_chain_rule(F(a), F(b), data) == evidence_exact(a, b, data)
        # the evidence does not depend on the order of the data
        perm = data[:]
        rng.shuffle(perm)
        assert evidence_chain_rule(F(a), F(b), perm) == evidence_exact(a, b, data)


def test_evidence_is_a_distribution_over_data_sets() -> None:
    n = 10
    total = F(0)
    by_count = [F(0)] * (n + 1)
    for seq in product((0, 1), repeat=n):
        p = evidence_exact(1, 1, seq)
        total += p
        by_count[sum(seq)] += p
    assert total == 1
    # under the uniform prior every count 0..n has probability 1 / (n + 1)
    assert all(c == F(1, n + 1) for c in by_count)


def test_closed_form_against_grid() -> None:
    for a, b, s, f in [(2.5, 1.5, 7, 3), (1.0, 1.0, 30, 70), (3.0, 4.0, 0, 5)]:
        exact = log_evidence(a, b, s, f)
        prior = lambda t, a=a, b=b: math.exp((a - 1) * math.log(t) + (b - 1) * math.log(1 - t) - (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)))
        assert abs(log_evidence_grid(prior, s, f) - exact) < 1e-6


def test_laplace_error_shrinks_like_one_over_n() -> None:
    errs = []
    for n in (10, 100, 1000, 10000):
        s = 3 * n // 10
        errs.append(abs(log_evidence(1.0, 1.0, s, n - s) - log_evidence_laplace(1.0, 1.0, s, n - s)))
    for e1, e2 in zip(errs, errs[1:]):
        # ten times more data, about ten times smaller error
        assert 7 < e1 / e2 < 13
    assert errs[-1] < 1e-4


def test_bic_error_stays_bounded_but_does_not_vanish() -> None:
    gaps = []
    for n in (10, 100, 1000, 10000, 100000):
        s = 3 * n // 10
        gaps.append(log_evidence(1.0, 1.0, s, n - s) - log_evidence_bic(s, n - s))
    limit = 0.5 * math.log(2 * math.pi * 0.3 * 0.7)
    assert abs(gaps[-1] - limit) < 1e-3
    assert abs(gaps[-1]) > 0.1
