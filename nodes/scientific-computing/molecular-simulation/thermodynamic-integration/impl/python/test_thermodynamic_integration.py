# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thermodynamic-integration/. The authors are listed in prov/G0H3ZS.jsonl.
import math
import random

import pytest

from thermodynamic_integration import (
    gauss_legendre_rule,
    mean_and_error,
    metropolis,
    simpson_rule,
    thermodynamic_integration,
    trapezoid_rule,
)

EXACT = 0.5 * math.log(2.0)  # k from 1 to 2 at kT = 1


def exact_mean(lam):
    # U_lam = (1 + lam) x^2 / 2, so dU/dlam = x^2 / 2 and <x^2> = 1 / (1 + lam).
    return 0.5 / (1.0 + lam)


def quad(rule, f):
    return sum(w * f(x) for x, w in zip(*rule))


def test_rules_are_exact_on_polynomials():
    for deg in range(2):
        assert quad(trapezoid_rule(3), lambda x: x ** deg) == pytest.approx(1 / (deg + 1), abs=1e-14)
    for deg in range(4):
        assert quad(simpson_rule(2), lambda x: x ** deg) == pytest.approx(1 / (deg + 1), abs=1e-14)
    for n in range(1, 7):
        for deg in range(2 * n):
            assert quad(gauss_legendre_rule(n), lambda x: x ** deg) == pytest.approx(1 / (deg + 1), abs=1e-13)
        # degree 2n is not integrated exactly
        assert abs(quad(gauss_legendre_rule(n), lambda x: x ** (2 * n)) - 1 / (2 * n + 1)) > 1e-9


def test_gauss_legendre_two_points():
    nodes, weights = gauss_legendre_rule(2)
    assert nodes == pytest.approx([0.5 - 0.5 / math.sqrt(3), 0.5 + 0.5 / math.sqrt(3)], abs=1e-14)
    assert weights == pytest.approx([0.5, 0.5], abs=1e-14)


def test_hand_values_of_quadrature_on_exact_means():
    assert quad(trapezoid_rule(2), exact_mean) == pytest.approx(0.354167, abs=1e-6)
    assert quad(simpson_rule(2), exact_mean) == pytest.approx(0.347222, abs=1e-6)
    assert quad(gauss_legendre_rule(2), exact_mean) == pytest.approx(0.346154, abs=1e-6)


def test_observed_order_of_trapezoid_and_simpson():
    e = [abs(quad(trapezoid_rule(k), exact_mean) - EXACT) for k in (2, 4, 8, 16)]
    for a, b in zip(e, e[1:]):
        assert math.log2(a / b) == pytest.approx(2.0, abs=0.2)
    e = [abs(quad(simpson_rule(k), exact_mean) - EXACT) for k in (2, 4, 8, 16)]
    for a, b in zip(e[1:], e[2:]):
        assert math.log2(a / b) == pytest.approx(4.0, abs=0.2)


def gauss_sample(lam, n, rng):
    return [rng.gauss(0.0, 1.0 / math.sqrt(1.0 + lam)) for _ in range(n)]


def test_sampled_harmonic_ti_matches_exact():
    rule = gauss_legendre_rule(3)
    est, se, means = thermodynamic_integration(*rule, gauss_sample, lambda lam, x: 0.5 * x * x,
                                               10000, random.Random(1))
    quad_err = abs(quad(rule, exact_mean) - EXACT)
    assert quad_err < 2e-5
    assert abs(est - EXACT) < 4 * se + quad_err
    for lam, g in zip(rule[0], means):
        assert g == pytest.approx(exact_mean(lam), abs=0.03)


def quartic(lam, x):
    return (1 - lam) * 0.5 * x * x + lam * 0.25 * x ** 4


def reference_quartic():
    h = 0.001
    z = [h * sum(math.exp(-quartic(lam, -8 + i * h)) for i in range(16001)) for lam in (0.0, 1.0)]
    return -math.log(z[1] / z[0])


def test_metropolis_quartic_against_partition_function_quadrature():
    ref = reference_quartic()
    assert ref == pytest.approx(-0.022510, abs=1e-6)

    def sample(lam, n, rng):
        return metropolis(lambda x: quartic(lam, x), 1.0, 0.0, 2.0, n, rng)

    est, se, _ = thermodynamic_integration(*gauss_legendre_rule(5), sample,
                                           lambda lam, x: 0.25 * x ** 4 - 0.5 * x * x,
                                           20000, random.Random(2), batches=20)
    # 5-point Gauss-Legendre leaves a quadrature error of about 2.3e-4 here.
    assert abs(est - ref) < 4 * se + 5e-4


def test_metropolis_samples_the_gaussian():
    xs = metropolis(lambda x: 0.5 * x * x, 1.0, 0.0, 2.5, 40000, random.Random(3))
    m, se = mean_and_error([x * x for x in xs], batches=20)
    assert abs(m - 1.0) < 4 * se


def test_bad_rule_arguments():
    with pytest.raises(ValueError):
        simpson_rule(3)
    with pytest.raises(ValueError):
        trapezoid_rule(0)
