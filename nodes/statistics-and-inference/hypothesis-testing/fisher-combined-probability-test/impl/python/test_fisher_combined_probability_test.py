# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-combined-probability-test/. The authors are listed in prov/SR875B.jsonl.

import math
import random
from fractions import Fraction

import pytest

from fisher_combined_probability_test import fisher_method
from stdist import chi2_ppf, chi2_sf


def product_cdf(k: int, q: float, steps: int = 4000) -> float:
    """Brute force: P(U_1 ... U_k <= q) for iid uniforms, by repeated one-dimensional integration.

    F_1(s) = min(s, 1) and F_j(s) = integral_0^1 F_(j-1)(s/u) du. The part u <= s gives s.
    On u in (s, 1) put u = s e^t, so F_j(s) = s + s integral_0^(-ln s) F_(j-1)(e^(-t)) e^t dt
    for s < 1. F_(j-1) is kept on a grid in t, and the integral is cumulated by Simpson's rule.
    """
    if q >= 1.0:
        return 1.0
    big_t = -math.log(q)
    h = big_t / steps
    ts = [h * i for i in range(steps + 1)]
    f = [math.exp(-t) for t in ts]  # F_1(e^(-t)) = e^(-t)
    for _ in range(2, k + 1):
        g = [f[i] * math.exp(ts[i]) for i in range(steps + 1)]
        cum = [0.0] * (steps + 1)
        for i in range(1, steps + 1):  # Simpson pairs for even i, a third-order rule for odd i
            if i % 2 == 0:
                cum[i] = cum[i - 2] + h / 3 * (g[i - 2] + 4 * g[i - 1] + g[i])
            else:
                cum[i] = cum[i - 1] + h / 12 * (5 * g[i - 1] + 8 * g[i] - g[i + 1])
        f = [math.exp(-ts[i]) * (1 + cum[i]) for i in range(steps + 1)]
    return f[-1]


def test_worked_example() -> None:
    x, p = fisher_method([0.08, 0.12, 0.06, 0.20])
    assert x == pytest.approx(18.137682, abs=1e-6)
    assert p == pytest.approx(0.020218, abs=1e-6)
    assert x > chi2_ppf(0.95, 8) == pytest.approx(15.5073, abs=1e-4)


def test_k1_returns_the_p_value_itself() -> None:
    # For k = 1, X = -2 ln p is chi-squared with 2 degrees of freedom and P(chi2_2 >= X) = e^(-X/2) = p.
    rng = random.Random(1)
    for _ in range(200):
        u = rng.random() or 0.5
        x, p = fisher_method([u])
        assert x == pytest.approx(-2 * math.log(u), rel=1e-15)
        assert p == pytest.approx(u, rel=1e-14)


def test_poisson_sum_identity_exactly() -> None:
    # S_k(h) = e^(-h) sum_(j<k) h^j/j! has S_k(0) = 1 and S_k'(h) = -e^(-h) h^(k-1)/(k-1)!, the
    # negative chi-squared(2k) density in h = x/2. The polynomial part of S_k' is checked in Fractions.
    for k in range(1, 12):
        for h in (Fraction(0), Fraction(1, 3), Fraction(5, 2), Fraction(17)):
            poly = sum(h ** j / math.factorial(j) for j in range(k))
            dpoly = sum(j * h ** (j - 1) / math.factorial(j) for j in range(1, k))
            assert dpoly - poly == -(h ** (k - 1)) / math.factorial(k - 1)
        assert sum(Fraction(0) ** j / math.factorial(j) for j in range(k)) == 1


def test_k2_closed_form() -> None:
    for a, b in ((0.03, 0.04), (0.5, 0.5), (0.9, 1e-6), (0.2, 0.7)):
        q = a * b
        assert fisher_method([a, b])[1] == pytest.approx(q * (1 - math.log(q)), rel=1e-13)


def test_against_incomplete_gamma_and_product_integral() -> None:
    rng = random.Random(2)
    for _ in range(100):
        k = rng.randint(1, 40)
        p = [rng.random() ** rng.choice((1, 2, 4)) or 0.5 for _ in range(k)]
        x, pc = fisher_method(p)
        assert pc == pytest.approx(chi2_sf(x, 2 * k), rel=1e-9, abs=1e-300)
    for k in (2, 3, 4):
        for p in ([0.3] * k, [0.01, 0.5, 0.9, 0.2][:k], [0.08, 0.12, 0.06, 0.20][:k]):
            assert fisher_method(p)[1] == pytest.approx(product_cdf(k, math.prod(p)), rel=1e-7)


def test_null_uniformity_by_monte_carlo() -> None:
    rng = random.Random(3)
    reps = 20000
    for k in (1, 3, 8):
        ps = [fisher_method([1.0 - rng.random() for _ in range(k)])[1] for _ in range(reps)]
        for u in (0.01, 0.05, 0.25, 0.5, 0.9):
            assert abs(sum(v <= u for v in ps) / reps - u) < 0.012


def test_perfect_dependence_inflates_the_size() -> None:
    # If all k p-values are the same uniform U, X = -2k ln U and the size is exp(-c/(2k)).
    for k, size in ((2, 0.0933003), (4, 0.1439320), (10, 0.2079367)):
        assert math.exp(-chi2_ppf(0.95, 2 * k) / (2 * k)) == pytest.approx(size, abs=1e-6)
    rng = random.Random(4)
    reps = 20000
    hits = 0
    for _ in range(reps):
        u = 1.0 - rng.random()
        hits += fisher_method([u, u])[1] <= 0.05
    assert abs(hits / reps - 0.0933) < 0.008


def test_order_monotonicity_and_edges() -> None:
    p = [0.3, 0.01, 0.7, 0.2]
    assert fisher_method(p) == fisher_method(sorted(p))
    assert fisher_method([0.3, 0.01, 0.7, 0.19])[1] < fisher_method(p)[1]
    assert fisher_method([1.0, 1.0]) == (0.0, 1.0)
    assert fisher_method([0.0, 0.5]) == (math.inf, 0.0)
    x, pc = fisher_method([1e-100] * 3)  # the product 1e-300 is near underflow; P is not
    assert pc == pytest.approx(chi2_sf(x, 6), rel=1e-9) and pc > 0.0
    x, pc = fisher_method([math.exp(-1.0)] * 2000)  # X = 4000 = degrees of freedom
    assert pc == pytest.approx(chi2_sf(x, 4000), rel=1e-9)


def test_rejects_bad_input() -> None:
    for bad in ([], [0.5, 1.5], [-0.1], [float("nan")]):
        with pytest.raises(ValueError):
            fisher_method(bad)
