# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anderson-darling-test/. The authors are listed in prov/7ZCNKW.jsonl.

import math
import random

import pytest

from anderson_darling_test import ad_statistic, ad_statistic_u, ad_test, adinf_cdf

X = [0.42, 0.06, 1.95, 0.88, 0.13, 3.10, 0.27, 0.71, 0.09, 0.35]


def exp_cdf(v: float) -> float:
    return 1.0 - math.exp(-v) if v > 0 else 0.0


def a2_by_integration(u: list[float]) -> float:
    """n times the integral of (F_n(t) - t)^2 / (t (1 - t)) over (0, 1), piece by piece.

    On a piece where F_n = c the integrand is c^2/t + (1 - c)^2/(1 - t) - 1, which has
    a closed-form integral. This uses the definition, not the sum of the code."""
    n = len(u)
    pts = [0.0] + sorted(u) + [1.0]
    total = 0.0
    for i in range(n + 1):
        a, b, c = pts[i], pts[i + 1], i / n
        part = -(b - a)
        if c > 0:
            part += c * c * (math.log(b) - math.log(a))
        if c < 1:
            part += (1 - c) ** 2 * (math.log1p(-a) - math.log1p(-b))
        total += part
    return n * total


def test_page_example() -> None:
    assert ad_statistic(X, exp_cdf) == pytest.approx(0.79588947, abs=1e-7)
    assert ad_test(X, exp_cdf)[1] == pytest.approx(0.48400265, abs=1e-6)
    assert ad_test(X, exp_cdf, "monte-carlo", b=9999, rng=random.Random(7))[1] == pytest.approx(0.4813, abs=1e-12)


def test_statistic_against_the_integral() -> None:
    rng = random.Random(1)
    for _ in range(300):
        u = [rng.random() for _ in range(rng.randint(1, 15))]
        assert ad_statistic_u(sorted(u)) == pytest.approx(a2_by_integration(u), rel=1e-9, abs=1e-12)


def test_one_observation_law() -> None:
    # n = 1: A^2 = -1 - ln u - ln(1 - u), so P(A^2 <= a) = sqrt(1 - 4 e^{-(1 + a)}) for a >= ln 4 - 1.
    grid = 200000
    values = [ad_statistic_u([(i + 0.5) / grid]) for i in range(grid)]
    for a in (0.5, 1.0, 2.0, 3.0):
        share = sum(v <= a for v in values) / grid
        assert share == pytest.approx(math.sqrt(1 - 4 * math.exp(-(1 + a))), abs=1e-4)
    assert min(values) == pytest.approx(math.log(4) - 1, abs=1e-9)


def test_limit_law_percentiles() -> None:
    # Percentiles of the limit law (Marsaglia and Marsaglia 2004): 2.4924 and 3.8781.
    assert adinf_cdf(2.4924) == pytest.approx(0.95, abs=1e-5)
    assert adinf_cdf(3.8781) == pytest.approx(0.99, abs=1e-5)
    assert adinf_cdf(3.857) == pytest.approx(0.98976, abs=1e-5)  # the 1954 value is a bit low
    assert adinf_cdf(0.0) == 0.0
    assert adinf_cdf(40.0) == pytest.approx(1.0, abs=1e-12)


def test_limit_law_mean_is_one() -> None:
    # The limit is sum_j Z_j^2 / (j (j + 1)), with mean sum_j 1 / (j (j + 1)) = 1.
    h, top = 0.04, 30.0
    steps = int(top / h)
    acc = 0.0
    for i in range(steps + 1):
        f = 1.0 - adinf_cdf(i * h, steps=400)
        acc += f if i in (0, steps) else (4.0 * f if i % 2 else 2.0 * f)
    assert acc * h / 3.0 == pytest.approx(1.0, abs=2e-3)


def test_monte_carlo_p_value_is_valid() -> None:
    rng = random.Random(3)
    r, alpha = 400, 0.1
    hits = 0
    for _ in range(r):
        x = [rng.random() for _ in range(8)]
        hits += ad_test(x, lambda v: v, "monte-carlo", b=99, rng=rng)[1] <= alpha
    assert hits / r <= alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_asymptotic_size_monte_carlo() -> None:
    rng = random.Random(4)
    r, alpha = 4000, 0.05
    crit = 2.4924  # the 95% point of the limit law
    hits = sum(ad_statistic_u(sorted(rng.random() for _ in range(10))) >= crit for _ in range(r))
    assert abs(hits / r - alpha) <= 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_invariance_under_monotone_maps() -> None:
    y = [math.log(v) for v in X]  # if X has CDF F_0, log X has CDF F_0(e^t)
    assert ad_statistic(y, lambda t: exp_cdf(math.exp(t))) == pytest.approx(ad_statistic(X, exp_cdf), rel=1e-12)


def test_edges() -> None:
    with pytest.raises(ValueError):
        ad_test([], exp_cdf)
    with pytest.raises(ValueError):
        ad_test(X, exp_cdf, "monte-carlo")
    with pytest.raises(ValueError):
        ad_test(X, exp_cdf, "exact")
    assert ad_test([-1.0, 0.5], exp_cdf) == (math.inf, 0.0)  # a point where F_0 = 0
