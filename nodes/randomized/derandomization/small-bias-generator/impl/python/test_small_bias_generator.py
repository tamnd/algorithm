# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-bias-generator/. The authors are listed in prov/4KEFV4.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from small_bias_generator import (
    field_degree_for,
    gf_mul,
    irreducible_polynomial,
    powering_bits,
    small_bias_generator,
)


def space(n: int, m: int) -> list[list[int]]:
    return [small_bias_generator(seed, n, m) for seed in range(1 << (2 * m))]


def max_bias(points: list[list[int]]) -> Fraction:
    n = len(points[0])
    worst = Fraction(0)
    for size in range(1, n + 1):
        for s in combinations(range(n), size):
            ones = sum(sum(p[i] for i in s) & 1 for p in points)
            bias = abs(Fraction(len(points) - 2 * ones, len(points)))
            worst = max(worst, bias)
    return worst


def test_irreducible_polynomials() -> None:
    assert irreducible_polynomial(1) == 0b11
    assert irreducible_polynomial(2) == 0b111
    assert irreducible_polynomial(3) == 0b1011
    assert irreducible_polynomial(4) == 0b10011
    assert irreducible_polynomial(8) == 0b100011011


def test_field_axioms_small() -> None:
    for m in (1, 2, 3, 4, 5):
        q = 1 << m
        for a in range(1, q):
            assert sum(1 for b in range(1, q) if gf_mul(a, b, m) == 1) == 1
        rng = random.Random(m)
        for _ in range(200):
            a, b, c = rng.randrange(q), rng.randrange(q), rng.randrange(q)
            assert gf_mul(a, b, m) == gf_mul(b, a, m)
            assert gf_mul(a, gf_mul(b, c, m), m) == gf_mul(gf_mul(a, b, m), c, m)
            assert gf_mul(a, b ^ c, m) == gf_mul(a, b, m) ^ gf_mul(a, c, m)


def test_example_of_page() -> None:
    # m = 3, modulus x^3 + x + 1, x = 2 (the element "x"), y = 3.
    assert powering_bits(2, 3, 7, 3) == [1, 1, 0, 0, 1, 0, 1]
    assert small_bias_generator((2 << 3) | 3, 7, 3) == [1, 1, 0, 0, 1, 0, 1]


def test_bias_bound_exact() -> None:
    for m in (2, 3, 4):
        for n in range(1, 9):
            bound = Fraction(n - 1, 1 << m)
            assert max_bias(space(n, m)) <= bound


def test_bound_is_attained() -> None:
    # The parity of bits 0 and 7 is <1 + x^7, y>, and x^7 = 1 for each x != 0 in GF(8).
    pts = space(8, 3)
    ones = sum((p[0] + p[7]) & 1 for p in pts)
    assert Fraction(len(pts) - 2 * ones, len(pts)) == Fraction(7, 8)


def test_seed_length() -> None:
    assert field_degree_for(1, 0.5) == 1
    assert field_degree_for(8, 1 / 8) == 6
    assert field_degree_for(1000, 0.01) == 17
    for n, eps in ((10, 0.3), (100, 0.05), (5000, 0.001)):
        m = field_degree_for(n, eps)
        assert (n - 1) <= eps * (1 << m)
        assert m == 1 or (n - 1) > eps * (1 << (m - 1))


def test_large_field_statistics() -> None:
    # Fixed seed. With m = 12 and n = 40 the bias bound is 39/4096 < 0.01.
    # For a fixed parity, 4000 random seeds give a mean within 0.06 of the
    # true bias, except with probability below 2 exp(-2 * 4000 * 0.06^2) < 1e-12.
    rng = random.Random(2024)
    m, n = 12, 40
    sets = [rng.sample(range(n), rng.randint(1, n)) for _ in range(5)]
    for s in sets:
        total = 0
        for _ in range(4000):
            bits = small_bias_generator(rng.randrange(1 << (2 * m)), n, m)
            total += 1 - 2 * (sum(bits[i] for i in s) & 1)
        assert abs(total / 4000) < 0.01 + 0.06


def test_bad_arguments() -> None:
    for call in (lambda: powering_bits(8, 0, 3, 3), lambda: small_bias_generator(64, 3, 3), lambda: field_degree_for(0, 0.1)):
        try:
            call()
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
