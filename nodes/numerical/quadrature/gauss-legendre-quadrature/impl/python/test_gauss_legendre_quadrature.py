# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-legendre-quadrature/. The authors are listed in prov/ACS9SM.jsonl.

import cmath
import math
import random
from fractions import Fraction as F

import pytest

from gauss_legendre_quadrature import composite, gauss_legendre, integrate, legendre_pair

U = 2.0 ** -53


def legendre_exact(n, x):
    """P_n at a rational point, in exact arithmetic (oracle)."""
    p_prev, p = F(1), F(x)
    if n == 0:
        return F(1)
    for k in range(1, n):
        p_prev, p = p, ((2 * k + 1) * F(x) * p - k * p_prev) / (k + 1)
    return p


def error_constant(n):
    """E_n(f) = c_n f^(2n)(xi) on [-1, 1]; c_n = 2^(2n+1) (n!)^4 / ((2n+1) ((2n)!)^3)."""
    return F(2 ** (2 * n + 1) * math.factorial(n) ** 4, (2 * n + 1) * math.factorial(2 * n) ** 3)


def test_worked_example():
    x, w = gauss_legendre(5)
    assert x[3] == pytest.approx(0.5384693101056831, abs=2e-16)
    assert x[4] == pytest.approx(0.906179845938664, abs=2e-16)
    assert x[2] == 0.0
    assert w[2] == pytest.approx(128 / 225, rel=1e-15)
    assert w[4] == pytest.approx(0.236926885056189, rel=1e-14)
    assert w[3] == pytest.approx(0.47862867049936636, rel=1e-14)
    err = (math.e - 1) - integrate(math.exp, 0, 1, 5)
    assert err == pytest.approx(6.54e-13, rel=0.01)
    c = float(error_constant(5)) / 2 ** 11  # mapped to [0, 1]
    assert c < err < c * math.e


@pytest.mark.parametrize("n", [1, 2, 3, 4, 7, 10, 15, 22])
def test_exact_to_2n_minus_1_and_constant_at_2n(n):
    x, w = gauss_legendre(n)
    for k in range(2 * n):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        assert abs(q - (2 / (k + 1) if k % 2 == 0 else 0.0)) <= 40 * n * U
    # E(x^(2n)) = c_n (2n)!, the squared norm of the monic Legendre polynomial
    e = 2 / (2 * n + 1) - math.fsum(wi * xi ** (2 * n) for xi, wi in zip(x, w))
    assert e == pytest.approx(float(error_constant(n) * math.factorial(2 * n)), rel=1e-7, abs=1e-14)
    assert e > 0


def test_nodes_are_sign_changes_of_exact_legendre():
    for n in [2, 5, 8, 13, 20, 31]:
        x, _ = gauss_legendre(n)
        for xi in x:
            if xi == 0.0:
                assert legendre_exact(n, F(0)) == 0
                continue
            d = 4e-15 * max(1.0, abs(xi))
            assert legendre_exact(n, F(xi - d)) * legendre_exact(n, F(xi + d)) < 0


def test_bruns_brackets_and_order():
    for n in [1, 2, 3, 10, 57, 200]:
        x, w = gauss_legendre(n)
        assert all(x[i] < x[i + 1] for i in range(n - 1))
        for i in range(1, n + 1):
            xi = x[n - i]
            assert math.cos(i * math.pi / (n + 0.5)) <= xi <= math.cos((i - 0.5) * math.pi / (n + 0.5))
        assert all(wi > 0 for wi in w)
        assert math.fsum(w) == pytest.approx(2.0, rel=1e-14)


