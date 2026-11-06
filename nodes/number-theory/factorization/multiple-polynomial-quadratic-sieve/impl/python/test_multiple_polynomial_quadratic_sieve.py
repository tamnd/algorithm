# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-polynomial-quadratic-sieve/. The authors are listed in prov/CEZR0P.jsonl.

import math
import random

import pytest

from multiple_polynomial_quadratic_sieve import (
    dependencies,
    exponents,
    factorize,
    montgomery_polynomial,
    mpqs,
    primes_up_to,
    sqrt_mod,
)

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


def test_example() -> None:
    n = 999983 * 1000037
    base = [-1, 2] + [p for p in primes_up_to(50)[1:] if pow(n % p, (p - 1) // 2, p) == 1]
    assert base == [-1, 2, 3, 5, 7, 13, 19, 29, 31, 37, 41, 43]
    assert math.isqrt(math.isqrt(2 * n) // 100) == 118
    qs = [q for q in range(119, 228) if is_prime(q) and pow(n % q, (q - 1) // 2, q) == 1]
    assert qs == [127, 131, 149, 151, 157, 163, 181, 199, 227]
    rows = [(151, -87, 128343750), (157, -54, 31072230), (163, -19, -28190370), (227, -7, -16909074)]
    x, total = 1, [0] * len(base)
    for q, t, v in rows:
        a, b, c = montgomery_polynomial(n, q)
        assert a == q * q and b * b - a * c == n and 0 < 2 * b <= a
        assert a * t * t + 2 * b * t + c == v
        assert (a * t + b) ** 2 - n == a * v
        total = [s + k for s, k in zip(total, exponents(v, base))]
        x = x * (a * t + b) * pow(q, -1, n) % n
    assert total == [2, 4, 8, 8, 2, 2, 0, 0, 2, 4, 2, 2]
    y = 1
    for p, k in zip(base[1:], total[1:]):
        y = y * p ** (k // 2) % n
    assert (x, y) == (48625850190, 717198484262)
    assert math.gcd(x - y, n) == 999983
    assert mpqs(n, 50, 100, 2) in (999983, 1000037)


def test_montgomery_polynomial() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(10**6, 10**18) | 1
        for q in range(3, 400, 2):
            if is_prime(q) and pow(n % q, (q - 1) // 2, q) == 1:
                a, b, c = montgomery_polynomial(n, q)
                assert a == q * q and b * b - a * c == n and 0 < 2 * b <= a
                break


def test_sqrt_mod() -> None:
    for p in primes_up_to(3000)[1:]:
        for a in range(0, p, max(1, p // 50)):
            if a == 0 or pow(a, (p - 1) // 2, p) == 1:
                r = sqrt_mod(a, p)
                assert r * r % p == a


def test_dependencies() -> None:
    rng = random.Random(7)
    for _ in range(200):
        rows = [rng.getrandbits(12) for _ in range(rng.randrange(1, 20))]
        found = dependencies(rows)
        for mask in found:
            acc = 0
            for j, v in enumerate(rows):
                if mask >> j & 1:
                    acc ^= v
            assert mask and acc == 0
        assert len(found) >= len(rows) - 12


def test_returns_divisor() -> None:
    rng = random.Random(1982)
    for _ in range(200):
        n = rng.randrange(10**4, 10**8) | 1
        if math.isqrt(n) ** 2 == n:
            continue
        g = mpqs(n)
        assert g == 1 or (1 < g < n and n % g == 0)
        if is_prime(n):
            assert g == 1


def test_sieve_splits_small() -> None:
    # Every odd composite n < 10^5 that is not a square and has no prime
    # factor below 100 is split on the first try.
    count = 0
    for n in range(10201, 100001, 2):
        if any(n % p == 0 for p in range(3, 101, 2)) or is_prime(n):
            continue
        if math.isqrt(n) ** 2 == n:
            continue
        count += 1
        g = mpqs(n)
        assert 1 < g < n and n % g == 0, n
    assert count > 2000


def test_edges() -> None:
    for n in (0, 1, 2, 4, 9, 10201):
        with pytest.raises(ValueError):
            mpqs(n)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**40) == [2] * 40
    assert factorize(101**2) == [101, 101]
    assert factorize(101**3) == [101] * 3
    assert factorize(10007**3) == [10007] * 3
    assert factorize(1000003**2) == [1000003, 1000003]


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
    for bits in range(4, 33):
        p, q = random_prime(rng, bits), random_prime(rng, bits)
        assert check(p * q) == sorted([p, q])


def test_close_primes() -> None:
    p = 1000003
    for _ in range(4):
        q = p + 2
        while not is_prime(q):
            q += 2
        assert check(p * q) == [p, q]
        p = q


def test_random_smooth() -> None:
    rng = random.Random(2047)
    primes = [p for p in range(101, 3000) if is_prime(p)]
    for k in range(1, 9):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
