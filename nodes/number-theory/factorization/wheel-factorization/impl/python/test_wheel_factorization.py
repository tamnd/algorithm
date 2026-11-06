# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wheel-factorization/. The authors are listed in prov/SXCYK3.jsonl.

import math
import random

import pytest

from wheel_factorization import wheel, wheel_factorization

BASES = [(), (2,), (2, 3), (2, 3, 5), (2, 3, 5, 7), (2, 3, 5, 7, 11)]
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


def check(n: int, basis: tuple[int, ...] = (2, 3, 5)) -> list[int]:
    f = wheel_factorization(n, basis)
    assert math.prod(f) == n
    assert all(is_prime(p) for p in f)
    assert f == sorted(f)
    return f


def spf_table(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for i in range(2, math.isqrt(limit) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def test_wheels() -> None:
    assert wheel(()) == (2, [1])
    assert wheel((2,)) == (3, [2])
    assert wheel((2, 3)) == (5, [2, 4])
    assert wheel((2, 3, 5)) == (7, [4, 2, 4, 2, 4, 6, 2, 6])
    s, gaps = wheel((2, 3, 5, 7))
    assert s == 11 and len(gaps) == 48 and sum(gaps) == 210


def test_example() -> None:
    assert wheel_factorization(8633) == [89, 97]
    assert wheel_factorization(9100) == [2, 2, 5, 5, 7, 13]


def test_edges() -> None:
    with pytest.raises(ValueError):
        wheel_factorization(0)
    with pytest.raises(ValueError):
        wheel_factorization(-5)
    for basis in BASES:
        assert wheel_factorization(1, basis) == []
        for p in (2, 3, 5, 7, 11, 13, 49, 121, 169):
            assert math.prod(check(p, basis)) == p
        assert check(2**40, basis) == [2] * 40
        assert check(7**12, basis) == [7] * 12
        assert check(100003**2, basis) == [100003] * 2
        assert check(99991 * 100003, basis) == [99991, 100003]
        assert check(2**31 - 1, basis) == [2**31 - 1]


def test_all_small() -> None:
    limit = 100000
    spf = spf_table(limit)
    for n in range(1, limit + 1):
        f = wheel_factorization(n)
        expect = []
        m = n
        while m > 1:
            expect.append(spf[m])
            m //= spf[m]
        assert f == expect


def test_all_bases_small() -> None:
    for basis in BASES:
        for n in range(1, 2001):
            f = wheel_factorization(n, basis)
            assert math.prod(f) == n and all(is_prime(p) for p in f)


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)


def test_random_semiprimes() -> None:
    rng = random.Random(30)
    for bits in range(2, 19):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q, (2, 3, 5, 7)) == sorted([p, q])


def test_random_smooth() -> None:
    rng = random.Random(210)
    primes = [p for p in range(2, 3000) if is_prime(p)]
    for k in range(1, 30):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
