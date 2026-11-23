# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-response/. The authors are listed in prov/935KM5.jsonl.
"""Randomized response (Warner 1965) with the truth probability of epsilon-LDP.

The privacy parameter is passed as the exact value e^epsilon, a positive
Fraction or int, so that the coin is exact and the pmf can be checked with
fractions. random.Random is used only so that the tests are reproducible; a
deployment needs a cryptographic source of randomness.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Sequence, Union

Rational = Union[int, Fraction]


def truth_probability(exp_epsilon: Rational) -> Fraction:
    """p = e^epsilon / (1 + e^epsilon). Precondition: exp_epsilon >= 1."""
    e = Fraction(exp_epsilon)
    if e < 1:
        raise ValueError("e^epsilon must be at least 1")
    return e / (1 + e)


def randomized_response(v: int, exp_epsilon: Rational, rng: random.Random) -> int:
    """Report the bit v with probability p = e^epsilon / (1 + e^epsilon), else report 1 - v.

    Precondition: v is 0 or 1, and exp_epsilon is a rational number >= 1.
    The report is epsilon-locally differentially private.
    Cost: O(1) word operations and one uniform draw from {0, ..., den(p) - 1}.
    """
    if v not in (0, 1):
        raise ValueError("v must be 0 or 1")
    p = truth_probability(exp_epsilon)  # @line L1
    c = 1 if rng.randrange(p.denominator) < p.numerator else 0  # @line L2
    if c == 1:  # @line L3
        return v
    return 1 - v  # @line L4


def estimate_fraction(reports: Sequence[int], exp_epsilon: Rational) -> Fraction:
    """The unbiased estimate (lambda - (1 - p)) / (2 p - 1) of the true fraction of ones.

    lambda is the fraction of ones among the reports. Precondition: at least
    one report, and exp_epsilon > 1 so that 2 p - 1 > 0. Cost: O(n).
    """
    if not reports:
        raise ValueError("need at least one report")
    p = truth_probability(exp_epsilon)
    if p == Fraction(1, 2):
        raise ValueError("epsilon = 0 gives no information")
    lam = Fraction(sum(reports), len(reports))  # @line L5
    return (lam - (1 - p)) / (2 * p - 1)  # @line L6


def report_pmf(v: int, exp_epsilon: Rational) -> dict[int, Fraction]:
    """The exact pmf of the report on input bit v."""
    p = truth_probability(exp_epsilon)
    return {v: p, 1 - v: 1 - p}


def estimate_variance(n: int, exp_epsilon: Rational) -> Fraction:
    """Var of the estimate on a fixed dataset of n bits: p (1 - p) / (n (2 p - 1)^2).

    Each report flips its bit with probability 1 - p, so each report has
    variance p (1 - p) whatever its true bit is. The value does not depend on
    the data. (Warner's formula for a random sample of a population adds the
    sampling variance pi (1 - pi) / n.)
    """
    p = truth_probability(exp_epsilon)
    return p * (1 - p) / (n * (2 * p - 1) ** 2)
