# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dot2-compensated-dot-product/. The authors are listed in prov/7CXZPB.jsonl.

"""Tests for Dot2: exact error-free transformations, the proved bound, and ill-conditioned cases."""

import math
import random
from fractions import Fraction

import pytest

from dot2_compensated_dot_product import dot2, naive_dot, two_product_dekker, two_product_fma, two_sum

U = Fraction(1, 2 ** 53)


def gamma(n: int) -> Fraction:
    return n * U / (1 - n * U)


def exact(x: list[float], y: list[float]) -> Fraction:
    return sum((Fraction(a) * Fraction(b) for a, b in zip(x, y)), Fraction(0))


def bound(x: list[float], y: list[float]) -> Fraction:
    n = len(x)
    return U * abs(exact(x, y)) + (1 + U) * gamma(n) ** 2 * sum(abs(Fraction(a) * Fraction(b)) for a, b in zip(x, y))


def gen_dot(n: int, log10_cond: float, rng: random.Random) -> tuple[list[float], list[float]]:
    """Ill-conditioned dot products in the spirit of Ogita, Rump and Oishi's GenDot (Algorithm 6.1)."""
    n2 = n // 2
    b = log10_cond * math.log2(10) / 2
    e = [round(rng.random() * b) for _ in range(n2)]
    e[0], e[-1] = round(b / 2) + 1, 0
    x = [(2 * rng.random() - 1) * 2.0 ** ei for ei in e]
    y = [(2 * rng.random() - 1) * 2.0 ** ei for ei in e]
    for i in range(n2, n):
        ei = round(b * (n - 1 - i) / (n - n2))
        xi = (2 * rng.random() - 1) * 2.0 ** ei
        yi = ((2 * rng.random() - 1) * 2.0 ** ei - float(exact(x, y))) / xi
        x.append(xi)
        y.append(yi)
    return x, y


def test_error_free_transformations_are_exact() -> None:
    rng = random.Random(1)
    for _ in range(3000):
        a = rng.uniform(-1, 1) * 2.0 ** rng.randint(-300, 300)
        b = rng.uniform(-1, 1) * 2.0 ** rng.randint(-300, 300)
        s, e = two_sum(a, b)
        assert Fraction(s) + Fraction(e) == Fraction(a) + Fraction(b) and s == a + b
        for tp in (two_product_fma, two_product_dekker):
            p, f = tp(a, b)
            assert Fraction(p) + Fraction(f) == Fraction(a) * Fraction(b) and p == a * b


def test_small_example() -> None:
    x = [1e16, 1.0, -1e16]
    y = [1.0, 1.0, 1.0]
    assert naive_dot(x, y) == 0.0
    assert dot2(x, y) == 1.0 and dot2(x, y, fma=False) == 1.0


def test_random_well_conditioned_is_correctly_rounded_or_near() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 60)
        x = [rng.uniform(0, 1) for _ in range(n)]
        y = [rng.uniform(0, 1) for _ in range(n)]
        r, t = dot2(x, y), exact(x, y)
        assert abs(Fraction(r) - t) <= bound(x, y)
        assert abs(Fraction(r) - t) <= Fraction(math.ulp(r))  # nonnegative data: within one ulp


def test_ill_conditioned_bound_holds() -> None:
    rng = random.Random(3)
    worse = 0
    for c in range(5, 40, 3):
        for _ in range(4):
            x, y = gen_dot(40, c, rng)
            t = exact(x, y)
            for f in (True, False):
                r = dot2(x, y, fma=f)
                assert abs(Fraction(r) - t) <= bound(x, y)
            if abs(Fraction(naive_dot(x, y)) - t) > abs(Fraction(dot2(x, y)) - t):
                worse += 1
    assert worse > 20


def test_relative_error_like_twice_the_precision() -> None:
    # Condition about 10^20: the naive result has no correct digit, Dot2 is still accurate.
    rng = random.Random(4)
    x, y = gen_dot(50, 20, rng)
    t = exact(x, y)
    cond = 2 * sum(abs(Fraction(a) * Fraction(b)) for a, b in zip(x, y)) / abs(t)
    rel = abs(Fraction(dot2(x, y)) - t) / abs(t)
    assert rel <= U + gamma(50) ** 2 * cond / 2 * (1 + U)
    assert rel < Fraction(1, 10 ** 6)


def test_zeros_signs_and_empty() -> None:
    assert dot2([], []) == 0.0
    assert dot2([0.0, -0.0], [5.0, 3.0]) == 0.0
    assert dot2([-2.0], [3.0]) == -6.0
    big = 2.0 ** 1023
    assert dot2([big, -big], [1.0, 1.0]) == 0.0


def test_nonfinite_and_underflow_limits() -> None:
    # Outside the assumptions: an infinite product makes the correction NaN.
    # (Python's math.fma raises ValueError on the invalid operation inf - inf.)
    assert math.isnan(dot2([math.inf], [1.0], fma=False))
    with pytest.raises(ValueError):
        dot2([math.inf], [1.0])
    # Underflow: TwoProduct is no longer exact, and the bound without an underflow term fails.
    x = [2.0 ** -600, 1.0]
    y = [2.0 ** -600, 0.0]
    assert dot2(x, y) == 0.0 and exact(x, y) == Fraction(1, 2 ** 1200)
    assert abs(Fraction(dot2(x, y)) - exact(x, y)) > bound(x, y)


def test_long_vectors_against_fsum_of_exact_parts() -> None:
    rng = random.Random(5)
    n = 2000
    x = [rng.uniform(-1, 1) for _ in range(n)]
    y = [rng.uniform(-1, 1) for _ in range(n)]
    parts = [v for a, b in zip(x, y) for v in two_product_fma(a, b)]
    ref = math.fsum(parts)  # the correctly rounded dot product
    assert abs(dot2(x, y) - ref) <= 2 * math.ulp(ref) + 1e-300
    assert abs(Fraction(dot2(x, y)) - exact(x, y)) <= bound(x, y)
