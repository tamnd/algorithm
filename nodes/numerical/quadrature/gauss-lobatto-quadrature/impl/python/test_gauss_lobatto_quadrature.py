# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-lobatto-quadrature/. The authors are listed in prov/4NBTQ5.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gauss_lobatto_quadrature import chebyshev_recurrence, composite, gauss_lobatto, integrate

U = 2.0 ** -53


def legendre_and_derivative(n, x):
    if n == 0:
        return 1.0, 0.0
    a, b = 1.0, x
    for k in range(1, n):
        a, b = b, ((2 * k + 1) * x * b - k * a) / (k + 1)
    return b, n * (x * b - a) / (x * x - 1.0)


def lobatto_constant(n):
    """E_n(f) = c_n f^(2n-2)(xi) for the n-point Legendre-Lobatto rule on [-1, 1]."""
    return F(-n * (n - 1) ** 3 * 2 ** (2 * n - 1) * math.factorial(n - 2) ** 4,
             (2 * n - 1) * math.factorial(2 * n - 2) ** 3)


def test_worked_example():
    x, w = gauss_lobatto(4)
    s = 1 / math.sqrt(5)
    assert x == pytest.approx([-1.0, -s, s, 1.0], abs=1e-15)
    assert w == pytest.approx([1 / 6, 5 / 6, 5 / 6, 1 / 6], abs=1e-15)
    x, w = gauss_lobatto(3)
    assert x == pytest.approx([-1.0, 0.0, 1.0], abs=1e-15) and w == pytest.approx([1 / 3, 4 / 3, 1 / 3])
    assert gauss_lobatto(2) == ([-1.0, 1.0], pytest.approx([1.0, 1.0]))


@pytest.mark.parametrize("n", [2, 3, 4, 5, 7, 9, 12])
def test_exact_to_2n_minus_3_and_constant_at_2n_minus_2(n):
    x, w = gauss_lobatto(n)
    for k in range(2 * n - 2):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        assert abs(q - (2 / (k + 1) if k % 2 == 0 else 0.0)) <= 60 * n * U
    k = 2 * n - 2
    e = 2 / (k + 1) - math.fsum(wi * xi ** k for xi, wi in zip(x, w))
    expect = float(lobatto_constant(n) * math.factorial(k))
    assert e == pytest.approx(expect, rel=1e-9)
    assert e < 0


def test_simpson_constant():
    assert lobatto_constant(3) == F(-1, 90)
    assert lobatto_constant(2) == F(-2, 3)


@pytest.mark.parametrize("n", [3, 4, 6, 11, 25, 60])
def test_closed_forms_legendre(n):
    x, w = gauss_lobatto(n)
    assert x[0] == -1.0 and x[-1] == 1.0
    end = 2 / (n * (n - 1))
    assert w[0] == pytest.approx(end, rel=1e-12) and w[-1] == pytest.approx(end, rel=1e-12)
    for j in range(1, n - 1):
        p, dp = legendre_and_derivative(n - 1, x[j])
        assert abs(dp) < 1e-12 * n * n
        assert w[j] == pytest.approx(end / p ** 2, rel=1e-12)
    assert all(wi > 0 for wi in w)
    assert all(x[i] < x[i + 1] for i in range(n - 1))
    assert x == pytest.approx([-t for t in reversed(x)], abs=1e-14)
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-14)


@pytest.mark.parametrize("n", [2, 3, 6, 10])
def test_chebyshev_lobatto_closed_form(n):
    x, w = gauss_lobatto(n, -1.0, 1.0, *chebyshev_recurrence(n))
    m = n - 1
    assert x == pytest.approx([-math.cos(math.pi * j / m) for j in range(n)], abs=1e-14)
    expect = [math.pi / m] * n
    expect[0] = expect[-1] = math.pi / (2 * m)
    assert w == pytest.approx(expect, rel=1e-12)


def test_other_interval_for_fixed_nodes():
    # w = 1 on [0, 1]: alpha_k = 1/2, beta_0 = 1, beta_k = k^2 / (4 (4k^2 - 1))
    n = 5
    alpha = [0.5] * n
    beta = [1.0] + [k * k / (4.0 * (4.0 * k * k - 1.0)) for k in range(1, n)]
    x, w = gauss_lobatto(n, 0.0, 1.0, alpha, beta)
    xr, wr = gauss_lobatto(n)
    assert x == pytest.approx([(t + 1) / 2 for t in xr], abs=1e-14)
    assert w == pytest.approx([t / 2 for t in wr], rel=1e-12)


