# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/general-number-field-sieve/. The authors are listed in prov/H28VR1.jsonl.

import math
import random

import pytest

from general_number_field_sieve import (
    algebraic_sqrt,
    balanced_base_m,
    base_m,
    dependencies,
    derivative,
    evaluate,
    factor_bases,
    factorize,
    find_relations,
    gnfs,
    homogeneous,
    inert_prime,
    is_inert,
    mulmod,
    product_in_order,
    relation_vector,
    select_polynomial,
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
    # Briggs's example: n = 45113 = 197 * 229 with m = 31.
    n = 45113
    f, m = base_m(n, 3, 31)
    assert (f, m) == ([8, 29, 15, 1], 31)
    primes, pairs, chars = factor_bases(f, 100, 10)
    assert (len(primes), len(pairs), len(chars)) == (25, 21, 10)
    assert pairs[:4] == [(2, 0), (7, 6), (17, 13), (23, 11)]
    assert chars[0] == (101, 87)
    assert inert_prime(f, 300) == 307
    rels = find_relations(n, f, m, primes, pairs, 68, 300, 500)
    assert len(rels) == 68 and max(r[1] for r in rels) == 9
    chosen = [(-116, 1), (-104, 1), (-32, 1), (-13, 1), (-4, 1), (1, 1), (142, 1), (-17, 3), (56, 3)]
    assert all((a, b) in [(r[0], r[1]) for r in rels] for a, b in chosen)
    u = math.prod(a - b * m for a, b in chosen)
    v = math.prod(homogeneous(f, a, b) for a, b in chosen)
    assert u == 161538300**2 and v == 3310622949437167616**2
    fp = derivative(f)
    gamma = product_in_order([[a, -b, 0] for a, b in chosen] + [fp, fp], f)
    assert gamma == [1383514992730880, 788159310461352, 222288412881565]
    delta = algebraic_sqrt(gamma, f, 307)
    assert delta == [-36380984, -8069491, -1426166]
    x = evaluate(fp, m) * 161538300 % n
    y = evaluate(delta, m, n)
    assert (x, y) == (6045, 9985)
    assert (x * x - y * y) % n == 0
    assert math.gcd(x - y, n) == 197
    assert gnfs(n, m=31, bound=100, width=300, chars=10) == 197


def test_polynomial_selection() -> None:
    assert select_polynomial(1040597897477, 3) == ([-966, 956, 122, 1], 10093)
    assert select_polynomial(1000003 * 1000033, 3) == ([-1061, -1539, 121, 1], 9960)
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(2**30, 2**80)
        for d in (3, 5):
            f, m = base_m(n, d)
            assert evaluate(f, m) == n and all(0 <= c < m for c in f[:-1])
            g = balanced_base_m(n, d, m)
            assert evaluate(g, m) == n and all(-m // 2 < c <= m // 2 for c in g[:-1])
        f, m = select_polynomial(n, 3)
        assert evaluate(f, m) == n and f[-1] == 1


def test_ring_arithmetic() -> None:
    rng = random.Random(11)
    for _ in range(200):
        d = rng.choice((3, 5))
        f = [rng.randrange(-50, 51) for _ in range(d)] + [1]
        u = [rng.randrange(-99, 100) for _ in range(d)]
        v = [rng.randrange(-99, 100) for _ in range(d)]
        w = mulmod(u, v, f)
        for t in range(-5, 6):
            # Evaluation at a root is a ring map, so test with f(t) as modulus.
            mod = abs(evaluate(f, t))
            if mod > 1:
                assert (evaluate(u, t) * evaluate(v, t) - evaluate(w, t)) % mod == 0


def brute_irreducible(f: list[int], p: int) -> bool:
    d = len(f) - 1
    for k in range(1, d // 2 + 1):
        for code in range(p**k):
            g = [(code // p**i) % p for i in range(k)] + [1]
            r = [c % p for c in f]
            for i in range(d, k - 1, -1):
                c = r[i]
                for j in range(k + 1):
                    r[i - k + j] = (r[i - k + j] - c * g[j]) % p
            if not any(r[:k]):
                return False
    return True


def test_is_inert() -> None:
    rng = random.Random(5)
    for _ in range(150):
        d = rng.choice((3, 5))
        p = rng.choice((2, 3, 5, 7))
        f = [rng.randrange(p) for _ in range(d)] + [1]
        assert is_inert(f, p) == brute_irreducible(f, p)


def test_algebraic_sqrt() -> None:
    rng = random.Random(9)
    for _ in range(60):
        f = [rng.randrange(-30, 31) for _ in range(3)] + [1]
        p = inert_prime(f, 300)
        if p == 0:
            continue
        delta = [rng.randrange(-10**6, 10**6) for _ in range(3)]
        gamma = mulmod(delta, delta, f)
        if all(c % p == 0 for c in gamma):
            continue
        r = algebraic_sqrt(gamma, f, p)
        assert r is not None and mulmod(r, r, f) == gamma
        assert r in (delta, [-c for c in delta])
        # A non-square gives None: multiply by alpha, whose norm -f(0) is
        # not a square for these f.
        if math.isqrt(abs(f[0])) ** 2 != abs(f[0]):
            assert algebraic_sqrt(mulmod(gamma, [0, 1, 0], f), f, p) is None


def test_relations() -> None:
    n = 1000003 * 1000033
    f, m = select_polynomial(n, 3)
    primes, pairs, chars = factor_bases(f, 400, 20)
    for p, r in pairs:
        assert evaluate(f, r, p) == 0
        for b in (1, 2, 5):
            assert homogeneous(f, b * r + p, b) % p == 0
    index = {pr: k for k, pr in enumerate(pairs)}
    rels = find_relations(n, f, m, primes, pairs, 150, 1200, 400)
    assert len(rels) == 150
    for rel in rels:
        a, b, u, eu, v, ev = rel
        assert math.gcd(a, b) == 1 and u == a - b * m and v == homogeneous(f, a, b)
        assert abs(u) == math.prod(p**e for p, e in zip(primes, eu))
        assert abs(v) == math.prod(p**e for p, e in zip(primes, ev))
        vec = relation_vector(rel, primes, pairs, index, chars)
        assert vec.bit_length() <= 2 + len(primes) + len(pairs) + len(chars)
    vectors = [relation_vector(r, primes, pairs, index, chars) for r in rels]
    for mask in dependencies(vectors)[:5]:
        chosen = [r for k, r in enumerate(rels) if mask >> k & 1]
        u = math.prod(r[2] for r in chosen)
        v = math.prod(r[4] for r in chosen)
        assert u > 0 and math.isqrt(u) ** 2 == u
        assert v > 0 and math.isqrt(v) ** 2 == v


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
    rng = random.Random(1990)
    wins = 0
    for _ in range(12):
        p, q = random_prime(rng, 13), random_prime(rng, 14)
        n = p * q
        g = gnfs(n)
        assert g in (1, p, q)
        wins += g > 1
    assert wins >= 10


def test_edges() -> None:
    with pytest.raises(ValueError):
        factorize(0)
    assert factorize(1) == []
    assert factorize(2) == [2]
    assert factorize(3) == [3]
    assert factorize(2**61 - 1) == [2**61 - 1]
    assert factorize(2**40) == [2] * 40
    assert factorize(1009**2) == [1009, 1009]
    assert factorize(1009**3) == [1009] * 3
    assert factorize(1000003**2) == [1000003, 1000003]
    assert factorize(10007**3) == [10007] * 3
    assert factorize(1009 * 1013) == [1009, 1013]
    assert factorize(1000003 * 1000033) == [1000003, 1000033]
    assert factorize(3 * 1000003 * 1000033) == [3, 1000003, 1000033]


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)
    assert factorize(3215031751) == [151, 751, 28351]


def test_close_primes() -> None:
    rng = random.Random(17)
    for bits in (16, 19, 22):
        p = random_prime(rng, bits)
        q = p + 2
        while not is_prime(q):
            q += 2
        assert check(p * q) == [p, q]


def test_random_semiprimes() -> None:
    rng = random.Random(2024)
    for bits in (11, 14, 17, 20, 22):
        for _ in range(2):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert check(p * q) == sorted((p, q))


def test_smooth_numbers() -> None:
    rng = random.Random(31)
    for size in (8, 16, 32, 64, 128):
        for _ in range(3):
            n = 1
            while n.bit_length() < size:
                n *= rng.choice((2, 3, 5, 7, 11, 13, 97, 997, 1009, 1013, 2003, 4001))
            check(n)


def test_all_small() -> None:
    for n in range(1, 100001):
        f = factorize(n)
        assert math.prod(f) == n
        assert all(is_prime(p) for p in f)
