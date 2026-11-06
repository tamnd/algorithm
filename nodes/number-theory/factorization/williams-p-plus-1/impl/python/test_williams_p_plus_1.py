# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/williams-p-plus-1/. The authors are listed in prov/XKCQGC.jsonl.

import math
import random

import pytest

from williams_p_plus_1 import factorize, lucas_v, primes_up_to, williams_p_plus_1

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


def plus_smooth_prime(rng: random.Random, bits: int, b: int) -> int:
    """A random prime p of about the given size with p + 1 = 2 * (distinct odd
    primes <= b), so every prime power in p + 1 is at most b."""
    small = primes_up_to(b)[1:]
    while True:
        m, used = 2, set()
        while m.bit_length() < bits:
            r = rng.choice(small)
            if r not in used:
                used.add(r)
                m *= r
        if is_prime(m - 1):
            return m - 1


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def check(n: int) -> list[int]:
    f = factorize(n)
    assert math.prod(f) == n
    assert all(is_prime(p) for p in f)
    assert f == sorted(f)
    return f


def test_lucas_v() -> None:
    for v in range(-3, 8):
        seq = [2, v]
        for _ in range(60):
            seq.append(v * seq[-1] - seq[-2])
        for m in range(1, 60):
            assert lucas_v(v, m, 1000003) == seq[m] % 1000003
    # The composition rule V_m(V_k(v)) = V_(mk)(v).
    assert lucas_v(lucas_v(6, 4, 5959), 15, 5959) == lucas_v(6, 60, 5959)


def test_example() -> None:
    assert lucas_v(6, 4, 5959) == 1154
    assert lucas_v(1154, 3, 5959) == 497
    assert lucas_v(497, 5, 5959) == 5607
    assert williams_p_plus_1(5959, 5, 6) == 59
    assert williams_p_plus_1(5959, 5, 3) == 1
    assert williams_p_plus_1(5959, 5, 5) == 101
    assert williams_p_plus_1(5959, 5, 9) == 5959
    assert math.gcd(pow(2, 60, 5959) - 1, 5959) == 1
    assert factorize(5959) == [59, 101]


def test_divisibility_theorem() -> None:
    rng = random.Random(1982)
    for _ in range(400):
        n = rng.randrange(3, 10**6)
        b = rng.randrange(1, 40)
        seed = rng.randrange(0, n)
        g = williams_p_plus_1(n, b, seed)
        assert n % g == 0
        m = 1
        for q in primes_up_to(b):
            qe = q
            while qe * q <= b:
                qe *= q
            m *= qe
        d = seed * seed - 4
        for p in primes_up_to(1000)[1:]:
            if n % p == 0 and d % p and m % (p - legendre(d, p)) == 0:
                assert g % p == 0


def test_edges() -> None:
    for args in ((2, 5, 0), (15, 0, 3), (15, 5, -1), (15, 5, 15)):
        with pytest.raises(ValueError):
            williams_p_plus_1(*args)
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


def test_smooth_p_plus_1_grow() -> None:
    rng = random.Random(299)
    for bits in range(16, 49, 4):
        p = plus_smooth_prime(rng, bits, 500)
        q = random_prime(rng, bits)
        hits = 0
        for seed in range(3, 23):
            g = williams_p_plus_1(p * q, 500, seed)
            assert g in (1, p, q, p * q)
            if legendre(seed * seed - 4, p) == -1:
                assert g % p == 0
                hits += g == p
        assert hits > 0
        if bits <= 32:
            assert check(p * q) == sorted([p, q])


def test_random_smooth() -> None:
    rng = random.Random(2047)
    primes = primes_up_to(3000)
    for k in range(1, 25):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert check(math.prod(f)) == f
