# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euclidean-algorithm/. The authors are listed in prov/4XB0RJ.jsonl.

import math
import random

from euclidean_algorithm import division_steps, euclidean_algorithm


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
    assert euclidean_algorithm(1071, 462) == 21
    assert euclidean_algorithm(462, 1071) == 21
    assert division_steps(1071, 462) == 3
    assert division_steps(462, 1071) == 4


def test_zero_one_negative_equal() -> None:
    assert euclidean_algorithm(0, 0) == 0
    assert euclidean_algorithm(0, 7) == 7
    assert euclidean_algorithm(-7, 0) == 7
    assert euclidean_algorithm(1, 10**30) == 1
    assert euclidean_algorithm(-12, 18) == 6
    assert euclidean_algorithm(12, -18) == 6
    assert euclidean_algorithm(-12, -18) == 6
    assert euclidean_algorithm(42, 42) == 42
    assert euclidean_algorithm(-42, 42) == 42


def test_powers_of_two() -> None:
    for i in range(0, 200, 7):
        for j in range(0, 200, 11):
            assert euclidean_algorithm(2**i, 2**j) == 2 ** min(i, j)
            assert euclidean_algorithm(3 * 2**i, 5 * 2**j) == 2 ** min(i, j)


def test_fibonacci_worst_case() -> None:
    for k in range(1, 300):
        a, b = fib(k + 2), fib(k + 1)
        assert euclidean_algorithm(a, b) == 1
        assert division_steps(a, b) == k


def test_lame_bound() -> None:
    rng = random.Random(77)
    phi = (1 + 5**0.5) / 2
    for _ in range(2000):
        b = rng.randint(1, 10**12)
        a = rng.randint(b, 10**15)
        assert division_steps(a, b) <= 1 + math.log(b, phi) + 1e-9
        assert division_steps(a, b) <= 5 * len(str(b))


def test_against_brute_force() -> None:
    rng = random.Random(4096)
    for _ in range(1500):
        a = rng.randint(-300, 300)
        b = rng.randint(-300, 300)
        assert euclidean_algorithm(a, b) == brute_gcd(a, b)


def test_large_against_math_gcd() -> None:
    rng = random.Random(31337)
    for _ in range(500):
        g = rng.getrandbits(rng.randint(1, 400))
        a = g * rng.getrandbits(rng.randint(1, 1200)) * rng.choice((1, -1))
        b = g * rng.getrandbits(rng.randint(1, 1200)) * rng.choice((1, -1))
        assert euclidean_algorithm(a, b) == math.gcd(a, b)
    big = 10**300 + 7
    assert euclidean_algorithm(big * 6, big * 10) == 2 * big
