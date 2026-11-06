# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve-of-atkin/. The authors are listed in prov/GPR00G.jsonl.

import random

from sieve_of_atkin import sieve_of_atkin


def is_prime_by_trial_division(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


def is_squarefree(m: int) -> bool:
    d = 2
    while d * d <= m:
        if m % (d * d) == 0:
            return False
        d += 1
    return True


LIMIT = 100000
PRIME = [is_prime_by_trial_division(m) for m in range(LIMIT + 1)]
PRIMES = [m for m in range(LIMIT + 1) if PRIME[m]]


def oracle(n: int) -> list[int]:
    return [p for p in PRIMES if p <= n]


def test_edges() -> None:
    for n in (-5, 0, 1):
        assert sieve_of_atkin(n) == []
    assert sieve_of_atkin(2) == [2]
    assert sieve_of_atkin(3) == [2, 3]
    assert sieve_of_atkin(4) == [2, 3]
    assert sieve_of_atkin(5) == [2, 3, 5]


def test_every_n_up_to_2000() -> None:
    for n in range(2001):
        assert sieve_of_atkin(n) == oracle(n)


def test_squares_of_primes_and_neighbours() -> None:
    for q in (5, 7, 11, 13, 17, 31, 97, 211, 307, 313):
        for n in (q * q - 1, q * q, q * q + 1, q, q + 1):
            assert sieve_of_atkin(n) == oracle(n)


def test_random_and_large() -> None:
    rng = random.Random(2004)
    for _ in range(10):
        n = rng.randint(2001, 30000)
        assert sieve_of_atkin(n) == oracle(n)
    assert sieve_of_atkin(LIMIT) == PRIMES


def test_parity_theorems() -> None:
    # Atkin and Bernstein, Theorems 6.1 to 6.3, for squarefree n coprime to 6 up to 20000.
    top = 20000
    count = [0] * (top + 1)
    for x in range(1, 100):
        for y in range(1, 150):
            a = 4 * x * x + y * y
            if a <= top and a % 12 in (1, 5):
                count[a] += 1
            b = 3 * x * x + y * y
            if b <= top and b % 12 == 7:
                count[b] += 1
            c = 3 * x * x - y * y
            if x > y and c <= top and c % 12 == 11:
                count[c] += 1
    for m in range(1, top + 1):
        if m % 2 and m % 3 and is_squarefree(m):
            assert (count[m] % 2 == 1) == PRIME[m]


def test_example() -> None:
    assert sieve_of_atkin(50) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert len(sieve_of_atkin(10**5)) == 9592
