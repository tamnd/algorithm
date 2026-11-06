# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve-of-eratosthenes/. The authors are listed in prov/F0W4PP.jsonl.

import random

from sieve_of_eratosthenes import prime_flags, sieve_of_eratosthenes


def is_prime_by_trial_division(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


LIMIT = 40000
ORACLE = [m for m in range(LIMIT + 1) if is_prime_by_trial_division(m)]


def oracle_primes(n: int) -> list[int]:
    return [p for p in ORACLE if p <= n]


def test_example() -> None:
    assert sieve_of_eratosthenes(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert len(sieve_of_eratosthenes(100)) == 25


def test_edges() -> None:
    assert sieve_of_eratosthenes(-5) == []
    assert sieve_of_eratosthenes(0) == []
    assert sieve_of_eratosthenes(1) == []
    assert sieve_of_eratosthenes(2) == [2]
    assert sieve_of_eratosthenes(3) == [2, 3]
    assert sieve_of_eratosthenes(4) == [2, 3]
    # n is a prime, a square of a prime, or one less than one
    for n in (7, 8, 9, 24, 25, 26, 48, 49, 50, 120, 121, 122, 168, 169, 170):
        assert sieve_of_eratosthenes(n) == oracle_primes(n)


def test_every_n_up_to_2000() -> None:
    for n in range(2001):
        assert sieve_of_eratosthenes(n) == oracle_primes(n)


def test_random_larger_n() -> None:
    rng = random.Random(4127)
    for _ in range(20):
        n = rng.randint(2001, LIMIT)
        assert sieve_of_eratosthenes(n) == oracle_primes(n)


def test_known_counts() -> None:
    assert len(sieve_of_eratosthenes(10**4)) == 1229
    assert len(sieve_of_eratosthenes(10**6)) == 78498


def test_flags() -> None:
    for n in (-1, 0, 1, 2, 30, 1000):
        table = prime_flags(n)
        assert len(table) == max(n + 1, 0)
        for m in range(len(table)):
            assert table[m] == int(is_prime_by_trial_division(m))
