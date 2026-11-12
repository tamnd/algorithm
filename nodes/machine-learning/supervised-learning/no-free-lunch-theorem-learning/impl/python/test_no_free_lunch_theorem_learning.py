# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-free-lunch-theorem-learning/. The authors are listed in prov/N9KRMF.jsonl.

import random
from fractions import Fraction

from no_free_lunch_theorem_learning import (all_learners_m1, constant, expected_risk, majority_fill,
                                            mean_off_sample_error, memorize, neighbor_fill, random_table,
                                            sequences, targets, worst_target)

NAMED = [memorize(0), memorize(1), majority_fill, neighbor_fill, random_table(3), random_table(11), constant(0)]


def test_theorem_for_every_learner_with_one_example() -> None:
    worst = []
    for a in all_learners_m1():
        _, e, p = worst_target(a, 1)
        assert e >= Fraction(1, 4)
        assert p >= Fraction(1, 7)
        worst.append(e)
    assert len(worst) == 256
    assert min(worst) == Fraction(1, 4)  # the constant 1/4 is reached for m = 1


def test_theorem_for_named_learners() -> None:
    for m in (2, 3):
        for a in NAMED:
            _, e, p = worst_target(a, m)
            assert e >= Fraction(1, 4)
            assert p >= Fraction(1, 7)


def test_average_over_targets() -> None:
    # For a learner that is consistent with its sample, the risk averaged over all targets is
    # (1/2) * P(a fixed point is unseen) = (1/2) (1 - 1/(2m))^m.
    for m in (1, 2, 3):
        ts = targets(2 * m)
        exact = Fraction(1, 2) * (1 - Fraction(1, 2 * m)) ** m
        for a in NAMED[:-1]:
            avg = sum((expected_risk(a, m, f) for f in ts), Fraction(0)) / len(ts)
            assert avg == exact
        assert exact >= Fraction(1, 4)


def test_off_sample_error_is_one_half_on_average_for_every_learner() -> None:
    for m in (1, 2):
        for a in NAMED:
            for xs in sequences(m, 2 * m):
                assert mean_off_sample_error(a, m, xs) == Fraction(1, 2)


def test_markov_step() -> None:
    # Z in [0, 1] with E[Z] >= 1/4 has P(Z > 1/8) >= 1/7.
    rng = random.Random(5)
    for _ in range(2000):
        vals = [Fraction(rng.randint(0, 16), 16) for _ in range(rng.randint(1, 6))]
        mean = sum(vals, Fraction(0)) / len(vals)
        if mean >= Fraction(1, 4):
            assert Fraction(sum(v > Fraction(1, 8) for v in vals), len(vals)) >= Fraction(1, 7)
