# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-quadrature/. The authors are listed in prov/CMS5QF.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gaussian_quadrature import (
    apply_rule,
    chebyshev_recurrence,
    gauss_legendre_on,
    gauss_rule,
    hermite_recurrence,
    laguerre_recurrence,
    legendre_recurrence,
    orthonormal_values,
    sturm_count,
)


def legendre_moment(k):
    return F(0) if k % 2 else F(2, k + 1)


def laguerre_moment(k):
    return F(math.factorial(k))


def hermite_moment_over_sqrtpi(k):
    # integral of x^k e^(-x^2) divided by sqrt(pi): (k-1)!! / 2^(k/2) for even k
    if k % 2:
        return F(0)
    r = F(1)
    for j in range(1, k, 2):
        r *= F(j, 2)
    return r


def exact_beta_legendre(k):
    return F(2) if k == 0 else F(k * k, 4 * k * k - 1)


def check_exactness(alpha, beta, moment, scale, n, beta_exact):
    x, w = gauss_rule(alpha, beta, n)
    for k in range(2 * n):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        size = math.fsum(abs(wi) * abs(xi) ** k for xi, wi in zip(x, w))
        assert abs(q - scale * float(moment(k))) <= 200 * n * 2.0 ** -53 * size + 1e-300
    # failure at degree 2n: E(x^(2n)) = ||pi_n||^2 = beta_0 beta_1 ... beta_n
    q = math.fsum(wi * xi ** (2 * n) for xi, wi in zip(x, w))
    e = scale * float(moment(2 * n)) - q
    norm2 = F(1)
    for k in range(n + 1):
        norm2 *= beta_exact(k)
    assert e > 0
    assert abs(e - scale * float(norm2)) <= 1e-9 * scale * float(norm2) + 1e-13 * scale * float(moment(2 * n))


def test_worked_example_three_points():
    a, b = legendre_recurrence(3)
    x, w = gauss_rule(a, b, 3)
    r = math.sqrt(0.6)
    assert x[0] == pytest.approx(-r, abs=1e-15)
    assert abs(x[1]) < 1e-15
    assert x[2] == pytest.approx(r, abs=1e-15)
    assert w == pytest.approx([5 / 9, 8 / 9, 5 / 9], abs=1e-15)
    assert math.fsum(v * v for v in orthonormal_values(a, b, 3, 0.0)) == pytest.approx(9 / 8, rel=1e-15)
    assert math.fsum(v * v for v in orthonormal_values(a, b, 3, r)) == pytest.approx(9 / 5, rel=1e-15)


@pytest.mark.parametrize("n", [1, 2, 3, 5, 8, 12, 20])
def test_exactness_legendre(n):
    a, b = legendre_recurrence(n + 1)
    check_exactness(a, b, legendre_moment, 1.0, n, exact_beta_legendre)


@pytest.mark.parametrize("n", [1, 2, 4, 7, 10])
def test_exactness_laguerre(n):
    a, b = laguerre_recurrence(n + 1)
    check_exactness(a, b, laguerre_moment, 1.0, n, lambda k: F(1) if k == 0 else F(k * k))


@pytest.mark.parametrize("n", [1, 2, 5, 9, 14])
def test_exactness_hermite(n):
    a, b = hermite_recurrence(n + 1)
    check_exactness(a, b, hermite_moment_over_sqrtpi, math.sqrt(math.pi), n,
                    lambda k: F(1) if k == 0 else F(k, 2))


def test_legendre_error_constant_closed_form():
    # E_n(x^(2n)) = 2^(2n+1) (n!)^4 / ((2n+1) ((2n)!)^2); for n = 2 this is 8/45
    for n in range(1, 9):
        x, w = gauss_rule(*legendre_recurrence(n), n)
        e = F(2, 2 * n + 1) - F(math.fsum(wi * xi ** (2 * n) for xi, wi in zip(x, w)))
        c = F(2 ** (2 * n + 1) * math.factorial(n) ** 4, (2 * n + 1) * math.factorial(2 * n) ** 2)
        assert abs(float(e - c)) <= 1e-14
    assert F(2 ** 5 * 2 ** 4, 5 * 24 ** 2) == F(8, 45)


