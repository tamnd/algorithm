# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-p-minus-1/. The authors are listed in prov/8SP71V.jsonl.

import math
import random

import pytest

from pollard_p_minus_1 import factorize, pollard_p_minus_1, primes_up_to

CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657,
              52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461,
              252601, 278545, 294409, 314821, 334153, 340561, 399001, 410041, 449065,
              488881, 512461, 3215031751]


def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3 * 10^24, written here independently."""
    assert n < 3317044064679887385961981
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in small:
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


def random_prime(rng: random.Random, bits: int) -> int:
    while True:
        p = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p):
            return p


def smooth_prime(rng: random.Random, bits: int, b: int) -> int:
    """A random prime p of about the given size with p - 1 b-smooth."""
    small = primes_up_to(b)
    while True:
        m = 2
        while m.bit_length() < bits:
            m *= rng.choice(small)
        if is_prime(m + 1):
            return m + 1


def check(n: int) -> list[int]:
    f = factorize(n)
    assert math.prod(f) == n
    assert all(is_prime(p) for p in f)
    assert f == sorted(f)
    return f


def test_example() -> None:
    assert pollard_p_minus_1(1403, 5) == 61
    assert pollard_p_minus_1(299, 5) == 13
    assert factorize(1403) == [23, 61]


def test_failures() -> None:
    # 2047 = 23 * 89, and 2 has order 11 modulo both primes.
    assert pollard_p_minus_1(2047, 10) == 1
    assert pollard_p_minus_1(2047, 12) == 2047
    assert pollard_p_minus_1(2047, 8, 12) == 89
    assert factorize(2047) == [23, 89]


def test_gcd_divides() -> None:
    rng = random.Random(1974)
    for _ in range(300):
        n = rng.randrange(3, 10**6)
        b = rng.randrange(1, 60)
        g = pollard_p_minus_1(n, b, rng.randrange(2, n))
        assert n % g == 0


def test_edges() -> None:
    for args in ((2, 5), (15, 0), (15, 5, 1), (15, 5, 15)):
        with pytest.raises(ValueError):
            pollard_p_minus_1(*args)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**40) == [2] * 40
    assert factorize(101**2) == [101, 101]
    assert factorize(1000003**2) == [1000003, 1000003]
    assert factorize(10007**3) == [10007] * 3
    assert factorize(1000003 * 1000033) == [1000003, 1000033]


def test_all_small() -> None:
    for n in range(1, 100001):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(is_prime(p) for p in f)


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)


def test_random_semiprimes() -> None:
    rng = random.Random(1403)
    for bits in range(4, 19):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_smooth_p_minus_1_grow() -> None:
    rng = random.Random(299)
    for bits in range(16, 41, 4):
        p = smooth_prime(rng, bits, 500)
        q = random_prime(rng, bits)
        assert pollard_p_minus_1(p * q, 500) in (p, p * q)
        assert check(p * q) == sorted([p, q])


def test_random_smooth() -> None:
    rng = random.Random(2047)
    primes = primes_up_to(3000)
    for k in range(1, 25):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
