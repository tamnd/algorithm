# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clopper-pearson-interval/. The authors are listed in prov/X4CPDK.jsonl.

import math
from fractions import Fraction

import pytest

from clopper_pearson_interval import clopper_pearson_interval
from stdist import beta_inc


def exact_pmf(n: int, p: Fraction) -> list[Fraction]:
    return [math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]


def test_page_examples() -> None:
    assert clopper_pearson_interval(3, 10) == pytest.approx((0.066739511, 0.652452850), abs=1e-8)
    assert clopper_pearson_interval(7, 20) == pytest.approx((0.153909, 0.592189), abs=1e-6)
    lo, hi = clopper_pearson_interval(0, 10)
    assert lo == 0.0 and hi == pytest.approx(1 - 0.025**0.1, abs=1e-14)
    lo, hi = clopper_pearson_interval(10, 10)
    assert hi == 1.0 and lo == pytest.approx(0.025**0.1, abs=1e-14)


def test_closed_forms_at_the_ends() -> None:
    # x = 0: P_U(X <= 0) = (1 - U)^n = alpha/2. x = n: L^n = alpha/2.
    for n in range(1, 60):
        for alpha in (0.01, 0.05, 0.1, 0.32):
            assert clopper_pearson_interval(0, n, alpha)[1] == pytest.approx(1 - (alpha / 2) ** (1 / n), abs=1e-13)
            assert clopper_pearson_interval(n, n, alpha)[0] == pytest.approx((alpha / 2) ** (1 / n), abs=1e-13)


def test_endpoints_solve_the_tail_equations_exactly() -> None:
    # Check with exact Fraction tails that each endpoint brackets alpha/2.
    alpha = Fraction(1, 20)
    for n in (1, 2, 5, 9, 16):
        for x in range(n + 1):
            lo, hi = clopper_pearson_interval(x, n, 0.05)
            eps = Fraction(1, 10**9)
            if x > 0:
                below = sum(exact_pmf(n, Fraction(lo) - eps)[x:])
                above = sum(exact_pmf(n, Fraction(lo) + eps)[x:])
                assert below < alpha / 2 < above
            if x < n:
                below = sum(exact_pmf(n, Fraction(hi) - eps)[: x + 1])
                above = sum(exact_pmf(n, Fraction(hi) + eps)[: x + 1])
                assert below > alpha / 2 > above


def test_beta_quantile_identity() -> None:
    # L is the alpha/2 quantile of Beta(x, n - x + 1); U is the 1 - alpha/2 quantile of Beta(x + 1, n - x).
    for n in (3, 10, 25, 80):
        for x in range(n + 1):
            lo, hi = clopper_pearson_interval(x, n, 0.05)
            if x > 0:
                assert beta_inc(x, n - x + 1, lo) == pytest.approx(0.025, abs=1e-10)
            if x < n:
                assert beta_inc(x + 1, n - x, hi) == pytest.approx(0.975, abs=1e-10)


def test_exact_coverage_is_at_least_nominal() -> None:
    # Exact coverage by summing binomial probabilities, on a grid of p.
    for n in (5, 10, 20, 30):
        intervals = [clopper_pearson_interval(x, n, 0.05) for x in range(n + 1)]
        bounds = [(Fraction(a), Fraction(b)) for a, b in intervals]
        for k in range(1, 200):
            p = Fraction(k, 200)
            w = exact_pmf(n, p)
            cover = sum(w[x] for x in range(n + 1) if bounds[x][0] <= p <= bounds[x][1])
            assert cover >= Fraction(95, 100), (n, p, float(cover))


def test_inverts_the_doubled_binomial_test() -> None:
    # p0 is inside [L, U] exactly when neither one-sided exact test rejects at alpha/2.
    alpha = Fraction(1, 20)
    for n in (4, 11, 18):
        for x in range(n + 1):
            lo, hi = clopper_pearson_interval(x, n, 0.05)
            for k in range(1, 400):
                p0 = Fraction(k, 400)
                w = exact_pmf(n, p0)
                accept = sum(w[x:]) > alpha / 2 and sum(w[: x + 1]) > alpha / 2
                assert accept == (lo < p0 < hi), (n, x, p0)


def test_symmetry_and_monotonicity() -> None:
    n = 40
    rows = [clopper_pearson_interval(x, n, 0.1) for x in range(n + 1)]
    for x in range(n + 1):
        assert rows[x][0] == pytest.approx(1 - rows[n - x][1], abs=1e-13)
    assert all(a[0] < b[0] and a[1] < b[1] for a, b in zip(rows, rows[1:]))


def test_large_n_and_errors() -> None:
    lo, hi = clopper_pearson_interval(500, 1000)
    assert 0.46 < lo < 0.47 and 0.53 < hi < 0.54
    assert lo == pytest.approx(1 - hi, abs=1e-12)
    for bad in ((3, 2), (-1, 5), (1, 0)):
        with pytest.raises(ValueError):
            clopper_pearson_interval(*bad)
    with pytest.raises(ValueError):
        clopper_pearson_interval(1, 5, 1.5)
