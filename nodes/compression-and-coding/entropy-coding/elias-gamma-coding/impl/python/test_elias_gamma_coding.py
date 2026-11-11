# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-gamma-coding/. The authors are listed in prov/6VVNKC.jsonl.

import random
from fractions import Fraction

import pytest

from elias_gamma_coding import (
    BitReader,
    BitWriter,
    decode_all,
    encode_all,
    gamma0_decode,
    gamma0_encode,
    gamma_codeword,
    gamma_decode,
    gamma_length,
)

# Pibiri and Venturini, Techniques for inverted index compression (arXiv:1908.10598v2),
# Table 3, column gamma(x), copied by hand. That survey writes the unary part as ones
# ended by a zero; the dot separates the unary part from the low bits.
PV_TABLE_3 = {1: "0.", 2: "10.0", 3: "10.1", 4: "110.00", 5: "110.01", 6: "110.10", 7: "110.11", 8: "1110.000"}

# ITU-T Rec. H.264 (11/2007), Section 9.1, Table 9-2, copied by hand: bit string -> codeNum.
# The ue(v) code of codeNum is the gamma codeword of codeNum + 1.
H264_TABLE_9_2 = {
    "1": 0, "010": 1, "011": 2, "00100": 3, "00101": 4, "00110": 5, "00111": 6,
    "0001000": 7, "0001001": 8, "0001010": 9,
}


def flip_unary_part(word: str) -> str:
    """Turn the survey form 1^n 0 . bits into the form 0^n 1 bits of this page."""
    unary, low = word.split(".")
    return unary.translate(str.maketrans("01", "10")) + low


def test_survey_table() -> None:
    for x, word in PV_TABLE_3.items():
        assert gamma_codeword(x) == flip_unary_part(word)


def test_h264_table() -> None:
    for bits, code_num in H264_TABLE_9_2.items():
        assert gamma_codeword(code_num + 1) == bits
        r = BitReader(int(bits.ljust(16, "0"), 2).to_bytes(2, "big"), len(bits))
        assert gamma0_decode(r) == code_num
        assert r.at_end()


def test_worked_examples() -> None:
    assert gamma_codeword(13) == "0001101"
    assert gamma_codeword(113) == "000000" + "1110001"
    data, nbits = encode_all([5, 1, 13, 2])
    assert nbits == 5 + 1 + 7 + 3
    w = BitWriter()
    for v in [5, 1, 13, 2]:
        w.write_bits(int(gamma_codeword(v), 2), gamma_length(v))
    assert w.getvalue() == (data, nbits)


def test_lengths() -> None:
    for x in range(1, 5000):
        assert len(gamma_codeword(x)) == gamma_length(x) == 2 * (x.bit_length() - 1) + 1
    for k in range(64):
        assert gamma_length(2**k) == 2 * k + 1
        assert gamma_length(2 ** (k + 1) - 1) == 2 * k + 1


def test_kraft_sum_tends_to_one() -> None:
    # The codewords of 1 .. 2^K - 1 have Kraft sum exactly 1 - 2^-K.
    for big_k in range(1, 14):
        s = sum(Fraction(1, 2 ** gamma_length(x)) for x in range(1, 2**big_k))
        assert s == 1 - Fraction(1, 2**big_k)


def test_prefix_free() -> None:
    words = [gamma_codeword(x) for x in range(1, 300)]
    for a in words:
        for b in words:
            assert a == b or not b.startswith(a)


def test_round_trip_random() -> None:
    rng = random.Random(11)
    for _ in range(500):
        values = [rng.randrange(1, 1 << rng.randrange(1, 40)) for _ in range(rng.randrange(25))]
        data, nbits = encode_all(values)
        assert nbits == sum(gamma_length(v) for v in values)
        assert decode_all(data, nbits) == values


def test_extremes_and_zero() -> None:
    values = [1, 2**63 - 1, 2**64 - 1, 2**64, 1]
    assert decode_all(*encode_all(values)) == values
    w = BitWriter()
    for v in [0, 0, 7, 0]:
        gamma0_encode(v, w)
    data, nbits = w.getvalue()
    r = BitReader(data, nbits)
    assert [gamma0_decode(r) for _ in range(4)] == [0, 0, 7, 0]
    with pytest.raises(ValueError):
        gamma_codeword(0)


def test_truncated_stream_raises() -> None:
    data, nbits = encode_all([1000])
    r = BitReader(data, nbits - 1)
    with pytest.raises(EOFError):
        gamma_decode(r)
