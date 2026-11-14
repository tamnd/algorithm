# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chi-squared-goodness-of-fit-test/. The authors are listed in prov/B43M8J.jsonl.

import math
import random
from fractions import Fraction
from statistics import NormalDist

import pytest

from chi_squared_goodness_of_fit_test import chi_squared_gof
from stdist import chi2_sf

MENDEL = [315, 108, 101, 32]
MENDEL_P = [9 / 16, 3 / 16, 3 / 16, 1 / 16]


def exact_pearson(observed: list[int], probs: list[Fraction]) -> Fraction:
    n = sum(observed)
    return sum((Fraction(o) - n * p) ** 2 / (n * p) for o, p in zip(observed, probs))


def compositions(n: int, k: int):
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, k - 1):
            yield (first, *rest)


def multinomial_pmf(counts: tuple[int, ...], probs: list[float]) -> float:
    coef = math.factorial(sum(counts))
    for c in counts:
        coef //= math.factorial(c)
    return coef * math.prod(p**c for p, c in zip(probs, counts))


def test_page_examples() -> None:
    x2, df, p = chi_squared_gof([5, 8, 9, 8, 10, 20])
    assert (df, x2) == (5, pytest.approx(13.4))
    assert p == pytest.approx(0.019905, abs=1e-6)
    x2, df, p = chi_squared_gof(MENDEL, MENDEL_P)
    assert (df, x2, p) == (3, pytest.approx(0.470024, abs=1e-6), pytest.approx(0.925426, abs=1e-6))
    g2, df, p = chi_squared_gof(MENDEL, MENDEL_P, statistic="g")
    assert (df, g2, p) == (3, pytest.approx(0.475445, abs=1e-6), pytest.approx(0.924252, abs=1e-6))


def test_statistic_against_fractions() -> None:
    assert exact_pearson([5, 8, 9, 8, 10, 20], [Fraction(1, 6)] * 6) == Fraction(67, 5)
    assert exact_pearson(MENDEL, [Fraction(9, 16), Fraction(3, 16), Fraction(3, 16), Fraction(1, 16)]) == Fraction(
        19600, 41700
    )
    rng = random.Random(7)
    for _ in range(300):
        k = rng.randint(2, 7)
        weights = [rng.randint(1, 9) for _ in range(k)]
        probs = [Fraction(w, sum(weights)) for w in weights]
        observed = [rng.randint(0, 40) for _ in range(k)]
        if sum(observed) == 0:
            continue
        x2, df, _ = chi_squared_gof(observed, [float(p) for p in probs])
        assert df == k - 1
        assert x2 == pytest.approx(float(exact_pearson(observed, probs)), rel=1e-12, abs=1e-12)


def test_two_cells_is_the_squared_z_statistic() -> None:
    # With k = 2, X^2 = (x - n p)^2 / (n p (1 - p)) = z^2, and the 1 df tail is erfc(|z| / sqrt 2).
    for x, n, p0 in ((60, 100, 0.5), (3, 40, 0.2), (17, 20, 0.6), (0, 9, 0.3)):
        z = (x - n * p0) / math.sqrt(n * p0 * (1 - p0))
        x2, df, p = chi_squared_gof([x, n - x], [p0, 1 - p0])
        assert df == 1
        assert x2 == pytest.approx(z * z, rel=1e-12)
        assert p == pytest.approx(math.erfc(abs(z) / math.sqrt(2)), rel=1e-9)


def test_g_statistic_close_to_pearson_for_large_counts() -> None:
    # G - X^2 tends to 0 under the null; for counts near their expected values the two agree closely.
    for scale in (10, 100, 1000):
        obs = [9 * scale + 1, 3 * scale - 1, 3 * scale + 1, scale - 1]
        x2 = chi_squared_gof(obs, MENDEL_P)[0]
        g2 = chi_squared_gof(obs, MENDEL_P, statistic="g")[0]
        assert abs(g2 - x2) < 0.6 / scale


def exact_size(n: int, probs: list[float], alpha: float = 0.05) -> float:
    return math.fsum(
        multinomial_pmf(c, probs) for c in compositions(n, len(probs)) if chi_squared_gof(list(c), probs)[2] <= alpha
    )


