# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levin-method/. The authors are listed in prov/BPA5JP.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from levin_method import chebyshev_values, levin, solve_complex


def poly_eval(coeffs, x):
    s = 0
    for c in reversed(coeffs):
        s = s * x + c
    return s


def poly_deriv(coeffs):
    return [k * c for k, c in enumerate(coeffs)][1:] or [0]


def fourier_oracle(coeffs, a, b, omega):
    """Integral of P(x) e^(i omega x) over [a, b] from the antiderivative
    e^(i omega x) sum_m (-1)^m P^(m)(x) / (i omega)^(m+1)."""
    def F(x):
        s, P, m = 0j, coeffs, 0
        while any(P):
            s += (-1) ** m * poly_eval(P, x) / (1j * omega) ** (m + 1)
            P, m = poly_deriv(P), m + 1
        return s * cmath.exp(1j * omega * x)
    return F(b) - F(a)


def gauss_legendre(m):
    xs, ws = [], []
    for i in range(1, m + 1):
        x = math.cos(math.pi * (i - 0.25) / (m + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, m + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = m * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def composite_gl(F, a, b, panels, m=20):
    xs, ws = gauss_legendre(m)
    h = (b - a) / panels
    s = 0j
    for p in range(panels):
        c = a + (p + 0.5) * h
        for x, w in zip(xs, ws):
            s += w * h / 2 * F(c + h / 2 * x)
    return s


def test_chebyshev_values():
    for t in (-1.0, -0.7, 0.0, 0.3, 0.99, 1.0):
        T, D = chebyshev_values(t, 9)
        for k in range(10):
            assert abs(T[k] - math.cos(k * math.acos(t))) < 1e-13
            if abs(t) < 1:
                th = math.acos(t)
                assert abs(D[k] - k * math.sin(k * th) / math.sin(th)) < 1e-11
            else:
                assert abs(D[k] - t ** (k + 1) * k * k) < 1e-11  # T_k'(1) = k^2, T_k'(-1) = (-1)^(k+1) k^2


def test_solver_exact_in_fractions():
    rng = random.Random(3)
    for m in range(1, 7):
        A = [[Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(m)] for _ in range(m)]
        for i in range(m):
            A[i][i] += 40
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 7)) for _ in range(m)]
        F = [sum(A[i][j] * x[j] for j in range(m)) for i in range(m)]
        assert solve_complex(A, F) == x
    with pytest.raises(ZeroDivisionError):
        solve_complex([[1, 2], [2, 4]], [1, 2])


def test_solver_complex_residual():
    rng = random.Random(4)
    m = 12
    A = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(m)] for _ in range(m)]
    F = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(m)]
    c = solve_complex(A, F)
    assert max(abs(sum(A[i][j] * c[j] for j in range(m)) - F[i]) for i in range(m)) < 1e-12


def test_exact_for_polynomials_with_linear_phase():
    for n in (1, 2, 5, 8):
        coeffs = [1.0, -2.0, 0.5, 3.0, -1.0, 0.25, 2.0, -0.5, 1.5][: n + 1]
        for omega in (3.0, 7.0, 300.0, -40.0):
            v = levin(lambda x: poly_eval(coeffs, x), lambda x: x, lambda x: 1.0, -0.5, 1.5, omega, n)
            ex = fourier_oracle(coeffs, -0.5, 1.5, omega)
            assert abs(v - ex) < 1e-11 * max(1.0, abs(ex))


def test_random_cases_against_closed_forms():
    rng = random.Random(5)
    worst = 0.0
    for case in range(500):
        n = rng.randint(1, 8)
        omega = rng.choice((1, -1)) * 10 ** rng.uniform(0, 3)
        q = [rng.uniform(-1, 1) for _ in range(n + 1)]
        if case % 2 == 0:
            # linear phase, f a polynomial of degree <= n
            a = rng.uniform(-2, 2)
            b = a + rng.choice((1, -1)) * rng.uniform(0.1, 2)
            v = levin(lambda x: poly_eval(q, x), lambda x: x, lambda x: 1.0, a, b, omega, n)
            ex = fourier_oracle(q, a, b, omega)
        else:
            # phase x^2/2 without stationary point, f = q' + i omega x q
            a = rng.uniform(0.5, 2)
            b = a + rng.uniform(0.1, 1)
            dq = poly_deriv(q)
            f = lambda x: poly_eval(dq, x) + 1j * omega * x * poly_eval(q, x)
            g = lambda x: x * x / 2
            v = levin(f, g, lambda x: x, a, b, omega, n)
            ex = poly_eval(q, b) * cmath.exp(1j * omega * g(b)) - poly_eval(q, a) * cmath.exp(1j * omega * g(a))
        worst = max(worst, abs(v - ex) / max(1.0, abs(ex)))
    assert worst < 1e-9


