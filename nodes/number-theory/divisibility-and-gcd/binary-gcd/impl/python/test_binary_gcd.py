# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-gcd/. The authors are listed in prov/NZK9TA.jsonl.

import math
import random

from binary_gcd import binary_gcd, loop_passes, trailing_zeros


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


def test_example() -> None:
    assert binary_gcd(240, 46) == 2
    assert loop_passes(240, 46) == 5
    assert binary_gcd(1071, 462) == 21


def test_trailing_zeros() -> None:
    for x in range(1, 2000):
        t = 0
        y = x
        while y % 2 == 0:
            y //= 2
            t += 1
        assert trailing_zeros(x) == t


def test_zero_one_negative_equal() -> None:
    assert binary_gcd(0, 0) == 0
    assert binary_gcd(0, 7) == 7
    assert binary_gcd(-7, 0) == 7
    assert binary_gcd(0, -8) == 8
    assert binary_gcd(1, 10**30) == 1
    assert binary_gcd(-12, 18) == 6
    assert binary_gcd(12, -18) == 6
    assert binary_gcd(-12, -18) == 6
    assert binary_gcd(42, 42) == 42
    assert binary_gcd(-42, 42) == 42
    assert binary_gcd(-(2**63), 2**62) == 2**62


def test_powers_of_two() -> None:
    for i in range(0, 200, 7):
        for j in range(0, 200, 11):
            assert binary_gcd(2**i, 2**j) == 2 ** min(i, j)
            assert binary_gcd(3 * 2**i, 5 * 2**j) == 2 ** min(i, j)
            assert binary_gcd(6 * 2**i, 9 * 2**j) == 3 * 2 ** min(i + 1, j)


def test_fibonacci() -> None:
    for k in range(1, 400):
        a, b = fib(k + 2), fib(k + 1)
        assert binary_gcd(a, b) == 1
        assert binary_gcd(fib(2 * k), fib(k)) == fib(k)


def test_pass_bound() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        a = rng.randrange(1, 2**64)
        b = rng.randrange(1, 2**64)
        assert loop_passes(a, b) <= 1 + (a * b).bit_length()
    for n in range(1, 200):
        # (2^n - 1, 1) needs one pass for each binary digit
        assert loop_passes(2**n - 1, 1) == n


def test_random_small_against_direct_search() -> None:
    rng = random.Random(1)
    for _ in range(1500):
        a = rng.randint(-300, 300)
        b = rng.randint(-300, 300)
        assert binary_gcd(a, b) == brute_gcd(a, b)


def test_random_large_against_math_gcd() -> None:
    rng = random.Random(2)
    for _ in range(500):
        g = rng.getrandbits(rng.randint(1, 400)) + 1
        a = g * rng.getrandbits(rng.randint(0, 1200)) * rng.choice([-1, 1])
        b = g * rng.getrandbits(rng.randint(0, 1200)) * rng.choice([-1, 1])
        assert binary_gcd(a, b) == math.gcd(a, b)
    big = 10**300 + 7
    for m in range(1, 50):
        assert binary_gcd(big * m, big * (m + 1)) == big * math.gcd(m, m + 1)
        assert binary_gcd(big * 2**m, big * 3**m) == big
