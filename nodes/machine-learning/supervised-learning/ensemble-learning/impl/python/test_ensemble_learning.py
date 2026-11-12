# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-learning/. The authors are listed in prov/1ASVXZ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from ensemble_learning import (ambiguity, condorcet_step, ensemble, majority_correct, variance_from_covariance,
                               variance_of_average)


def test_majority_probability_by_enumeration() -> None:
    for m in (1, 3, 5, 7):
        for p in (Fraction(1, 3), Fraction(1, 2), Fraction(3, 5), Fraction(9, 10)):
            total = Fraction(0)
            for votes in itertools.product((0, 1), repeat=m):
                if sum(votes) > m // 2:
                    total += p ** sum(votes) * (1 - p) ** (m - sum(votes))
            assert total == majority_correct(m, p)


def test_condorcet_monotone_and_to_one() -> None:
    for p in (Fraction(51, 100), Fraction(3, 5), Fraction(2, 5), Fraction(1, 2)):
        for m in range(1, 40, 2):
            gain = majority_correct(m + 2, p) - majority_correct(m, p)
            assert gain == condorcet_step(m, p)
            if p > Fraction(1, 2):
                assert gain > 0
            elif p < Fraction(1, 2):
                assert gain < 0
            else:
                assert gain == 0
    # Hoeffding: P(majority wrong) <= exp(-2 m (p - 1/2)^2).
    for m in (11, 51, 101, 201):
        p = Fraction(3, 5)
        assert float(1 - majority_correct(m, p)) <= math.exp(-2 * m * 0.01)


def test_variance_of_average() -> None:
    for m in (1, 2, 5, 10):
        for rho in (0.0, 0.3, 1.0, -1 / (m - 1) if m > 1 else 0.0):
            sigma2 = 2.5
            cov = [[sigma2 if a == b else rho * sigma2 for b in range(m)] for a in range(m)]
            assert abs(variance_from_covariance(cov) - variance_of_average(sigma2, rho, m)) < 1e-12
    # A shared component gives correlation rho exactly: X_j = sqrt(rho) Z + sqrt(1 - rho) E_j.
    rng = random.Random(1)
    rho, m, trials = 0.4, 6, 40000
    acc = acc2 = 0.0
    for _ in range(trials):
        z = rng.gauss(0, 1)
        avg = sum(math.sqrt(rho) * z + math.sqrt(1 - rho) * rng.gauss(0, 1) for _ in range(m)) / m
        acc += avg
        acc2 += avg * avg
    var = acc2 / trials - (acc / trials) ** 2
    assert abs(var - variance_of_average(1.0, rho, m)) < 0.02


def test_ambiguity_decomposition() -> None:
    rng = random.Random(2)
    for _ in range(200):
        m = rng.randrange(1, 8)
        preds = [rng.gauss(0, 2) for _ in range(m)]
        raw = [rng.random() + 1e-3 for _ in range(m)]
        weights = [r / sum(raw) for r in raw]
        y = rng.gauss(0, 2)
        err, member, amb = ambiguity(preds, weights, y)
        assert abs(err - (member - amb)) < 1e-9
        assert amb >= 0 and err <= member + 1e-12


def test_template_runs_members_in_order() -> None:
    data = [(x, 2 * x + 1) for x in range(5)]

    def learner(s):
        mean = sum(y for _, y in s) / len(s)
        return lambda x: mean

    def make_set(j, s, members):
        # Each member sees the residuals of the earlier members, as in boosting.
        return [(x, y - sum(f(x) for f in members)) for x, y in s]

    f = ensemble(data, [learner, learner], make_set, sum)
    assert f(0) == 5.0  # the first member predicts the mean 5, the second the mean residual 0
    g = ensemble(data, [learner] * 3, lambda j, s, members: s[j:], lambda v: sum(v) / len(v))
    assert g(0) == (5.0 + 6.0 + 7.0) / 3
