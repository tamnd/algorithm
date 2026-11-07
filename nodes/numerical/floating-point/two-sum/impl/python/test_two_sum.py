# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-sum/. The authors are listed in prov/FP385Q.jsonl.

import math
import random
import struct
from fractions import Fraction

from two_sum import round_to_precision, two_sum, two_sum_emulated

TINY = 2.0**-1074
MIN_NORMAL = 2.0**-1022
MAX = (2.0 - 2.0**-52) * 2.0**1023


def from_bits(n: int) -> float:
    return struct.unpack("<d", struct.pack("<Q", n))[0]


def exact_ok(a: float, b: float) -> bool:
    s, t = two_sum(a, b)
    if s != a + b:
        return False
    if Fraction(a) + Fraction(b) != Fraction(s) + Fraction(t):
        return False
    return t == 0.0 or abs(Fraction(t)) <= Fraction(math.ulp(s)) / 2


def test_examples():
    assert two_sum(1.0, 2.0**-53) == (1.0, 2.0**-53)
    assert two_sum(2.0**-53, 1.0) == (1.0, 2.0**-53)
    assert two_sum(0.1, 0.2) == (0.30000000000000004, -2.0**-55)
    assert two_sum(1e16, 1.5) == (1e16 + 2, -0.5)
    assert two_sum(2.0**-60, 1.0) == (1.0, 2.0**-60)
    assert two_sum(1.0, -1.0) == (0.0, 0.0)


def test_both_orders_random():
    rng = random.Random(12345)
    for _ in range(20000):
        a = math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1023))
        b = math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1023))
        if math.isinf(a + b):
            continue
        assert exact_ok(a, b) and exact_ok(b, a)


def test_close_exponents():
    rng = random.Random(7)
    for _ in range(20000):
        e = rng.randint(-1000, 960)
        a = math.ldexp(rng.uniform(-1, 1), e)
        b = math.ldexp(rng.uniform(-1, 1), e + rng.randint(-60, 60))
        assert exact_ok(a, b) and exact_ok(b, a)


def test_random_bit_patterns_and_subnormals():
    rng = random.Random(99)
    for _ in range(10000):
        a = from_bits(rng.getrandbits(64))
        b = from_bits(rng.getrandbits(64))
        if not (math.isfinite(a) and math.isfinite(b)) or math.isinf(a + b):
            continue
        assert exact_ok(a, b)
    for k in range(1, 200):
        assert exact_ok(k * TINY, MIN_NORMAL - TINY)
        assert exact_ok(-k * TINY, MIN_NORMAL)


def test_agrees_with_fsum():
    rng = random.Random(3)
    for _ in range(5000):
        a = rng.uniform(-1e10, 1e10)
        b = rng.uniform(-1, 1) * 10.0 ** rng.randint(-30, 10)
        s, t = two_sum(a, b)
        assert t == math.fsum([a, b, -s])


def test_exhaustive_small_precision():
    # all pairs of floats in binary formats with p = 2, 3, 4 and exponents -3 .. 3
    for p in (2, 3, 4):
        emin, emax = -3, 3
        floats = set()
        for e in range(emin, emax + 1):
            for m in range(2 ** (p - 1), 2**p):
                v = Fraction(m) * Fraction(2) ** (e - p + 1)
                floats.update((v, -v))
        for m in range(0, 2 ** (p - 1)):
            v = Fraction(m) * Fraction(2) ** (emin - p + 1)
            floats.update((v, -v))
        floats = sorted(floats)
        for a in floats:
            for b in floats:
                s, t = two_sum_emulated(a, b, p, emin)
                assert s + t == a + b, (p, a, b)


def test_rounding_emulation_matches_hardware():
    rng = random.Random(5)
    for _ in range(2000):
        a = rng.uniform(-10, 10)
        b = rng.uniform(-10, 10)
        assert round_to_precision(Fraction(a) + Fraction(b), 53, -1022) == Fraction(a + b)


def test_overflow():
    s, t = two_sum(MAX, MAX)
    assert s == math.inf and math.isnan(t)
    s, t = two_sum(MAX, -MAX)
    assert (s, t) == (0.0, 0.0)
