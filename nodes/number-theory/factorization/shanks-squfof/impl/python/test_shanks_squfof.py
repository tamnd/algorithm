# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shanks-squfof/. The authors are listed in prov/QBJ183.jsonl.

import math
import random

import pytest

from shanks_squfof import MULTIPLIERS, factorize, squfof

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


def check(n: int) -> list[int]:
    f = factorize(n)
    assert math.prod(f) == n
    assert all(is_prime(p) for p in f)
    assert f == sorted(f)
    return f


def small_primes(b: int) -> list[int]:
    return [p for p in range(2, b + 1) if is_prime(p)]


def test_examples() -> None:
    assert squfof(11111) == 41
    assert squfof(13231) == 101
    assert factorize(11111) == [41, 271]
    assert factorize(13231) == [101, 131]


def test_returns_divisor() -> None:
    rng = random.Random(1975)
    for _ in range(2000):
        n = rng.randrange(3, 10**7) | 1
        if math.isqrt(n) ** 2 == n:
            continue
        for k in (1, 3, 5, 7, 11):
            if math.isqrt(k * n) ** 2 == k * n:
                continue
            g = squfof(n, k)
            assert g == 1 or (1 < g < n and n % g == 0)
            if is_prime(n):
                assert g == 1


def test_squfof_all_small() -> None:
    # Every odd composite non-square n < 30000 is split by some multiplier.
    for n in range(9, 30001, 2):
        if is_prime(n) or math.isqrt(n) ** 2 == n:
            continue
        for k in MULTIPLIERS:
            if math.gcd(k, n) > 1 or math.isqrt(k * n) ** 2 == k * n:
                continue
            g = squfof(n, k)
            if g > 1:
                assert n % g == 0 and g < n
                break
        else:
            raise AssertionError(n)


def test_edges() -> None:
    for args in ((2,), (1,), (10,), (9,), (15, 0), (7, 7)):
        with pytest.raises(ValueError):
            squfof(*args)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**40) == [2] * 40
    assert factorize(101**2) == [101, 101]
    assert factorize(101**3) == [101] * 3
    assert factorize(1000003**2) == [1000003, 1000003]
    assert factorize(10007**3) == [10007] * 3
    assert factorize(1000003 * 1000033) == [1000003, 1000033]


def test_all_small() -> None:
    for n in range(1, 100001):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(is_prime(p) for p in f)


def test_carmichael() -> None:
    for n in CARMICHAEL + [2199733160881]:
        check(n)


def test_random_semiprimes() -> None:
    rng = random.Random(1403)
    for bits in range(4, 27):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_close_primes() -> None:
    p = 1000003
    for _ in range(10):
        q = p + 2
        while not is_prime(q):
            q += 2
        assert check(p * q) == [p, q]
        p = q


def test_products_of_large_primes() -> None:
    rng = random.Random(1155)
    for k in range(1, 5):
        f = sorted(random_prime(rng, 17) for _ in range(k))
        assert check(math.prod(f)) == f


def test_random_smooth() -> None:
    rng = random.Random(2047)
    primes = small_primes(3000)
    for k in range(1, 25):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
