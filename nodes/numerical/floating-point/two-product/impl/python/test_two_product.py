# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-product/. The authors are listed in prov/Q0TV83.jsonl.

import math
import random
from fractions import Fraction

from two_product import _fma_fallback, two_product, two_product_emulated, two_product_fma


def exact(a: float, b: float, x: float, y: float) -> bool:
    return Fraction(x) + Fraction(y) == Fraction(a) * Fraction(b)


def test_examples():
    assert two_product(0.1, 0.1) == (0.010000000000000002, -8.326672684688674e-19)
    a = 1.0 + 2.0**-52
    assert two_product(a, a) == (1.0 + 2.0**-51, 2.0**-104)
    assert two_product(3.0, 1.0 / 3.0) == (1.0, -(2.0**-54))
    assert two_product(2.0, 3.0) == (6.0, 0.0)


def test_random_exact_and_matches_fma():
    rng = random.Random(1971)
    for _ in range(20000):
        a = math.ldexp(rng.uniform(-1, 1), rng.randint(-480, 480))
        b = math.ldexp(rng.uniform(-1, 1), rng.randint(-480, 480))
        x, y = two_product(a, b)
        assert x == a * b
        assert exact(a, b, x, y)
        assert (x, y) == two_product_fma(a, b)
        assert abs(Fraction(y)) <= abs(Fraction(x)) * Fraction(1, 2**53)


def test_fma_fallback_agrees():
    rng = random.Random(7)
    for _ in range(3000):
        a, b, c = (rng.uniform(-1e3, 1e3) for _ in range(3))
        assert _fma_fallback(a, b, c) == float(Fraction(a) * Fraction(b) + Fraction(c))
        if hasattr(math, "fma"):
            assert math.fma(a, b, c) == _fma_fallback(a, b, c)


def test_hard_significands():
    vals = [1.0 + 2.0**-52, 2.0 - 2.0**-52, 1.5 + 2.0**-52, 1.0 + 2.0**-26, 1.0 + 2.0**-27, 1.0 + 2.0**-28]
    for a in vals:
        for b in vals:
            for sa in (1.0, -1.0):
                x, y = two_product(sa * a, b)
                assert exact(sa * a, b, x, y)


def test_underflow_loses_error():
    # e_a + e_b = -1000 < -970: the error 2^-1104 is below the smallest subnormal
    a = 2.0**-500 * (1.0 + 2.0**-52)
    x, y = two_product(a, a)
    assert y == 0.0 and not exact(a, a, x, y)
    # e_a + e_b = -960 >= -970: exact again, with a subnormal error
    a = 2.0**-480 * (1.0 + 2.0**-52)
    x, y = two_product(a, a)
    assert exact(a, a, x, y) and y == 2.0**-1064


def test_overflow_of_split():
    a = 2.0**1000
    x, y = two_product(a, 2.0**-1000)
    assert x == 1.0 and math.isnan(y)
    x, y = two_product_fma(a, 2.0**-1000)
    assert (x, y) == (1.0, 0.0)


def test_exhaustive_small_precision():
    for p in (4, 5, 6):
        emin = -30
        sig = [Fraction(m, 2 ** (p - 1)) for m in range(2 ** (p - 1), 2**p)]
        for a in sig:
            for b in sig:
                for sb in (1, -1):
                    x, y = two_product_emulated(a, sb * b, p, emin)
                    assert x + y == a * sb * b, (p, a, b)
