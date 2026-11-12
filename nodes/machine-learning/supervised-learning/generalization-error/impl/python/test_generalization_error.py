# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalization-error/. The authors are listed in prov/3V7ENF.jsonl.

import math
import random
from fractions import Fraction

from generalization_error import (binomial_cdf, empirical_risks, experiment, hoeffding_epsilon,
                                  prob_min_at_most, union_epsilon)


def test_bounds_closed_form() -> None:
    assert abs(hoeffding_epsilon(50, 0.05) - math.sqrt(math.log(40) / 100)) < 1e-12
    assert abs(union_epsilon(50, 0.05, 200) - math.sqrt(math.log(8000) / 100)) < 1e-12
    assert union_epsilon(50, 0.05, 1) == hoeffding_epsilon(50, 0.05)


def test_binomial_tail_exact() -> None:
    assert binomial_cdf(4, 1) == Fraction(5, 16)
    assert binomial_cdf(4, 4) == 1
    assert prob_min_at_most(4, 2, 0) == 1 - Fraction(15, 16) ** 2


def test_empirical_risk() -> None:
    h = [0b1010, 0b0000]
    assert empirical_risks(h, [0, 1, 3], [0, 1, 1]) == [Fraction(0), Fraction(2, 3)]


def test_fixed_hypothesis_and_union_bound_hold_but_erm_breaks_the_fixed_bound() -> None:
    r = experiment(200, 50, 1 << 12, 0.05, 400, random.Random(1))
    assert r["fixed"] <= 0.05
    assert r["any_union"] <= 0.05
    exact = float(prob_min_at_most(50, 200, 15))
    assert abs(exact - 0.4837) < 1e-3
    assert abs(r["erm"] - exact) < 0.08
