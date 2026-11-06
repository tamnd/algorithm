# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-euclidean-algorithm/. The authors are listed in prov/QQCABS.jsonl.

import math
import random

import pytest

from extended_euclidean_algorithm import extended_euclidean_algorithm as egcd
from extended_euclidean_algorithm import modular_inverse


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def brute_gcd(a: int, b: int) -> int:
    """The largest d that divides both, by direct search (small inputs only)."""
    a, b = abs(a), abs(b)
    if a == 0 and b == 0:
        return 0
    for d in range(max(a, b), 0, -1):
        if a % d == 0 and b % d == 0:
            return d
    raise AssertionError("unreachable")


def check(a: int, b: int, g_ref: int) -> None:
    g, x, y = egcd(a, b)
    assert g == g_ref
    assert a * x + b * y == g
    if a != 0 and b != 0:
        assert abs(x) <= abs(b) // g
        assert abs(y) <= abs(a) // g
        if abs(a) % abs(b) != 0:
            assert 2 * g * abs(x) <= abs(b)
            assert 2 * g * abs(y) <= abs(a)
        else:
            assert x == 0 and abs(y) == 1


def test_example() -> None:
    assert egcd(240, 46) == (2, -9, 47)
    assert egcd(1071, 462) == (21, -3, 7)


def test_zero_one_negative_equal() -> None:
    assert egcd(0, 0) == (0, 1, 0)
    assert egcd(0, 5) == (5, 0, 1)
    assert egcd(5, 0) == (5, 1, 0)
    assert egcd(0, -5) == (5, 0, -1)
    assert egcd(-5, 0) == (5, -1, 0)
    assert egcd(7, 7) == (7, 0, 1)
    assert egcd(1, 1) == (1, 0, 1)
    assert egcd(-240, 46) == (2, 9, 47)
    assert egcd(240, -46) == (2, -9, -47)
    assert egcd(-240, -46) == (2, 9, -47)
    for a in range(-30, 31):
        for b in range(-30, 31):
            check(a, b, brute_gcd(a, b))


def test_powers_of_two() -> None:
    for i in range(0, 150, 7):
        for j in range(0, 150, 11):
            check(2**i, 2**j, 2 ** min(i, j))
            check(3 * 2**i, -5 * 2**j, 2 ** min(i, j))


def test_fibonacci() -> None:
    for k in range(3, 300):
        a, b = fib(k + 1), fib(k)
        g, x, y = egcd(a, b)
        assert g == 1 and a * x + b * y == 1
        # by Cassini's identity the coefficients are consecutive Fibonacci numbers
        assert {abs(x), abs(y)} == {fib(k - 2), fib(k - 1)}


def test_random_small_against_direct_search() -> None:
    rng = random.Random(1)
    for _ in range(1500):
        a = rng.randint(-500, 500)
        b = rng.randint(-500, 500)
        check(a, b, brute_gcd(a, b))


def test_random_large_against_math_gcd() -> None:
    rng = random.Random(2)
    for _ in range(500):
        g = rng.getrandbits(rng.randint(1, 400)) + 1
        a = g * rng.getrandbits(rng.randint(0, 1200)) * rng.choice([-1, 1])
        b = g * rng.getrandbits(rng.randint(0, 1200)) * rng.choice([-1, 1])
        check(a, b, math.gcd(a, b))
    big = 10**300 + 7
    for m in range(1, 40):
        check(big * m, big * (m + 1), big)


def test_modular_inverse_against_pow() -> None:
    rng = random.Random(3)
    for _ in range(800):
        m = rng.choice([rng.randint(1, 1000), rng.getrandbits(900) + 1])
        a = rng.randint(-(10**300), 10**300)
        if math.gcd(a, m) == 1:
            assert modular_inverse(a, m) == pow(a, -1, m)
        else:
            with pytest.raises(ValueError):
                modular_inverse(a, m)
