# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-lehmer-test/. The authors are listed in prov/X19VXC.jsonl.

import random

import pytest

from lucas_lehmer_test import is_mersenne_number_prime, lucas_lehmer_residues, lucas_lehmer_test, reduce_mersenne

LIMIT = 100_000
# Exponents p of the Mersenne primes 2^p - 1 with p < 5000.
MERSENNE_EXPONENTS = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423]


def trial_division_is_prime(n: int) -> bool:
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


def strong_probable_prime(n: int, a: int) -> bool:
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


def is_prime_u64(n: int) -> bool:
    """Miller-Rabin with the first twelve prime bases, exact for n < 2^64."""
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if n < 2:
        return False
    for p in bases:
        if n % p == 0:
            return n == p
    return all(strong_probable_prime(n, a) for a in bases)


def test_example_p7_and_p11() -> None:
    assert lucas_lehmer_residues(7) == [4, 14, 67, 42, 111, 0]
    assert lucas_lehmer_residues(11)[-1] == 1736
    assert lucas_lehmer_test(7) is True and lucas_lehmer_test(11) is False
    assert 2047 == 23 * 89


def test_reduce_mersenne() -> None:
    rng = random.Random(1)
    for p in [2, 3, 5, 13, 31, 61, 89, 127, 521]:
        m = (1 << p) - 1
        for x in [0, 1, m - 1, m, m + 1, m * m, (m - 1) ** 2 + m - 2]:
            assert reduce_mersenne(x, p) == x % m
        for _ in range(200):
            x = rng.randrange(0, m * m * 4)
            assert reduce_mersenne(x, p) == x % m


def test_all_mersenne_numbers_up_to_limit_against_trial_division() -> None:
    n = 0
    p = 0
    while n <= LIMIT:
        assert is_mersenne_number_prime(n) == trial_division_is_prime(n), n
        p += 1
        n = (1 << p) - 1
    for m in range(LIMIT + 1):
        if (m + 1) & m:
            with pytest.raises(ValueError):
                is_mersenne_number_prime(m)


def test_all_exponents_up_to_64_against_miller_rabin() -> None:
    for p in range(2, 65):
        assert lucas_lehmer_test(p) == is_prime_u64((1 << p) - 1), p


def test_known_exponents_below_5000() -> None:
    found = [p for p in range(2, 5000) if trial_division_is_prime(p) and lucas_lehmer_test(p)]
    assert found == MERSENNE_EXPONENTS


def test_composite_exponents_give_false() -> None:
    for p in range(4, 400):
        if not trial_division_is_prime(p):
            assert lucas_lehmer_test(p) is False


def test_large_cases() -> None:
    assert lucas_lehmer_test(4423) is True  # 1332 decimal digits
    assert lucas_lehmer_test(1277) is False  # composite with no known factor
    assert lucas_lehmer_test(67) is False
    assert ((1 << 67) - 1) == 193707721 * 761838257287
    assert lucas_lehmer_test(4219) is False


def test_bad_input() -> None:
    for p in (-1, 0, 1):
        with pytest.raises(ValueError):
            lucas_lehmer_test(p)