def test_spectral_in_n():
    ex = (cmath.exp(1 + 10j) - 1) / (1 + 10j)
    errs = [abs(levin(math.exp, lambda x: x, lambda x: 1.0, 0.0, 1.0, 10.0, n) - ex) for n in (2, 4, 6, 8, 10)]
    assert all(errs[i + 1] < errs[i] / 10 for i in range(3))
    assert errs[-1] < 1e-14


def test_error_decays_like_omega_to_the_minus_two_for_fixed_n():
    worst = 0.0
    for k in range(120):
        w = 10 ** (1 + 3 * k / 119)
        ex = (cmath.exp(1 + 1j * w) - 1) / (1 + 1j * w)
        e = abs(levin(math.exp, lambda x: x, lambda x: 1.0, 0.0, 1.0, w, 2) - ex)
        worst = max(worst, e * w * w)
    assert worst < 1.0
    # while |I| itself only decays like 1/omega
    assert abs((cmath.exp(1 + 1e4j) - 1) / (1 + 1e4j)) * 1e4 > 1.0


def test_nonlinear_phase_against_composite_gauss():
    f = lambda x: 1 / (1 + x)
    g = lambda x: x + x * x / 2
    dg = lambda x: 1 + x
    for w in (10.0, 100.0, 1000.0):
        ref = composite_gl(lambda x: f(x) * cmath.exp(1j * w * g(x)), 0.0, 1.0, int(w) + 10)
        assert abs(levin(f, g, dg, 0.0, 1.0, w, 16) - ref) < 1e-12
        assert abs(levin(f, g, dg, 0.0, 1.0, w, 2) - ref) < 10 / w ** 2


def test_stationary_point_breaks_the_method():
    g = lambda x: (x - 0.5) ** 2
    dg = lambda x: 2 * (x - 0.5)
    w = 100.0
    ref = composite_gl(lambda x: math.exp(x) * cmath.exp(1j * w * g(x)), 0.0, 1.0, 200)
    assert abs(levin(math.exp, g, dg, 0.0, 1.0, w, 17) - ref) > 0.1


def test_edges():
    one = lambda x: 1.0
    lin = lambda x: x
    d1 = lambda x: 1.0
    assert levin(one, lin, d1, 2.0, 2.0, 5.0, 3) == 0
    v = levin(math.exp, lin, d1, 0.0, 1.0, 30.0, 12)
    assert abs(levin(math.exp, lin, d1, 1.0, 0.0, 30.0, 12) + v) < 1e-14
    assert abs(levin(math.exp, lin, d1, 0.0, 1.0, -30.0, 12) - v.conjugate()) < 1e-14
    # a single linear piece, n = 1
    assert abs(levin(one, lin, d1, 0.0, 1.0, 3.0, 1) - (cmath.exp(3j) - 1) / 3j) < 1e-15
    for bad in ((0.0, 1.0, 0.0, 4), (0.0, 1.0, 1.0, 0), (0.0, math.inf, 1.0, 4)):
        with pytest.raises(ValueError):
            levin(one, lin, d1, *bad)
    # tiny omega: the system tends to a singular one
    ex = (cmath.exp(1 + 1e-6j) - 1) / (1 + 1e-6j)
    assert abs(levin(math.exp, lin, d1, 0.0, 1.0, 1e-6, 10) - ex) > 1e-3
    assert abs(levin(math.exp, lin, d1, 0.0, 1.0, 1e-2, 10) - (cmath.exp(1 + 1e-2j) - 1) / (1 + 1e-2j)) < 1e-6


def test_evaluation_counts():
    calls = {"f": 0, "g": 0, "dg": 0}

    def f(x):
        calls["f"] += 1
        return math.cos(x)

    def g(x):
        calls["g"] += 1
        return x + x ** 3

    def dg(x):
        calls["dg"] += 1
        return 1 + 3 * x * x

    levin(f, g, dg, 0.0, 2.0, 50.0, 9)
    assert calls == {"f": 10, "g": 2, "dg": 10}
