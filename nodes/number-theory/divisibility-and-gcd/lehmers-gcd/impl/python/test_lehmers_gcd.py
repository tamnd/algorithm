# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lehmers-gcd/. The authors are listed in prov/RN6MV6.jsonl.

import math
import random

from lehmers_gcd import lehmer_gcd


def brute_gcd(a: int, b: int) -> int:
    """Largest common divisor by direct search (small inputs only)."""
    a, b = abs(a), abs(b)
    if a == 0 or b == 0:
        return a + b
    return max(d for d in range(1, min(a, b) + 1) if a % d == 0 and b % d == 0)


def fib(n: int) -> int:
    x, y = 0, 1
    for _ in range(n):
        x, y = y, x + y
    return x


def test_example() -> None:
    assert lehmer_gcd(27182818, 10000000, w=8) == 2
    assert lehmer_gcd(1071, 462, w=4) == 21
    assert lehmer_gcd(12257478, 400528, w=8) == math.gcd(12257478, 400528)


def test_zero_one_signs_equal() -> None:
    for w in (2, 8, 64):
        assert lehmer_gcd(0, 0, w) == 0
        assert lehmer_gcd(0, 5, w) == 5
        assert lehmer_gcd(-5, 0, w) == 5
        assert lehmer_gcd(1, 10**50, w) == 1
        assert lehmer_gcd(10**50, 1, w) == 1
        assert lehmer_gcd(-12, -18, w) == 6
        assert lehmer_gcd(-(10**40), 10**30, w) == 10**30
        x = 3**200
        assert lehmer_gcd(x, x, w) == x
        assert lehmer_gcd(-x, x, w) == x


def test_powers_of_two() -> None:
    for w in (3, 16, 64):
        for i in range(0, 600, 37):
            for j in range(0, 600, 41):
                assert lehmer_gcd(2**i, 2**j, w) == 2 ** min(i, j)
                assert lehmer_gcd(2**i * 3, 2**j * 9, w) == 2 ** min(i, j) * 3


def test_fibonacci() -> None:
    for w in (2, 8, 32, 64):
        for n in range(1, 1500, 47):
            assert lehmer_gcd(fib(n + 1), fib(n), w) == 1
            # gcd(F_m, F_n) = F_gcd(m, n)
            assert lehmer_gcd(fib(2 * n), fib(3 * n), w) == fib(n)


def test_small_against_brute_force() -> None:
    rng = random.Random(1938)
    for _ in range(1500):
        a = rng.randint(-3000, 3000)
        b = rng.randint(-3000, 3000)
        w = rng.choice([2, 3, 4, 6, 8])
        assert lehmer_gcd(a, b, w) == brute_gcd(a, b)


def test_large_against_reference() -> None:
    rng = random.Random(64)
    for _ in range(500):
        da = rng.choice([5, 30, 100, 300, 600])
        db = rng.choice([5, 30, 100, 300, 600])
        g = rng.randint(1, 10 ** rng.choice([1, 20, 150]))
        a = g * rng.randint(-(10**da), 10**da)
        b = g * rng.randint(-(10**db), 10**db)
        w = rng.choice([2, 7, 16, 32, 64])
        assert lehmer_gcd(a, b, w) == math.gcd(a, b)