def test_random_polynomials_against_rational_oracle():
    rng = random.Random(20240611)
    rules = {n: gauss_rule(*legendre_recurrence(n), n) for n in range(1, 13)}
    for _ in range(600):
        n = rng.randint(1, 12)
        deg = rng.randint(0, 2 * n - 1)
        c = [F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(deg + 1)]
        a = F(rng.randint(-40, 40), 8)
        b = a + F(rng.randint(0, 40), 8)
        exact = sum(ck * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        x, w = rules[n]
        mid, half = float(a + b) / 2, float(b - a) / 2
        terms = []
        for xi, wi in zip(x, w):
            t = mid + half * xi
            terms.append(wi * sum(float(ck) * t ** k for k, ck in enumerate(c)))
        q = half * math.fsum(terms)
        size = half * math.fsum(abs(v) for v in terms) + abs(float(exact))
        assert abs(q - float(exact)) <= 1e-12 * size + 1e-300


def test_random_polynomials_laguerre_and_hermite():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 10)
        deg = rng.randint(0, 2 * n - 1)
        c = [rng.randint(-9, 9) for _ in range(deg + 1)]
        x, w = gauss_rule(*laguerre_recurrence(n), n)
        q = math.fsum(wi * sum(ck * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w))
        exact = sum(ck * math.factorial(k) for k, ck in enumerate(c))
        size = sum(abs(ck) * math.factorial(k) for k, ck in enumerate(c))
        assert abs(q - exact) <= 1e-11 * size
        x, w = gauss_rule(*hermite_recurrence(n), n)
        q = math.fsum(wi * sum(ck * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w))
        ex = sum(ck * float(hermite_moment_over_sqrtpi(k)) for k, ck in enumerate(c)) * math.sqrt(math.pi)
        size = sum(abs(ck) * float(hermite_moment_over_sqrtpi(k + k % 2)) for k, ck in enumerate(c)) * 2
        assert abs(q - ex) <= 1e-11 * size


def test_weights_positive_and_sum_to_mu0():
    for rec, mu0 in [(legendre_recurrence, 2.0), (chebyshev_recurrence, math.pi),
                     (laguerre_recurrence, 1.0), (hermite_recurrence, math.sqrt(math.pi))]:
        for n in [1, 2, 3, 10, 40]:
            x, w = gauss_rule(*rec(n), n)
            assert all(wi > 0 for wi in w)
            assert all(x[i] < x[i + 1] for i in range(n - 1))
            assert math.fsum(w) == pytest.approx(mu0, rel=1e-13)


def test_chebyshev_closed_form():
    for n in [1, 4, 7, 16]:
        x, w = gauss_rule(*chebyshev_recurrence(n), n)
        for j in range(n):
            assert x[j] == pytest.approx(math.cos((2 * (n - j) - 1) * math.pi / (2 * n)), abs=1e-14)
            assert w[j] == pytest.approx(math.pi / n, rel=1e-13)


def test_symmetry_legendre():
    n = 11
    x, w = gauss_rule(*legendre_recurrence(n), n)
    for j in range(n):
        assert x[j] == pytest.approx(-x[n - 1 - j], abs=1e-15)
        assert w[j] == pytest.approx(w[n - 1 - j], rel=1e-13)


def test_sturm_count_matches_nodes():
    n = 9
    a, b = legendre_recurrence(n)
    x, _ = gauss_rule(a, b, n)
    for j in range(n):
        assert sturm_count(a, b, n, x[j] - 1e-9) == j
        assert sturm_count(a, b, n, x[j] + 1e-9) == j + 1
    assert sturm_count(a, b, n, -2.0) == 0
    assert sturm_count(a, b, n, 2.0) == n


def test_closed_forms_smooth():
    cases = [
        (math.exp, -1.0, 1.0, math.e - 1 / math.e, 8),
        (math.sin, 0.0, math.pi, 2.0, 10),
        (lambda t: math.exp(math.cos(t)), 0.0, 2 * math.pi, 2 * math.pi * 1.2660658777520082, 32),
        (lambda t: 1 / (1 + t * t), -1.0, 1.0, math.pi / 2, 32),
        (lambda t: math.cos(20 * t), -1.0, 1.0, math.sin(20) / 10, 32),
    ]
    for f, a, b, ex, n in cases:
        assert gauss_legendre_on(f, a, b, n) == pytest.approx(ex, abs=1e-14)


