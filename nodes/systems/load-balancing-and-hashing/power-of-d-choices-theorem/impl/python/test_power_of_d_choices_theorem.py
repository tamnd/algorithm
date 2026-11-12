# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-of-d-choices-theorem/. The authors are listed in prov/AKHE82.jsonl.

import math
import random

from power_of_d_choices_theorem import (betas, closed_form_bound, failure_bound, greedy_max_load,
                                        i_star, leading_term, proof_bound)


def test_recursion_values_of_the_page() -> None:
    b = betas(10 ** 6, 2)
    assert sorted(b) == [6, 7, 8, 9]
    assert round(b[6]) == 183940 and round(b[7]) == 91970 and round(b[8]) == 22992 and round(b[9]) == 1437
    assert i_star(10 ** 6, 2) == 9 and proof_bound(10 ** 6, 2) == 11
    assert i_star(10 ** 6, 3) == 7 and i_star(10 ** 9, 2) == 10


def test_recursion_rule_and_closed_form() -> None:
    for n in (10 ** 3, 10 ** 5, 10 ** 8, 10 ** 12):
        for d in (2, 3, 4):
            b = betas(n, d)
            assert b[6] >= n / 6  # at most n/6 bins can hold 6 or more of n balls
            for i in range(6, max(b)):
                p = (b[i] / n) ** d
                assert math.isclose(b[i + 1], math.e * n * p)
                assert n * p >= 2 * math.log(n)
                assert b[i] <= n / 2 ** (d ** (i - 6)) * (1 + 1e-12)
            top = max(b)
            assert n * (b[top] / n) ** d < 2 * math.log(n)
            assert top <= 6 + math.ceil(math.log(math.log2(n), d))
            assert closed_form_bound(n, d) >= b[top] * (1 - 1e-12)


def test_failure_probability_is_small_for_large_n() -> None:
    assert failure_bound(10 ** 6, 2) < 1e-4
    assert failure_bound(10 ** 9, 2) < 1e-9
    assert failure_bound(10 ** 9, 3) < 1e-16


def test_simulated_max_load_within_bounds() -> None:
    c = 2
    rng = random.Random(11)
    for n in (1000, 5000, 30000):
        for d in (2, 3, 4):
            for _ in range(3):
                m = greedy_max_load(n, n, d, rng)
                assert m <= leading_term(n, d) + c
                assert m <= proof_bound(n, d)


def test_one_choice_exceeds_the_two_choice_bound() -> None:
    rng = random.Random(12)
    n = 30000
    one = greedy_max_load(n, n, 1, rng)
    assert one > leading_term(n, 2) + 2
