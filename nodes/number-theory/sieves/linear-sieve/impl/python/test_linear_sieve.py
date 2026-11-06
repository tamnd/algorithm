# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-sieve/. The authors are listed in prov/0C3CNA.jsonl.

import random

from linear_sieve import factorize, linear_sieve


def least_prime_factor_by_trial_division(m: int) -> int:
    d = 2
    while d * d <= m:
        if m % d == 0:
            return d
        d += 1
    return m


def factor_by_trial_division(m: int) -> list[tuple[int, int]]:
    out, d = [], 2
    while d * d <= m:
        e = 0
        while m % d == 0:
            m //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1
    if m > 1:
        out.append((m, 1))
    return out


LIMIT = 40000
ORACLE_LP = [0, 0] + [least_prime_factor_by_trial_division(m) for m in range(2, LIMIT + 1)]


def check(n: int) -> None:
    lp, primes = linear_sieve(n)
    assert lp == ORACLE_LP[: n + 1]
    assert primes == [m for m in range(2, n + 1) if ORACLE_LP[m] == m]


def test_example() -> None:
    lp, primes = linear_sieve(20)
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19]
    assert lp[2:] == [2, 3, 2, 5, 2, 7, 2, 3, 2, 11, 2, 13, 2, 3, 2, 17, 2, 19, 2]


def test_edges() -> None:
    assert linear_sieve(0) == ([0], [])
    assert linear_sieve(1) == ([0, 0], [])
    assert linear_sieve(2) == ([0, 0, 2], [2])
    for n in (3, 4, 8, 9, 10, 24, 25, 26, 48, 49, 120, 121, 168, 169, 289):
        check(n)


def test_every_n_up_to_2000() -> None:
    for n in range(2001):
        check(n)


def test_random_larger_n() -> None:
    rng = random.Random(1978)
    for _ in range(10):
        check(rng.randint(2001, LIMIT))


def test_each_composite_written_once() -> None:
    n = 5000
    lp, primes = linear_sieve(n)
    writes = 0
    for i in range(2, n + 1):
        for p in primes:
            if p > lp[i] or p * i > n:
                break
            writes += 1
    assert writes == n - 1 - len(primes)


def test_factorize() -> None:
    lp, _ = linear_sieve(LIMIT)
    assert factorize(360, lp) == [(2, 3), (3, 2), (5, 1)]
    assert factorize(1, lp) == []
    rng = random.Random(87)
    for m in [2, 3, 4, 39601, 39989, LIMIT] + [rng.randint(2, LIMIT) for _ in range(500)]:
        assert factorize(m, lp) == factor_by_trial_division(m)
