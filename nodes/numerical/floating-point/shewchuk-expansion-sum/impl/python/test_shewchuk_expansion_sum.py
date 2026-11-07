# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shewchuk-expansion-sum/. The authors are listed in prov/A734Z5.jsonl.

import math
import random
from fractions import Fraction

from shewchuk_expansion_sum import (expansion_sum, grow_expansion, round_expansion,
                                    shewchuk_sum, two_sum, value)


def lowest_bit(x):
    n, d = abs(x).as_integer_ratio()
    return Fraction(n & -n, d)


def nonoverlapping_increasing(e):
    for a, b in zip(e, e[1:]):
        if a == 0.0 or b == 0.0:
            return False
        if not abs(a) < lowest_bit(b):
            return False
    return True


def rand_float(rng, lo=-60, hi=60):
    return rng.choice((1, -1)) * math.ldexp(rng.random() + 1.0, rng.randint(lo, hi))


def test_two_sum_exact():
    rng = random.Random(1)
    for _ in range(3000):
        a, b = rand_float(rng), rand_float(rng)
        s, t = two_sum(a, b)
        assert Fraction(s) + Fraction(t) == Fraction(a) + Fraction(b)


def test_grow_expansion_invariants():
    rng = random.Random(2)
    for trial in range(200):
        e, total = [], Fraction(0)
        for _ in range(rng.randint(1, 60)):
            x = rand_float(rng, -80, 80)
            e = grow_expansion(e, x)
            total += Fraction(x)
            assert value(e) == total
            assert nonoverlapping_increasing(e)


def test_expansion_sum_exact():
    rng = random.Random(3)
    for trial in range(200):
        e = f = []
        for _ in range(10):
            e = grow_expansion(e, rand_float(rng))
        for _ in range(10):
            f = grow_expansion(f, rand_float(rng))
        g = expansion_sum(e, f)
        assert value(g) == value(e) + value(f)
        assert nonoverlapping_increasing(g)


def test_correct_rounding_random():
    rng = random.Random(4)
    for trial in range(1500):
        xs = [rand_float(rng, -40, 40) for _ in range(rng.randint(1, 30))]
        exact = sum((Fraction(x) for x in xs), Fraction(0))
        assert shewchuk_sum(xs) == float(exact)
        assert shewchuk_sum(xs) == math.fsum(xs)


def test_ties_and_near_ties():
    u = 2.0 ** -53
    cases = [
        [1.0, u],                     # tie, stays at 1 (even)
        [1.0, u, u * u],              # just above the tie
        [1.0, u, -u * u],             # just below the tie
        [1.0 + 2 * u, u],             # tie, goes up to the even neighbour
        [1.0, -u / 2],                # tie below a power of two
        [1.0, -u / 2, -2.0 ** -200],
        [1e308, -1e308, 1e308, 2.0 ** -1074],
    ]
    for xs in cases:
        exact = sum((Fraction(x) for x in xs), Fraction(0))
        assert shewchuk_sum(xs) == float(exact), xs


def test_catastrophic_cancellation():
    assert shewchuk_sum([1e100, 1.0, -1e100]) == 1.0
    assert shewchuk_sum([0.1, 0.2, 0.3]) == 0.6
    rng = random.Random(5)
    for trial in range(100):
        xs = [rand_float(rng, -30, 30) for _ in range(50)]
        ys = xs + [-x for x in xs] + [1.5]
        rng.shuffle(ys)
        assert shewchuk_sum(ys) == 1.5


def test_subnormal_inputs():
    rng = random.Random(6)
    for trial in range(300):
        xs = [rng.randint(-10 ** 6, 10 ** 6) * 5e-324 for _ in range(10)] + [rand_float(rng, -1074, -1000)]
        exact = sum((Fraction(x) for x in xs), Fraction(0))
        assert shewchuk_sum(xs) == float(exact)


def test_specials():
    assert shewchuk_sum([]) == 0.0
    assert shewchuk_sum([1.0, math.inf]) == math.inf
    assert math.isnan(shewchuk_sum([math.inf, -math.inf]))
    try:
        shewchuk_sum([1.7e308, 1.7e308])
    except OverflowError:
        pass
    else:
        raise AssertionError("expected OverflowError")
    assert round_expansion([]) == 0.0
