# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proth-test/. The authors are listed in prov/ACSTC1.jsonl.

import math
import random

import pytest

from proth_test import is_proth_number, jacobi, proth_split, proth_test

LIMIT = 100_000


def is_prime_td(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def jacobi_slow(a: int, n: int) -> int:
    """Product of Legendre symbols by Euler's criterion, for odd n."""
    out, m, p = 1, n, 3
    while m > 1:
        if p * p > m:
            p = m
        while m % p == 0:
            out *= 0 if a % p == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
            m //= p
        p += 2
    return out


def strong_probable(n: int, a: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def probably_prime(n: int) -> bool:
    return all(strong_probable(n, a) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41) if a % n)


def test_examples() -> None:
    assert proth_split(97) == (3, 5) and jacobi(2, 97) == 1 and jacobi(3, 97) == 1 and jacobi(5, 97) == -1
    assert pow(5, 48, 97) == 96 and proth_test(97) == (True, {"base": 5})
    assert proth_split(65) == (1, 6) and jacobi(2, 65) == 1 and jacobi(3, 65) == -1
    assert pow(3, 32, 65) == 61 and proth_test(65) == (False, {"base": 3, "residue": 61})
    assert proth_test(13) == (True, {"base": 2}) and pow(2, 6, 13) == 12
    assert proth_test(25) == (False, {"square_root": 5})
    assert proth_test(1729) == (False, {"factor": 7})  # a Carmichael number


def test_rejects_non_proth_numbers() -> None:
    for n in (-5, 0, 1, 2, 4, 7, 11, 19, 23, 37, 561, 2047, 10**6):
        assert not is_proth_number(n)
        with pytest.raises(ValueError):
            proth_test(n)


def test_jacobi_against_euler() -> None:
    for n in range(1, 400, 2):
        for a in range(-5, 2 * n):
            assert jacobi(a, n) == jacobi_slow(a % n, n), (a, n)


def test_all_proth_numbers_up_to_limit() -> None:
    count = primes = 0
    for n in range(LIMIT + 1):
        k, m = proth_split(n) if n >= 3 and n % 2 else (0, 0)
        assert is_proth_number(n) == (n >= 3 and n % 2 == 1 and k < 2**m)
        if not is_proth_number(n):
            continue
        count += 1
        verdict, ev = proth_test(n)
        assert verdict == is_prime_td(n), n
        primes += verdict
        if verdict:
            a = ev["base"]
            assert jacobi(a, n) == -1 and pow(a, (n - 1) // 2, n) == n - 1
        elif "factor" in ev:
            assert 1 < ev["factor"] < n and n % ev["factor"] == 0
    assert (count, primes) == (450, 99)


def test_fermat_numbers() -> None:
    for j in range(0, 13):
        f = 2 ** (2**j) + 1
        assert proth_test(f)[0] == (j <= 4), j
    # Pepin: for j >= 1 the base 3 has (3/F_j) = -1; check that our search finds a valid base.
    for j in range(1, 13):
        f = 2 ** (2**j) + 1
        assert jacobi(3, f) == -1


def test_three_times_power_of_two() -> None:
    expected = [2, 5, 6, 8, 12, 18, 30, 36, 41, 66, 189, 201, 209, 276, 353, 408, 438, 534]
    found = [m for m in range(2, 700) if proth_test(3 * 2**m + 1)[0]]
    assert found == expected
    for m in range(2, 700):
        assert proth_test(3 * 2**m + 1)[0] == probably_prime(3 * 2**m + 1)


def test_random_large_proth_numbers() -> None:
    rng = random.Random(1)
    checked = primes = 0
    while checked < 400:
        m = rng.randrange(300, 1100)
        k = rng.randrange(1, 2**20) | 1
        n = k * 2**m + 1
        verdict, ev = proth_test(n)
        assert verdict == probably_prime(n)
        if not verdict and "residue" in ev:
            assert ev["residue"] != n - 1 and jacobi(ev["base"], n) == -1
        checked += 1
        primes += verdict
    assert primes > 0


def test_proth_squares() -> None:
    """(2^a + 1)^2 - 1 = 2^(a+1) (2^(a-1) + 1), so these squares are Proth numbers."""
    for a in (2, 4, 8, 16, 100, 534, 1000):
        n = (2**a + 1) ** 2
        assert is_proth_number(n)
        assert proth_test(n) == (False, {"square_root": 2**a + 1})
    for n in (25, 289, 66049, 4295098369):
        assert is_proth_number(n) and proth_test(n)[0] is False
