# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moments-accountant/. The authors are listed in prov/BBS4G5.jsonl.

import math
import random
from fractions import Fraction

import pytest

from moments_accountant import delta_for_epsilon, log_moment, moments_accountant


def exact_moment(q, b, a):
    """A_a as an exact Fraction when exp(1 / (2 sigma^2)) = b is rational.

    Then exp((k^2 - k) / (2 sigma^2)) = b^(k^2 - k), and the binomial sum is
    rational. This oracle never uses logs or the code under test.
    """
    total = Fraction(0)
    for k in range(a + 1):
        total += math.comb(a, k) * (1 - q) ** (a - k) * q**k * b ** (k * k - k)
    return total


def log_fraction(x):
    return math.log(x.numerator) - math.log(x.denominator)


def sigma_for(b):
    """The sigma with exp(1 / (2 sigma^2)) = b, for b > 1."""
    return 1.0 / math.sqrt(2.0 * math.log(b))


def gauss_log_pdf(z, mean, sigma):
    return -((z - mean) ** 2) / (2 * sigma * sigma) - math.log(sigma * math.sqrt(2 * math.pi))


def integral_moments(q, sigma, lam, n=2000):
    """E1 = E_mu0[(mu0/mu)^lam] and E2 = E_mu[(mu/mu0)^lam] by Simpson's rule.

    mu0 = N(0, sigma^2) and mu = (1-q) N(0, sigma^2) + q N(1, sigma^2). This
    oracle integrates the densities and does not use the binomial formula.
    """
    lo = -12.0 * sigma - 1.0
    hi = lam + 1 + 12.0 * sigma + 1.0
    h = (hi - lo) / n
    e1 = e2 = 0.0
    for i in range(n + 1):
        z = lo + i * h
        l0 = gauss_log_pdf(z, 0.0, sigma)
        l1 = gauss_log_pdf(z, 1.0, sigma)
        top = max(l0, l1)
        lm = top + math.log((1 - q) * math.exp(l0 - top) + q * math.exp(l1 - top))
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        e1 += w * math.exp((lam + 1) * l0 - lam * lm)
        e2 += w * math.exp((lam + 1) * lm - lam * l0)
    return e1 * h / 3, e2 * h / 3


def test_worked_example():
    expected = [0.017037, 0.063425, 0.176018, 0.519510]
    for lam, want in enumerate(expected, start=1):
        assert abs(log_moment(0.1, 1.0, lam) - want) < 1e-6
    eps, lam = moments_accountant(0.1, 1.0, 10, 1e-5, max_order=8)
    assert lam == 4
    assert abs(eps - 4.1770) < 1e-4


def test_abadi_example():
    # q = 0.01, sigma = 4, delta = 1e-5, 10000 steps: Abadi et al. report about 1.26.
    eps, lam = moments_accountant(0.01, 4.0, 10000, 1e-5)
    assert lam == 19
    assert abs(eps - 1.2586) < 1e-3


def test_no_sampling_is_gaussian_rdp():
    # q = 1 is the plain Gaussian mechanism: alpha(lam) = lam (lam + 1) / (2 sigma^2).
    for lam in range(1, 20):
        assert log_moment(1.0, 2.0, lam) == pytest.approx(lam * (lam + 1) / 8, rel=1e-12)


def test_empty_sample_costs_nothing():
    for lam in range(1, 10):
        assert log_moment(0.0, 1.0, lam) == 0.0
    eps, lam = moments_accountant(0.0, 1.0, 100, 1e-5, max_order=16)
    assert lam == 16
    assert eps == pytest.approx(math.log(1e5) / 16)


def test_second_moment_closed_form():
    # A_2 = 1 + q^2 (e^(1/sigma^2) - 1), exactly, when exp(1/(2 sigma^2)) = 2.
    q = Fraction(3, 10)
    a2 = 1 + q * q * (Fraction(4) - 1)
    assert a2 == exact_moment(q, Fraction(2), 2)
    assert log_moment(0.3, sigma_for(2), 1) == pytest.approx(log_fraction(a2), rel=1e-12)


def test_small_sigma_does_not_overflow():
    value = log_moment(0.5, 0.3, 32)
    assert math.isfinite(value)
    # The sum is at least its last term, q^33 exp((33^2 - 33) / (2 sigma^2)).
    assert value >= 33 * math.log(0.5) + (33 * 33 - 33) / (2 * 0.09) - 1e-6


def test_bad_input():
    for args in [(-0.1, 1.0, 1), (1.1, 1.0, 1), (0.5, 0.0, 1), (0.5, 1.0, 0)]:
        with pytest.raises(ValueError):
            log_moment(*args)
    with pytest.raises(ValueError):
        moments_accountant(0.1, 1.0, 0, 1e-5)
    with pytest.raises(ValueError):
        moments_accountant(0.1, 1.0, 10, 1.0)


def test_monotone():
    base, _ = moments_accountant(0.02, 1.5, 200, 1e-6)
    more_steps, _ = moments_accountant(0.02, 1.5, 400, 1e-6)
    more_noise, _ = moments_accountant(0.02, 3.0, 200, 1e-6)
    larger_delta, _ = moments_accountant(0.02, 1.5, 200, 1e-3)
    larger_rate, _ = moments_accountant(0.05, 1.5, 200, 1e-6)
    assert more_steps > base
    assert more_noise < base
    assert larger_delta < base
    assert larger_rate > base


def test_delta_for_epsilon_inverts():
    eps, _ = moments_accountant(0.01, 1.1, 1000, 1e-5)
    assert delta_for_epsilon(0.01, 1.1, 1000, eps) <= 1e-5 * (1 + 1e-9)
    assert delta_for_epsilon(0.01, 1.1, 1000, eps * 0.9) > 1e-5
    assert delta_for_epsilon(0.5, 0.5, 100, 0.0) == 1.0


def test_against_numerical_integration():
    rng = random.Random(20160)
    for _ in range(30):
        q = rng.uniform(0.001, 1.0)
        sigma = rng.uniform(0.8, 4.0)
        lam = rng.randint(1, 6)
        e1, e2 = integral_moments(q, sigma, lam)
        assert math.log(e2) == pytest.approx(log_moment(q, sigma, lam), abs=1e-6)
        # The add direction dominates the remove direction (Mironov, Talwar and Zhang).
        assert e1 <= e2 * (1 + 1e-9)


def test_random_against_exact_fractions():
    rng = random.Random(1908)
    for _ in range(500):
        q = Fraction(rng.randint(0, 64), 64)
        b = Fraction(rng.randint(66, 256), 64)
        sigma = sigma_for(b)
        max_order = rng.randint(1, 8)
        steps = rng.randint(1, 50)
        delta = Fraction(1, rng.randint(2, 10**6))
        logs = [log_fraction(exact_moment(q, b, lam + 1)) for lam in range(1, max_order + 1)]
        lam = rng.randint(1, max_order)
        assert log_moment(float(q), sigma, lam) == pytest.approx(logs[lam - 1], rel=1e-9, abs=1e-12)
        want = min(
            (steps * logs[i] - log_fraction(delta)) / (i + 1) for i in range(max_order)
        )
        got, _ = moments_accountant(float(q), sigma, steps, float(delta), max_order)
        assert got == pytest.approx(want, rel=1e-9)
