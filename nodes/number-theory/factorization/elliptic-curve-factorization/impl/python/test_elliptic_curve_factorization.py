# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elliptic-curve-factorization/. The authors are listed in prov/FMGN8V.jsonl.

import math
import random

from elliptic_curve_factorization import Found, add, ecm, factorize, iroot, multiply, primes_up_to

import pytest

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




def brute_count(a: int, b: int, p: int) -> int:
    """The number of points of y^2 = x^3 + a x + b over F_p, O included."""
    squares = [0] * p
    for y in range(p):
        squares[y * y % p] += 1
    return 1 + sum(squares[(x * x * x + a * x + b) % p] for x in range(p))


def test_example() -> None:
    p, q = 1129, 2029
    n = p * q
    assert n == 2290741
    x, y, a = 2, 3, 1
    b = (y * y - x**3 - a * x) % n
    assert b == n - 1 and math.gcd(4 * a**3 + 27 * b * b, n) == 1
    assert brute_count(a, b % p, p) == 1120 and brute_count(a, b % q, q) == 2083
    pt = (x, y)
    for r in (2, 2, 2, 2, 3, 3, 5):
        pt = multiply(pt, r, a, n)
    assert pt == (1115156, 449422)
    two = add(pt, pt, a, n)
    three = add(two, pt, a, n)
    six = add(three, three, a, n)
    assert six == (2200125, 2229695)
    assert (pt[0] - six[0]) % n == 1205772 and math.gcd(1205772, n) == p
    with pytest.raises(Found) as e:
        add(six, pt, a, n)
    assert e.value.g == p
    # Over F_p the point P has order 560 = 2^4 5 7; over F_q it has the prime order 2083.
    mod_p = (x, y)
    for _ in range(558):
        mod_p = add(mod_p, (x, y), a, p)
        assert mod_p is not None
    assert add(mod_p, (x, y), a, p) is None
    assert multiply((x, y), 2083, a, q) is None


def test_group_law_mod_prime() -> None:
    rng = random.Random(7)
    for p in (101, 307, 1009):
        for _ in range(5):
            a, x, y = rng.randrange(p), rng.randrange(p), rng.randrange(p)
            b = (y * y - x**3 - a * x) % p
            if (4 * a**3 + 27 * b * b) % p == 0:
                continue
            order = brute_count(a, b, p)
            assert abs(order - (p + 1)) <= 2 * math.isqrt(p) + 1
            assert multiply((x, y), order, a, p) is None
            u = multiply((x, y), 5, a, p)
            v = multiply((x, y), 7, a, p)
            w = multiply((x, y), 11, a, p)
            assert add(add(u, v, a, p), w, a, p) == add(u, add(v, w, a, p), a, p)
            assert add(u, v, a, p) == multiply((x, y), 12, a, p)


def test_returns_divisor() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randrange(10**6, 10**9) | 1
        if n % 3 == 0:
            continue
        g = ecm(n, 50, 500, 3, seed=rng.randrange(1000))
        assert g == 1 or (1 < g < n and n % g == 0)
    for p in (1000003, 2**31 - 1, 2**61 - 1):
        assert ecm(p, 200, 2000, 5) == 1


def test_ecm_splits_small() -> None:
    # Every composite n < 40000 with no prime factor below 100 and not a perfect power.
    count = 0
    for n in range(10201, 40001, 2):
        if any(n % p == 0 for p in range(3, 101, 2)) or is_prime(n):
            continue
        if math.isqrt(n) ** 2 == n:
            continue
        g = ecm(n, 30, 300, 40, seed=n)
        assert 1 < g < n and n % g == 0, n
        count += 1
    assert count > 400


def test_edges() -> None:
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
    assert factorize(10007**3 * 10009) == [10007] * 3 + [10009]
    assert factorize(2**67 - 1) == [193707721, 761838257287]
    assert iroot(10**30, 3) == 10**10 and iroot(10**30 - 1, 3) == 10**10 - 1


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
    for bits in range(4, 31):
        for _ in range(2):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])


def test_small_factor_of_large_number() -> None:
    rng = random.Random(77)
    for bits in (16, 20, 24):
        p = random_prime(rng, bits)
        big = random_prime(rng, 80)
        assert check(p * big) == sorted([p, big])


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
    assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
