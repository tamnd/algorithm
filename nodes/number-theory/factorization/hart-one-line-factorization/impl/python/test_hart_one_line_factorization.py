# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hart-one-line-factorization/. The authors are listed in prov/D0TMW5.jsonl.

import math
import random

import pytest

from hart_one_line_factorization import factorize, hart_olf, iroot

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
    n = 200633
    assert n == 313 * 641
    rows = []
    for i in range(1, 9):
        s = math.isqrt(n * i)
        if s * s < n * i:
            s += 1
        rows.append((i, s, s * s - n * i))
    assert rows == [(1, 448, 71), (2, 634, 690), (3, 776, 277), (4, 896, 284),
                    (5, 1002, 839), (6, 1098, 1806), (7, 1186, 2165), (8, 1267, 225)]
    assert all(math.isqrt(m) ** 2 != m for _, _, m in rows[:7])
    assert 1267 * 1267 - 15 * 15 == 8 * n == 1252 * 1282
    assert math.gcd(n, 1267 - 15) == 313
    assert hart_olf(n) == 313


def test_hart_example() -> None:
    # The example of Hart, Section 2: found at i = 400 with multiplier 1.
    # p = nextprime(10^29 + 5342347) and q = nextprime(10^31 + 2232788).
    p = 100000000000000000000005342361
    q = 10000000000000000000000002232811
    assert pow(2, p - 1, p) == 1 and pow(3, q - 1, q) == 1
    assert hart_olf(p * q, 1, 400) == q
    assert hart_olf(p * q, 1, 399) == 1
    assert hart_olf(p * q, 480, 1000) in (p, q)


def test_returns_proper_factor() -> None:
    # Every square found in the allowed range gives a proper factor.
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(1000, 10**9)
        for mult in (1, 3, 480):
            g = hart_olf(n, mult, 200)
            assert g == 1 or (1 < g < n and n % g == 0)
    for p in (101, 10007, 1000003, 2**31 - 1):
        for mult in (1, 480):
            assert hart_olf(p, mult, 10**4) == 1


def test_squares_always_split() -> None:
    # Directly: for every square m in range, gcd(n, s - t) is proper (Lemma 2).
    for n in range(4, 3000):
        for i in range(1, 60):
            x = n * i
            s = math.isqrt(x)
            if s * s < x:
                s += 1
            if 2 * s - 1 >= n:
                break
            t = math.isqrt(s * s - x)
            if t * t == s * s - x:
                assert 1 < math.gcd(n, s - t) < n, (n, i)


def test_olf_splits_small() -> None:
    # Every composite n in [7, 30000), not a square, with no prime factor up to
    # n^(1/3). For n = 6 the range 2 sqrt(n i) + 1 <= n ends before a square.
    assert hart_olf(6) == 1
    count = 0
    for n in range(7, 30000):
        c = iroot(n, 3)
        if is_prime(n) or any(n % p == 0 for p in range(2, c + 1)):
            continue
        if math.isqrt(n) ** 2 == n:
            continue
        assert hart_olf(n) > 1, n
        count += 1
    assert count > 1000


def test_edges() -> None:
    for args in ((1,), (0,), (15, 0)):
        with pytest.raises(ValueError):
            hart_olf(*args)
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(4) == [2, 2]
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
    for bits in range(4, 25):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_unbalanced() -> None:
    rng = random.Random(99)
    for a, b in ((12, 20), (14, 24), (16, 22)):
        p, q = random_prime(rng, a), random_prime(rng, b)
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
