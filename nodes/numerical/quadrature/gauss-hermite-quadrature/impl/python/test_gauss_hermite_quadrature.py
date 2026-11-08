# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-hermite-quadrature/. The authors are listed in prov/VYBGF4.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from gauss_hermite_quadrature import (expectation, gauss_hermite, gauss_hermite_log, hermite_recurrence, integrate,
                                      integrate_plain)

U = 2.0 ** -53
SP = math.sqrt(math.pi)


def moment(k):
    """Integral of x^k e^(-x^2) over the real line."""
    return 0.0 if k % 2 else math.gamma((k + 1) / 2)


def test_worked_example():
    x, w = gauss_hermite(3)
    r = math.sqrt(1.5)
    assert x == pytest.approx([-r, 0.0, r], abs=1e-15)
    assert w == pytest.approx([SP / 6, 2 * SP / 3, SP / 6], rel=1e-14)
    x, w = gauss_hermite(2)
    assert x == pytest.approx([-math.sqrt(0.5), math.sqrt(0.5)]) and w == pytest.approx([SP / 2, SP / 2])
    al, be = hermite_recurrence(3)
    assert al == [0.0, 0.0, 0.0] and be == [SP, 0.5, 1.0]


@pytest.mark.parametrize("n", [1, 2, 3, 4, 6, 9, 13])
def test_exact_to_2n_minus_1_and_constant_at_2n(n):
    x, w = gauss_hermite(n)
    for k in range(2 * n):
        q = math.fsum(wi * xi ** k for xi, wi in zip(x, w))
        assert abs(q - moment(k)) <= 300 * n * U * max(1.0, moment(k + (k % 2)))
    k = 2 * n
    e = moment(k) - math.fsum(wi * xi ** k for xi, wi in zip(x, w))
    norm2 = SP * math.factorial(n) / 2 ** n  # |pi_n|^2 = beta_0 beta_1 ... beta_n
    assert abs(e - norm2) <= 1e-9 * norm2 + 300 * n * U * moment(k)
    assert e > 0
    assert all(wi > 0 for wi in w) and all(x[i] < x[i + 1] for i in range(n - 1))
    assert x == [-t for t in reversed(x)]


def test_random_polynomials_rational_oracle():
    """Integral of x^(2m) e^(-x^2) is sqrt(pi) (2m)! / (4^m m!): rational multiples of sqrt(pi)."""
    rng = random.Random(1864)
    rules = {n: gauss_hermite(n) for n in range(1, 12)}
    for _ in range(600):
        n = rng.randint(1, 11)
        c = [F(rng.randint(-40, 40), rng.randint(1, 9)) for _ in range(rng.randint(1, 2 * n))]
        exact = sum(ck * F(math.factorial(k), 4 ** (k // 2) * math.factorial(k // 2))
                    for k, ck in enumerate(c) if k % 2 == 0)
        x, w = rules[n]
        terms = [wi * sum(float(ck) * xi ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w)]
        size = math.fsum(wi * sum(abs(float(ck)) * abs(xi) ** k for k, ck in enumerate(c)) for xi, wi in zip(x, w))
        assert abs(math.fsum(terms) - SP * float(exact)) <= 1e-12 * size + 1e-300


def test_rates_on_closed_forms():
    for om in (1.0, 5.0):
        assert integrate(lambda t: math.cos(om * t), 40) == pytest.approx(SP * math.exp(-om * om / 4), abs=1e-14)
    exact = math.pi * math.e * math.erfc(1.0)  # integral of e^(-x^2) / (1 + x^2)
    errs = {n: abs(integrate(lambda t: 1 / (1 + t * t), n) - exact) for n in (8, 32, 128)}
    assert errs[8] > 1e-3 and 1e-7 < errs[32] < 1e-5 and errs[128] < 1e-12  # roughly exp(-2.8 sqrt(n))
    # a kink at 0: |x| converges like n^(-1)
    e1, e2 = abs(integrate(abs, 32) - 1), abs(integrate(abs, 128) - 1)
    assert math.log2(e1 / e2) / 2 == pytest.approx(1.0, abs=0.05)
    # a jump at 0: sign(x) e^x
    jump = integrate(lambda t: math.copysign(math.exp(t), t), 64)
    exact_jump = SP * math.exp(0.25) * math.erf(0.5)
    assert 1e-4 < abs(jump - exact_jump) < 0.1


def test_expectations():
    assert expectation(math.exp, 16) == pytest.approx(math.exp(0.5), rel=1e-15)
    assert expectation(lambda t: t * t, 2, mu=3.0, sigma=2.0) == pytest.approx(13.0, rel=1e-14)
    assert expectation(lambda t: t ** 4, 3) == pytest.approx(3.0, rel=1e-14)
    # a kink at 1 (call option payoff): slow algebraic convergence
    call = math.exp(-0.5) / math.sqrt(2 * math.pi) - 0.5 * math.erfc(1 / math.sqrt(2))
    errs = [abs(expectation(lambda t: max(t - 1.0, 0.0), n) - call) for n in (12, 50, 200)]
    assert errs[2] < 2e-3 and max(errs) > 1e-3
    with pytest.raises(ValueError):
        expectation(math.exp, 4, sigma=0.0)


def test_modified_weights():
    assert integrate_plain(lambda t: math.exp(-t * t / 4), 20, width=2.0) == pytest.approx(2 * SP, rel=1e-14)
    assert integrate_plain(lambda t: 1 / math.cosh(t), 64) == pytest.approx(math.pi, abs=1e-3)
    e1 = abs(integrate_plain(lambda t: 1 / (1 + t ** 4), 32) - math.pi / math.sqrt(2))
    e2 = abs(integrate_plain(lambda t: 1 / (1 + t ** 4), 128) - math.pi / math.sqrt(2))
    assert e2 > 1e-5 and e1 / e2 > 4  # algebraic decay: slow
    with pytest.raises(ValueError):
        integrate_plain(math.exp, 4, width=-1.0)


def test_large_n_logs_and_underflow():
    x, lw = gauss_hermite_log(200)
    assert x[-1] == pytest.approx(19.34, abs=0.01)  # below sqrt(2n + 1) = 20.02
    assert lw[-1] < -350 and math.isfinite(lw[-1])
    assert math.fsum(math.exp(t) for t in lw) == pytest.approx(SP, rel=1e-13)
    x, lw = gauss_hermite_log(400)
    assert lw[-1] < -745  # the weight itself underflows
    _, w = gauss_hermite(400)
    assert w[-1] == 0.0 and w[0] == 0.0


def test_edge_cases():
    assert gauss_hermite(1) == ([0.0], [pytest.approx(SP)])
    assert integrate(lambda t: 7.0, 1) == pytest.approx(7 * SP)
    with pytest.raises(ValueError):
        gauss_hermite(0)
    # an odd integrand integrates to exactly 0 by symmetry
    assert integrate(lambda t: t ** 3 * math.exp(t * t / 2) - t, 15) == 0.0
