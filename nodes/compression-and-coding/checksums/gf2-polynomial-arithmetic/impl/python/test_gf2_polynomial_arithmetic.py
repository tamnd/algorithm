# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gf2-polynomial-arithmetic/. The authors are listed in prov/DX1XMN.jsonl.

import random

from gf2_polynomial_arithmetic import (
    add, deg, divmod2, gcd, is_irreducible, is_irreducible_brute, is_primitive,
    mod, mul, mulmod, necklace_count, order_of_x, powmod, to_str,
)

RNG = random.Random(20261111)


def test_examples() -> None:
    assert add(0b1011, 0b0110) == 0b1101
    assert mul(0b1011, 0b101) == 0b100111  # (x^3+x+1)(x^2+1) = x^5+x^2+x+1
    assert divmod2(0b11100110, 0b1011) == (0b11001, 0b101)
    assert to_str(0b100111) == "x^5 + x^2 + x + 1"
    # FIPS 197, Section 4.2: {57} * {83} = {c1} modulo x^8+x^4+x^3+x+1.
    assert mulmod(0x57, 0x83, 0x11B) == 0xC1


def test_ring_laws_random() -> None:
    for _ in range(300):
        a, b, c = (RNG.getrandbits(RNG.randrange(1, 40)) for _ in range(3))
        assert mul(a, b) == mul(b, a)
        assert mul(a, add(b, c)) == add(mul(a, b), mul(a, c))
        assert mul(mul(a, b), c) == mul(a, mul(b, c))
        if b:
            q, r = divmod2(a, b)
            assert add(mul(q, b), r) == a and deg(r) < deg(b)


def test_mul_against_integer_definition() -> None:
    # The coefficient of x^k in a*b is the parity of the pairs i + j = k.
    for _ in range(200):
        a, b = RNG.getrandbits(12), RNG.getrandbits(12)
        want = 0
        for k in range(24):
            s = sum(((a >> i) & 1) & ((b >> (k - i)) & 1) for i in range(k + 1))
            want |= (s & 1) << k
        assert mul(a, b) == want


def test_gcd_divides_and_bezout_free_check() -> None:
    for _ in range(200):
        g = RNG.getrandbits(6) | 1
        a = mul(g, RNG.getrandbits(10) | 1)
        b = mul(g, RNG.getrandbits(10) | 1)
        d = gcd(a, b)
        assert mod(a, d) == 0 and mod(b, d) == 0 and mod(d, g) == 0


def test_powmod_against_repeated_multiplication() -> None:
    for _ in range(100):
        m = RNG.getrandbits(12) | (1 << 12)
        a = RNG.getrandbits(12)
        e = RNG.randrange(60)
        r = 1
        for _ in range(e):
            r = mulmod(r, a, m)
        assert powmod(a, e, m) == mod(r, m)


def test_irreducible_counts_match_necklace_formula() -> None:
    # Known counts of irreducible binary polynomials of degree 1 to 10.
    known = [2, 1, 2, 3, 6, 9, 18, 30, 56, 99]
    for d in range(1, 11):
        polys = range(1 << d, 1 << (d + 1))
        rabin = sum(1 for f in polys if is_irreducible(f))
        assert rabin == necklace_count(d) == known[d - 1]
        if d <= 9:
            brute = sum(1 for f in polys if is_irreducible_brute(f))
            assert brute == rabin


def test_rabin_agrees_with_brute_force() -> None:
    for f in range(2, 1 << 11):
        assert is_irreducible(f) == is_irreducible_brute(f)


def test_primitive() -> None:
    assert is_primitive(0b1011) and order_of_x(0b1011) == 7
    assert is_irreducible(0b11111) and not is_primitive(0b11111)
    assert order_of_x(0b11111) == 5
    assert is_irreducible(0x11B) and order_of_x(0x11B) == 51
    # The number of primitive polynomials of degree d is phi(2^d - 1) / d.
    phi = {2: 2, 3: 6, 4: 8, 5: 30, 6: 36, 7: 126, 8: 128}
    for d, p in phi.items():
        cnt = sum(1 for f in range(1 << d, 1 << (d + 1)) if is_primitive(f))
        assert cnt == p // d
