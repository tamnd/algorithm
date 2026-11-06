# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lehman-factorization/. The authors are listed in prov/DT65XZ.jsonl.

import math
import random

import pytest

from lehman_factorization import factorize, icbrt, lehman_factorization

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
    assert lehman_factorization(2581) == 89
    assert factorize(2581) == [29, 89]


def test_icbrt() -> None:
    for x in range(0, 3000):
        c = icbrt(x)
        assert c**3 <= x < (c + 1) ** 3
    for e in range(1, 200, 7):
        x = 3**e
        c = icbrt(x)
        assert c**3 <= x < (c + 1) ** 3


def test_split_or_prime() -> None:
    for n in range(22, 30000):
        d = lehman_factorization(n)
        if is_prime(n):
            assert d == n
        else:
            assert 1 < d < n and n % d == 0


def test_edges() -> None:
    for bad in (-1, 0, 1, 21):
        with pytest.raises(ValueError):
            lehman_factorization(bad)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(4) == [2, 2]
    assert factorize(21) == [3, 7]
    assert lehman_factorization(23) == 23
    assert lehman_factorization(25) == 5
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**50) == [2] * 50
    assert factorize(1000003**2) == [1000003] * 2
    assert factorize(10007**3) == [10007] * 3


def test_all_small() -> None:
    for n in range(1, 100001):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(is_prime(p) for p in f)


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)


def test_random_semiprimes_grow() -> None:
    rng = random.Random(1974)
    for bits in range(4, 21):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_unbalanced_and_close() -> None:
    rng = random.Random(637)
    for bits in range(10, 17, 2):
        p, q = random_prime(rng, bits), random_prime(rng, 2 * bits)
        assert check(p * q) == sorted([p, q])
        p = random_prime(rng, 2 * bits)
        q = p + 2
        while not is_prime(q):
            q += 2
        assert check(p * q) == [p, q]


def test_random_smooth() -> None:
    rng = random.Random(1643)
    primes = [p for p in range(2, 2000) if is_prime(p)]
    for k in range(1, 25):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