def test_random_polynomials_rational_oracle():
    rng = random.Random(1852)
    rules = {n: gauss_lobatto(n) for n in range(2, 13)}
    for _ in range(600):
        n = rng.randint(2, 12)
        c = [F(rng.randint(-40, 40), rng.randint(1, 9)) for _ in range(rng.randint(1, 2 * n - 2))]
        a = F(rng.randint(-20, 20), 4)
        b = a + F(rng.randint(-20, 20), 4)
        exact = sum(ck * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        x, w = rules[n]
        mid, half = float(a + b) / 2, float(b - a) / 2
        terms = [half * wi * sum(float(ck) * (mid + half * xi) ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(abs(t) for t in terms) + abs(float(exact))
        assert abs(math.fsum(terms) - float(exact)) <= 1e-12 * size + 1e-300


def test_closed_forms_and_rates():
    assert integrate(math.exp, 0, 1, 8) == pytest.approx(math.e - 1, abs=1e-15)
    assert integrate(math.sin, 0, math.pi, 12) == pytest.approx(2.0, abs=1e-14)
    assert integrate(lambda t: 1 / (1 + t * t), -1, 1, 30) == pytest.approx(math.pi / 2, abs=1e-14)
    assert integrate(lambda t: math.exp(math.cos(t)), 0, 2 * math.pi, 30) == pytest.approx(
        2 * math.pi * 1.2660658777520082, abs=1e-12)
    assert integrate(lambda t: math.cos(20 * t), -1, 1, 30) == pytest.approx(math.sin(20) / 10, abs=1e-12)
    e1 = abs(integrate(math.sqrt, 0, 1, 16) - 2 / 3)
    e2 = abs(integrate(math.sqrt, 0, 1, 32) - 2 / 3)
    assert math.log2(e1 / e2) == pytest.approx(3.0, abs=0.3)
    with pytest.raises(ValueError):
        integrate(math.log, 0, 1, 4)  # the endpoint 0 is always a node
    with pytest.raises(ZeroDivisionError):
        integrate(lambda t: t ** -0.5, 0, 1, 4)


def test_composite_shares_endpoints_and_rate():
    errs = []
    for m in [1, 2, 4, 8, 16]:
        v, evals = composite(math.exp, 0.0, 1.0, 3, m)
        assert evals == 2 * m + 1
        errs.append(abs(v - (math.e - 1)))
    rates = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    assert all(abs(r - 4.0) < 0.1 for r in rates)  # n = 3 is composite Simpson, h^4
    v, evals = composite(math.exp, 0.0, 1.0, 5, 4)
    assert evals == 17 and abs(v - (math.e - 1)) < 1e-11
    calls = []
    composite(lambda t: calls.append(t) or 1.0, 0.0, 1.0, 4, 6)
    assert len(calls) == len(set(calls)) == 6 * 3 + 1


def test_edge_cases():
    assert integrate(math.exp, 3.0, 3.0, 4) == 0.0
    assert integrate(math.exp, 1.0, 0.0, 8) == pytest.approx(-(math.e - 1), rel=1e-14)
    assert integrate(lambda t: 5.0, 0.0, 2.0, 2) == 10.0
    v, evals = composite(math.exp, 0.0, 1.0, 2, 1)
    assert evals == 2 and v == pytest.approx((1 + math.e) / 2)
    with pytest.raises(ValueError):
        gauss_lobatto(1)
    with pytest.raises(ValueError):
        gauss_lobatto(3, 1.0, -1.0)
    with pytest.raises(ValueError):
        gauss_lobatto(4, -1.0, 1.0, [0.0] * 4, [2.0, -0.3, 0.2, 0.1])
    with pytest.raises(ValueError):
        composite(math.exp, 0.0, 1.0, 3, 0)
    x, w = gauss_lobatto(120)
    assert math.fsum(w) == pytest.approx(2.0, rel=1e-13)
    assert w[0] == pytest.approx(2 / (120 * 119), rel=1e-11)
