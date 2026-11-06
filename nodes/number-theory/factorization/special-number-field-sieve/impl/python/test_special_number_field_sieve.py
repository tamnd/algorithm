# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/special-number-field-sieve/. The authors are listed in prov/89BD3K.jsonl.

import math
import random

import pytest

from special_number_field_sieve import (
    algebraic_sqrt,
    dependencies,
    derivative,
    evaluate,
    factor_bases,
    factorize,
    find_relations,
    general_bound,
    homogeneous,
    inert_prime,
    integer_roots,
    is_inert,
    mulmod,
    product_in_order,
    relation_vector,
    select_polynomial,
    snfs,
    special_form,
    special_polynomial,
    value_size,
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
    # n = 2^41 - 1 = 13367 * 164511353 with f = x^3 - 2 and m = 2^14.
    n = 2**41 - 1
    f, m = special_polynomial(2, 41, -1, 3)
    assert (f, m) == ([-2, 0, 0, 1], 16384)
    assert evaluate(f, m) == 2 * n
    primes, pairs, chars = factor_bases(f, 200, 10)
    assert (len(primes), len(pairs), len(chars)) == (46, 40, 10)
    assert pairs[:6] == [(2, 0), (3, 2), (5, 3), (11, 7), (17, 8), (23, 16)]
    assert chars[:2] == [(223, 68), (223, 179)]
    assert inert_prime(f, 400) == 463
    rels = find_relations(n, f, m, primes, pairs, 108, 600, 1000)
    assert len(rels) == 108 and max(r[1] for r in rels) == 59
    assert [(r[0], r[1], r[2], r[4]) for r in rels[:3]] == [
        (-224, 1, -16608, -11239426), (-208, 1, -16592, -8998914), (-176, 1, -16560, -5451778)]
    index = {pr: k for k, pr in enumerate(pairs)}
    vectors = [relation_vector(r, primes, pairs, index, chars) for r in rels]
    deps = dependencies(vectors)
    assert len(deps) == 21
    fp = derivative(f)
    assert evaluate(fp, m) == 805306368
    outcomes = []
    for mask in deps:
        chosen = [r for k, r in enumerate(rels) if mask >> k & 1]
        v = math.isqrt(math.prod(r[2] for r in chosen))
        assert v * v == math.prod(r[2] for r in chosen)
        x = 805306368 * v % n
        gamma = product_in_order([[a, -b, 0] for a, b, *_ in chosen] + [fp, fp], f)
        delta = algebraic_sqrt(gamma, f, 463)
        assert delta is not None and mulmod(delta, delta, f) == gamma
        y = evaluate(delta, m, n)
        assert (x * x - y * y) % n == 0
        outcomes.append((len(chosen), math.gcd(x - y, n)))
    assert outcomes[1] == (52, 164511353)
    assert sum(1 < g < n for _, g in outcomes) == 8
    assert snfs(n, f, m, 200, 600, 10) == 164511353


def test_cole_m67() -> None:
    # Cole's 1903 factorization of 2^67 - 1, found again with x^3 - 4 and m = 2^23.
    n = 2**67 - 1
    f, m = special_polynomial(2, 67, -1, 3)
    assert (f, m) == ([-4, 0, 0, 1], 2**23) and evaluate(f, m) == 4 * n
    assert snfs(n, f, m) == 193707721
    general = select_polynomial(n, 3)
    assert value_size(f, m, 3 * general_bound(n)) < value_size(*general, 3 * general_bound(n))


def test_special_polynomial() -> None:
    rng = random.Random(4)
    for _ in range(500):
        r, e = rng.randrange(2, 13), rng.randrange(1, 200)
        s = rng.choice([-1, 1]) * rng.randrange(1, 13)
        d = rng.choice((3, 5))
        f, m = special_polynomial(r, e, s, d)
        t = d * (-(-e // d)) - e
        assert 0 <= t < d and f[1:] == [0] * (d - 1) + [1]
        assert evaluate(f, m) == r**t * (r**e + s)


def test_special_form() -> None:
    for r, e, s in ((2, 41, -1), (2, 64, 1), (10, 17, -1), (3, 41, -1), (6, 23, 1), (7, 30, 2)):
        form = special_form(r**e + s)
        assert form is not None
        a, b, c = form
        assert a**b + c == r**e + s and abs(c) <= 12
    assert special_form(1000003 * 1000033) is None
    assert special_form(12345) is None


def test_algebraic_factor() -> None:
    # 2^33 - 1 with d = 3 gives f = x^3 - 1 = (x - 1)(x^2 + x + 1).
    n = 2**33 - 1
    f, m = special_polynomial(2, 33, -1, 3)
    assert f == [-1, 0, 0, 1] and integer_roots(f) == [1]
    assert snfs(n, f, m) == 2**11 - 1
    assert integer_roots([-2, 0, 0, 1]) == [] and integer_roots([8, 0, 0, 1]) == [-2]
    assert sorted(integer_roots([-32, 0, 0, 0, 0, 1])) == [2]


def test_is_inert() -> None:
    for c in (2, 3, 4, 5, 10):
        for p in (2, 3, 5, 7, 11, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127):
            if c % p == 0:
                continue
            expected = p % 3 == 1 and pow(c, (p - 1) // 3, p) != 1
            assert is_inert([-c, 0, 0, 1], p) == expected
    # x^5 - 2 modulo 11: 11 = 1 mod 5 and 2 is not a fifth power modulo 11.
    assert is_inert([-2, 0, 0, 0, 0, 1], 11)
    assert not is_inert([-2, 0, 0, 0, 0, 1], 7)


def test_algebraic_sqrt() -> None:
    rng = random.Random(9)
    for c in (2, 3, 5, 6, 7):
        f = [-c, 0, 0, 1]
        p = inert_prime(f, 300)
        assert p % 4 == 3 and is_inert(f, p)
        for _ in range(10):
            delta = [rng.randrange(-10**8, 10**8) for _ in range(3)]
            gamma = mulmod(delta, delta, f)
            if all(x % p == 0 for x in gamma):
                continue
            r = algebraic_sqrt(gamma, f, p)
            assert r in (delta, [-x for x in delta])
            # alpha has norm c, which is not a square here.
            assert algebraic_sqrt(mulmod(gamma, [0, 1, 0], f), f, p) is None


def test_relations() -> None:
    n = 2**59 - 1
    f, m = special_polynomial(2, 59, -1, 3)
    primes, pairs, chars = factor_bases(f, 300, 10)
    rels = find_relations(n, f, m, primes, pairs, 60, 900, 300)
    assert len(rels) == 60
    for a, b, u, eu, v, ev in rels:
        assert math.gcd(a, b) == 1 and u == a - b * m and v == homogeneous(f, a, b)
        assert abs(u) == math.prod(p**e for p, e in zip(primes, eu))
        assert abs(v) == math.prod(p**e for p, e in zip(primes, ev))


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
    with pytest.raises(ValueError):
        snfs(2**41 - 3, [-2, 0, 0, 1], 2**14)
    for e in (37, 41, 43, 47):
        n = 2**e - 1
        f, m = special_polynomial(2, e, -1, 3)
        g = snfs(n, f, m)
        assert 1 < g < n and n % g == 0


def test_cunningham() -> None:
    assert check(2**59 - 1) == [179951, 3203431780337]
    assert check(2**64 + 1) == [274177, 67280421310721]
    assert check(10**17 - 1) == [3, 3, 2071723, 5363222357]
    assert check(3**41 - 1) == [2, 83, 2526913, 86950696619]
    assert check(2**63 - 1) == [7, 7, 73, 127, 337, 92737, 649657]
    assert check(2**66 - 1) == [3, 3, 7, 23, 67, 89, 683, 20857, 599479]
    assert check(6**23 + 1) == [7, 113958101, 990000731]


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
