# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pairwise-summation/. The authors are listed in prov/QGCJX6.jsonl.

import math
import random
from fractions import Fraction

from pairwise_summation import depth, pairwise_sum, pairwise_sum_iterative, recursive_sum

U = Fraction(1, 2**53)


def gamma(h: int) -> Fraction:
    return h * U / (1 - h * U)


def exact(xs) -> Fraction:
    return sum((Fraction(x) for x in xs), Fraction(0))


def ceil_log2(n: int) -> int:
    return (n - 1).bit_length()


def test_small_cases():
    assert pairwise_sum([]) == 0.0
    assert pairwise_sum_iterative([]) == 0.0
    assert pairwise_sum([2.5]) == 2.5
    assert pairwise_sum([0.1, 0.2]) == 0.1 + 0.2
    assert pairwise_sum([1.0, 2.0, 3.0, 4.0]) == (1.0 + 2.0) + (3.0 + 4.0)


def test_worked_example():
    xs = [1.0] + [2.0**-53] * 7
    assert recursive_sum(xs) == 1.0
    assert pairwise_sum(xs) == 1.0 + 3 * 2.0**-52
    assert Fraction(pairwise_sum(xs)) == exact(xs) - Fraction(1, 2**53)
    assert math.fsum(xs) == 1.0 + 2.0**-50


def test_repeated_tenth():
    xs = [0.1] * 10**5
    assert pairwise_sum(xs) == math.fsum(xs)
    assert recursive_sum(xs) != math.fsum(xs)


def test_depth_is_ceil_log2():
    for n in range(1, 3000):
        assert depth(n) == ceil_log2(n)
    for n in (1, 7, 8, 9, 100, 1000):
        for b in (1, 2, 8, 128):
            d = depth(n, b)
            assert d <= (min(n, b) - 1) + max(0, ceil_log2(-(-n // b)))


def test_error_bound_random():
    rng = random.Random(20240601)
    for trial in range(200):
        n = rng.randint(1, 600)
        kind = trial % 4
        if kind == 0:
            xs = [rng.random() for _ in range(n)]
        elif kind == 1:
            xs = [rng.uniform(-1, 1) for _ in range(n)]
        elif kind == 2:
            xs = [math.ldexp(rng.uniform(-1, 1), rng.randint(-60, 60)) for _ in range(n)]
        else:
            xs = [rng.choice([1e16, -1e16, 1.0, 0.5, 3.0]) for _ in range(n)]
        ex = exact(xs)
        abssum = exact(abs(x) for x in xs)
        for block in (1, 4, 32):
            err = abs(Fraction(pairwise_sum(xs, block)) - ex)
            assert err <= gamma(depth(n, block)) * abssum
        err = abs(Fraction(pairwise_sum_iterative(xs)) - ex)
        assert err <= gamma(ceil_log2(n)) * abssum


def test_exact_on_integers():
    rng = random.Random(5)
    xs = [float(rng.randint(-(2**40), 2**40)) for _ in range(1000)]
    assert Fraction(pairwise_sum(xs)) == exact(xs)


def test_beats_recursive_on_large_positive_sum():
    rng = random.Random(1)
    xs = [rng.random() for _ in range(100000)]
    ex = exact(xs)
    e_rec = abs(Fraction(recursive_sum(xs)) - ex)
    e_pw = abs(Fraction(pairwise_sum(xs)) - ex)
    assert e_pw < e_rec
    assert e_pw <= 2 * U * ex


def test_special_values():
    inf, nan = math.inf, math.nan
    assert pairwise_sum([1.0, inf, 2.0]) == inf
    assert math.isnan(pairwise_sum([inf, -inf]))
    assert math.isnan(pairwise_sum([1.0, nan]))
    big = 1.7976931348623157e308
    # (big + big) + (-big - big) = inf + (-inf): the exact sum 0 is lost to overflow
    assert math.isnan(pairwise_sum([big, big, -big, -big]))
    assert recursive_sum([big, big, -big, -big]) == inf
    assert math.copysign(1.0, pairwise_sum([-0.0, -0.0])) == -1.0


def test_block_argument():
    try:
        pairwise_sum([1.0], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("block 0 accepted")
    xs = [0.1 * i for i in range(50)]
    assert pairwise_sum(xs, 100) == recursive_sum(xs)
