# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/veltkamp-splitting/. The authors are listed in prov/Z6SW6X.jsonl.

import math
import random
from fractions import Fraction

from veltkamp_splitting import significant_bits, veltkamp_split, veltkamp_split_emulated


def ulp_exp(a: float) -> int:
    """The exponent of ulp(a) for a normal float a."""
    return math.frexp(a)[1] - 53


def check(a: float, s: int) -> None:
    hi, lo = veltkamp_split(a, s)
    assert Fraction(hi) + Fraction(lo) == Fraction(a)
    assert significant_bits(hi) <= 53 - s
    assert significant_bits(lo) <= max(s - 1, 1)
    if a != 0.0:
        quantum = Fraction(2) ** (ulp_exp(a) + s)
        assert (Fraction(hi) / quantum).denominator == 1
        assert abs(Fraction(lo)) <= quantum / 2


def test_examples():
    hi, lo = veltkamp_split(0.1)
    assert hi == 0.09999999962747097 and lo == 3.7252903539730653e-10
    hi, lo = veltkamp_split(math.pi)
    assert (hi, lo) == (3.1415926814079285, -2.781813535079891e-08)
    assert veltkamp_split(1.0) == (1.0, 0.0)
    assert veltkamp_split(0.0) == (0.0, 0.0)


def test_random_s27():
    rng = random.Random(2718)
    for _ in range(10000):
        a = math.ldexp(rng.uniform(-1, 1), rng.randint(-1000, 990))
        check(a, 27)


def test_all_split_points():
    rng = random.Random(31)
    for s in range(1, 53):
        for _ in range(300):
            check(math.ldexp(rng.uniform(-1, 1), rng.randint(-900, 900)), s)


def test_hard_significands():
    # all-ones significands and halfway patterns force rounding ties and carries
    for s in (2, 26, 27, 28):
        for a in (2.0 - 2.0**-52, 1.0 + 2.0**-52, 1.5, 1.0 + 2.0 ** (-53 + s), 1.0 + 2.0 ** (-54 + s)):
            check(a, s)
            check(-a * 2.0**100, s)


def test_products_of_parts_are_exact():
    rng = random.Random(4)
    for _ in range(5000):
        a = rng.uniform(-1e5, 1e5)
        b = rng.uniform(-1e5, 1e5)
        ah, al = veltkamp_split(a)
        bh, bl = veltkamp_split(b)
        for x, y in ((ah, bh), (ah, bl), (al, bh), (al, bl)):
            assert Fraction(x * y) == Fraction(x) * Fraction(y)


def test_exhaustive_small_precision():
    for p in (4, 5, 6, 7):
        emin = -4
        for s in range(1, p):
            for m in range(2 ** (p - 1), 2**p):
                for e in (-4, 0, 3):
                    a = Fraction(m) * Fraction(2) ** (e - p + 1)
                    hi, lo = veltkamp_split_emulated(a, s, p, emin)
                    assert hi + lo == a
                    quantum = Fraction(2) ** (e - p + 1 + s)
                    assert (hi / quantum).denominator == 1, (p, s, a)
                    assert abs(lo) <= quantum / 2


def test_overflow_limit():
    big = 1.7976931348623157e308
    hi, lo = veltkamp_split(big)
    assert math.isinf(hi) or math.isnan(hi) or math.isnan(lo)
    hi, lo = veltkamp_split(big / 2.0**28)
    assert Fraction(hi) + Fraction(lo) == Fraction(big / 2.0**28)


def test_subnormal_inputs():
    rng = random.Random(5)
    for _ in range(5000):
        a = rng.uniform(-1, 1) * 2.0**-1022 * rng.choice([1, 2.0**-10, 2.0**-30, 2.0**-45])
        hi, lo = veltkamp_split(a)
        assert Fraction(hi) + Fraction(lo) == Fraction(a)
        assert significant_bits(hi) <= 26 and significant_bits(lo) <= 26
