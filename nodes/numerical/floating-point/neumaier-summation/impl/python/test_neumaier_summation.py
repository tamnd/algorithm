# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neumaier-summation/. The authors are listed in prov/C00E29.jsonl.

import math
import random
import sys
from fractions import Fraction

from neumaier_summation import neumaier_parts, neumaier_sum

U = Fraction(1, 2**53)


def gamma(k: int) -> Fraction:
    return k * U / (1 - k * U)


def exact(xs) -> Fraction:
    return sum((Fraction(x) for x in xs), Fraction(0))


def kahan_sum(xs) -> float:
    s = 0.0
    c = 0.0
    for x in xs:
        y = x - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def gen(rng: random.Random, kind: int, n: int) -> list[float]:
    if kind == 0:
        return [rng.random() for _ in range(n)]
    if kind == 1:
        return [rng.uniform(-1, 1) for _ in range(n)]
    if kind == 2:
        return [math.ldexp(rng.uniform(-1, 1), rng.randint(-200, 200)) for _ in range(n)]
    # ill conditioned: big terms that cancel, plus small ones
    xs = []
    for _ in range(n // 2):
        b = math.ldexp(rng.uniform(1, 2), rng.randint(30, 90))
        xs += [b, -b]
    xs += [rng.uniform(-1, 1) for _ in range(n - len(xs))]
    rng.shuffle(xs)
    return xs


def test_small_cases():
    assert neumaier_sum([]) == 0.0
    assert neumaier_sum([3.5]) == 3.5
    assert neumaier_sum([0.1, 0.2]) == 0.30000000000000004


def test_large_term_example():
    xs = [1.0, 1e100, 1.0, -1e100]
    assert neumaier_sum(xs) == 2.0
    assert kahan_sum(xs) == 0.0
    s, qs, c = neumaier_parts(xs)
    assert (s, qs, c) == (0.0, [0.0, 1.0, 1.0, 0.0], 2.0)


def test_errors_are_exact():
    rng = random.Random(3)
    for trial in range(200):
        xs = gen(rng, trial % 4, rng.randint(1, 60))
        s, qs, _ = neumaier_parts(xs)
        # s_n + sum of q_i equals the exact sum
        assert Fraction(s) + exact(qs) == exact(xs)


def test_proved_bound():
    rng = random.Random(11)
    for trial in range(400):
        n = rng.randint(1, 300)
        xs = gen(rng, trial % 4, n)
        ex = exact(xs)
        a = exact(abs(x) for x in xs)
        err = abs(Fraction(neumaier_sum(xs)) - ex)
        assert err <= U * abs(ex) + (1 + U) * gamma(max(n - 2, 0)) * gamma(max(n - 1, 0)) * a


def test_correctly_rounded_when_well_conditioned():
    rng = random.Random(1)
    xs = [rng.random() for _ in range(50000)]
    assert neumaier_sum(xs) == math.fsum(xs)


def test_matches_builtin_sum_on_recent_python():
    if sys.version_info < (3, 12):
        return
    rng = random.Random(8)
    for trial in range(200):
        xs = gen(rng, trial % 4, rng.randint(1, 100))
        assert neumaier_sum(xs) == sum(xs)


def test_special_values():
    # the error term becomes inf - inf = NaN; CPython's sum() tests for this case
    assert math.isnan(neumaier_sum([1.0, math.inf]))
    assert math.isnan(neumaier_sum([math.inf, -math.inf]))
    assert math.isnan(neumaier_sum([math.nan, 1.0]))
