# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve-of-sundaram/. The authors are listed in prov/KQBYRB.jsonl.

import random

from sieve_of_sundaram import sieve_of_sundaram


def is_prime_by_trial_division(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


LIMIT = 30000
ORACLE = [m for m in range(LIMIT + 1) if is_prime_by_trial_division(m)]


def oracle_primes(n: int) -> list[int]:
    return [p for p in ORACLE if p <= n]


def test_example() -> None:
    assert sieve_of_sundaram(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_edges() -> None:
    assert sieve_of_sundaram(-3) == []
    assert sieve_of_sundaram(0) == []
    assert sieve_of_sundaram(1) == []
    assert sieve_of_sundaram(2) == [2]
    assert sieve_of_sundaram(3) == [2, 3]
    # even n with n + 1 prime: the bound k = (n - 1) // 2 must not reach n + 1
    for n in (4, 6, 10, 12, 16, 18, 22, 28, 30, 100):
        assert sieve_of_sundaram(n) == oracle_primes(n)
    # n equal to a square of a prime
    for n in (9, 25, 49, 121, 169, 289, 361, 529, 841, 961):
        assert sieve_of_sundaram(n) == oracle_primes(n)


def test_every_n_up_to_2000() -> None:
    for n in range(2001):
        assert sieve_of_sundaram(n) == oracle_primes(n)


def test_random_larger_n() -> None:
    rng = random.Random(1934)
    for _ in range(15):
        n = rng.randint(2001, LIMIT)
        assert sieve_of_sundaram(n) == oracle_primes(n)
