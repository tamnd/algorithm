# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cipolla-algorithm/. The authors are listed in prov/W39G65.jsonl.

import random

import pytest

from cipolla_algorithm import cipolla_sqrt, power_mod


def is_probable_prime(n, rng):
    """Miller-Rabin with Python's pow, used only to build reference primes."""
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(30):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_square_reference(n, p):
    """Euler's criterion with Python's pow, used only as the reference."""
    n %= p
    return n == 0 or pow(n, (p - 1) // 2, p) == 1


SMALL_PRIMES = [p for p in range(3, 400) if all(p % q for q in range(2, int(p**0.5) + 1))]


def large_primes():
    rng = random.Random(10)
    primes = [10**9 + 7, 998244353, 2**61 - 1, 2**127 - 1, 2**255 - 19, 2**521 - 1, 2**607 - 1]
    for e in (40, 200, 500, 900):
        while True:  # a prime p = 1 + 2^e * odd, so p - 1 has a large power of two
            p = (rng.randrange(1, 2**64) | 1) * 2**e + 1
            if is_probable_prime(p, rng):
                primes.append(p)
                break
    while True:  # a random prime of several hundred decimal digits
        p = rng.randrange(10**300, 10**301) | 1
        if is_probable_prime(p, rng):
            primes.append(p)
            break
    return primes


LARGE_PRIMES = large_primes()


def test_wikipedia_example():
    class Fixed:
        def randrange(self, p):
            return 2

    assert cipolla_sqrt(10, 13, Fixed()) == 6
    assert cipolla_sqrt(10, 13, random.Random(0)) in (6, 7)


def test_power_mod():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randrange(1, 10**rng.randrange(1, 200))
        b, e = rng.randrange(-10**50, 10**50), rng.randrange(0, 10**30)
        assert power_mod(b, e, m) == pow(b, e, m)


def test_every_residue_small_primes():
    rng = random.Random(2)
    for p in SMALL_PRIMES:
        squares = {x * x % p for x in range(p)}
        for n in range(p):
            x = cipolla_sqrt(n, p, rng)
            if n in squares:
                assert x is not None and 0 <= x < p and x * x % p == n
            else:
                assert x is None


def test_edge_values():
    rng = random.Random(3)
    for p in SMALL_PRIMES + LARGE_PRIMES:
        assert cipolla_sqrt(0, p, rng) == 0
        assert cipolla_sqrt(p, p, rng) == 0
        assert cipolla_sqrt(7 * p, p, rng) == 0
        assert cipolla_sqrt(1, p, rng) in (1, p - 1)
        x = cipolla_sqrt(p - 1, p, rng)
        if p % 4 == 1:
            assert x * x % p == p - 1
        else:
            assert x is None


def test_random_large_primes():
    rng = random.Random(4)
    count = 0
    for p in LARGE_PRIMES:
        for _ in range(100 if p < 2**130 else 12):
            r = rng.randrange(p)
            n = r * r % p
            x = cipolla_sqrt(n, p, rng)
            assert x * x % p == n and x in (r, (p - r) % p)
            m = rng.randrange(p)
            x = cipolla_sqrt(m, p, rng)
            assert (x is not None) == is_square_reference(m, p)
            if x is not None:
                assert x * x % p == m % p
            count += 2
    for _ in range(500):
        p = rng.choice(SMALL_PRIMES[5:])
        n = rng.randrange(-10**300, 10**300)
        x = cipolla_sqrt(n, p, rng)
        assert (x is not None) == is_square_reference(n, p)
        count += 1
    assert count >= 1000


def test_modulus_two():
    assert cipolla_sqrt(0, 2) == 0
    assert cipolla_sqrt(1, 2) == 1
    assert cipolla_sqrt(10**300 + 1, 2) == 1


def test_bad_and_composite_moduli():
    for p in (-5, 0, 1):
        with pytest.raises(ValueError):
            cipolla_sqrt(1, p)
    rng = random.Random(5)
    composites = [4, 8, 16, 2**64, 9, 15, 21, 341, 561, 1105, 3**5, 10**300 + 1, 2**1000]
    for m in composites:
        for _ in range(30):
            n = rng.randrange(m)
            try:
                x = cipolla_sqrt(n, m, rng)
            except ValueError:
                continue
            assert x is None or x * x % m == n % m
