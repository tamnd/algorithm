# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kahan-summation/. The authors are listed in prov/7H2DE0.jsonl.

import math
import random
from fractions import Fraction

from kahan_summation import kahan_steps, kahan_sum, kahan_sum_corrected

U = Fraction(1, 2**53)


def exact(xs) -> Fraction:
    return sum((Fraction(x) for x in xs), Fraction(0))


def recursive_sum(xs) -> float:
    s = 0.0
    for x in xs:
        s += x
    return s


def exponent(x: float) -> int:
    return max(math.frexp(x)[1] - 1, -1022)


def hypothesis_holds(xs) -> bool:
    """Every addition s + y has s = 0 or exponent(s) >= exponent(y)."""
    s = 0.0
    c = 0.0
    for x in xs:
        y = x - c
        if s != 0.0 and y != 0.0 and exponent(s) < exponent(y):
            return False
        t = s + y
        c = (t - s) - y
        s = t
    return True


def bound(xs) -> Fraction:
    n = len(xs)
    return (2 * U + (n + 4) * U * U) * exact(abs(x) for x in xs)


def test_small_cases():
    assert kahan_sum([]) == 0.0
    assert kahan_sum([3.25]) == 3.25
    assert kahan_sum([0.1, 0.2]) == 0.1 + 0.2


def test_trace_example():
    xs = [1e16, 1.0, 1.0, 1.0, 1.0]
    steps = kahan_steps(xs)
    assert [c for (_, _, c, _) in steps] == [0.0, -1.0, 0.0, 1.0, 0.0]
    assert [s for (_, _, _, s) in steps] == [1e16, 1e16, 1e16 + 2, 1e16 + 4, 1e16 + 4]
    assert kahan_sum(xs) == 1e16 + 4
    assert recursive_sum(xs) == 1e16


def test_tiny_terms():
    xs = [1.0] + [2.0**-53] * 7
    assert kahan_sum(xs) == math.fsum(xs) == 1.0 + 2.0**-50
    assert recursive_sum(xs) == 1.0


def test_repeated_tenth():
    xs = [0.1] * 10**5
    assert kahan_sum(xs) == math.fsum(xs)


def test_correction_is_exact_under_hypothesis():
    rng = random.Random(77)
    for _ in range(300):
        xs = [rng.uniform(0, 1) * 2.0 ** rng.randint(-30, 0) for _ in range(rng.randint(1, 80))]
        s = Fraction(0)
        c = Fraction(0)
        ok = hypothesis_holds(xs)
        for (y, t, cn, _), x in zip(kahan_steps(xs), xs):
            if ok:
                # c is the exact negated rounding error of t = fl(s + y)
                assert Fraction(cn) == (Fraction(t) - s) - Fraction(y)
                assert abs(Fraction(cn)) <= U * abs(Fraction(t))
            s = Fraction(t)


def test_proved_bound_when_hypothesis_holds():
    rng = random.Random(2024)
    checked = 0
    for trial in range(300):
        n = rng.randint(1, 400)
        if trial % 3 == 0:
            xs = [rng.random() for _ in range(n)]
        elif trial % 3 == 1:
            xs = [rng.uniform(-1, 1) for _ in range(n)]
        else:
            xs = [math.ldexp(rng.uniform(0.5, 1), rng.randint(-40, 0)) for _ in range(n)]
        err = abs(Fraction(kahan_sum(xs)) - exact(xs))
        if hypothesis_holds(xs):
            checked += 1
            assert err <= bound(xs)
    assert checked > 50


def test_observed_bound_in_general():
    rng = random.Random(99)
    for _ in range(300):
        n = rng.randint(1, 300)
        xs = [math.ldexp(rng.uniform(-1, 1), rng.randint(-80, 80)) for _ in range(n)]
        err = abs(Fraction(kahan_sum(xs)) - exact(xs))
        assert err <= bound(xs)


def test_large_random_error_independent_of_n():
    rng = random.Random(1)
    xs = [rng.random() for _ in range(100000)]
    ex = exact(xs)
    assert abs(Fraction(kahan_sum(xs)) - ex) <= U * ex


def test_known_failure_large_term():
    xs = [1.0, 1e100, 1.0, -1e100]
    assert kahan_sum(xs) == 0.0
    assert math.fsum(xs) == 2.0
    assert kahan_sum_corrected(xs) == 0.0


def test_special_values():
    # the correction becomes inf - inf = NaN, which poisons the next term
    assert kahan_sum([1.0, math.inf]) == math.inf
    assert math.isnan(kahan_sum([1.0, math.inf, 1.0]))
    assert math.isnan(kahan_sum([math.nan, 1.0]))
    assert kahan_sum([-0.0]) == 0.0
