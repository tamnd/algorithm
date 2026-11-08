# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-laguerre-quadrature/. The authors are listed in prov/B0FCH8.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gauss_laguerre_quadrature import (gauss_laguerre, gauss_laguerre_log, integrate, integrate_plain,
                                       laguerre_recurrence)

U = 2.0 ** -53
GOMPERTZ = 0.5963473623231940743  # integral of e^(-x) / (1 + x) over (0, infinity)


def test_worked_example():
    x, w = gauss_laguerre(2)
    s2 = math.sqrt(2)
    assert x == pytest.approx([2 - s2, 2 + s2], abs=1e-15)
    assert w == pytest.approx([(2 + s2) / 4, (2 - s2) / 4], abs=1e-15)
    al, be = laguerre_recurrence(3)
    assert al == [1.0, 3.0, 5.0] and be == [1.0, 1.0, 4.0]


@pytest.mark.parametrize("a", [0.0, -0.5, 0.5, 2.0, -0.9])
@pytest.mark.parametrize("n", [1, 2, 3, 5, 8, 12])
def test_exact_to_2n_minus_1_and_constant_at_2n(a, n):
    x, w = gauss_laguerre(n, a)
    for k in range(2 * n):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        assert q == pytest.approx(math.gamma(k + a + 1), rel=300 * n * U)
    k = 2 * n
    exact = math.gamma(k + a + 1)
    e = exact - math.fsum(wi * xi ** k for xi, wi in zip(x, w))
    norm2 = math.factorial(n) * math.gamma(n + a + 1)  # |pi_n|^2 = beta_0 beta_1 ... beta_n
    assert abs(e - norm2) <= 1e-9 * norm2 + 300 * n * U * exact
    assert e > 0
    assert all(wi > 0 for wi in w) and all(0 < x[i] < x[i + 1] for i in range(n - 1))


def test_random_polynomials_rational_oracle():
    """Integral of e^(-x) x^k is k!, so random rational polynomials have rational integrals."""
    rng = random.Random(1879)
    rules = {n: gauss_laguerre(n) for n in range(1, 11)}
    for _ in range(600):
        n = rng.randint(1, 10)
        c = [F(rng.randint(-40, 40), rng.randint(1, 9)) for _ in range(rng.randint(1, 2 * n))]
        exact = sum(ck * math.factorial(k) for k, ck in enumerate(c))
        x, w = rules[n]
        terms = [wi * sum(float(ck) * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(wi * sum(abs(float(ck)) * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w))
        assert abs(math.fsum(terms) - float(exact)) <= 1e-12 * size + 1e-300


def test_rates_on_closed_forms():
    errs = {n: abs(integrate(lambda t: 1 / (1 + t), n) - GOMPERTZ) for n in (4, 16, 64)}
    # subgeometric: roughly exp(-4 sqrt(n))
    assert errs[4] > 1e-3 and 1e-7 < errs[16] < 1e-5 and errs[64] < 1e-12
    assert integrate(math.cos, 32) == pytest.approx(0.5, abs=1e-14)
    assert integrate(math.sin, 32) == pytest.approx(0.5, abs=1e-14)
    # sqrt(x) in f: slow, about n^(-3/2); in the weight (a = 1/2): exact with one node
    e1 = abs(integrate(math.sqrt, 16) - math.sqrt(math.pi) / 2)
    e2 = abs(integrate(math.sqrt, 64) - math.sqrt(math.pi) / 2)
    assert math.log2(e1 / e2) / 2 == pytest.approx(1.5, abs=0.1)
    assert integrate(lambda t: 1.0, 1, 0.5) == pytest.approx(math.sqrt(math.pi) / 2, rel=1e-15)
    assert integrate(lambda t: math.exp(-t), 30, -0.5) == pytest.approx(math.sqrt(math.pi / 2), abs=1e-12)


def test_modified_weights():
    assert integrate_plain(lambda t: math.exp(-t * t), 64) == pytest.approx(math.sqrt(math.pi) / 2, abs=1e-9)
    assert integrate_plain(lambda t: math.exp(-3 * t), 4, rate=3.0) == pytest.approx(1 / 3, rel=1e-14)
    assert integrate_plain(lambda t: math.exp(-(t - 2)), 3, lo=2.0) == pytest.approx(1.0, rel=1e-14)
    # algebraic decay: the rule converges only like n^(-1)
    e1 = abs(integrate_plain(lambda t: 1 / (1 + t * t), 32) - math.pi / 2)
    e2 = abs(integrate_plain(lambda t: 1 / (1 + t * t), 64) - math.pi / 2)
    assert e2 > 1e-3 and math.log2(e1 / e2) == pytest.approx(1.0, abs=0.15)


def test_large_n_weights_underflow_but_logs_do_not():
    x, lw = gauss_laguerre_log(200)
    assert x[-1] == pytest.approx(767.8, abs=0.5)  # largest node about 3.84 n
    assert lw[-1] < -700 and math.isfinite(lw[-1])
    assert math.fsum(math.exp(t) for t in lw) == pytest.approx(1.0, rel=1e-12)
    _, w = gauss_laguerre(200)
    assert w[-1] == 0.0 or w[-1] < 1e-300
    assert integrate(lambda t: 1 / (1 + t), 200) == pytest.approx(GOMPERTZ, abs=1e-14)


def test_edge_cases():
    x, w = gauss_laguerre(1)
    assert x == pytest.approx([1.0]) and w == pytest.approx([1.0])
    x, w = gauss_laguerre(1, 2.0)
    assert x == pytest.approx([3.0]) and w == pytest.approx([2.0])
    with pytest.raises(ValueError):
        gauss_laguerre(0)
    with pytest.raises(ValueError):
        gauss_laguerre(3, -1.0)
    with pytest.raises(ValueError):
        integrate_plain(math.exp, 3, rate=0.0)
    # a kink inside (0, infinity): convergence is slow but steady
    exact = 2 * math.exp(-1)  # integral of e^(-x) |x - 1|
    errs = [abs(integrate(lambda t: abs(t - 1), n) - exact) for n in (8, 32, 128)]
    assert errs[0] > errs[1] > errs[2] and errs[2] < 5e-3
