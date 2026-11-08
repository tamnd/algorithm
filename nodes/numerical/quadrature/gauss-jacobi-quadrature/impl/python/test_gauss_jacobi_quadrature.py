# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-jacobi-quadrature/. The authors are listed in prov/47J4QB.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gauss_jacobi_quadrature import gauss_jacobi, integrate, jacobi_recurrence

U = 2.0 ** -53


def moment(k, a, b):
    """Integral of (1 - x)^a (1 + x)^b (1 + x)^k over (-1, 1) = 2^(a+b+k+1) B(a+1, b+k+1)."""
    return math.exp((a + b + k + 1) * math.log(2.0) + math.lgamma(a + 1) + math.lgamma(b + k + 1)
                    - math.lgamma(a + b + k + 2))


def norm2(n, a, b):
    """|pi_n|^2 for the monic Jacobi polynomial, closed form."""
    s = 2 * n + a + b
    return math.exp((s + 1) * math.log(2.0) + math.lgamma(n + 1) + math.lgamma(n + a + 1) + math.lgamma(n + b + 1)
                    + math.lgamma(n + a + b + 1) - math.log(s + 1) - 2 * math.lgamma(s + 1))


def test_worked_example():
    x, w = gauss_jacobi(2, 0.0, 1.0)
    s6 = math.sqrt(6)
    assert x == pytest.approx([(1 - s6) / 5, (1 + s6) / 5], abs=1e-15)
    assert w == pytest.approx([1 - s6 / 9, 1 + s6 / 9], abs=1e-15)
    al, be = jacobi_recurrence(2, 0.0, 1.0)
    assert al == pytest.approx([1 / 3, 1 / 15]) and be == pytest.approx([2.0, 2 / 9])


@pytest.mark.parametrize("a,b", [(0.0, 0.0), (-0.5, -0.5), (0.5, 0.5), (0.0, -0.5), (1.5, -0.75), (-0.9, 3.0), (7.0, 2.0)])
@pytest.mark.parametrize("n", [1, 2, 3, 5, 8])
def test_exact_to_2n_minus_1_and_constant_at_2n(a, b, n):
    x, w = gauss_jacobi(n, a, b)
    for k in range(2 * n):
        q = math.fsum(wi * (1 + xi) ** k for xi, wi in zip(x, w))
        assert q == pytest.approx(moment(k, a, b), rel=200 * n * U)
    # E((1 + x)^(2n)) = |pi_n|^2, since (1 + x)^(2n) has 2n-th derivative (2n)!
    k = 2 * n
    e = moment(k, a, b) - math.fsum(wi * (1 + xi) ** k for xi, wi in zip(x, w))
    # the subtraction cancels: allow rounding relative to the size of the moment
    assert abs(e - norm2(n, a, b)) <= 1e-9 * norm2(n, a, b) + 64 * n * U * moment(k, a, b)
    assert e > 0
    assert all(wi > 0 for wi in w) and all(x[i] < x[i + 1] for i in range(n - 1))
    assert all(-1 < xi < 1 for xi in x)


def test_norm_is_product_of_betas():
    for a, b in [(0.0, 0.0), (-0.5, 0.25), (2.0, 5.0)]:
        _, be = jacobi_recurrence(12, a, b)
        for n in range(1, 11):
            assert math.prod(be[: n + 1]) == pytest.approx(norm2(n, a, b), rel=1e-12)


@pytest.mark.parametrize("n", [1, 3, 10, 40])
def test_chebyshev_closed_forms(n):
    x, w = gauss_jacobi(n, -0.5, -0.5)
    assert x == pytest.approx([-math.cos((2 * j - 1) * math.pi / (2 * n)) for j in range(1, n + 1)], abs=1e-14)
    assert w == pytest.approx([math.pi / n] * n, rel=1e-12)
    x, w = gauss_jacobi(n, 0.5, 0.5)
    t = [math.pi * j / (n + 1) for j in range(n, 0, -1)]
    assert x == pytest.approx([math.cos(s) for s in t], abs=1e-14)
    assert w == pytest.approx([math.pi / (n + 1) * math.sin(s) ** 2 for s in t], rel=1e-11)


