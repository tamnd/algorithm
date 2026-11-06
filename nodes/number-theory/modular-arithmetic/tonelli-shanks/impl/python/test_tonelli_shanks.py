# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tonelli-shanks/. The authors are listed in prov/5CEZWX.jsonl.

import random

import pytest

from tonelli_shanks import mod_pow, sqrt_mod_prime, tonelli_shanks


def is_probable_prime(n: int) -> bool:
    """Miller-Rabin with fixed and random bases, using pow as a reference (test helper only)."""
    if n < 2:
        return False
    for small in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % small == 0:
            return n == small
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    rng = random.Random(n)
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] + [rng.randrange(2, n - 1) for _ in range(8)]
    for b in bases:
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


SMALL_PRIMES = [p for p in range(3, 400) if all(p % d for d in range(2, p))]


def check(a: int, p: int) -> None:
    x = tonelli_shanks(a, p)
    is_residue = a % p == 0 or pow(a, (p - 1) // 2, p) == 1
    if is_residue:
        assert x is not None and 0 <= x < p
        assert (x * x - a) % p == 0
    else:
        assert x is None


def test_examples() -> None:
    assert tonelli_shanks(5, 41) == 28
    assert tonelli_shanks(2, 113) == 62
    assert tonelli_shanks(10, 13) == 7
    assert sqrt_mod_prime(5, 41) == 13
    assert tonelli_shanks(3, 41) is None
    assert tonelli_shanks(0, 41) == 0
    assert tonelli_shanks(41, 41) == 0


def test_mod_pow() -> None:
    rng = random.Random(1)
    for _ in range(500):
        m = rng.randrange(1, 10**12)
        b = rng.randrange(-(10**15), 10**15)
        e = rng.randrange(0, 10**12)
        assert mod_pow(b, e, m) == pow(b, e, m)
    assert mod_pow(0, 0, 7) == 1
    assert mod_pow(5, 0, 1) == 0


def test_rejects_bad_modulus() -> None:
    for p in [-7, 0, 1, 2, 4, 1024]:
        with pytest.raises(ValueError):
            tonelli_shanks(1, p)


def test_exhaustive_small_primes() -> None:
    for p in SMALL_PRIMES:
        squares = {x * x % p for x in range(p)}
        for a in range(-p, 2 * p):
            x = tonelli_shanks(a, p)
            if a % p in squares:
                assert x is not None and (x * x - a) % p == 0
            else:
                assert x is None
        assert len(squares) == (p + 1) // 2


def test_random_word_sized() -> None:
    rng = random.Random(2025)
    primes = []
    while len(primes) < 60:
        n = rng.randrange(3, 2**64) | 1
        if is_probable_prime(n):
            primes.append(n)
    for _ in range(3000):
        p = rng.choice(primes)
        a = rng.choice([0, 1, p - 1, rng.randrange(p), rng.randrange(p) ** 2])
        check(a, p)


def test_large_two_adic_valuation() -> None:
    rng = random.Random(77)
    primes = [
        65537,  # 2^16 + 1
        998244353,  # 119 * 2^23 + 1
        3221225473,  # 3 * 2^30 + 1
        2**224 - 2**96 + 1,  # the NIST P-224 prime, s = 96
        2**255 - 19,  # s = 2
        2**127 - 1,  # s = 1
        2**521 - 1,  # s = 1
    ]
    k = 1
    while not is_probable_prime(k * 2**200 + 1):
        k += 2
    primes.append(k * 2**200 + 1)
    for p in primes:
        for _ in range(40):
            y = rng.randrange(p)
            check(y * y % p, p)
            check(rng.randrange(p), p)
        check(p - 1, p)
        check(1, p)


def test_large_random_primes() -> None:
    rng = random.Random(9)
    count = 0
    while count < 30:
        digits = rng.randrange(20, 310)
        p = rng.randrange(10 ** (digits - 1), 10**digits) | 1
        if not is_probable_prime(p):
            continue
        count += 1
        for _ in range(10):
            y = rng.randrange(p)
            check(y * y % p, p)
            check(rng.randrange(p), p)


def test_root_pair() -> None:
    rng = random.Random(3)
    for _ in range(500):
        p = rng.choice(SMALL_PRIMES)
        y = rng.randrange(1, p)
        r = sqrt_mod_prime(y * y, p)
        assert r is not None and r <= p - r
        assert r in (y, p - y)
