# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clenshaw-curtis-quadrature/. The authors are listed in prov/AP29J0.jsonl.

import cmath
import math
import random
from fractions import Fraction as F

import pytest

from clenshaw_curtis_quadrature import (chebyshev_points, clenshaw_curtis, clenshaw_curtis_weights,
                                        clenshaw_curtis_weights_direct, dct1, fft, integrate)

U = 2.0 ** -53


def degree(n):
    big_n = n - 1
    return big_n + 1 if big_n % 2 == 0 else big_n


def test_fft_against_direct_dft():
    rng = random.Random(1965)
    for m in (1, 2, 3, 5, 6, 8, 12, 17, 31, 64, 100):
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(m)]
        direct = [sum(x[j] * cmath.exp(-2j * math.pi * j * k / m) for j in range(m)) for k in range(m)]
        assert max(abs(p - q) for p, q in zip(fft(x), direct)) <= 1e-13 * m


def test_dct_recovers_chebyshev_coefficients():
    # f = T_3 + 2 T_0 - 0.5 T_6 sampled at 9 points
    n = 9
    xs = chebyshev_points(n)
    f = [math.cos(3 * math.acos(x)) + 2 - 0.5 * math.cos(6 * math.acos(x)) for x in xs]
    a = dct1(f)
    expect = [2, 0, 0, 1, 0, 0, -0.5, 0, 0]
    assert a == pytest.approx(expect, abs=1e-15)


