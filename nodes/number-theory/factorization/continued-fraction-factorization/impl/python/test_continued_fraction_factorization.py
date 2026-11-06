# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/continued-fraction-factorization/. The authors are listed in prov/ZB7C0A.jsonl.

import math
import random

import pytest

from continued_fraction_factorization import (
    MULTIPLIERS,
    cfrac,
    dependencies,
    exponents,
    factor_base,
    factorize,
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
    n = 9073
    base = factor_base(n, 20)
    assert base == [-1, 2, 3, 7, 11, 13]
    assert exponents(-48, base) == [1, 4, 1, 0, 0, 0]
    assert exponents(139, base) is None
    assert (95 * 2619) % n == 3834
    assert math.gcd(3834 - 36, n) == 211
    assert cfrac(n, 1, 20) in (43, 211)
    assert factorize(n) == [43, 211]


def test_convergent_identity() -> None:
    # A_(i-1)^2 - D B_(i-1)^2 = (-1)^i Q_i for the first 200 steps.
    for d in (9073, 11111, 87463, 10**12 + 39):
        a0 = math.isqrt(d)
        p, q_prev, q = a0, 1, d - a0 * a0
        a_prev, a, b_prev, b_cur = 1, a0, 0, 1
        for i in range(1, 200):
            assert a * a - d * b_cur * b_cur == (-1) ** i * q
            assert 0 < q < 2 * math.isqrt(d) + 2
            b = (a0 + p) // q
            p_new = b * q - p
            q_prev, q = q, q_prev + b * (p - p_new)
            p = p_new
            a_prev, a = a, b * a + a_prev
            b_prev, b_cur = b_cur, b * b_cur + b_prev


def test_dependencies() -> None:
    rng = random.Random(7)
    for _ in range(200):
        rows = [rng.getrandbits(12) for _ in range(rng.randrange(1, 20))]
        for mask in dependencies(rows):
            acc = 0
            for j, v in enumerate(rows):
                if mask >> j & 1:
                    acc ^= v
            assert mask and acc == 0
        assert len(dependencies(rows)) >= len(rows) - 12


def test_returns_divisor() -> None:
    rng = random.Random(1975)
    for _ in range(300):
        n = rng.randrange(10**4, 10**8) | 1
        if math.isqrt(n) ** 2 == n:
            continue
        g = cfrac(n)
        assert g == 1 or (1 < g < n and n % g == 0)
        if is_prime(n):
            assert g == 1


def test_edges() -> None:
    for args in ((2,), (1,), (9,), (15, 0), (7, 7)):
        with pytest.raises(ValueError):
            cfrac(*args)
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


def test_multipliers_cover_small() -> None:
    # Every odd n < 30000 with two prime factors above 100 is split by some k.
    for n in range(10201, 30001, 2):
        if any(n % p == 0 for p in range(3, 101, 2)) or is_prime(n):
            continue
        if math.isqrt(n) ** 2 == n:
            continue
        for k in MULTIPLIERS:
            if math.gcd(k, n) > 1 or math.isqrt(k * n) ** 2 == k * n:
                continue
            g = cfrac(n, k)
            if g > 1:
                assert n % g == 0 and g < n
                break
        else:
            raise AssertionError(n)


def test_carmichael() -> None:
    for n in CARMICHAEL + [2199733160881]:
        check(n)


def test_random_semiprimes() -> None:
    rng = random.Random(1403)
    for bits in range(4, 31):
        for _ in range(2):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_close_primes() -> None:
    p = 1000003
    for _ in range(6):
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