def test_exact_size_by_enumeration() -> None:
    # The null law is a finite multinomial, so the true size of the asymptotic test can be computed exactly.
    assert exact_size(10, [1 / 3] * 3) == pytest.approx(0.058985, abs=1e-6)
    assert exact_size(30, [1 / 3] * 3) == pytest.approx(0.047786, abs=1e-6)
    assert exact_size(20, [0.25] * 4) == pytest.approx(0.041518, abs=1e-6)
    assert exact_size(20, [0.7, 0.1, 0.1, 0.1]) == pytest.approx(0.049088, abs=1e-6)
    assert exact_size(50, [0.7, 0.1, 0.1, 0.1]) == pytest.approx(0.051288, abs=1e-6)


def test_enumeration_against_brute_force_sampling() -> None:
    # Brute force: draw multinomial samples cell by cell and count rejections.
    rng = random.Random(11)
    probs = [1 / 3] * 3
    runs, rejected = 20000, 0
    for _ in range(runs):
        counts = [0, 0, 0]
        for _ in range(10):
            counts[rng.choices(range(3), probs)[0]] += 1
        rejected += chi_squared_gof(counts, probs)[2] <= 0.05
    size = exact_size(10, probs)
    assert abs(rejected / runs - size) < 4 * math.sqrt(size * (1 - size) / runs)


def test_fitted_parameter_hardy_weinberg() -> None:
    obs = [298, 489, 213]
    n = sum(obs)
    theta = (2 * obs[0] + obs[1]) / (2 * n)
    assert theta == 0.5425
    probs = [theta * theta, 2 * theta * (1 - theta), (1 - theta) ** 2]
    x2, df, p = chi_squared_gof(obs, probs, fitted=1)
    assert df == 1
    assert x2 == pytest.approx(0.221490, abs=1e-6)
    assert p == pytest.approx(0.637907, abs=1e-6)
    assert chi_squared_gof(obs, probs)[2] == pytest.approx(0.895167, abs=1e-6)


def test_chernoff_lehmann_raw_data_estimates() -> None:
    # Mean and standard deviation estimated from the raw normal data, six fixed bins.
    # The true law lies between chi2 with k - 1 - s = 3 and k - 1 = 5 degrees of freedom.
    rng = random.Random(5)
    cuts = [-1.5, -0.75, 0.0, 0.75, 1.5]
    std = NormalDist()
    runs, rej3, rej5 = 4000, 0, 0
    for _ in range(runs):
        x = [rng.gauss(0, 1) for _ in range(100)]
        m = math.fsum(x) / len(x)
        s = math.sqrt(math.fsum((v - m) ** 2 for v in x) / len(x))
        counts = [0] * 6
        for v in x:
            counts[sum(v > c for c in cuts)] += 1
        cdf = [0.0] + [std.cdf((c - m) / s) for c in cuts] + [1.0]
        probs = [cdf[i + 1] - cdf[i] for i in range(6)]
        x2, _, p = chi_squared_gof(counts, probs, fitted=2)
        rej3 += p <= 0.05
        rej5 += chi2_sf(x2, 5) <= 0.05
    assert rej3 / runs == pytest.approx(0.055, abs=1e-12)
    assert rej5 / runs == pytest.approx(0.01125, abs=1e-12)
    assert rej5 < 0.05 * runs


def test_errors() -> None:
    with pytest.raises(ValueError):
        chi_squared_gof([5])
    with pytest.raises(ValueError):
        chi_squared_gof([1, -1])
    with pytest.raises(ValueError):
        chi_squared_gof([1, 2], [0.5, 0.6])
    with pytest.raises(ValueError):
        chi_squared_gof([1, 2], [1.0, 0.0])
    with pytest.raises(ValueError):
        chi_squared_gof([0, 0])
    with pytest.raises(ValueError):
        chi_squared_gof([1, 2, 3], fitted=2)
    with pytest.raises(ValueError):
        chi_squared_gof([1, 2], statistic="z")