def test_random_polynomials_rational_oracle():
    rng = random.Random(1814)
    rules = {n: gauss_legendre(n) for n in range(1, 14)}
    for _ in range(700):
        n = rng.randint(1, 13)
        c = [F(rng.randint(-40, 40), rng.randint(1, 9)) for _ in range(rng.randint(1, 2 * n))]
        a = F(rng.randint(-30, 30), 4)
        b = a + F(rng.randint(-30, 30), 4)
        exact = sum(ck * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        x, w = rules[n]
        mid, half = float(a + b) / 2, float(b - a) / 2
        terms = [half * wi * sum(float(ck) * (mid + half * xi) ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(abs(t) for t in terms) + abs(float(exact))
        assert abs(math.fsum(terms) - float(exact)) <= 1e-12 * size + 1e-300


def test_bernstein_ellipse_bound():
    def max_on_ellipse(f, rho):
        return max(abs(f((rho * cmath.exp(1j * t) + cmath.exp(-1j * t) / rho) / 2))
                   for t in (2 * math.pi * k / 720 for k in range(720)))
    for f, g, ex in [(math.exp, cmath.exp, math.e - 1 / math.e),
                     (lambda t: 1 / (1 + t * t), lambda z: 1 / (1 + z * z), math.pi / 2)]:
        for n in [2, 4, 6, 8]:
            err = abs(integrate(f, -1, 1, n) - ex)
            for rho in [1.5, 2.0, 2.3]:
                m = max_on_ellipse(g, rho) * 1.01
                assert err <= 64 / 15 * m * rho ** (2 - 2 * n) / (rho * rho - 1) + 4 * U


def test_geometric_rate_runge():
    e = [abs(integrate(lambda t: 1 / (1 + t * t), -1, 1, n) - math.pi / 2) for n in (6, 10)]
    rate = (e[0] / e[1]) ** (1 / 4)
    assert rate == pytest.approx((1 + math.sqrt(2)) ** 2, rel=0.15)


def test_closed_forms():
    assert integrate(math.sin, 0, math.pi, 12) == pytest.approx(2.0, abs=1e-15)
    assert integrate(lambda t: math.exp(math.cos(t)), 0, 2 * math.pi, 30) == pytest.approx(
        2 * math.pi * 1.2660658777520082, abs=1e-13)
    assert integrate(lambda t: math.cos(30 * t), -1, 1, 40) == pytest.approx(math.sin(30) / 15, abs=1e-13)
    assert abs(integrate(lambda t: math.cos(30 * t), -1, 1, 10) - math.sin(30) / 15) > 1e-2


def test_singular_and_kinked_integrands():
    def obs(f, ex, a, b):
        e1, e2 = abs(integrate(f, a, b, 20) - ex), abs(integrate(f, a, b, 40) - ex)
        return math.log2(e1 / e2)
    assert obs(math.sqrt, 2 / 3, 0, 1) == pytest.approx(3.0, abs=0.2)
    assert obs(math.log, -1.0, 0, 1) == pytest.approx(2.0, abs=0.2)
    assert obs(lambda t: t ** -0.5, 2.0, 0, 1) == pytest.approx(1.0, abs=0.2)
    # a kink off the center: algebraic, roughly n^(-2), and not monotone
    kink = [abs(integrate(lambda t: abs(t - 0.3), -1, 1, n) - 1.09) for n in (10, 40, 160)]
    assert kink[0] > 1e-3 and kink[1] < 1e-3 and kink[2] < 1e-4
    # a jump: convergence like n^(-1) at best, no blow-up
    step = lambda t: 1.0 if t > 0.1 else 0.0
    assert abs(integrate(step, -1, 1, 64) - 0.9) < 0.05


def test_composite_rates():
    # n = 3 per panel: h^6 for e^x, h^(3/2) for sqrt near 0
    e1, e2 = (abs(composite(math.exp, 0, 1, 3, m) - (math.e - 1)) for m in (2, 4))
    assert math.log2(e1 / e2) == pytest.approx(6.0, abs=0.2)
    e1, e2 = (abs(composite(math.sqrt, 0, 1, 3, m) - 2 / 3) for m in (8, 16))
    assert math.log2(e1 / e2) == pytest.approx(1.5, abs=0.1)
    assert composite(math.exp, 0, 1, 4, 1) == pytest.approx(integrate(math.exp, 0, 1, 4), rel=1e-15)
    with pytest.raises(ValueError):
        composite(math.exp, 0, 1, 3, 0)


def test_edge_cases():
    assert integrate(math.exp, 1.5, 1.5, 7) == 0.0
    assert integrate(math.exp, 1.0, 0.0, 7) == pytest.approx(-(math.e - 1), rel=1e-14)
    x, w = gauss_legendre(1)
    assert x == [0.0] and w == [2.0]
    with pytest.raises(ValueError):
        gauss_legendre(0)
    # a long interval: rounding is relative to the size of the integral
    assert integrate(lambda t: t ** 3, 0, 1e6, 2) == pytest.approx(0.25e24, rel=1e-14)
    p, q = legendre_pair(3, 0.5)
    assert p == pytest.approx(-0.4375) and q == pytest.approx(-0.125)


def test_large_n():
    n = 400
    x, w = gauss_legendre(n)
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-14)
    assert math.fsum(wi * math.cos(xi) for xi, wi in zip(x, w)) == pytest.approx(2 * math.sin(1), rel=1e-14)
