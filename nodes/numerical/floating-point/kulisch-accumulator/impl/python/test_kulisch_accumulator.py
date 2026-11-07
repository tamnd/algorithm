# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kulisch-accumulator/. The authors are listed in prov/CV0X1C.jsonl.

import math
import random
from fractions import Fraction

from kulisch_accumulator import OFFSET, KulischAccumulator, exact_dot, exact_sum

MAX = 1.7976931348623157e308


def rnd(x: Fraction) -> float:
    try:
        return float(x)  # correctly rounded in CPython
    except OverflowError:
        return math.inf if x > 0 else -math.inf


def test_examples():
    assert exact_sum([1e100, 1.0, -1e100]) == 1.0
    assert exact_sum([0.1] * 10) == 1.0
    assert exact_sum([1.0, 2.0**-60, -1.0]) == 2.0**-60
    assert exact_sum([5e-324, 5e-324]) == 1e-323
    assert exact_sum([MAX, MAX, -MAX]) == MAX  # the intermediate 2*MAX is held exactly
    assert exact_dot([1e300, 1e300], [1e300, -1e300]) == 0.0
    assert exact_dot([1e-160, 3.0], [1e-160, 0.0]) == rnd(Fraction(1e-160) ** 2)  # a subnormal result
    assert exact_sum([]) == 0.0


def test_random_sums_and_dots_against_fractions():
    rng = random.Random(1)
    for _ in range(200):
        xs = [math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1020)) for _ in range(40)]
        ys = [math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1020)) for _ in range(40)]
        assert exact_sum(xs) == rnd(sum(map(Fraction, xs)))
        assert exact_dot(xs, ys) == rnd(sum(Fraction(x) * Fraction(y) for x, y in zip(xs, ys)))


def test_ill_conditioned_sums():
    rng = random.Random(2)
    for _ in range(200):
        xs = [rng.uniform(-1, 1) * 10.0 ** rng.randint(-30, 30) for _ in range(30)]
        xs += [-x for x in xs[:25]] + [rng.uniform(-1e-20, 1e-20)]
        rng.shuffle(xs)
        assert exact_sum(xs) == rnd(sum(map(Fraction, xs)))


def test_order_independent():
    rng = random.Random(3)
    xs = [math.ldexp(rng.uniform(-1, 1), rng.randint(-200, 200)) for _ in range(300)]
    ref = exact_sum(xs)
    for _ in range(5):
        rng.shuffle(xs)
        assert exact_sum(xs) == ref


def test_exact_register_contents():
    rng = random.Random(4)
    acc, total = KulischAccumulator(), Fraction(0)
    for _ in range(500):
        a = math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1023))
        b = math.ldexp(rng.uniform(-1, 1), rng.randint(-1074, 1023 - max(0, math.frexp(a)[1])))
        acc.add_product(a, b)
        total += Fraction(a) * Fraction(b)
        assert Fraction(acc.value(), 2**OFFSET) == total


def test_long_carry_and_borrow():
    acc = KulischAccumulator()
    acc.add(-(2.0**-1074))  # register becomes all ones: borrow through every limb
    assert acc.value() == -(1 << (OFFSET - 1074))
    acc.add(2.0**-1074)  # carry back through every limb
    assert acc.value() == 0 and all(limb == 0 for limb in acc.limbs)


def test_rounding_ties_and_overflow():
    assert exact_sum([1.0, 2.0**-53]) == 1.0  # tie, to even
    assert exact_sum([1.0, 2.0**-53, 2.0**-1074]) == 1.0 + 2.0**-52  # just above the tie
    assert exact_sum([1.0 + 2.0**-52, 2.0**-53]) == 1.0 + 2.0**-51  # tie, to even (up)
    assert exact_sum([MAX, MAX]) == math.inf
    assert exact_sum([MAX, 2.0**970]) == math.inf  # rounds to 2^1024
    assert exact_sum([MAX, 2.0**969]) == MAX


def test_special_values():
    assert math.isnan(exact_sum([1.0, math.nan]))
    assert math.isnan(exact_sum([math.inf, -math.inf]))
    assert exact_sum([math.inf, 1e308, 1e308]) == math.inf
    assert math.isnan(exact_dot([math.inf], [0.0]))
