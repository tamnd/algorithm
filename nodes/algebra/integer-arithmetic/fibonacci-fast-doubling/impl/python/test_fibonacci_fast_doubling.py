# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-fast-doubling/. The authors are listed in prov/N8HHBP.jsonl.

import math
import random

from fibonacci_fast_doubling import fib_pair, fibonacci, fibonacci_mod


def table(limit: int) -> list[int]:
    """F(0) .. F(limit) by the defining recurrence, the oracle."""
    f = [0, 1]
    while len(f) <= limit:
        f.append(f[-1] + f[-2])
    return f


F = table(6000)


def test_example() -> None:
    assert fib_pair(11) == (89, 144)
    assert fibonacci(100) == 354224848179261915075


def test_edges() -> None:
    assert fib_pair(0) == (0, 1)
    assert fib_pair(1) == (1, 1)
    assert fib_pair(2) == (1, 2)
    for k in range(1, 13):
        assert fibonacci(2**k) == F[2**k]
        assert fibonacci(2**k - 1) == F[2**k - 1]
    assert fibonacci_mod(10**18, 1) == 0
    try:
        fibonacci(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_all_small() -> None:
    for n in range(0, 2001):
        assert fib_pair(n) == (F[n], F[n + 1])


def test_random_against_recurrence() -> None:
    rng = random.Random(1123)
    for _ in range(500):
        n = rng.randrange(0, 6000)
        assert fibonacci(n) == F[n]


def test_large_identities() -> None:
    rng = random.Random(58)
    for _ in range(20):
        n = rng.randrange(10**4, 10**5)
        a, b = fib_pair(n)
        c = fibonacci(n - 1)
        assert b * c - a * a == (-1) ** n  # Cassini
        m = rng.randrange(1, 300)
        assert math.gcd(fibonacci(m * 7), fibonacci(m * 5)) == fibonacci(m)


def test_modular() -> None:
    rng = random.Random(606)
    for _ in range(500):
        n = rng.randrange(0, 6000)
        m = rng.randrange(1, 10**6)
        assert fibonacci_mod(n, m) == F[n] % m
    assert fibonacci_mod(60, 10) == 0 and fibonacci_mod(61, 10) == 1  # Pisano period 60
    assert fibonacci_mod(10**18, 10**9 + 7) == fibonacci_mod(10**18 % (2 * 10**9 + 16), 10**9 + 7)
