# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welch-t-test/. The authors are listed in prov/C3KW5Q.jsonl.

import math
import random
from fractions import Fraction

import pytest

from stdist import t_sf
from welch_t_test import welch_df, welch_t_test

DRUG_1 = [0.7, -1.6, -0.2, -1.2, -0.1, 3.4, 3.7, 0.8, 0.0, 2.0]
DRUG_2 = [1.9, 0.8, 1.1, 0.1, -0.1, 4.4, 5.5, 1.6, 4.6, 3.4]
SE4 = 4.0 * math.sqrt(0.05 * 0.95 / 4000)  # four standard errors of a size near 0.05, r = 4000


def exact_parts(x: list[int], y: list[int]) -> tuple[Fraction, Fraction]:
    """(t^2, nu) in exact arithmetic, from the definitions with divisors m - 1 and n - 1."""
    m, n = len(x), len(y)
    mx, my = Fraction(sum(x), m), Fraction(sum(y), n)
    a = sum((v - mx) ** 2 for v in x) / Fraction(m - 1) / m
    b = sum((v - my) ** 2 for v in y) / Fraction(n - 1) / n
    nu = (a + b) ** 2 / (a * a / (m - 1) + b * b / (n - 1))
    return (mx - my) ** 2 / (a + b), nu


def test_degrees_of_freedom_against_fractions() -> None:
    rng = random.Random(12)
    checked = 0
    for _ in range(80):
        m, n = rng.randint(2, 9), rng.randint(2, 9)
        x = [rng.randint(-15, 15) for _ in range(m)]
        y = [rng.randint(-15, 15) for _ in range(n)]
        if len(set(x)) == 1 and len(set(y)) == 1:
            continue
        t2, nu = exact_parts(x, y)
        t, got_nu, _ = welch_t_test(x, y)
        assert abs(got_nu - float(nu)) <= 1e-12 * float(nu)
        assert abs(t * t - float(t2)) <= 1e-12 * max(1.0, float(t2))
        # Proved bounds: min(m, n) - 1 <= nu <= m + n - 2.
        assert min(m, n) - 1 <= nu <= m + n - 2
        checked += 1
    assert checked > 60


def test_degrees_of_freedom_cases() -> None:
    # Equal sizes and equal sample variances give the pooled value 2n - 2.
    assert abs(welch_df(2.0, 7, 2.0, 7) - 12.0) < 1e-12
    # The upper bound m + n - 2 holds with equality when a / (m - 1) = b / (n - 1).
    assert abs(welch_df(4.0, 5, 9.0, 10) - 13.0) < 1e-12
    # One variance much larger than the other: nu tends to that sample's n - 1.
    assert abs(welch_df(1.0, 5, 1e-12, 30) - 4.0) < 1e-9
    assert abs(welch_df(1e-12, 5, 1.0, 30) - 29.0) < 1e-9


def test_sleep_data() -> None:
    t, nu, p = welch_t_test(DRUG_1, DRUG_2)
    assert abs(t - (-1.8608134674868533)) < 1e-9
    assert abs(nu - 17.77647351617849) < 1e-9
    assert abs(p - 2.0 * t_sf(abs(t), nu)) < 1e-15
    assert abs(p - 0.07939414018735817) < 1e-9


def test_equal_sizes_give_the_pooled_statistic() -> None:
    rng = random.Random(4)
    for _ in range(20):
        n = rng.randint(2, 12)
        x = [rng.gauss(1.0, 2.0) for _ in range(n)]
        y = [rng.gauss(0.0, 0.5) for _ in range(n)]
        mx, my = sum(x) / n, sum(y) / n
        sp2 = (sum((v - mx) ** 2 for v in x) + sum((v - my) ** 2 for v in y)) / (2 * n - 2)
        pooled = (mx - my) / math.sqrt(sp2 * 2.0 / n)
        assert abs(welch_t_test(x, y)[0] - pooled) < 1e-10


def null_size(m: int, sd_x: float, n: int, sd_y: float, r: int, seed: int,
              alternative: str = "two-sided") -> float:
    rng = random.Random(seed)
    hits = 0
    for _ in range(r):
        x = [rng.gauss(5.0, sd_x) for _ in range(m)]
        y = [rng.gauss(5.0, sd_y) for _ in range(n)]
        hits += welch_t_test(x, y, alternative=alternative)[2] <= 0.05
    return hits / r


def test_size_near_alpha_with_unequal_variances_and_sizes() -> None:
    # The case where the pooled test has size 0.30. The Welch size is not exactly 0.05
    # (about 0.053 in a run with r = 20000), so allow 0.01 on top of 4 standard errors.
    assert abs(null_size(5, 3.0, 25, 1.0, 4000, 5) - 0.05) < SE4 + 0.01
    assert abs(null_size(5, 1.0, 25, 3.0, 4000, 6) - 0.05) < SE4 + 0.01


def test_one_sided_size() -> None:
    assert abs(null_size(8, 2.0, 16, 1.0, 4000, 9, "greater") - 0.05) < SE4 + 0.01


def test_limit_of_one_dominant_variance_is_exact() -> None:
    # sigma_y -> 0: the statistic tends to the one-sample t of x, nu tends to m - 1,
    # and the size tends to alpha exactly.
    assert abs(null_size(4, 1.0, 20, 1e-6, 4000, 7) - 0.05) < SE4


def test_welch_is_only_approximate() -> None:
    # With m = 2 and equal variances the size is far above 0.05 (about 0.119 with r = 20000).
    assert null_size(2, 1.0, 20, 1.0, 4000, 8) > 0.05 + SE4


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        welch_t_test([1.0], [1.0, 2.0])
    with pytest.raises(ValueError):
        welch_t_test([1.0, 1.0], [2.0, 2.0])
    with pytest.raises(ValueError):
        welch_t_test([1.0, 2.0], [2.0, 3.0], alternative="both")
    with pytest.raises(ValueError):
        welch_df(0.0, 3, 0.0, 3)
