# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-theorem/. The authors are listed in prov/ND3FAB.jsonl.

"""Bayes' theorem on a finite partition, in the probability form and the odds form.

Exact arithmetic with fractions.Fraction is used in the tests, but the
functions work with any numbers that support +, * and /.
"""

from fractions import Fraction
from typing import Sequence


def posterior(prior: Sequence[Fraction], likelihood: Sequence[Fraction]) -> list[Fraction]:
    """Return Pr(A_j | B) for a partition A_1..A_k.

    prior[j] is Pr(A_j) and likelihood[j] is Pr(B | A_j). The evidence
    Pr(B) is the sum of the products (the law of total probability). It
    must be positive.
    """
    if len(prior) != len(likelihood):
        raise ValueError("prior and likelihood differ in length")
    joint = [p * l for p, l in zip(prior, likelihood)]
    evidence = sum(joint)
    if evidence <= 0:
        raise ValueError("Pr(B) = 0: the posterior is not defined")
    return [j / evidence for j in joint]


def posterior_odds(prior_odds: Fraction, likelihood_ratio: Fraction) -> Fraction:
    """Odds form: posterior odds = likelihood ratio * prior odds."""
    return likelihood_ratio * prior_odds


def odds_to_probability(odds: Fraction) -> Fraction:
    return odds / (1 + odds)


def probability_to_odds(p: Fraction) -> Fraction:
    if p >= 1:
        raise ValueError("odds of probability 1 are infinite")
    return p / (1 - p)
