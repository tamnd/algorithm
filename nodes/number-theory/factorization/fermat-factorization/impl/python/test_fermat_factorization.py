# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-factorization/. The authors are listed in prov/GZCF2N.jsonl.

import math
import random

import pytest

from fermat_factorization import factorize, fermat_factorization

CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657,
              52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461,
              252601, 278545, 294409, 314821, 334153, 340561, 399001, 410041, 449065,
              488881, 512461]


def is_prime_td(n: int) -> bool:
    """Primality by trial division (used for small numbers)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


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


def next_prime(x: int) -> int:
    x += 1
    while not is_prime(x):
        x += 1
    return x


def check(n: int) -> list[int]:
    f = factorize(n)
    assert math.prod(f) == n
    assert all(is_prime(p) for p in f)
    assert f == sorted(f)
    return f


def test_example() -> None:
    assert fermat_factorization(5959) == (59, 101)
    assert fermat_factorization(8051) == (83, 97)
    assert factorize(5959) == [59, 101]


def test_split_is_closest_pair() -> None:
    for n in range(1, 4000, 2):
        a, b = fermat_factorization(n)
        assert a * b == n and a <= b
        assert a == max(d for d in range(1, math.isqrt(n) + 1) if n % d == 0)
        assert (a == 1) == (n == 1 or is_prime_td(n))


def test_edges() -> None:
    for bad in (0, -3, 2, 10):
        with pytest.raises(ValueError):
            fermat_factorization(bad)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert fermat_factorization(1) == (1, 1)
    assert fermat_factorization(9) == (3, 3)
    assert fermat_factorization(3 * 1009) == (3, 1009)
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**40) == [2] * 40
    assert factorize(3**30) == [3] * 30
    assert factorize(1000003**2) == [1000003, 1000003]
    assert factorize(101**5) == [101] * 5


def test_all_small() -> None:
    for n in range(1, 100001):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(is_prime(p) for p in f)


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)


def test_close_primes_grow() -> None:
    rng = random.Random(1643)
    for bits in range(8, 81, 4):
        p = random_prime(rng, bits)
        q = next_prime(p)
        assert fermat_factorization(p * q) == (p, q)
        assert check(p * q) == [p, q]


def test_random_semiprimes() -> None:
    rng = random.Random(2581)
    for bits in range(2, 17):
        for _ in range(4):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_random_smooth() -> None:
    rng = random.Random(8051)
    primes = [p for p in range(2, 200) if is_prime_td(p)]
    for k in range(1, 30):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
