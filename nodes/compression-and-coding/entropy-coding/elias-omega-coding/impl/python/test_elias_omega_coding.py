# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-omega-coding/. The authors are listed in prov/7AJD58.jsonl.

import random
from fractions import Fraction

import pytest

from elias_omega_coding import (
    BitReader,
    decode_all,
    encode_all,
    omega_codeword,
    omega_decode,
    omega_length,
)

# Codewords worked out by hand from Elias's definition (groups, then a final 0).
# They agree with the table in the English Wikipedia article "Elias omega coding".
# No standard publishes official test vectors for this code.
TABLE = {
    1: "0",
    2: "10" + "0",
    3: "11" + "0",
    4: "10" + "100" + "0",
    5: "10" + "101" + "0",
    7: "10" + "111" + "0",
    8: "11" + "1000" + "0",
    15: "11" + "1111" + "0",
    16: "10" + "100" + "10000" + "0",
    100: "10" + "110" + "1100100" + "0",
    1000: "11" + "1001" + "1111101000" + "0",
}


def oracle_codeword(x: int) -> str:
    """Omega codeword from Python's bin(), built from the right with a loop."""
    s = "0"
    while x > 1:
        s = bin(x)[2:] + s
        x = len(bin(x)) - 3
    return s


def delta_length(x: int) -> int:
    n = x.bit_length() - 1
    return n + 2 * ((n + 1).bit_length() - 1) + 1


def test_table() -> None:
    for x, word in TABLE.items():
        assert omega_codeword(x) == word


def test_worked_example_decode() -> None:
    word = TABLE[1000]
    r = BitReader(int(word, 2).to_bytes(3, "big"), 24)
    r.pos = 24 - len(word)
    assert omega_decode(r) == 1000 and r.at_end()


def test_length_recurrence() -> None:
    for x in range(1, 5000):
        assert len(omega_codeword(x)) == omega_length(x)
        if x > 1:
            n = x.bit_length() - 1
            assert omega_length(x) == (n + 1) + omega_length(n)
    assert [omega_length(x) for x in (1, 2, 4, 16, 2**16)] == [1, 3, 6, 11, 28]


def test_crossover_with_delta() -> None:
    # Lengths depend only on N = floor(log2 x), so test x = 2^N.
    shorter = [n for n in range(0, 1200) if omega_length(2**n) < delta_length(2**n)]
    assert shorter[:5] == [1, 3, 15, 127, 255]
    assert shorter[5:] == list(range(511, 1200))


def test_kraft_sum_below_one() -> None:
    s = sum(Fraction(1, 2 ** omega_length(x)) for x in range(1, 2**14))
    assert Fraction(3, 4) < s < 1


def test_prefix_free() -> None:
    words = [omega_codeword(x) for x in range(1, 300)]
    for a in words:
        for b in words:
            assert a == b or not b.startswith(a)


def test_round_trip_random_against_oracle() -> None:
    rng = random.Random(31)
    for _ in range(500):
        values = [rng.randrange(1, 1 << rng.randrange(1, 80)) for _ in range(rng.randrange(20))]
        for v in values:
            assert omega_codeword(v) == oracle_codeword(v)
        data, nbits = encode_all(values)
        assert nbits == sum(omega_length(v) for v in values)
        assert decode_all(data, nbits) == values


def test_edge_cases() -> None:
    assert decode_all(*encode_all([])) == []
    assert decode_all(*encode_all([1] * 9)) == [1] * 9
    big = [2**64 - 1, 2**64, 2**2000 + 3]
    assert decode_all(*encode_all(big)) == big
    with pytest.raises(ValueError):
        omega_codeword(0)
    data, nbits = encode_all([1000])
    with pytest.raises(EOFError):
        omega_decode(BitReader(data, nbits - 1))