def test_worked_example_exact_weights():
    """n = 5: nodes 0, +-1/sqrt 2, +-1; weights 1/15, 8/15, 4/5. Exact on degree 5, error 2/105 on x^6."""
    x, w = clenshaw_curtis_weights(5)
    assert x == pytest.approx([1, math.sqrt(0.5), 0, -math.sqrt(0.5), -1], abs=2e-16)
    assert w == pytest.approx([1 / 15, 8 / 15, 4 / 5, 8 / 15, 1 / 15], abs=1e-16)
    wf = [F(1, 15), F(8, 15), F(4, 5), F(8, 15), F(1, 15)]
    x2 = [F(1), F(1, 2), F(0), F(1, 2), F(1)]  # squares of the nodes, exact
    for k in (0, 2, 4):  # odd powers vanish by symmetry
        assert sum((wi * xi ** (k // 2) for wi, xi in zip(wf, x2)), F(0)) == F(2, k + 1)
    assert F(2, 7) - sum((wi * xi ** 3 for wi, xi in zip(wf, x2)), F(0)) == F(2, 105)
    # n = 3 is Simpson's rule: 1/3, 4/3, 1/3, exact on cubics, error 4/15 on x^4
    x, w = clenshaw_curtis_weights(3)
    assert w == pytest.approx([1 / 3, 4 / 3, 1 / 3], abs=1e-16)
    assert F(2, 5) - (F(1, 3) + F(1, 3)) == F(-4, 15)


@pytest.mark.parametrize("n", [2, 3, 4, 5, 8, 9, 16, 17, 30, 33, 64, 100])
def test_fft_weights_match_explicit_formula_and_are_positive(n):
    x, w = clenshaw_curtis_weights(n)
    wd = clenshaw_curtis_weights_direct(n)
    assert max(abs(p - q) for p, q in zip(w, wd)) <= 20 * U
    assert all(t > 0 for t in w)
    assert math.fsum(w) == pytest.approx(2.0, abs=20 * U)
    big_n = n - 1
    end = 1 / (big_n * big_n - 1) if big_n % 2 == 0 else 1 / (big_n * big_n)
    assert w[0] == pytest.approx(end, rel=1e-13) and w[-1] == w[0]
    assert x == [-t for t in reversed(x)]


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 9, 12, 17, 24, 33])
def test_exactness_and_failure_at_next_degree(n):
    x, w = clenshaw_curtis_weights(n)
    d = degree(n)
    for k in range(d + 1):
        exact = 2 / (k + 1) if k % 2 == 0 else 0.0
        assert abs(math.fsum(wi * xi ** k for xi, wi in zip(x, w)) - exact) <= 10 * U
    k = d + 1
    err = (2 / (k + 1) if k % 2 == 0 else 0.0) - math.fsum(wi * xi ** k for xi, wi in zip(x, w))
    assert abs(err) > 100 * U  # -4/15 at n = 3, 5.7e-14 at n = 33


def test_random_polynomial_oracle():
    rng = random.Random(1960)
    for _ in range(600):
        n = rng.randint(2, 20)
        c = [F(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(rng.randint(1, degree(n) + 1))]
        a = rng.uniform(-3.0, 3.0)
        b = a + rng.choice([-1, 1]) * rng.uniform(0.01, 2.0)
        fa, fb = F(a), F(b)
        exact = sum((ck * (fb ** (k + 1) - fa ** (k + 1)) / (k + 1) for k, ck in enumerate(c)), F(0))
        cf = [float(t) for t in c]
        size = abs(b - a) * sum(abs(ck) * max(abs(a), abs(b)) ** k for k, ck in enumerate(cf))
        value = clenshaw_curtis(lambda t: math.fsum(ck * t ** k for k, ck in enumerate(cf)), a, b, n)
        assert abs(value - float(exact)) <= 1e-13 * size + 1e-300


def test_geometric_rates_for_analytic_integrands():
    ex = math.e - 1
    assert abs(clenshaw_curtis(math.exp, 0.0, 1.0, 9) - ex) < 1e-13
    assert clenshaw_curtis(math.exp, 0.0, 1.0, 17) == pytest.approx(ex, abs=4e-16)
    # Runge function: poles at +-i/5, rho = (1 + sqrt 26)/5; observed rate about rho^(-2N) (the kink phenomenon)
    exact = 0.4 * math.atan(5.0)
    errs = {n: abs(clenshaw_curtis(lambda t: 1 / (1 + 25 * t * t), -1.0, 1.0, n) - exact) for n in (17, 33, 65)}
    rho = (1 + math.sqrt(26)) / 5
    for n1, n2 in ((17, 33), (33, 65)):
        per_step = (errs[n1] / errs[n2]) ** (1 / (n2 - n1))
        assert rho < per_step < rho ** 2 * 1.02
    assert errs[65] < 1e-10
    # proved bound (64/15) M rho^(1-N) / (rho^2 - 1) on the ellipse with parameter r < rho
    r = 1.2
    m = max(abs(1 / (1 + 25 * z * z)) for z in [((r * cmath.exp(1j * t) + 1 / (r * cmath.exp(1j * t))) / 2)
                                                for t in [2 * math.pi * k / 4000 for k in range(4000)]])
    for n, e in errs.items():
        assert e <= 64 / 15 * m * r ** (1 - (n - 1)) / (r * r - 1)
    # periodic integrand: converges, but the trapezoidal rule would be better
    ecos = 2 * math.pi * 1.2660658777520082
    assert abs(clenshaw_curtis(lambda t: math.exp(math.cos(t)), 0, 2 * math.pi, 33) - ecos) < 1e-13


def test_algebraic_rates():
    # sqrt x: an x^(1/2) endpoint singularity gives N^(-3)
    e1 = abs(clenshaw_curtis(math.sqrt, 0.0, 1.0, 65) - 2 / 3)
    e2 = abs(clenshaw_curtis(math.sqrt, 0.0, 1.0, 129) - 2 / 3)
    assert math.log2(e1 / e2) == pytest.approx(3.0, abs=0.1)
    # an interior kink converges slowly and irregularly
    errs = [abs(clenshaw_curtis(lambda t: abs(t - 1 / 3), 0.0, 1.0, n) - 5 / 18) for n in (33, 65, 129, 257)]
    assert errs[-1] < 1e-5 and errs[0] > 1e-4


def test_oscillatory():
    # cos(100 x) on [0, 1]: nothing until N exceeds about 50, then fast convergence
    ex = math.sin(100.0) / 100
    errs = {n: abs(clenshaw_curtis(lambda t: math.cos(100 * t), 0.0, 1.0, n) - ex) for n in (17, 33, 65, 129)}
    assert errs[17] > 0.1 and errs[33] > 1e-5 and errs[65] < 1e-8 and errs[129] < 1e-15


def test_adaptive_doubling_reuses_values():
    calls = []

    def f(t):
        calls.append(t)
        return math.exp(t)
    v, est, used, status = integrate(f, 0.0, 1.0)
    assert status == "ok" and used == len(calls) == 17 and v == pytest.approx(math.e - 1, abs=4e-16)
    v, est, used, status = integrate(lambda t: 1 / (1 + 25 * t * t), -1.0, 1.0)
    assert status == "ok" and used == 257 and abs(v - 0.4 * math.atan(5.0)) < 1e-15
    v, est, used, status = integrate(math.sqrt, 0.0, 1.0, tol=1e-10)
    assert status == "ok" and used == 2049 and abs(v - 2 / 3) < 1e-10
    # unreachable tolerance within the budget
    v, est, used, status = integrate(math.sqrt, 0.0, 1.0, tol=1e-14, max_n=1025)
    assert status == "limit" and used == 1025 and abs(v - 2 / 3) < 1e-9


def test_edge_cases():
    assert clenshaw_curtis(math.exp, 1.0, 1.0, 9) == 0.0
    assert integrate(math.exp, 1.0, 1.0) == (0.0, 0.0, 0, "ok")
    assert clenshaw_curtis(math.exp, 1.0, 0.0, 17) == pytest.approx(-(math.e - 1), abs=4e-16)
    assert clenshaw_curtis(lambda t: 3.0, -2.0, 5.0, 2) == pytest.approx(21.0)  # n = 2 is the trapezoidal rule
    with pytest.raises(ValueError):
        clenshaw_curtis(math.exp, 0.0, 1.0, 1)
    # the endpoints are nodes: an endpoint singularity is evaluated
    with pytest.raises(ZeroDivisionError):
        clenshaw_curtis(lambda t: t ** -0.5, 0.0, 1.0, 9)
    with pytest.raises(ValueError):
        clenshaw_curtis(math.log, 0.0, 1.0, 9)
    # a jump: first order at best
    jump = [abs(clenshaw_curtis(lambda t: 0.0 if t < 0.3 else 1.0, 0.0, 1.0, n) - 0.7) for n in (65, 257)]
    assert 1e-5 < jump[1] < 1e-2
    # an infinite interval mapped to [-1, 1]: x = t / (1 - t^2), integral of 1/(1 + x^2) is pi
    # after simplification the mapped integrand (1 + t^2) / ((1 - t^2)^2 + t^2) is rational and smooth
    def mapped(t):
        return (1 + t * t) / ((1 - t * t) ** 2 + t * t)
    assert clenshaw_curtis(mapped, -1.0, 1.0, 33) == pytest.approx(math.pi, abs=1e-14)


def test_large_n_runs_fast():
    assert clenshaw_curtis(math.exp, 0.0, 1.0, 2 ** 14 + 1) == pytest.approx(math.e - 1, abs=1e-15)
    assert clenshaw_curtis(math.exp, 0.0, 1.0, 3001) == pytest.approx(math.e - 1, abs=1e-15)  # Bluestein length


@pytest.mark.parametrize("big_n", [1, 3, 5, 7, 9, 15])
def test_error_constant_for_odd_n(big_n):
    """For odd N the error on x^(N+1) is the integral of the monic node polynomial: 2^(3-N) / (N (N^2 - 4))."""
    x, w = clenshaw_curtis_weights(big_n + 1)
    k = big_n + 1
    err = 2 / (k + 1) - math.fsum(wi * xi ** k for xi, wi in zip(x, w))
    expect = -4 / 3 if big_n == 1 else 2.0 ** (3 - big_n) / (big_n * (big_n * big_n - 4))
    assert err == pytest.approx(expect, rel=1e-9)
