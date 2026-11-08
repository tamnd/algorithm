# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fejer-quadrature/. The authors are listed in prov/MK9GM6.jsonl.

import cmath
import math
import random
from fractions import Fraction as F

import pytest

from fejer_quadrature import fejer, fejer1_weights, fejer2_weights, fejer_points, fft, integrate

U = 2.0 ** -53
WEIGHTS = {1: fejer1_weights, 2: fejer2_weights}


def degree(n):
    return n if n % 2 else n - 1


def rule_from_fft(n, kind):
    """Recover the weights from the FFT-based rule by applying it to the Lagrange data e_j."""
    xs = fejer_points(n, kind)
    w = []
    for j in range(n):
        table = {x: (1.0 if i == j else 0.0) for i, x in enumerate(xs)}
        w.append(fejer(lambda t: table[t], -1.0, 1.0, n, kind))
    return w


def test_fft_against_direct_dft():
    rng = random.Random(1933)
    for m in (1, 2, 3, 6, 8, 10, 14, 32, 66):
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(m)]
        direct = [sum(x[j] * cmath.exp(-2j * math.pi * j * k / m) for j in range(m)) for k in range(m)]
        assert max(abs(p - q) for p, q in zip(fft(x), direct)) <= 1e-13 * m


def test_worked_examples_exact():
    # second rule, n = 3: nodes 0, +-1/sqrt 2, equal weights 2/3; degree 3; error 1/15 on x^4
    assert fejer_points(3, 2) == pytest.approx([math.sqrt(0.5), 0.0, -math.sqrt(0.5)], abs=2e-16)
    assert fejer2_weights(3) == pytest.approx([2 / 3] * 3, abs=1e-15)
    w, sq = [F(2, 3)] * 3, [F(1, 2), F(0), F(1, 2)]
    for k in (0, 2):
        assert sum((wi * s ** (k // 2) for wi, s in zip(w, sq)), F(0)) == F(2, k + 1)
    assert F(2, 5) - sum((wi * s ** 2 for wi, s in zip(w, sq)), F(0)) == F(1, 15)
    # first rule, n = 3: nodes 0, +-sqrt(3)/2, weights 4/9, 10/9, 4/9; error -1/10 on x^4
    assert fejer_points(3, 1) == pytest.approx([math.sqrt(0.75), 0.0, -math.sqrt(0.75)], abs=2e-16)
    assert fejer1_weights(3) == pytest.approx([4 / 9, 10 / 9, 4 / 9], abs=1e-15)
    w, sq = [F(4, 9), F(10, 9), F(4, 9)], [F(3, 4), F(0), F(3, 4)]
    for k in (0, 2):
        assert sum((wi * s ** (k // 2) for wi, s in zip(w, sq)), F(0)) == F(2, k + 1)
    assert F(2, 5) - sum((wi * s ** 2 for wi, s in zip(w, sq)), F(0)) == F(-1, 10)
    # n = 1: both are the midpoint rule
    assert fejer(lambda t: 3 * t + 1, 0.0, 2.0, 1, 1) == fejer(lambda t: 3 * t + 1, 0.0, 2.0, 1, 2) == 8.0


@pytest.mark.parametrize("kind", [1, 2])
@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 8, 9, 16, 21, 33])
def test_fft_rule_matches_explicit_weights_positive_symmetric(n, kind):
    w = WEIGHTS[kind](n)
    assert max(abs(p - q) for p, q in zip(rule_from_fft(n, kind), w)) <= 20 * U
    assert all(t > 0 for t in w)
    assert math.fsum(w) == pytest.approx(2.0, abs=20 * U)
    xs = fejer_points(n, kind)
    assert xs == [-t for t in reversed(xs)] and all(-1 < t < 1 for t in xs)


@pytest.mark.parametrize("kind", [1, 2])
@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 8, 9, 16, 17, 32, 33])
def test_exactness_and_failure_at_next_degree(n, kind):
    xs, w = fejer_points(n, kind), WEIGHTS[kind](n)
    d = degree(n)
    for k in range(d + 1):
        exact = 2 / (k + 1) if k % 2 == 0 else 0.0
        assert abs(math.fsum(wi * xi ** k for xi, wi in zip(xs, w)) - exact) <= 10 * U
    k = d + 1  # always even
    err = 2 / (k + 1) - math.fsum(wi * xi ** k for xi, wi in zip(xs, w))
    assert abs(err) > 100 * U  # 4e-13 (first rule) and 7e-12 (second rule) at n = 33
    # the first rule errs low, the second high, on x^(d+1)
    assert n == 1 or (err < 0) == (kind == 1)


def test_random_polynomial_oracle():
    rng = random.Random(1958)
    for _ in range(600):
        n, kind = rng.randint(1, 20), rng.choice([1, 2])
        c = [F(rng.randint(-30, 30), rng.randint(1, 7)) for _ in range(rng.randint(1, degree(n) + 1))]
        a = rng.uniform(-3.0, 3.0)
        b = a + rng.choice([-1, 1]) * rng.uniform(0.01, 2.0)
        fa, fb = F(a), F(b)
        exact = sum((ck * (fb ** (k + 1) - fa ** (k + 1)) / (k + 1) for k, ck in enumerate(c)), F(0))
        cf = [float(t) for t in c]
        size = abs(b - a) * sum(abs(ck) * max(abs(a), abs(b)) ** k for k, ck in enumerate(cf))
        value = fejer(lambda t: math.fsum(ck * t ** k for k, ck in enumerate(cf)), a, b, n, kind)
        assert abs(value - float(exact)) <= 1e-13 * size + 1e-300


@pytest.mark.parametrize("kind", [1, 2])
def test_closed_forms_and_rates(kind):
    assert fejer(math.exp, 0.0, 1.0, 16, kind) == pytest.approx(math.e - 1, abs=4e-16)
    runge = [abs(fejer(lambda t: 1 / (1 + 25 * t * t), -1.0, 1.0, n, kind) - 0.4 * math.atan(5.0))
             for n in (16, 32, 64, 128)]
    assert runge[0] > 1e-3 and runge[3] < 1e-13
    # endpoint singularities are never evaluated; rates N^(-3), N^(-2) (times a log), N^(-1)
    for f, exact, rate in ((math.sqrt, 2 / 3, 3.0), (math.log, -1.0, 2.0), (lambda t: t ** -0.5, 2.0, 1.0)):
        e1 = abs(fejer(f, 0.0, 1.0, 127, kind) - exact)
        e2 = abs(fejer(f, 0.0, 1.0, 255, kind) - exact)
        assert math.log2(e1 / e2) == pytest.approx(rate, abs=0.1)
    ecos = 2 * math.pi * 1.2660658777520082
    assert fejer(lambda t: math.exp(math.cos(t)), 0.0, 2 * math.pi, 32, kind) == pytest.approx(ecos, abs=1e-12)
    osc = [abs(fejer(lambda t: math.cos(100 * t), 0.0, 1.0, n, kind) - math.sin(100.0) / 100) for n in (16, 128)]
    assert osc[0] > 1e-3 and osc[1] < 1e-15


def test_nested_doubling():
    calls = []

    def f(t):
        calls.append(t)
        return math.exp(t)
    v, est, used, status = integrate(f, 0.0, 1.0)
    assert status == "ok" and used == len(calls) == 31 and len(set(calls)) == 31
    assert v == pytest.approx(math.e - 1, abs=4e-16)
    v, est, used, status = integrate(lambda t: 1 / (1 + 25 * t * t), -1.0, 1.0)
    assert status == "ok" and used == 255 and abs(v - 0.4 * math.atan(5.0)) < 1e-14
    v, est, used, status = integrate(math.sqrt, 0.0, 1.0)
    assert status == "ok" and used == 4095 and abs(v - 2 / 3) < 1e-10
    # x^(-1/2) converges like 1/N: the tolerance cannot be reached within the budget
    v, est, used, status = integrate(lambda t: t ** -0.5, 0.0, 1.0, max_n=1023)
    assert status == "limit" and used == 1023 and 1e-4 < abs(v - 2.0) < 1e-2


def test_edge_cases():
    assert fejer(math.exp, 2.0, 2.0, 8) == 0.0
    assert integrate(math.exp, 2.0, 2.0) == (0.0, 0.0, 0, "ok")
    assert fejer(math.exp, 1.0, 0.0, 16, 1) == pytest.approx(-(math.e - 1), abs=1e-15)
    assert fejer(math.exp, 1.0, 0.0, 16, 2) == pytest.approx(-(math.e - 1), abs=1e-15)
    with pytest.raises(ValueError):
        fejer(math.exp, 0.0, 1.0, 0)
    with pytest.raises(ValueError):
        fejer(math.exp, 0.0, 1.0, 4, kind=3)
    # a jump: slow
    jump = abs(fejer(lambda t: 0.0 if t < 0.3 else 1.0, 0.0, 1.0, 255) - 0.7)
    assert 1e-6 < jump < 1e-2
    # an infinite interval: x = t / (1 - t^2) maps (-1, 1) onto the real line, and the open rule never hits t = +-1
    def mapped(t):
        x = t / (1 - t * t)
        return math.exp(-x * x) * (1 + t * t) / (1 - t * t) ** 2
    assert fejer(mapped, -1.0, 1.0, 127) == pytest.approx(math.sqrt(math.pi), abs=1e-10)
