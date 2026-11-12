# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golay-code/. The authors are listed in prov/Q2MXRM.jsonl.

import random
from itertools import combinations
from math import comb

from golay_code import (
    B, GOLAY_G, TERNARY_G, decode, decode24, encode, encode24, gf2_mod, gf2_mul, poly_mod_p,
    syndrome, ternary_words, vec_times_b, weight_distribution,
)


def test_generator_divides_x23_plus_1() -> None:
    x23 = (1 << 23) | 1
    assert gf2_mod(x23, GOLAY_G) == 0
    # x^23 + 1 = (x + 1) g(x) g~(x), where g~ is the reciprocal x^11 + x^9 + x^7 + x^6 + x^5 + x + 1
    recip = int(format(GOLAY_G, "012b")[::-1], 2)
    assert recip == (1 << 11) | (1 << 9) | (1 << 7) | (1 << 6) | (1 << 5) | (1 << 1) | 1
    assert gf2_mul(gf2_mul(0b11, GOLAY_G), recip) == x23


def test_weight_distribution_23() -> None:
    words = [encode(m) for m in range(2 ** 12)]
    assert all(syndrome(c) == 0 for c in words)
    a = weight_distribution(words, 23)
    assert {i: v for i, v in enumerate(a) if v} == {0: 1, 7: 253, 8: 506, 11: 1288, 12: 1288,
                                                     15: 506, 16: 253, 23: 1}


def test_perfect() -> None:
    assert 2 ** 12 * sum(comb(23, i) for i in range(4)) == 2 ** 23
    from golay_code import build_syndrome_table
    assert len(build_syndrome_table()) == 2 ** 11


def test_decoder_corrects_every_pattern_up_to_3() -> None:
    rng = random.Random(1949)
    msgs = [rng.randrange(2 ** 12) for _ in range(3)]
    for m in msgs:
        c = encode(m)
        for w in range(4):
            for pos in combinations(range(23), w):
                e = sum(1 << p for p in pos)
                assert decode(c ^ e) == c
    # with 4 errors the decoder returns the unique codeword at distance 3, never the sent one
    c = encode(msgs[0])
    for _ in range(200):
        e = sum(1 << p for p in rng.sample(range(23), 4))
        out = decode(c ^ e)
        assert out != c and (out ^ c ^ e).bit_count() == 3


def test_extended_code_matrix() -> None:
    rows = [[(B[i] >> j) & 1 for j in range(12)] for i in range(12)]
    assert all(rows[i][j] == rows[j][i] for i in range(12) for j in range(12))  # symmetric
    for i in range(12):
        assert vec_times_b(B[i]) == 1 << i  # B^2 = I
    a = weight_distribution([encode24(m) for m in range(2 ** 12)], 24)
    assert {i: v for i, v in enumerate(a) if v} == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}


def test_arithmetic_decoder() -> None:
    rng = random.Random(1975)
    c = encode24(rng.randrange(2 ** 12))
    for w in range(4):  # every pattern of weight <= 3: 2325 patterns
        for pos in combinations(range(24), w):
            e = sum(1 << p for p in pos)
            assert decode24(c ^ e) == c
    for pos in combinations(range(24), 4):  # every pattern of weight 4 is detected
        e = sum(1 << p for p in pos)
        assert decode24(c ^ e) is None


def test_ternary_golay() -> None:
    x11_minus_1 = [2] + [0] * 10 + [1]
    assert poly_mod_p(x11_minus_1, TERNARY_G, 3) == [0] * 5
    words = ternary_words()
    assert len(set(words)) == 729
    a = weight_distribution(words, 11)
    assert {i: v for i, v in enumerate(a) if v} == {0: 1, 5: 132, 6: 132, 8: 330, 9: 110, 11: 24}
    assert 3 ** 6 * sum(comb(11, i) * 2 ** i for i in range(3)) == 3 ** 11  # perfect
    ext = [w + ((-sum(w)) % 3,) for w in words]
    b = weight_distribution(ext, 12)
    assert {i: v for i, v in enumerate(b) if v} == {0: 1, 6: 264, 9: 440, 12: 24}