def test_geometric_rate_runge():
    # 1/(1+x^2) is analytic in the Bernstein ellipse with rho < 1 + sqrt(2)
    rho2 = (1 + math.sqrt(2)) ** 2
    e8 = abs(gauss_legendre_on(lambda t: 1 / (1 + t * t), -1, 1, 8) - math.pi / 2)
    e12 = abs(gauss_legendre_on(lambda t: 1 / (1 + t * t), -1, 1, 12) - math.pi / 2)
    observed = (e8 / e12) ** (1 / 4)
    assert 0.8 * rho2 < observed < 1.2 * rho2


def test_oscillatory_needs_n_above_omega():
    # cos(20x) on [-1, 1]: the rule needs about pi nodes per wavelength before it converges
    ex = math.sin(20) / 10
    assert abs(gauss_legendre_on(lambda t: math.cos(20 * t), -1, 1, 8) - ex) > 0.1
    assert abs(gauss_legendre_on(lambda t: math.cos(20 * t), -1, 1, 24) - ex) < 1e-9


def test_algebraic_rates_for_singular_integrands():
    def rate(f, ex):
        e1 = abs(gauss_legendre_on(f, 0, 1, 32) - ex)
        e2 = abs(gauss_legendre_on(f, 0, 1, 64) - ex)
        return math.log2(e1 / e2)
    assert rate(math.sqrt, 2 / 3) == pytest.approx(3.0, abs=0.15)
    assert rate(math.log, -1.0) == pytest.approx(2.0, abs=0.15)
    assert rate(lambda t: t ** -0.5, 2.0) == pytest.approx(1.0, abs=0.15)
    # a kink: |x| on [-1, 1]
    e1 = abs(gauss_legendre_on(abs, -1, 1, 32) - 1)
    e2 = abs(gauss_legendre_on(abs, -1, 1, 64) - 1)
    assert math.log2(e1 / e2) == pytest.approx(2.0, abs=0.15)


def test_infinite_intervals():
    x, w = gauss_rule(*hermite_recurrence(20), 20)
    assert apply_rule(math.cos, x, w) == pytest.approx(math.sqrt(math.pi) * math.exp(-0.25), abs=1e-14)
    x, w = gauss_rule(*laguerre_recurrence(30), 30)
    assert apply_rule(math.sin, x, w) == pytest.approx(0.5, abs=1e-14)
    # weight x^(-1/2) e^(-x): the endpoint singularity sits in the weight
    x, w = gauss_rule(*laguerre_recurrence(30, -0.5), 30)
    ex = math.sqrt(math.pi) * math.cos(math.pi / 8) / 2 ** 0.25
    assert apply_rule(math.cos, x, w) == pytest.approx(ex, abs=1e-13)


def test_edge_cases():
    assert gauss_legendre_on(math.exp, 2.0, 2.0, 5) == 0.0
    fwd = gauss_legendre_on(math.exp, 0.0, 1.0, 10)
    assert gauss_legendre_on(math.exp, 1.0, 0.0, 10) == pytest.approx(-fwd, rel=1e-15)
    # n = 1 is the midpoint rule
    x, w = gauss_rule(*legendre_recurrence(1), 1)
    assert x == [0.0] or abs(x[0]) < 1e-300
    assert w[0] == pytest.approx(2.0, rel=1e-15)
    assert gauss_legendre_on(lambda t: t * t, 0.0, 1.0, 1) == pytest.approx(0.25, rel=1e-15)
    with pytest.raises(ValueError):
        gauss_rule([0.0], [2.0], 0)
    with pytest.raises(ValueError):
        gauss_rule([0.0, 0.0], [2.0], 2)
    with pytest.raises(ValueError):
        gauss_rule([0.0, 0.0], [2.0, -1.0], 2)


def test_large_n_accuracy():
    n = 150
    x, w = gauss_rule(*legendre_recurrence(n), n)
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-14)
    assert apply_rule(math.exp, x, w) == pytest.approx(math.e - 1 / math.e, rel=1e-14)
    # largest node close to the asymptotic cos(pi (1 - 1/4) / (n + 1/2))
    assert x[-1] == pytest.approx(math.cos(0.75 * math.pi / (n + 0.5)), abs=1e-5)
