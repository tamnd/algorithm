# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bch-code/. The authors are listed in prov/RQPH9G.jsonl.

import random

from bch_code import (bch_generator, cyclotomic_coset, encode_systematic, gf2_mod, minimal_polynomial,
                      min_distance)
from gf import GF2m

F16 = GF2m(4, 0b10011)  # alpha is a root of x^4 + x + 1
F32 = GF2m(5, 0b100101)  # alpha is a root of x^5 + x^2 + 1


def test_cosets_and_minimal_polynomials_n15() -> None:
    assert cyclotomic_coset(1, 15) == [1, 2, 4, 8]
    assert cyclotomic_coset(3, 15) == [3, 6, 12, 9]
    assert cyclotomic_coset(5, 15) == [5, 10]
    assert minimal_polynomial(F16, 1, 15, 1) == 0b10011  # x^4 + x + 1
    assert minimal_polynomial(F16, 1, 15, 3) == 0b11111  # x^4 + x^3 + x^2 + x + 1
    assert minimal_polynomial(F16, 1, 15, 5) == 0b111  # x^2 + x + 1
    assert minimal_polynomial(F16, 1, 15, 7) == 0b11001  # x^4 + x^3 + 1


def test_known_generators_n15() -> None:
    # Lin and Costello, Error Control Coding, 2nd ed., Appendix C (octal, highest power left):
    # (15, 11) t = 1: 23; (15, 7) t = 2: 721; (15, 5) t = 3: 2467.
    assert bch_generator(F16, 3)[0] == 0o23
    assert bch_generator(F16, 5)[0] == 0o721  # x^8 + x^7 + x^6 + x^4 + 1
    assert bch_generator(F16, 7)[0] == 0o2467  # x^10 + x^8 + x^5 + x^4 + x^2 + x + 1
    assert 0o721 == 0b111010001
    assert 0o2467 == 0b10100110111


def test_known_generators_n31() -> None:
    # Lin and Costello, Appendix C, n = 31, alpha a root of x^5 + x^2 + 1 (octal 45)
    table = {3: (26, 0o45), 5: (21, 0o3551), 7: (16, 0o107657), 11: (11, 0o5423325), 15: (6, 0o313365047)}
    for delta, (k, g_oct) in table.items():
        g, _ = bch_generator(F32, delta)
        assert g == g_oct
        assert 31 - (g.bit_length() - 1) == k


def test_generator_divides_xn_minus_1() -> None:
    for field in (F16, F32):
        n = field.n
        for delta in range(2, n + 1):
            g, _ = bch_generator(field, delta)
            assert gf2_mod((1 << n) | 1, g) == 0


def test_bch_bound_and_actual_distance_n15() -> None:
    expected = {3: (11, 3), 5: (7, 5), 6: (5, 7), 7: (5, 7)}
    for delta, (k, d) in expected.items():
        g, _ = bch_generator(F16, delta)
        assert 15 - (g.bit_length() - 1) == k
        assert min_distance(g, 15) == d >= delta


def test_bch_bound_all_b_n15() -> None:
    for b in range(15):
        for delta in range(2, 9):
            g, _ = bch_generator(F16, delta, b)
            if g.bit_length() - 1 < 15:
                assert min_distance(g, 15) >= delta


def test_check_bits_at_most_m_t() -> None:
    for field in (F16, F32):
        for t in range(1, 8):
            g, _ = bch_generator(field, 2 * t + 1)
            assert g.bit_length() - 1 <= min(field.m * t, field.n)


def test_31_16_7() -> None:
    g, _ = bch_generator(F32, 7)
    assert min_distance(g, 31) == 7


def test_non_primitive_n17_beats_the_bound() -> None:
    # n = 17 divides 2^8 - 1; the coset of 1 mod 17 has 8 elements, so k = 9.
    f256 = GF2m(8, 0x11D)
    g, zeros = bch_generator(f256, 3, 1, 17)
    assert zeros == [1, 2, 4, 8, 9, 13, 15, 16]
    assert min_distance(g, 17) == 5  # the BCH bound only gives 3


def test_systematic_encoding() -> None:
    rng = random.Random(5)
    g, _ = bch_generator(F16, 5)
    for _ in range(200):
        m = rng.randrange(1 << 7)
        c = encode_systematic(m, 15, g)
        assert c >> 8 == m and gf2_mod(c, g) == 0
        beta = 2  # alpha
        for j in (1, 2, 3, 4):  # the consecutive zeros
            p = [(c >> i) & 1 for i in range(15)]
            assert F16.peval(p, F16.pow(beta, j)) == 0
