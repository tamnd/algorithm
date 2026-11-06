# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-rho/. The authors are listed in prov/ZGK3CY.jsonl.

import math
import random

import pytest

from pollard_rho import factorize, pollard_rho

CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657,
              52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461,
              252601, 278545, 294409, 314821, 334153, 340561, 399001, 410041, 449065,
              488881, 512461, 3215031751, 2199733160881]


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
    assert pollard_rho(8051, 1, 2) == 97
    assert pollard_rho(1387, -1, 2) == 19
    assert factorize(8051) == [83, 97]


def test_divisor_always() -> None:
    rng = random.Random(1975)
    for _ in range(500):
        n = rng.randrange(2, 10**5)
        g = pollard_rho(n, rng.randrange(1, 50), rng.randrange(0, n))
        assert g > 1 and n % g == 0


def test_edges() -> None:
    for args in ((1,), (0,), (15, 1, 15), (15, 1, -1)):
        with pytest.raises(ValueError):
            pollard_rho(*args)
    with pytest.raises(ValueError):
        factorize(0)
    with pytest.raises(ValueError):
        factorize(-6)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(4) == [2, 2]
    assert factorize(9) == [3, 3]
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**64) == [2] * 64
    assert factorize(3**40) == [3] * 40
    assert factorize(1000003**2) == [1000003, 1000003]
    assert factorize(10007**4) == [10007] * 4
    assert factorize(2**64 + 1) == [274177, 67280421310721]


def test_all_small() -> None:
    for n in range(1, 100001):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(is_prime(p) for p in f)


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)


def test_random_semiprimes_grow() -> None:
    rng = random.Random(8051)
    for bits in range(4, 33, 2):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_close_primes() -> None:
    rng = random.Random(1387)
    for bits in range(8, 33, 4):
        p = random_prime(rng, bits)
        q = next_prime(p)
        assert check(p * q) == [p, q]


def test_unbalanced() -> None:
    rng = random.Random(97)
    for bits in range(8, 25, 4):
        p, q = random_prime(rng, bits), random_prime(rng, 80 - bits)
        assert check(p * q) == sorted([p, q])


def test_random_smooth() -> None:
    rng = random.Random(1981)
    primes = [p for p in range(2, 5000) if is_prime(p)]
    for k in range(1, 30):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
