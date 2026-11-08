# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagged-fibonacci-generator/. The authors are listed in prov/V53JWN.jsonl.

import itertools
import random

import pytest

from lagged_fibonacci_generator import (
    KnuthRanArray,
    LaggedFibonacci,
    max_period,
    period,
    seeded,
    trinomial_is_primitive,
)

PRIMITIVE_SMALL = [(2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 3)]


def naive(j, k, w, op, init, count):
    xs = list(init)
    m = 1 << w
    for _ in range(count):
        a, b = xs[-k], xs[-j]
        xs.append({"add": (a + b) % m, "sub": (a - b) % m, "mul": (a * b) % m, "xor": a ^ b}[op])
    return xs[k:]


def test_knuth_ran_array_check_value():
    # Knuth's rng.c prints 995235265 for both of these runs.
    g = KnuthRanArray(310952)
    for _ in range(2010):
        a = g.ran_array(1009)
    assert a[0] == 995235265
    g = KnuthRanArray(310952)
    for _ in range(1010):
        a = g.ran_array(2009)
    assert a[0] == 995235265


def test_circular_buffer_matches_recurrence():
    rng = random.Random(3)
    for op in ("add", "sub", "mul", "xor"):
        for _ in range(20):
            k = rng.randint(2, 12)
            j = rng.randint(1, k - 1)
            w = rng.choice([1, 3, 8, 32, 64])
            init = [rng.getrandbits(w) | 1 for _ in range(k)]
            g = LaggedFibonacci(j, k, w, op, init)
            assert [g.next() for _ in range(100)] == naive(j, k, w, op, init, 100)


def test_fibonacci_mod_two_power():
    # Lags (2, 1) give the Fibonacci numbers; their period modulo 16 is 24.
    g = LaggedFibonacci(1, 2, 4, "add", [0, 1])
    assert [g.next() for _ in range(8)] == [1, 2, 3, 5, 8, 13, 5, 2]
    assert period(1, 2, 4, "add", [0, 1]) == (0, 24)


@pytest.mark.parametrize("k,j", PRIMITIVE_SMALL)
def test_additive_period_is_maximal_for_every_seed_with_an_odd_value(k, j):
    assert trinomial_is_primitive(k, j)
    for w in (1, 2, 3):
        if 2 ** (w * k) > 4096:
            seeds = [[1] + [0] * (k - 1), list(range(3, 3 + k)), [2**w - 1] * k]
        else:
            seeds = [s for s in itertools.product(range(2**w), repeat=k) if any(x % 2 for x in s)]
        for s in seeds:
            for op in ("add", "sub"):
                assert period(j, k, w, op, s) == (0, max_period(k, w, op))


def test_multiplicative_maximal_period_reached_but_not_by_all_odd_seeds():
    for k, j in [(2, 1), (3, 1), (4, 1), (5, 2)]:
        for w in (3, 4, 5):
            periods = {period(j, k, w, "mul", s)[1] for s in itertools.product(range(1, 2**w, 2), repeat=k)} if (2 ** (w - 1)) ** k <= 4096 else {
                period(j, k, w, "mul", [3] + [1] * (k - 1))[1]
            }
            assert max(periods) == max_period(k, w, "mul")
    assert period(1, 2, 5, "mul", [1, 1]) == (0, 1)  # all ones is a fixed point


def test_xor_and_non_primitive_trinomial():
    assert period(1, 4, 8, "xor", [1, 0, 0, 0]) == (0, 15)
    assert not trinomial_is_primitive(4, 2)  # x^4 + x^2 + 1 = (x^2 + x + 1)^2
    periods = {period(2, 4, 3, "add", s)[1] for s in itertools.product(range(8), repeat=4) if any(x % 2 for x in s)}
    assert max(periods) < max_period(4, 3, "add")


def test_classic_lags_are_primitive_trinomials():
    for k, j in [(55, 24), (100, 37), (607, 273)]:
        assert trinomial_is_primitive(k, j)
    assert max_period(55, 32, "add") == (2**55 - 1) * 2**31


def test_three_point_relation_of_additive_generator():
    g = seeded(24, 55, 32, "add", 2024)
    xs = [g.next() for _ in range(20000)]
    hits = total = 0
    for n in range(55, len(xs)):
        d = (xs[n] - xs[n - 24] - xs[n - 55]) % 2**32
        assert d == 0
        u0, u1, u2 = xs[n - 55] / 2**32, xs[n - 24] / 2**32, xs[n] / 2**32
        assert round(u2 - u1 - u0) in (0, -1)
        if u0 + u1 < 0.5:
            total += 1
            hits += u2 < 0.5
    assert total > 1000 and hits == total  # independent values would give about half


def test_top_bits_chi_square():
    g = seeded(24, 55, 32, "add", 7)
    counts = [0] * 16
    n = 16000
    for _ in range(n):
        counts[g.next() >> 28] += 1
    chi2 = sum((c - n / 16) ** 2 / (n / 16) for c in counts)
    assert chi2 < 37.70  # 0.999 quantile of chi-square with 15 degrees of freedom


def test_edge_cases():
    with pytest.raises(ValueError):
        LaggedFibonacci(24, 55, 32, "add", [0] * 55)
    with pytest.raises(ValueError):
        LaggedFibonacci(1, 3, 8, "mul", [1, 2, 3])
    with pytest.raises(ValueError):
        LaggedFibonacci(1, 3, 8, "xor", [0, 0, 0])
    with pytest.raises(ValueError):
        LaggedFibonacci(3, 3, 8, "add", [1, 1, 1])
    with pytest.raises(ValueError):
        LaggedFibonacci(1, 3, 8, "add", [1, 1])
    top = 2**64 - 1
    g = LaggedFibonacci(1, 2, 64, "add", [top, top])
    assert g.next() == top - 1
    u = seeded(24, 55, 64, "add", 1).uniform()
    assert 0.0 <= u < 1.0
