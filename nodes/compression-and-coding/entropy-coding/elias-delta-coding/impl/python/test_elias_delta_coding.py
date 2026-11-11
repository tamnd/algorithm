# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-delta-coding/. The authors are listed in prov/5Y2VCC.jsonl.

import math
import random
from fractions import Fraction

import pytest

from elias_delta_coding import (
    BitReader,
    decode_all,
    delta_codeword,
    delta_decode,
    delta_length,
    encode_all,
    gamma_length,
)

# Pibiri and Venturini, Techniques for inverted index compression (arXiv:1908.10598v2),
# Table 3, column delta(x), copied by hand. The survey writes unary as ones ended by a
# zero, so its gamma part is 1^n 0 then n bits; the dot ends the gamma part.
PV_TABLE_3 = {1: "0.", 2: "100.0", 3: "100.1", 4: "101.00", 5: "101.01", 6: "101.10", 7: "101.11", 8: "11000.000"}


def flip_gamma_part(word: str) -> str:
    """Turn the survey form (unary as 1^n 0) into the form of this page (0^n 1)."""
    head, low = word.split(".")
    n = len(head) - len(head.lstrip("1"))
    unary = head[: n + 1].translate(str.maketrans("01", "10"))
    return unary + head[n + 1 :] + low


def oracle_codeword(x: int) -> str:
    """Delta codeword built from Python's bin(), independent of the bit writer."""
    digits = bin(x)[2:]
    length = bin(len(digits))[2:]
    return "0" * (len(length) - 1) + length + digits[1:]


def test_survey_table() -> None:
    for x, word in PV_TABLE_3.items():
        assert delta_codeword(x) == flip_gamma_part(word)


def test_worked_examples() -> None:
    assert delta_codeword(1) == "1"
    assert delta_codeword(10) == "00100" + "010"
    assert delta_codeword(17) == "00101" + "0001"
    assert delta_codeword(1000) == "0001010" + "111101000"


def test_lengths_formula() -> None:
    for x in range(1, 20000):
        n = math.floor(math.log2(x))  # exact for small x
        expected = n + 2 * math.floor(math.log2(n + 1)) + 1
        assert len(delta_codeword(x)) == delta_length(x) == expected


def test_crossover_with_gamma() -> None:
    equal = [x for x in range(1, 70) if delta_length(x) == gamma_length(x)]
    longer = [x for x in range(1, 70) if delta_length(x) > gamma_length(x)]
    assert equal == [1, 4, 5, 6, 7] + list(range(16, 32))
    assert longer == [2, 3] + list(range(8, 16))
    for k in range(5, 200):
        assert delta_length(2**k) < gamma_length(2**k)
        assert delta_length(2 ** (k + 1) - 1) < gamma_length(2 ** (k + 1) - 1)


def test_asymptotically_optimal_ratio() -> None:
    # l(x) / log2 x tends to 1 for delta and to 2 for gamma.
    ratios = [delta_length(2**k) / k for k in (16, 256, 4096, 65536)]
    assert all(a > b for a, b in zip(ratios, ratios[1:]))
    assert ratios[-1] < 1.001
    assert gamma_length(2**65536) / 65536 > 1.99


def test_kraft_sum() -> None:
    # Codewords of 1 .. 2^K - 1 have Kraft sum equal to the gamma Kraft sum of 1 .. K.
    for big_k in range(1, 15):
        s = sum(Fraction(1, 2 ** delta_length(x)) for x in range(1, 2**big_k))
        assert s == sum(Fraction(1, 2 ** gamma_length(m)) for m in range(1, big_k + 1))
    assert s < 1


def test_prefix_free() -> None:
    words = [delta_codeword(x) for x in range(1, 260)]
    for a in words:
        for b in words:
            assert a == b or not b.startswith(a)


def test_round_trip_random_against_oracle() -> None:
    rng = random.Random(23)
    for _ in range(500):
        values = [rng.randrange(1, 1 << rng.randrange(1, 70)) for _ in range(rng.randrange(20))]
        for v in values:
            assert delta_codeword(v) == oracle_codeword(v)
        data, nbits = encode_all(values)
        assert nbits == sum(delta_length(v) for v in values)
        assert decode_all(data, nbits) == values


def test_edge_cases() -> None:
    assert decode_all(*encode_all([])) == []
    big = [1, 2**64 - 1, 2**64, 2**1000 + 12345]
    assert decode_all(*encode_all(big)) == big
    with pytest.raises(ValueError):
        delta_codeword(0)
    data, nbits = encode_all([1000])
    with pytest.raises(EOFError):
        delta_decode(BitReader(data, nbits - 1))
