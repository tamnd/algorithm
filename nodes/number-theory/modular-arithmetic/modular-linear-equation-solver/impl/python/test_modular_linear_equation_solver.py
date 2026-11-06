# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modular-linear-equation-solver/. The authors are listed in prov/XRMYSW.jsonl.

import math
import random

import pytest

from modular_linear_equation_solver import extended_euclid
from modular_linear_equation_solver import modular_linear_equation_solver as solve
from modular_linear_equation_solver import solve_compact


def brute(a: int, b: int, n: int) -> list[int]:
    """Every x in 0..n-1 with n | a*x - b, by direct test (small n only)."""
    return [x for x in range(n) if (a * x - b) % n == 0]


def check_compact(a: int, b: int, n: int) -> None:
    """Check the compact answer against the theory, using math.gcd as reference."""
    d = math.gcd(a, n)
    r = solve_compact(a, b, n)
    if b % d != 0:
        assert r is None
        return
    assert r is not None
    x0, m = r
    assert m == n // d and 0 <= x0 < m
    assert (a * x0 - b) % n == 0
    # x0 + m is again a solution, and the solutions are a single class mod m
    assert (a * (x0 + m) - b) % n == 0


def test_examples() -> None:
    assert solve(14, 30, 100) == [45, 95]
    assert solve(35, 10, 50) == [6, 16, 26, 36, 46]
    assert solve(8, 12, 28) == [5, 12, 19, 26]
    assert solve(8, 13, 28) == []
    assert extended_euclid(14, 100) == (2, -7, 1)


def test_edges() -> None:
    assert solve(5, 3, 1) == [0]
    assert solve(0, 0, 1) == [0]
    assert solve(0, 0, 7) == list(range(7))
    assert solve(0, 3, 7) == []
    assert solve(1, 0, 2) == [0]
    assert solve(1, 1, 2) == [1]
    assert solve(-3, 4, 10) == [2]
    assert solve(3, -4, 10) == [2]
    assert solve(10 + 3, 4 + 20, 10) == solve(3, 4, 10)
    assert solve(64, 0, 1024) == list(range(0, 1024, 16))
    with pytest.raises(ValueError):
        solve(1, 1, 0)
    with pytest.raises(ValueError):
        solve_compact(1, 1, -5)


def test_exhaustive_small() -> None:
    for n in range(1, 41):
        for a in range(-n, 2 * n + 1):
            for b in range(-2, n + 2):
                assert solve(a, b, n) == brute(a, b, n)


def test_inverse_cases() -> None:
    for n in (2, 3, 7, 8, 9, 15, 16, 97, 100, 1024):
        for a in range(n):
            xs = solve(a, 1, n)
            if math.gcd(a, n) == 1:
                assert len(xs) == 1 and a * xs[0] % n == 1
                assert xs[0] == pow(a, -1, n)
            else:
                assert xs == []


def test_powers_of_two_and_m_minus_one() -> None:
    for k in range(0, 70, 3):
        n = 2**k
        for a in (0, 1, n - 1, 2 ** (k // 2), 3 * 2 ** (k // 3), 12345):
            for b in (0, 1, n - 1, 2 ** (k // 2), 2 ** (k // 3)):
                check_compact(a, b, n)


def test_random_small_against_brute() -> None:
    rng = random.Random(31)
    for _ in range(2000):
        n = rng.randint(1, 300)
        a = rng.randint(-1000, 1000)
        b = rng.randint(-1000, 1000)
        if rng.random() < 0.3:
            g = rng.randint(1, 20)
            a, n = a * g, n * g
            b = b * g if rng.random() < 0.7 else b
        assert solve(a, b, n) == brute(a, b, n)


def test_random_large() -> None:
    rng = random.Random(32)
    for _ in range(600):
        digits = rng.choice([20, 100, 300, 600])
        n = rng.randint(1, 10**digits)
        d = rng.choice([1, 2, 3, 7, 64, rng.randint(1, 50)])
        a = rng.randint(-(10**digits), 10**digits) * d
        n = n * d
        b = rng.randint(0, 10**digits) * (d if rng.random() < 0.8 else 1)
        check_compact(a, b, n)
        if math.gcd(a, n) <= 64:
            xs = solve(a, b, n)
            g = math.gcd(a, n)
            assert len(xs) == (g if b % g == 0 else 0)
            for x in xs:
                assert 0 <= x < n and (a * x - b) % n == 0
            assert xs == sorted(set(xs))


def test_large_primes_and_composites() -> None:
    p = 2**521 - 1  # a Mersenne prime
    q = 2**127 - 1  # a Mersenne prime
    for n in (p, q, p * q, p * p, 2**600):
        for a in (1, 2, 3, n - 1, q, p, 2**64, 10**150 + 7):
            for b in (0, 1, n - 1, q, 2**64):
                check_compact(a, b, n)
