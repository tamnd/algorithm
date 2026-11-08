# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-radau-quadrature/. The authors are listed in prov/T8RETN.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gauss_radau_quadrature import gauss_radau, integrate, laguerre_recurrence

U = 2.0 ** -53


def legendre(n, x):
    a, b = 1.0, x
    if n == 0:
        return 1.0
    for k in range(1, n):
        a, b = b, ((2 * k + 1) * x * b - k * a) / (k + 1)
    return b


def radau_constant(n):
    """E_n(f) = c_n f^(2n-1)(xi) for the Legendre-Radau rule with the node -1."""
    return F(2 ** (2 * n - 1) * n * math.factorial(n - 1) ** 4, math.factorial(2 * n - 1) ** 3)


def test_worked_example():
    x, w = gauss_radau(3)
    s6 = math.sqrt(6)
    assert x == pytest.approx([-1.0, (1 - s6) / 5, (1 + s6) / 5], abs=1e-15)
    assert w == pytest.approx([2 / 9, (16 + s6) / 18, (16 - s6) / 18], abs=1e-15)
    x, w = gauss_radau(2)
    assert x == pytest.approx([-1.0, 1 / 3]) and w == pytest.approx([0.5, 1.5])


@pytest.mark.parametrize("n", [1, 2, 3, 4, 6, 9, 12])
def test_exact_to_2n_minus_2_and_constant_at_2n_minus_1(n):
    x, w = gauss_radau(n)
    for k in range(2 * n - 1):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        assert abs(q - (2 / (k + 1) if k % 2 == 0 else 0.0)) <= 60 * n * U
    k = 2 * n - 1
    e = (2 / (k + 1) if k % 2 == 0 else 0.0) - math.fsum(wi * xi ** k for xi, wi in zip(x, w))
    expect = float(radau_constant(n) * math.factorial(2 * n - 1))
    assert e == pytest.approx(expect, rel=1e-9)
    assert e > 0


@pytest.mark.parametrize("n", [2, 3, 5, 10, 25, 60])
def test_closed_forms_legendre(n):
    x, w = gauss_radau(n)
    assert x[0] == -1.0
    assert w[0] == pytest.approx(2 / n ** 2, rel=1e-13)
    for j in range(1, n):
        assert abs(legendre(n - 1, x[j]) + legendre(n, x[j])) < 1e-13
        assert w[j] == pytest.approx((1 - x[j]) / (n * n * legendre(n - 1, x[j]) ** 2), rel=1e-12)
    assert all(wi > 0 for wi in w)
    assert all(x[i] < x[i + 1] for i in range(n - 1))
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-14)


def test_right_endpoint_is_mirror():
    for n in [2, 5, 8]:
        xl, wl = gauss_radau(n, -1.0)
        xr, wr = gauss_radau(n, 1.0)
        assert xr[-1] == 1.0
        assert xr == pytest.approx([-t for t in reversed(xl)], abs=1e-14)
        assert wr == pytest.approx(list(reversed(wl)), rel=1e-12)


def test_random_polynomials_rational_oracle():
    rng = random.Random(1880)
    rules = {(n, s): gauss_radau(n, s) for n in range(1, 12) for s in (-1.0, 1.0)}
    for _ in range(600):
        n = rng.randint(1, 11)
        side = rng.choice((-1.0, 1.0))
        c = [F(rng.randint(-40, 40), rng.randint(1, 9)) for _ in range(rng.randint(1, 2 * n - 1))]
        a = F(rng.randint(-20, 20), 4)
        b = a + F(rng.randint(-20, 20), 4)
        exact = sum(ck * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        x, w = rules[(n, side)]
        mid, half = float(a + b) / 2, float(b - a) / 2
        terms = [half * wi * sum(float(ck) * (mid + half * xi) ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(abs(t) for t in terms) + abs(float(exact))
        assert abs(math.fsum(terms) - float(exact)) <= 1e-12 * size + 1e-300


def test_laguerre_radau_at_zero():
    for n in [1, 2, 3, 6, 10]:
        x, w = gauss_radau(n, 0.0, *laguerre_recurrence(n))
        assert x[0] == 0.0
        for k in range(2 * n - 1):
            q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
            assert q == pytest.approx(math.factorial(k), rel=1e-11)
        assert all(wi > 0 for wi in w)
    x, w = gauss_radau(3, 0.0, *laguerre_recurrence(3))
    assert x == pytest.approx([0.0, 3 - math.sqrt(3), 3 + math.sqrt(3)], abs=1e-14)
    assert w[0] == pytest.approx(1 / 3, rel=1e-14)


def test_closed_forms_and_rates():
    assert integrate(math.exp, 0, 1, 8) == pytest.approx(math.e - 1, abs=1e-15)
    assert integrate(math.sin, 0, math.pi, 12) == pytest.approx(2.0, abs=1e-14)
    assert integrate(lambda t: 1 / (1 + t * t), -1, 1, 30) == pytest.approx(math.pi / 2, abs=1e-14)
    assert integrate(lambda t: math.exp(math.cos(t)), 0, 2 * math.pi, 30) == pytest.approx(
        2 * math.pi * 1.2660658777520082, abs=1e-12)
    assert integrate(lambda t: math.cos(20 * t), -1, 1, 30) == pytest.approx(math.sin(20) / 10, abs=1e-12)
    e1 = abs(integrate(math.sqrt, 0, 1, 16) - 2 / 3)
    e2 = abs(integrate(math.sqrt, 0, 1, 32) - 2 / 3)
    assert math.log2(e1 / e2) == pytest.approx(3.0, abs=0.2)
    # log x would be evaluated at the fixed node 0: put the fixed node at the other end
    e = abs(integrate(math.log, 0, 1, 32, fixed_left=False) + 1)
    assert e < 1e-3
    with pytest.raises(ValueError):
        integrate(math.log, 0, 1, 4, fixed_left=True)


def test_edge_cases():
    assert integrate(math.exp, 3.0, 3.0, 4) == 0.0
    assert integrate(math.exp, 1.0, 0.0, 8) == pytest.approx(-(math.e - 1), rel=1e-14)
    x, w = gauss_radau(1)
    assert x == [-1.0] and w == [2.0]
    assert integrate(lambda t: 5.0, 0.0, 2.0, 1) == 10.0
    with pytest.raises(ValueError):
        gauss_radau(0)
    with pytest.raises(ValueError):
        gauss_radau(3, -1.0, [0.0, 0.0, 0.0], [2.0, -1.0, 0.2])
    x, w = gauss_radau(150)
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-13)
    assert w[0] == pytest.approx(2 / 150 ** 2, rel=1e-12)
