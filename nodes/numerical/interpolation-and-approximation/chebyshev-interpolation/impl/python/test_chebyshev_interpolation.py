# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-interpolation/. The authors are listed in prov/YWEZA4.jsonl.

import math
import random

import pytest

from chebyshev_interpolation import (adaptive_chebyshev, chebyshev_coefficients, chebyshev_eval,
                                     chebyshev_interpolation, chebyshev_points, clenshaw)


def lagrange(xs, ys, t):
    """Independent oracle: the Lagrange form, evaluated directly."""
    total = 0.0
    for j, xj in enumerate(xs):
        w = 1.0
        for m, xm in enumerate(xs):
            if m != j:
                w *= (t - xm) / (xj - xm)
        total += w * ys[j]
    return total


def cheb_T(k, x):
    return math.cos(k * math.acos(max(-1.0, min(1.0, x))))


def test_random_data_against_lagrange():
    rng = random.Random(1854)
    for trial in range(600):
        n = rng.randint(0, 14)
        xs = chebyshev_points(n)
        ys = [rng.uniform(-1, 1) for _ in xs]
        c = chebyshev_coefficients(ys)
        assert len(c) == n + 1
        for j, x in enumerate(xs):  # interpolation at the nodes, including t exactly at a node
            assert abs(clenshaw(c, x) - ys[j]) <= 1e-13
        t = rng.uniform(-1.2, 1.2)
        assert abs(clenshaw(c, t) - lagrange(xs, ys, t)) <= 1e-11


def test_recovers_polynomials_and_aliases():
    rng = random.Random(1938)
    for _ in range(100):
        n = rng.randint(1, 20)
        a = [rng.uniform(-1, 1) for _ in range(n + 1)]
        ys = [clenshaw(a, x) for x in chebyshev_points(n)]
        c = chebyshev_coefficients(ys)
        assert max(abs(u - v) for u, v in zip(a, c)) <= 1e-13
    # T_{2n-k} and T_{2n+k} alias to T_k on n + 1 second-kind points (0 < k < n)
    for n in (5, 8, 13):
        for k in range(1, n):
            for m in (2 * n - k, 2 * n + k):
                c = chebyshev_coefficients([cheb_T(m, x) for x in chebyshev_points(n)])
                e = [0.0] * (n + 1)
                e[k] = 1.0
                assert max(abs(u - v) for u, v in zip(c, e)) <= 1e-12


def test_page_example_exp():
    c = chebyshev_interpolation(math.exp, 4)
    want = [1.26607, 1.13032, 0.27154, 0.0448798, 0.00547424]
    for u, v in zip(c, want):
        assert abs(u - v) <= 1e-5 * max(1.0, abs(v)) + 5e-9


def test_error_bounds():
    xs = [math.cos(math.pi * (j + 0.3) / 700) for j in range(700)]
    runge = lambda x: 1 / (1 + 25 * x * x)
    # ATAP Theorem 8.2 with rho = 1.2: M = max |f| on the ellipse, bounded by 6.27
    for n in (40, 80, 120):
        c = chebyshev_interpolation(runge, n)
        err = max(abs(runge(x) - chebyshev_eval(c, x)) for x in xs)
        assert err <= 4 * 6.27 * 1.2 ** (-n) / 0.2 + 1e-14
    # |x|: ATAP Theorem 7.2 with nu = 1, V = 2: error <= 4V/(pi (n - 1))
    for n in (10, 20, 40):
        c = chebyshev_interpolation(abs, n)
        err = max(abs(abs(x) - chebyshev_eval(c, x)) for x in xs + [0.0])
        assert err <= 8 / (math.pi * (n - 1))
    # Lebesgue bound: error <= (1 + Lambda_n) E_n with Lambda_n <= (2/pi) log(n + 1) + 1;
    # E_n(exp) >= |a_{n+1}| / 2 roughly, so check observed error is within a factor 4 of a_{n+1}
    for n in (4, 6, 8):
        c = chebyshev_interpolation(math.exp, n)
        err = max(abs(math.exp(x) - chebyshev_eval(c, x)) for x in xs)
        a_next = 2 * sum((0.5) ** (n + 1 + 2 * m) / (math.factorial(m) * math.factorial(n + 1 + m)) for m in range(10))
        assert a_next < err < 4 * a_next


def test_interval_mapping_and_edges():
    f = lambda t: 3 * t ** 3 - t + 2
    c = chebyshev_interpolation(f, 3, 2.0, 5.0)
    for t in (2.0, 2.5, 3.7, 5.0, 6.0):
        assert abs(chebyshev_eval(c, t, 2.0, 5.0) - f(t)) <= 1e-10 * abs(f(t))
    assert chebyshev_interpolation(lambda t: 7.0, 0) == [7.0]
    assert chebyshev_points(1) == [1.0, -1.0]
    c = chebyshev_interpolation(lambda t: 2 * t + 1, 1)
    assert abs(c[0] - 1) < 1e-15 and abs(c[1] - 2) < 1e-15
    pts = chebyshev_points(9)
    assert all(pts[j] == -pts[9 - j] for j in range(10))
    with pytest.raises(ValueError):
        chebyshev_interpolation(math.exp, -1)
    with pytest.raises(ValueError):
        chebyshev_interpolation(math.exp, 3, 1.0, 1.0)


def test_adaptive():
    c = adaptive_chebyshev(math.exp)
    assert 12 <= len(c) <= 16
    xs = [math.cos(math.pi * (j + 0.3) / 500) for j in range(500)]
    assert max(abs(math.exp(x) - clenshaw(c, x)) for x in xs) <= 1e-14
    r = lambda x: 1 / (1 + 25 * x * x)
    c = adaptive_chebyshev(r)
    assert max(abs(r(x) - clenshaw(c, x)) for x in xs) <= 1e-13
    # a large odd-even structure: odd function gives zero even coefficients
    c = chebyshev_interpolation(math.sin, 15)
    assert max(abs(c[k]) for k in range(0, 16, 2)) <= 1e-15
