# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-strassen-primality-test/. The authors are listed in prov/XD7T81.jsonl.

import random
from fractions import Fraction
from math import gcd

from solovay_strassen_primality_test import is_euler_probable_prime, jacobi, solovay_strassen


def sieve(n: int) -> list[bool]:
    is_p = [False, False] + [True] * (n - 1)
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return is_p


IS_PRIME = sieve(10000)


def factor(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def phi(n: int) -> int:
    out = n
    for p in set(factor(n)):
        out = out // p * (p - 1)
    return out


def jacobi_by_factoring(a: int, n: int) -> int:
    """The product of Legendre symbols (a/p), each from Euler's criterion."""
    out = 1
    for p in factor(n):
        r = pow(a, (p - 1) // 2, p)
        out *= 0 if r == 0 else (1 if r == 1 else -1)
    return out


def strong_liar(n: int, a: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if pow(a, d, n) == 1:
        return True
    return any(pow(a, 2**j * d, n) == n - 1 for j in range(s))


def euler_liars(n: int) -> list[int]:
    return [a for a in range(1, n) if is_euler_probable_prime(n, a)]


def odd_composites(limit: int) -> list[int]:
    return [n for n in range(9, limit, 2) if not IS_PRIME[n]]


def test_jacobi_matches_factoring() -> None:
    for n in range(1, 400, 2):
        for a in range(0, n + 3):
            assert jacobi(a, n) == jacobi_by_factoring(a, n), (a, n)
    assert jacobi(1001, 9907) == jacobi_by_factoring(1001, 9907)


def test_primes_pass_every_base() -> None:
    for n in range(3, 2000, 2):
        if IS_PRIME[n]:
            assert all(is_euler_probable_prime(n, a) for a in range(1, n))


def test_small_inputs() -> None:
    rng = random.Random(0)
    assert [n for n in range(0, 30) if solovay_strassen(n, 5, rng)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_liars_match_brute_force() -> None:
    for n in odd_composites(600):
        brute = [
            a for a in range(1, n) if gcd(a, n) == 1 and pow(a, (n - 1) // 2, n) == jacobi_by_factoring(a, n) % n
        ]
        assert euler_liars(n) == brute


def test_half_bound() -> None:
    for n in odd_composites(1500):
        count = len(euler_liars(n))
        # Strictly below one half in this range; the bound is reached first at 1729.
        assert Fraction(count, phi(n)) < Fraction(1, 2)
        assert Fraction(count - 2, n - 3) <= Fraction(1, 2)
    for n in (1729, 2465):
        assert Fraction(len(euler_liars(n)), phi(n)) == Fraction(1, 2)


def test_liars_form_a_subgroup() -> None:
    for n in (45, 91, 561, 1105):
        liars = set(euler_liars(n))
        assert all(a * b % n in liars for a in liars for b in liars)
        assert phi(n) % len(liars) == 0


def test_strong_liars_are_euler_liars() -> None:
    for n in odd_composites(800):
        strong = {a for a in range(1, n) if strong_liar(n, a)}
        euler = set(euler_liars(n))
        assert strong <= euler
        if n % 4 == 3:
            assert strong == euler
    assert sorted(set(euler_liars(45)) - {a for a in range(1, 45) if strong_liar(45, a)}) == [19, 26]


def test_carmichael_numbers() -> None:
    expected = {561: 80, 1105: 192, 1729: 648, 2465: 896, 2821: 540, 6601: 1320, 8911: 1782}
    for n, count in expected.items():
        assert all(pow(a, n - 1, n) == 1 for a in range(1, n) if gcd(a, n) == 1)
        assert len(euler_liars(n)) == count
        assert 2 * count <= phi(n)


def test_example_values() -> None:
    assert jacobi(2, 561) == 1 and pow(2, 280, 561) == 1
    assert is_euler_probable_prime(561, 2)
    for a in (5, 7):
        assert jacobi(a, 561) == 1 and pow(a, 280, 561) == 67
        assert not is_euler_probable_prime(561, a)
    for a in (174, 47):
        assert jacobi(a, 221) == -1 and pow(a, 110, 221) == 220
        assert is_euler_probable_prime(221, a)
    assert jacobi(5, 97) == -1 and pow(5, 48, 97) == 96
    assert jacobi(2, 1729) == 1 and pow(2, 864, 1729) == 1
    assert jacobi(2, 1001) == 1 and pow(2, 500, 1001) == 529
    assert not is_euler_probable_prime(1001, 2)
    assert jacobi(3, 9) == 0 and not is_euler_probable_prime(9, 3)


def test_random_rounds() -> None:
    rng = random.Random(42)
    for n in range(2, 2000):
        assert solovay_strassen(n, 30, rng) == IS_PRIME[n]
    trials = 20000
    passed = sum(solovay_strassen(561, 1, rng) for _ in range(trials))
    assert abs(passed / trials - 78 / 558) < 0.015
