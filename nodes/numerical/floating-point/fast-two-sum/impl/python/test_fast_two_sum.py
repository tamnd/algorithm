# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-two-sum/. The authors are listed in prov/R9EM9Q.jsonl.

import math
import random
import struct
from fractions import Fraction

from fast_two_sum import exponent, fast_two_sum, precondition_holds

TINY = 2.0**-1074  # smallest subnormal
MIN_NORMAL = 2.0**-1022
MAX = (2.0 - 2.0**-52) * 2.0**1023


def exact_ok(a: float, b: float) -> bool:
    s, t = fast_two_sum(a, b)
    if s != a + b:
        return False
    if Fraction(a) + Fraction(b) != Fraction(s) + Fraction(t):
        return False
    # |t| <= ulp(s)/2: the pair is nonoverlapping
    return t == 0.0 or abs(Fraction(t)) <= Fraction(math.ulp(s)) / 2


def from_bits(n: int) -> float:
    return struct.unpack("<d", struct.pack("<Q", n))[0]


def test_example_rows():
    s, t = fast_two_sum(1.0, 2.0**-53 + 2.0**-105)
    assert s == 1.0 + 2.0**-52 and t == -(2.0**-53) + 2.0**-105
    s, t = fast_two_sum(0.2, 0.1)
    assert s == 0.30000000000000004 and t == -(2.0**-55)
    s, t = fast_two_sum(1e16, 1.5)
    assert s == 1.0000000000000002e16 and t == -0.5
    s, t = fast_two_sum(1.0, 1.5)  # same exponent, |a| < |b|: allowed
    assert (s, t) == (2.5, 0.0)


def test_lost_low_part():
    s, t = fast_two_sum(1.0, 2.0**-60)
    assert (s, t) == (1.0, 2.0**-60)


def test_precondition_violated_gives_wrong_error():
    assert not precondition_holds(2.0**-60, 1.0)
    s, t = fast_two_sum(2.0**-60, 1.0)
    assert (s, t) == (1.0, 0.0)
    assert Fraction(s) + Fraction(t) != Fraction(2.0**-60) + 1


def test_exponent():
    assert exponent(1.0) == 0 and exponent(1.5) == 0 and exponent(2.0) == 1
    assert exponent(0.1) == -4 and exponent(-3.0) == 1
    assert exponent(TINY) == -1022 and exponent(MIN_NORMAL) == -1022 and exponent(0.0) == -1022


def test_zeros_and_signs():
    for a, b in [(0.0, 0.0), (-0.0, 0.0), (0.0, -0.0), (-0.0, -0.0), (1.0, -1.0), (-2.5, 2.5)]:
        assert exact_ok(a, b)
    s, t = fast_two_sum(-0.0, -0.0)
    assert math.copysign(1.0, s) == -1.0


def test_subnormals_and_extremes():
    cases = [
        (TINY, TINY),
        (3 * TINY, -TINY),
        (MIN_NORMAL, -TINY),
        (MIN_NORMAL, TINY),
        (MAX, -MAX),
        (MAX, -1.0),
        (MAX / 2, MAX / 4),
        (1.0, -(2.0**-53)),
        (1.0, 2.0**-53),  # a tie, to even
        (1.0 + 2.0**-52, 2.0**-53),  # a tie, to even (upward)
    ]
    for a, b in cases:
        assert precondition_holds(a, b)
        assert exact_ok(a, b)


def test_overflow_is_not_hidden():
    s, t = fast_two_sum(MAX, 2.0**970)
    assert s == math.inf and t == -math.inf  # the pair is meaningless after overflow


def test_random_wide_range():
    rng = random.Random(20240501)
    count = 0
    while count < 3000:
        a = from_bits(rng.getrandbits(64))
        b = from_bits(rng.getrandbits(64))
        if not (math.isfinite(a) and math.isfinite(b)):
            continue
        if abs(a) < abs(b):
            a, b = b, a
        if not math.isfinite(a + b):
            continue
        assert exact_ok(a, b)
        count += 1


def test_random_close_exponents():
    rng = random.Random(7)
    for _ in range(3000):
        e = rng.randint(-1070, 1000)
        a = math.ldexp(rng.uniform(1.0, 2.0), e) * rng.choice((1, -1))
        b = math.ldexp(rng.uniform(1.0, 2.0), e - rng.randint(0, 60)) * rng.choice((1, -1))
        assert precondition_holds(a, b)
        assert exact_ok(a, b)


def test_random_same_exponent_any_order():
    rng = random.Random(99)
    for _ in range(2000):
        e = rng.randint(-1060, 1000)
        a = math.ldexp(rng.uniform(1.0, 2.0), e) * rng.choice((1, -1))
        b = math.ldexp(rng.uniform(1.0, 2.0), e) * rng.choice((1, -1))
        assert exponent(a) == exponent(b)
        assert exact_ok(a, b) and exact_ok(b, a)


def test_agrees_with_fsum():
    rng = random.Random(3)
    for _ in range(1000):
        a = rng.uniform(-1e6, 1e6)
        b = rng.uniform(-1.0, 1.0) * 2.0 ** rng.randint(-80, 0)
        s, t = fast_two_sum(a, b)
        assert math.fsum([s, t, -a, -b]) == 0.0
