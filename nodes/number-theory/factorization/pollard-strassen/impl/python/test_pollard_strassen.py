# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-strassen/. The authors are listed in prov/CC5JPW.jsonl.

import math
import random

import pytest

from pollard_strassen import (
    SMALL,
    factorize,
    least_prime_factor,
    multipoint_eval,
    poly_mul,
    poly_rem,
    product_tree,
    rising_product,
    series_inverse,
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



def naive_mul(a, b, n):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return [c % n for c in out]


def test_poly_mul_both_paths():
    rng = random.Random(1)
    for la, lb in [(1, 1), (3, 70), (SMALL, SMALL + 1), (SMALL + 1, SMALL + 1), (90, 130)]:
        n = rng.randrange(2, 10**15)
        a = [rng.randrange(n) for _ in range(la)]
        b = [rng.randrange(n) for _ in range(lb)]
        assert poly_mul(a, b, n) == naive_mul(a, b, n)
    assert poly_mul([], [1], 7) == []


def test_series_inverse_and_rem():
    rng = random.Random(2)
    n = 10**12 + 39
    g = [1] + [rng.randrange(n) for _ in range(80)]
    h = series_inverse(g, 100, n)
    assert naive_mul(g, h, n)[:100] == [1] + [0] * 99
    for d, la in [(1, 5), (5, 40), (30, 31), (30, 100), (60, 200)]:
        g = [rng.randrange(n) for _ in range(d)] + [1]
        a = [rng.randrange(n) for _ in range(la)]
        r = poly_rem(a, g, n)
        assert len(r) == d
        # a - r must be a multiple of g: divide it by schoolbook long division.
        t = [(x - (r[i] if i < d else 0)) % n for i, x in enumerate(a)]
        for i in range(len(t) - 1, d - 1, -1):
            c = t[i]
            for j in range(d + 1):
                t[i - d + j] = (t[i - d + j] - c * g[j]) % n
        assert all(x == 0 for x in t)


def test_multipoint_eval_both_paths():
    rng = random.Random(3)
    n = 1000000007
    for k, deg in [(1, 0), (5, 5), (SMALL, 40), (SMALL + 1, 30), (100, 150)]:
        f = [rng.randrange(n) for _ in range(deg + 1)]
        pts = [rng.randrange(n) for _ in range(k)]
        want = [sum(c * pow(a, i, n) for i, c in enumerate(f)) % n for a in pts]
        assert multipoint_eval(f, pts, n) == want


def test_rising_product():
    n = 10**9 + 7
    for b in (1, 2, 7, SMALL, SMALL + 1, 60):
        f = rising_product(b, n)
        assert f == product_tree([[i, 1] for i in range(1, b + 1)], n)[-1][0]
        assert f[-1] == 1 and f[0] == math.factorial(b) % n
        assert f[-2] == b * (b + 1) // 2 % n


def test_example():
    n, b = 200633, 22
    f = rising_product(b, n)
    assert len(f) == 23 and f[0] == 119722 and f[21] == 253
    v = multipoint_eval(f, [j * b for j in range(b)], n)
    assert v[:4] == [119722, 88821, 83241, 173552]
    assert v[13] == 128367 and v[14] == 53210 == 313 * 170
    for j in range(b):
        assert v[j] == math.prod(range(j * b + 1, j * b + b + 1)) % n
    assert [j for j in range(b) if math.gcd(v[j], n) > 1] == [14]
    assert least_prime_factor(n) == 313
    assert check(n) == [313, 641]


def test_gcd_equal_to_n():
    # 17 and 19 lie in the same block (15, 20], so the gcd is 323 itself.
    n = 323
    v = multipoint_eval(rising_product(5, n), [0, 5, 10, 15, 20], n)
    assert v[3] == 0 and math.gcd(v[3], n) == n
    assert least_prime_factor(n) == 17


def test_edges():
    with pytest.raises(ValueError):
        factorize(0)
    with pytest.raises(ValueError):
        least_prime_factor(1)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert least_prime_factor(2) == 2 and least_prime_factor(3) == 3
    assert least_prime_factor(4) == 2


def test_all_small():
    limit = 10**5
    lpf = list(range(limit + 1))
    for p in range(2, math.isqrt(limit) + 1):
        if lpf[p] == p:
            for m in range(p * p, limit + 1, p):
                if lpf[m] == m:
                    lpf[m] = p
    for n in range(1, limit + 1):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(lpf[p] == p for p in f)
        assert f == sorted(f)
    for n in range(2, 3000):
        assert least_prime_factor(n) == lpf[n]


def test_primes_powers_squares():
    for p in (101, 65537, 1000003, 999999937):
        assert least_prime_factor(p) == p
        assert check(p) == [p]
    for p, e in ((2, 40), (3, 25), (7, 14), (101, 6), (65537, 2)):
        assert check(p**e) == [p] * e
    for p in (1009, 30011, 999983):
        assert check(p * p) == [p, p]


def test_carmichael():
    for n in CARMICHAEL:
        f = check(n)
        assert len(f) >= 3


def test_random_semiprimes():
    rng = random.Random(4)
    for bits in (4, 6, 8, 10, 12, 14, 16, 18, 20):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted([p, q])
            assert least_prime_factor(p * q) == min(p, q)


def test_unbalanced_and_close():
    assert check(3 * 1000003) == [3, 1000003]
    assert check(1000003 * 1000033) == [1000003, 1000033]
    assert check(999983 * 1000003) == [999983, 1000003]
    assert check(65521 * 65537) == [65521, 65537]


def test_random_smooth():
    rng = random.Random(5)
    small = [p for p in range(2, 200) if is_prime(p)]
    for size in (10, 20, 30, 40):
        for _ in range(3):
            n, want = 1, []
            while n.bit_length() < size:
                p = rng.choice(small)
                n *= p
                want.append(p)
            assert check(n) == sorted(want)
