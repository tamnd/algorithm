# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dixon-random-squares/. The authors are listed in prov/11JRDA.jsonl.

import math
import random

import pytest

from dixon_random_squares import dependencies, dixon, exponents, factorize, primes_up_to

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
    n = 91363
    rng = random.Random(30)
    draws = [rng.randrange(1, n) for _ in range(145)]
    smooth = [(t + 1, z) for t, z in enumerate(draws) if exponents(z * z % n, [2, 3, 5, 7])]
    assert smooth == [(31, 32587), (124, 4287), (137, 65076), (143, 18166), (145, 51078)]
    assert all(math.gcd(z, n) == 1 for z in draws)
    assert [z * z % n for _, z in smooth] == [420, 14406, 28000, 400, 256]
    assert 32587 * 4287 * 65076 % n == 2**4 * 3 * 5**2 * 7**3 % n == 46148
    assert math.gcd(18166 - 20, n) == 211
    assert dixon(n, 7, 1, seed=30) == 211


def test_primes_and_exponents() -> None:
    assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert exponents(420, [2, 3, 5, 7]) == [2, 1, 1, 1]
    assert exponents(1, [2, 3]) == [0, 0]
    assert exponents(22, [2, 3, 5, 7]) is None


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
    rng = random.Random(1981)
    for _ in range(300):
        n = rng.randrange(3, 10**6)
        g = dixon(n, seed=rng.randrange(100))
        assert g == 1 or (1 < g < n and n % g == 0)
        if is_prime(n):
            assert g == 1


def test_dixon_splits_small() -> None:
    # Every odd composite n < 10^5 that is not a square and has no prime
    # factor below 100 is split with seed 0.
    for n in range(10201, 100001, 2):
        if any(n % p == 0 for p in range(3, 101, 2)) or is_prime(n):
            continue
        if math.isqrt(n) ** 2 == n:
            continue
        g = dixon(n)
        assert 1 < g < n and n % g == 0, n


def test_edges() -> None:
    for n in (0, 1, 2):
        with pytest.raises(ValueError):
            dixon(n)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**40) == [2] * 40
    assert factorize(101**2) == [101, 101]
    assert factorize(1009**2) == [1009, 1009]
    assert factorize(1009**3) == [1009] * 3
    assert factorize(10007**2) == [10007, 10007]
    assert factorize(1000003**2) == [1000003, 1000003]
    assert factorize(2**31 - 1) == [2**31 - 1]


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
    for bits in range(4, 17):
        for _ in range(2):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_close_primes() -> None:
    p = 10007
    for _ in range(6):
        q = p + 2
        while not is_prime(q):
            q += 2
        assert check(p * q) == [p, q]
        p = q


def test_random_smooth() -> None:
    rng = random.Random(2047)
    primes = [p for p in range(1009, 5000) if is_prime(p)]
    for k in range(1, 6):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
