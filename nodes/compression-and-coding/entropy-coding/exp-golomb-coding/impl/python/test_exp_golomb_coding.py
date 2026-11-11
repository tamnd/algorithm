# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exp-golomb-coding/. The authors are listed in prov/GFRAJT.jsonl.

import random

import pytest

from exp_golomb_coding import (
    BitReader,
    BitWriter,
    code_num_to_se,
    decode_all,
    encode_all,
    expgolomb_codeword,
    expgolomb_decode,
    expgolomb_length,
    se_decode,
    se_encode,
    se_to_code_num,
    ue_decode,
)

# ITU-T Rec. H.264 (11/2007), Section 9.1, Table 9-2 (explicit form), copied by hand:
# bit string -> codeNum.
H264_TABLE_9_2 = {
    "1": 0, "010": 1, "011": 2, "00100": 3, "00101": 4, "00110": 5, "00111": 6,
    "0001000": 7, "0001001": 8, "0001010": 9,
}

# ITU-T Rec. H.264 (11/2007), Section 9.1.1, Table 9-3, copied by hand:
# codeNum -> syntax element value for se(v).
H264_TABLE_9_3 = {0: 0, 1: 1, 2: -1, 3: 2, 4: -2, 5: 3, 6: -3}

# Pibiri and Venturini, Techniques for inverted index compression (arXiv:1908.10598v2),
# Table 3, column ExpG2(x) for x = 1 .. 8, copied by hand. The survey codes x >= 1 as the
# order-2 codeword of x - 1, with unary as ones ended by a zero; the dot ends the unary part.
PV_TABLE_3_EXPG2 = {
    1: "0.00", 2: "0.01", 3: "0.10", 4: "0.11", 5: "10.000", 6: "10.001", 7: "10.010", 8: "10.011",
}


def reader_for(bits: str) -> BitReader:
    w = BitWriter()
    for c in bits:
        w.write_bit(int(c))
    return BitReader(*w.getvalue())


def h264_ue_decode_oracle(bits: str) -> tuple[int, int]:
    """Section 9.1 of H.264, written as in the standard:
    leadingZeroBits = -1; for (b = 0; !b; leadingZeroBits++) b = read_bits(1);
    codeNum = 2^leadingZeroBits - 1 + read_bits(leadingZeroBits).
    Returns (codeNum, bits used)."""
    pos = 0
    leading_zero_bits = -1
    b = 0
    while not b:
        b = int(bits[pos])
        pos += 1
        leading_zero_bits += 1
    suffix = int(bits[pos : pos + leading_zero_bits] or "0", 2)
    pos += leading_zero_bits
    return 2**leading_zero_bits - 1 + suffix, pos


def h264_egk_suffix_oracle(sym: int, k: int) -> str:
    """The EGk binarization of H.264 Section 9.3.2.3, written as in the standard.
    Its unary part uses ones ended by a zero (the reverse of Section 9.1)."""
    out = []
    while True:
        if sym >= (1 << k):
            out.append("1")
            sym -= 1 << k
            k += 1
        else:
            out.append("0")
            while k:
                k -= 1
                out.append(str((sym >> k) & 1))
            break
    return "".join(out)


def flip_unary(word: str) -> str:
    """Turn 1^n 0 rest into 0^n 1 rest."""
    n = len(word) - len(word.lstrip("1"))
    return "0" * n + "1" + word[n + 1 :]


def test_h264_table_9_2() -> None:
    for bits, code_num in H264_TABLE_9_2.items():
        assert expgolomb_codeword(code_num, 0) == bits
        r = reader_for(bits)
        assert ue_decode(r) == code_num and r.at_end()


def test_h264_table_9_3() -> None:
    for code_num, value in H264_TABLE_9_3.items():
        assert code_num_to_se(code_num) == value
        assert se_to_code_num(value) == code_num
    w = BitWriter()
    for v in [0, 1, -1, 2, -2, 3, -3, 1000, -1000]:
        se_encode(v, w)
    r = BitReader(*w.getvalue())
    assert [se_decode(r) for _ in range(9)] == [0, 1, -1, 2, -2, 3, -3, 1000, -1000]


def test_h264_decode_procedure_oracle() -> None:
    for c in range(0, 3000):
        word = expgolomb_codeword(c, 0)
        assert h264_ue_decode_oracle(word + "1") == (c, len(word))


def test_h264_egk_binarization() -> None:
    for k in range(0, 6):
        for x in range(0, 600):
            assert expgolomb_codeword(x, k) == flip_unary(h264_egk_suffix_oracle(x, k))


def test_survey_table_order_2() -> None:
    for x, word in PV_TABLE_3_EXPG2.items():
        assert expgolomb_codeword(x - 1, 2) == flip_unary(word.replace(".", ""))


def test_lengths() -> None:
    for k in range(0, 8):
        for x in range(0, 2000):
            assert len(expgolomb_codeword(x, k)) == expgolomb_length(x, k)
        # The first 2^k values take k + 1 bits; the next 2^(k+1) take k + 3 bits.
        assert {expgolomb_length(x, k) for x in range(2**k)} == {k + 1}
        assert {expgolomb_length(x, k) for x in range(2**k, 3 * 2**k)} == {k + 3}


def test_round_trip_random() -> None:
    rng = random.Random(71)
    for _ in range(500):
        k = rng.randrange(0, 12)
        values = [rng.randrange(0, 1 << rng.randrange(1, 50)) for _ in range(rng.randrange(20))]
        data, nbits = encode_all(values, k)
        assert nbits == sum(expgolomb_length(v, k) for v in values)
        assert decode_all(data, nbits, k) == values


def test_worked_example() -> None:
    table = {0: "100", 3: "111", 4: "01000", 9: "01101", 11: "01111", 12: "0010000", 28: "000100000"}
    for x, word in table.items():
        assert expgolomb_codeword(x, 2) == word
    assert expgolomb_decode(2, reader_for("01101")) == 9
    assert expgolomb_length(1000, 0) == 19 and expgolomb_length(1000, 2) == 17


def test_edge_cases() -> None:
    assert expgolomb_codeword(0, 0) == "1"
    assert expgolomb_codeword(0, 3) == "1000"
    assert decode_all(*encode_all([], 2), 2) == []
    assert decode_all(*encode_all([2**64 - 1, 0], 0), 0) == [2**64 - 1, 0]
    with pytest.raises(ValueError):
        expgolomb_codeword(-1, 0)
    data, nbits = encode_all([300], 2)
    with pytest.raises(EOFError):
        expgolomb_decode(2, BitReader(data, nbits - 1))
