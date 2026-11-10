# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ams-sketch/. The authors are listed in prov/ATY7TN.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations, product

import pytest

from ams_sketch import GF64, AMSSketch, FourWiseSign, gf_mul

GF8 = (3, 0b1011)  # GF(2^3) with x^3 + x + 1


def poly_mulmod(a: int, b: int, m: int) -> int:
    """Product of GF(2)[x] polynomials a and b modulo m (bit masks)."""
    deg = m.bit_length() - 1
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a >> deg & 1:
            a ^= m
    return r


def poly_gcd(a: int, b: int) -> int:
    while b:
        while a and a.bit_length() >= b.bit_length():
            a ^= b << (a.bit_length() - b.bit_length())
        a, b = b, a
    return a


def test_field_polynomial_is_irreducible() -> None:
    # Rabin: f of degree 64 is irreducible iff x^(2^64) = x mod f and gcd(x^(2^32) - x, f) = 1.
    bits, f = GF64
    v = 0b10
    powers = {}
    for k in range(1, bits + 1):
        v = poly_mulmod(v, v, f)
        powers[k] = v
    assert powers[bits] == 0b10
    assert poly_gcd(f, powers[bits // 2] ^ 0b10) == 1


def test_fast_sign_matches_horner() -> None:
    rng = random.Random(7)
    for _ in range(20):
        s = FourWiseSign.random(rng)
        for _ in range(20):
            x = rng.getrandbits(64)
            assert s(x) == s.direct(x)
    for coeffs in product(range(8), repeat=4):
        s = FourWiseSign(coeffs, GF8)
        assert all(s(x) == s.direct(x) for x in range(8))


def gf8_family() -> list[FourWiseSign]:
    return [FourWiseSign(c, GF8) for c in product(range(8), repeat=4)]


def test_gf8_signs_are_four_wise_independent_exactly() -> None:
    fam = gf8_family()
    table = [[s(x) for x in range(8)] for s in fam]
    for quad in combinations(range(8), 4):
        joint = Counter(tuple(row[x] for x in quad) for row in table)
        assert len(joint) == 16 and set(joint.values()) == {len(fam) // 16}
    # The field multiplication is associative and distributive on GF(8).
    for a, b, c in product(range(8), repeat=3):
        assert gf_mul(gf_mul(a, b, GF8), c, GF8) == gf_mul(a, gf_mul(b, c, GF8), GF8)
        assert gf_mul(a, b ^ c, GF8) == gf_mul(a, b, GF8) ^ gf_mul(a, c, GF8)


def test_unbiased_and_exact_variance_over_all_sign_functions() -> None:
    fam = gf8_family()
    table = [[s(x) for x in range(8)] for s in fam]
    rng = random.Random(11)
    vectors = [[3, 0, 0, 0, 0, 0, 0, 0], [1] * 8, [2, -1, 0, 4, 0, 0, -3, 1]]
    vectors += [[rng.randrange(-5, 6) for _ in range(8)] for _ in range(4)]
    for f in vectors:
        f2 = sum(v * v for v in f)
        zs = [sum(row[x] * f[x] for x in range(8)) for row in table]
        mean = Fraction(sum(z * z for z in zs), len(zs))
        var = Fraction(sum(z**4 for z in zs), len(zs)) - mean * mean
        assert mean == f2
        cross = sum(f[i] ** 2 * f[j] ** 2 for i, j in combinations(range(8), 2))
        assert var == 4 * cross
        assert var <= 2 * f2 * f2


def test_linear_merge_and_turnstile() -> None:
    rng = random.Random(3)
    base = AMSSketch(4, 3, rng)
    a, b, ab = base.empty_like(), base.empty_like(), base.empty_like()
    s1 = [(rng.randrange(1000), rng.randrange(-3, 5)) for _ in range(100)]
    s2 = [(rng.randrange(1000), rng.randrange(-3, 5)) for _ in range(100)]
    for x, c in s1:
        a.update(x, c)
        ab.update(x, c)
    for x, c in s2:
        b.update(x, c)
        ab.update(x, c)
    assert a.merge(b).z == ab.z
    assert ab.subtract(b).z == a.z
    for x, c in s1:
        a.update(x, -c)
    assert all(v == 0 for row in a.z for v in row)
    with pytest.raises(ValueError):
        a.merge(AMSSketch(4, 3, random.Random(4)))


def stream_counts(rng: random.Random, n: int, total: int) -> Counter:
    weights = [1 / (i + 1) for i in range(n)]
    return Counter(rng.choices(range(n), weights=weights, k=total))


def test_group_failure_at_most_one_third() -> None:
    eps = 0.7
    t = math.ceil(6 / eps**2)
    trials = 200
    fails = 0
    for seed in range(trials):
        rng = random.Random(seed)
        f = stream_counts(rng, 40, 400)
        sk = AMSSketch(t, 1, rng)
        for x, c in f.items():
            # Spread the labels over the field; an odd multiplier is a bijection mod 2^64.
            sk.update(x * 0x9E3779B97F4A7C15 % (1 << 64), c)
        f2 = sum(v * v for v in f.values())
        fails += abs(sk.estimate() - f2) > eps * f2
    assert fails / trials <= 1 / 3 + 3 * math.sqrt((1 / 3) * (2 / 3) / trials)


def test_median_failure_at_most_delta() -> None:
    eps, delta = 0.8, 0.1
    trials = 20
    fails = 0
    for seed in range(trials):
        rng = random.Random(10_000 + seed)
        f = stream_counts(rng, 30, 300)
        sk = AMSSketch.from_error(eps, delta, rng)
        assert (sk.t, sk.r) == (10, 42)
        for x, c in f.items():
            sk.update(x, c)
        f2 = sum(v * v for v in f.values())
        fails += abs(sk.estimate() - f2) > eps * f2
    assert fails / trials <= delta + 3 * math.sqrt(delta * (1 - delta) / trials)