def test_random_polynomials_rational_oracle():
    """Weight 1 + x (a = 0, b = 1) has rational moments; compare with Fraction arithmetic."""
    rng = random.Random(1859)
    rules = {n: gauss_jacobi(n, 0.0, 1.0) for n in range(1, 11)}
    for _ in range(600):
        n = rng.randint(1, 10)
        c = [F(rng.randint(-40, 40), rng.randint(1, 9)) for _ in range(rng.randint(1, 2 * n))]
        exact = sum(ck * (F(1 - (-1) ** (k + 1), k + 1) + (F(2, k + 2) if k % 2 else F(0))) for k, ck in enumerate(c))
        x, w = rules[n]
        terms = [wi * sum(float(ck) * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(wi * sum(abs(float(ck)) * abs(xi) ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w))
        assert abs(math.fsum(terms) - float(exact)) <= 1e-13 * size + 1e-300


def test_singular_endpoint_absorbed_by_weight():
    exact = math.fsum(1 / (math.factorial(k) * (k + 0.5)) for k in range(30))  # integral of x^(-1/2) e^x on [0, 1]
    errs = [abs(integrate(math.exp, 0, 1, n, 0.0, -0.5) - exact) for n in (2, 3, 4, 6)]
    assert errs[0] < 1e-3 and errs[1] < 2e-6 and errs[2] < 2e-9 and errs[3] < 1e-14
    # Gauss-Legendre on the singular integrand converges only like n^(-1)
    e1 = abs(integrate(lambda t: math.exp(t) / math.sqrt(t), 0, 1, 16) - exact)
    e2 = abs(integrate(lambda t: math.exp(t) / math.sqrt(t), 0, 1, 64) - exact)
    assert e1 > 1e-2 and math.log2(e1 / e2) / 2 == pytest.approx(1.0, abs=0.1)
    j0 = math.fsum((-1) ** k / (math.factorial(k) ** 2 * 4 ** k) for k in range(30))
    assert integrate(math.cos, -1, 1, 8, -0.5, -0.5) == pytest.approx(math.pi * j0, abs=1e-14)
    # sqrt(x) on [0, 1] is the weight itself: one node is exact
    assert integrate(lambda t: 1.0, 0, 1, 1, 0.0, 0.5) == pytest.approx(2 / 3, rel=1e-15)


def test_closed_forms_with_legendre_weight():
    assert integrate(math.exp, 0, 1, 8) == pytest.approx(math.e - 1, abs=1e-15)
    assert integrate(math.sin, 0, math.pi, 12) == pytest.approx(2.0, abs=1e-14)
    assert integrate(lambda t: 1 / (1 + t * t), -1, 1, 30) == pytest.approx(math.pi / 2, abs=1e-14)
    assert integrate(lambda t: math.cos(20 * t), -1, 1, 30) == pytest.approx(math.sin(20) / 10, abs=1e-13)
    assert integrate(lambda t: math.exp(math.cos(t)), 0, 2 * math.pi, 30) == pytest.approx(
        2 * math.pi * 1.2660658777520082, abs=1e-12)
    # log x: no endpoint evaluation, slow algebraic convergence
    assert abs(integrate(math.log, 0, 1, 64) + 1) < 1e-3


def test_edge_cases():
    assert integrate(math.exp, 2.0, 2.0, 5, 0.3, -0.4) == 0.0
    with pytest.raises(ValueError):
        integrate(math.exp, 1.0, 0.0, 5)
    for bad in [(-1.0, 0.0), (0.0, -1.5)]:
        with pytest.raises(ValueError):
            gauss_jacobi(3, *bad)
    with pytest.raises(ValueError):
        gauss_jacobi(0)
    x, w = gauss_jacobi(1, 2.0, 0.0)
    assert x == pytest.approx([-0.5]) and w == pytest.approx([8 / 3])
    x, w = gauss_jacobi(4, -0.999, -0.999)  # weights near the singular limit
    assert math.fsum(w) == pytest.approx(moment(0, -0.999, -0.999), rel=1e-13)
    x, w = gauss_jacobi(150, 0.3, -0.7)
    assert math.fsum(w) == pytest.approx(moment(0, 0.3, -0.7), rel=1e-12)
    assert all(wi > 0 for wi in w)
