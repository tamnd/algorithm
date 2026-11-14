# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/student-t-test/. The authors are listed in prov/M2JJ9R.jsonl.

import math
import random
from fractions import Fraction

import pytest

from student_t_test import one_sample_t_test, paired_t_test, pooled_t_test, t_p_value

# Cushny and Peebles (1905), as used by Student (1908): extra hours of sleep under two drugs.
DRUG_1 = [0.7, -1.6, -0.2, -1.2, -0.1, 3.4, 3.7, 0.8, 0.0, 2.0]
DRUG_2 = [1.9, 0.8, 1.1, 0.1, -0.1, 4.4, 5.5, 1.6, 4.6, 3.4]


def exact_t_squared(x: list[Fraction], mu0: Fraction) -> Fraction:
    """t^2 = n (xbar - mu0)^2 / S^2 with S^2 = sum (x_i - xbar)^2 / (n - 1), in exact arithmetic."""
    n = len(x)
    mean = sum(x, Fraction(0)) / n
    s2 = sum(((v - mean) ** 2 for v in x), Fraction(0)) / (n - 1)
    return n * (mean - mu0) ** 2 / s2


def test_sleep_data_paired() -> None:
    t, df, p = paired_t_test(DRUG_2, DRUG_1)
    d = [Fraction(b).limit_denominator(10) - Fraction(a).limit_denominator(10)
         for a, b in zip(DRUG_1, DRUG_2)]
    assert df == 9
    assert abs(t * t - float(exact_t_squared(d, Fraction(0)))) < 1e-9
    assert abs(t - 4.062127683382037) < 1e-9
    assert abs(p - 0.0028328901973842632) < 1e-9
    assert abs(paired_t_test(DRUG_2, DRUG_1, alternative="greater")[2] - p / 2.0) < 1e-15


def test_paired_is_one_sample_on_differences() -> None:
    rng = random.Random(3)
    for _ in range(20):
        n = rng.randint(2, 15)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        y = [v + rng.gauss(0.3, 0.5) for v in x]
        for alt in ("two-sided", "greater", "less"):
            assert paired_t_test(x, y, 0.1, alt) == one_sample_t_test(
                [a - b for a, b in zip(x, y)], 0.1, alt)


def test_statistic_against_fractions() -> None:
    rng = random.Random(8)
    for _ in range(60):
        n = rng.randint(2, 12)
        x = [rng.randint(-20, 20) for _ in range(n)]
        if len(set(x)) == 1:
            continue
        mu0 = rng.randint(-3, 3)
        t, df, _ = one_sample_t_test(x, mu0)
        assert df == n - 1
        exact = exact_t_squared([Fraction(v) for v in x], Fraction(mu0))
        assert abs(t * t - float(exact)) <= 1e-12 * max(1.0, float(exact))


def test_pooled_against_fractions() -> None:
    rng = random.Random(9)
    for _ in range(40):
        m, n = rng.randint(1, 8), rng.randint(2, 8)
        x = [Fraction(rng.randint(-9, 9)) for _ in range(m)]
        y = [Fraction(rng.randint(-9, 9)) for _ in range(n)]
        mx, my = sum(x) / m, sum(y) / n
        sp2 = (sum((v - mx) ** 2 for v in x) + sum((v - my) ** 2 for v in y)) / (m + n - 2)
        if sp2 == 0:
            continue
        t2 = (mx - my) ** 2 / (sp2 * (Fraction(1, m) + Fraction(1, n)))
        t, df, _ = pooled_t_test([float(v) for v in x], [float(v) for v in y])
        assert df == m + n - 2
        assert abs(t * t - float(t2)) <= 1e-12 * max(1.0, float(t2))


def test_two_observations_give_the_cauchy_law() -> None:
    # With n = 2 the null law is t with 1 degree of freedom: P(|T| >= t) = 1 - 2 atan(t) / pi.
    for x in ([0.0, 1.0], [3.0, 3.5], [-2.0, 5.0], [1.0, 1.001]):
        t, df, p = one_sample_t_test(x, 0.0)
        assert df == 1
        assert abs(p - (1.0 - 2.0 * math.atan(abs(t)) / math.pi)) < 1e-12


def test_small_p_value_is_not_zero() -> None:
    # P(T_30 > 20) is about 1e-19; 1 - cdf would round it to 0.
    p = t_p_value(20.0, 30, "greater")
    assert 0.0 < p < 1e-17
    assert t_p_value(0.0, 5) == 1.0


def null_size(n: int, alternative: str, r: int, seed: int) -> float:
    rng = random.Random(seed)
    hits = 0
    for _ in range(r):
        hits += one_sample_t_test([rng.gauss(10.0, 3.0) for _ in range(n)], 10.0, alternative)[2] <= 0.05
    return hits / r


@pytest.mark.parametrize("n,alternative,seed", [(3, "two-sided", 1), (5, "greater", 2), (12, "less", 3)])
def test_monte_carlo_size_is_alpha_under_normality(n: int, alternative: str, seed: int) -> None:
    r = 4000
    assert abs(null_size(n, alternative, r, seed) - 0.05) < 4.0 * math.sqrt(0.05 * 0.95 / r)


def test_p_values_are_uniform_under_the_null() -> None:
    rng = random.Random(21)
    r = 3000
    ps = [one_sample_t_test([rng.gauss(0.0, 1.0) for _ in range(4)])[2] for _ in range(r)]
    for u in (0.1, 0.3, 0.5, 0.8):
        assert abs(sum(p <= u for p in ps) / r - u) < 4.0 * math.sqrt(u * (1.0 - u) / r)


def pooled_size(m: int, sd_x: float, n: int, sd_y: float, r: int, seed: int) -> float:
    rng = random.Random(seed)
    hits = 0
    for _ in range(r):
        x = [rng.gauss(0.0, sd_x) for _ in range(m)]
        y = [rng.gauss(0.0, sd_y) for _ in range(n)]
        hits += pooled_t_test(x, y)[2] <= 0.05
    return hits / r


def test_pooled_size_is_alpha_with_equal_variances() -> None:
    r = 4000
    assert abs(pooled_size(5, 2.0, 25, 2.0, r, 4) - 0.05) < 4.0 * math.sqrt(0.05 * 0.95 / r)


def test_pooled_test_fails_with_unequal_variances_and_sizes() -> None:
    # The small sample is the noisy one: the pooled S^2 is dominated by the quiet large sample,
    # the standard error is too small, and the test rejects a true null far too often.
    r = 4000
    size = pooled_size(5, 3.0, 25, 1.0, r, 5)
    assert size > 0.05 + 4.0 * math.sqrt(0.05 * 0.95 / r)
    assert size > 0.2
    # The large sample is the noisy one: the test almost never rejects.
    assert pooled_size(5, 1.0, 25, 3.0, r, 6) < 0.01


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        one_sample_t_test([1.0])
    with pytest.raises(ValueError):
        one_sample_t_test([2.0, 2.0, 2.0])
    with pytest.raises(ValueError):
        paired_t_test([1.0, 2.0], [1.0])
    with pytest.raises(ValueError):
        t_p_value(1.0, 3, "both")
