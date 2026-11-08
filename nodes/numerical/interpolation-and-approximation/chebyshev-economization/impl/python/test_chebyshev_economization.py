# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-economization/. The authors are listed in prov/4BG9SS.jsonl.
import math
import random
from fractions import Fraction as F

import pytest

from chebyshev_economization import (
    chebyshev_to_power,
    clenshaw,
    economize,
    horner,
    power_to_chebyshev,
)


def cheb_T(k, x):
    """T_k(x) by the three-term recurrence (exact for Fraction x)."""
    t0, t1 = 1, x
    if k == 0:
        return F(1) if isinstance(x, F) else 1.0
    for _ in range(k - 1):
        t0, t1 = t1, 2 * x * t1 - t0
    return t1


def rand_poly(rng, n):
    return [F(rng.randint(-50, 50), rng.randint(1, 20)) for _ in range(n + 1)]


def test_conversion_exact_random():
    rng = random.Random(1938)
    for _ in range(300):
        n = rng.randint(0, 12)
        b = rand_poly(rng, n)
        c = power_to_chebyshev(b)
        assert len(c) == n + 1
        for _ in range(3):
            x = F(rng.randint(-40, 40), rng.randint(1, 13))
            assert sum(c[k] * cheb_T(k, x) for k in range(n + 1)) == horner(b, x)
            assert clenshaw(c, x) == horner(b, x)
        assert chebyshev_to_power(c) == b


def test_known_expansions():
    # x^5 = (10 T_1 + 5 T_3 + T_5) / 16
    assert power_to_chebyshev([F(0)] * 5 + [F(1)]) == [0, F(10, 16), 0, F(5, 16), 0, F(1, 16)]
    # x^k = 2^(1-k) sum binom(k, (k-j)/2) T_j, with the j = 0 term halved
    for k in range(0, 15):
        c = power_to_chebyshev([F(0)] * k + [F(1)])
        for j in range(k + 1):
            if (k - j) % 2:
                assert c[j] == 0
            else:
                w = F(math.comb(k, (k - j) // 2), 2 ** k)
                assert c[j] == (w if j == 0 else 2 * w)
    # T_n -> monomials: leading coefficient 2^(n-1)
    for n in range(1, 12):
        a = chebyshev_to_power([F(0)] * n + [F(1)])
        assert a[n] == 2 ** (n - 1)


def test_economize_bound_random():
    rng = random.Random(1956)
    for _ in range(250):
        n = rng.randint(0, 10)
        b = rand_poly(rng, n)
        tol = F(rng.randint(0, 200), 100)
        c_full = power_to_chebyshev(b)
        c, e = economize(b, tol)
        m = len(c) - 1
        assert c == c_full[:m + 1]
        assert e == sum(abs(v) for v in c_full[m + 1:])
        assert e <= tol
        # maximality: dropping one more term would exceed tol (unless m == 0)
        if m > 0:
            assert e + abs(c_full[m]) > tol
        for _ in range(4):
            x = F(rng.randint(-60, 60), 60)
            assert abs(horner(b, x) - clenshaw(c, x)) <= e


def test_one_step_is_minimax():
    # Dropping only the top term leaves error c_N T_N, which equioscillates N + 1 times.
    rng = random.Random(1854)
    for _ in range(100):
        n = rng.randint(1, 9)
        b = rand_poly(rng, n)
        if b[-1] == 0:
            b[-1] = F(1)
        c = power_to_chebyshev(b)
        assert c[n] == b[n] / 2 ** (n - 1)
        q = chebyshev_to_power(c[:n])
        q = q + [F(0)] * (n + 1 - len(q))
        err = [b[i] - q[i] for i in range(n + 1)]
        # err is c_n T_n
        assert err == [c[n] * v for v in chebyshev_to_power([F(0)] * n + [F(1)])]


def test_float_matches_fraction():
    rng = random.Random(1960)
    for _ in range(200):
        n = rng.randint(0, 12)
        b = [rng.uniform(-1, 1) for _ in range(n + 1)]
        cf = power_to_chebyshev(b)
        ce = power_to_chebyshev([F(v) for v in b])
        scale = sum(abs(v) for v in b)
        for u, v in zip(cf, ce):
            assert abs(u - float(v)) <= 1e-14 * max(scale, 1.0)
        c, e = economize(b, 1e-3)
        for i in range(21):
            x = -1 + i / 10
            assert abs(horner(b, x) - clenshaw(c, x)) <= e + 1e-13 * max(scale, 1.0)


def test_exp_example():
    b = [F(1, math.factorial(k)) for k in range(6)]
    c, e = economize(b, F(1, 1000))
    assert len(c) == 5 and e == F(1, 1920)
    a = chebyshev_to_power(c)
    assert a == [F(1), 1 - F(1, 384), F(1, 2), F(17, 96), F(1, 24)]
    xs = [math.cos(math.pi * i / 400) for i in range(401)]
    err = max(abs(math.exp(x) - horner([float(v) for v in a], x)) for x in xs)
    assert 2.0e-3 < err < 2.2e-3
    taylor4 = max(abs(math.exp(x) - horner([float(v) for v in b[:5]], x)) for x in xs)
    assert taylor4 > 4 * err


def test_edges():
    assert economize([F(3)], F(10)) == ([F(3)], 0)
    assert economize([2.0, 0.0, 0.0], 0.0) == ([2.0], 0.0)
    c, e = economize([F(1), F(1)], F(0))
    assert c == [F(1), F(1)] and e == 0
    c, e = economize([F(1), F(1)], F(1))
    assert c == [F(1)] and e == 1
    with pytest.raises(ValueError):
        economize([1.0], -1.0)
    with pytest.raises(ValueError):
        power_to_chebyshev([])


def test_monomial_conversion_growth():
    # Sum of |monomial coefficients| of T_n is about (1 + sqrt 2)^n / 2.
    for n in (10, 20, 30):
        a = chebyshev_to_power([F(0)] * n + [F(1)])
        s = sum(abs(v) for v in a)
        r = float(s) / ((1 + math.sqrt(2)) ** n / 2)
        assert 0.99 < r < 1.01
