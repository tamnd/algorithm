# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golomb-coding/. The authors are listed in prov/MNB3EF.jsonl.

import heapq
import math
import random
from fractions import Fraction

import pytest

from golomb_coding import (
    BitReader,
    BitWriter,
    decode_all,
    encode_all,
    golomb_codeword,
    golomb_decode,
    golomb_length,
    optimal_m,
    truncated_binary_decode,
    truncated_binary_encode,
)

# Pibiri and Venturini, Techniques for inverted index compression (arXiv:1908.10598v2),
# Table 3, column G2(x) for x = 1 .. 8, copied by hand. The survey codes x >= 1 as the
# Golomb codeword of x - 1, with unary as ones ended by a zero; the dot ends the unary part.
PV_TABLE_3_G2 = {1: "0.0", 2: "0.1", 3: "10.0", 4: "10.1", 5: "110.0", 6: "110.1", 7: "1110.0", 8: "1110.1"}


def truncated_binary_oracle(r: int, m: int) -> str:
    """Truncated binary from its definition: the first u values get the short
    words 0 .. u-1 in k bits, the rest get the long words 2u .. 2m-1 in k+1 bits."""
    k = math.floor(math.log2(m))
    u = 2 ** (k + 1) - m
    if r < u:
        return format(r, "b").zfill(k) if k else ""
    return format(r + u, "b").zfill(k + 1)


def golomb_oracle(x: int, m: int) -> str:
    q, r = divmod(x, m)
    return "1" * q + "0" + truncated_binary_oracle(r, m)


def tb_word(r: int, m: int) -> str:
    w = BitWriter()
    truncated_binary_encode(r, m, w)
    return w.bits()


def test_truncated_binary() -> None:
    assert [tb_word(r, 5) for r in range(5)] == ["00", "01", "10", "110", "111"]
    assert [tb_word(r, 3) for r in range(3)] == ["0", "10", "11"]
    assert [tb_word(r, 6) for r in range(6)] == ["00", "01", "100", "101", "110", "111"]
    assert [tb_word(r, 8) for r in range(8)] == [format(r, "03b") for r in range(8)]
    assert tb_word(0, 1) == ""
    for m in range(1, 70):
        words = [tb_word(r, m) for r in range(m)]
        assert words == [truncated_binary_oracle(r, m) for r in range(m)]
        # A complete prefix code on m symbols: Kraft sum exactly 1.
        assert sum(Fraction(1, 2 ** len(t)) for t in words) == 1
        for a in words:
            assert all(a == b or not b.startswith(a) for b in words)
        for r, t in enumerate(words):
            rd = BitReader(int(t or "0", 2).to_bytes(2, "big"), 16)
            rd.pos = 16 - len(t)
            assert truncated_binary_decode(m, rd) == r and rd.at_end()


def test_survey_table() -> None:
    for x, word in PV_TABLE_3_G2.items():
        assert golomb_codeword(x - 1, 2) == word.replace(".", "")


def test_worked_example() -> None:
    # m = 5, x = 17: q = 3, r = 2 -> 1110 then 10.
    assert golomb_codeword(17, 5) == "1110" + "10"
    # m = 5, x = 9: q = 1, r = 4 -> 10 then 111.
    assert golomb_codeword(9, 5) == "10" + "111"
    assert decode_all(*encode_all([17, 9, 0, 4], 5), 5) == [17, 9, 0, 4]


def test_unary_is_golomb_one() -> None:
    for x in range(50):
        assert golomb_codeword(x, 1) == "1" * x + "0"


def test_round_trip_random_against_oracle() -> None:
    rng = random.Random(53)
    for _ in range(600):
        m = rng.randrange(1, 300)
        values = [rng.randrange(0, 20 * m) for _ in range(rng.randrange(20))]
        for v in values:
            assert golomb_codeword(v, m) == golomb_oracle(v, m)
            assert golomb_length(v, m) == len(golomb_oracle(v, m))
        data, nbits = encode_all(values, m)
        assert decode_all(data, nbits, m) == values


def huffman_cost(weights: list[Fraction]) -> Fraction:
    """Expected length of a Huffman code: the sum of all merged weights."""
    heap = list(weights)
    heapq.heapify(heap)
    cost = Fraction(0)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        cost += a + b
        heapq.heappush(heap, a + b)
    return cost


def golomb_expected_length(theta: Fraction, m: int) -> Fraction:
    """Exact expected Golomb length for P(x) = (1 - theta) theta^x."""
    tm = theta**m
    unary = 1 + tm / (1 - tm)
    rem = sum((1 - theta) * theta**r / (1 - tm) * len(truncated_binary_oracle(r, m)) for r in range(m))
    return unary + rem


@pytest.mark.parametrize("theta", [Fraction(1, 2), Fraction(3, 5), Fraction(7, 10), Fraction(4, 5), Fraction(9, 10)])
def test_optimal_against_huffman(theta: Fraction) -> None:
    # Truncate the source after K symbols and lump the tail into one symbol. Any prefix
    # code for the full source gives a code for the lumped source that is no longer,
    # so the Huffman cost of the lumped source is a lower bound on the optimum.
    big_k = 1
    while theta**big_k > Fraction(1, 10**12):
        big_k += 1
    probs = [(1 - theta) * theta**x for x in range(big_k)]
    lower = huffman_cost(probs + [theta**big_k])
    m_star = optimal_m(theta)
    best = golomb_expected_length(theta, m_star)
    assert lower <= best < lower + Fraction(1, 10**9)
    for m in range(1, 4 * m_star + 3):
        assert golomb_expected_length(theta, m) >= best
    assert golomb_expected_length(theta, m_star + 1) > best + Fraction(1, 10**6)
    if m_star > 1:
        assert golomb_expected_length(theta, m_star - 1) > best + Fraction(1, 10**6)


def test_optimal_m_rule() -> None:
    assert optimal_m(Fraction(1, 2)) == 1
    assert optimal_m(Fraction(3, 5)) == 1  # 0.6 + 0.36 <= 1
    assert optimal_m(Fraction(7, 10)) == 2
    assert optimal_m(Fraction(9, 10)) == 7
    for i in range(1, 200):
        theta = Fraction(i, 200)
        m = optimal_m(theta)
        assert theta**m + theta ** (m + 1) <= 1
        assert m == 1 or theta ** (m - 1) + theta**m > 1
        assert m == max(1, math.ceil(math.log(1 + i / 200) / -math.log(i / 200)))


def test_edge_cases() -> None:
    assert decode_all(*encode_all([], 7), 7) == []
    assert decode_all(*encode_all([0, 2**40], 2**20 + 1), 2**20 + 1) == [0, 2**40]
    with pytest.raises(ValueError):
        golomb_codeword(-1, 3)
    with pytest.raises(ValueError):
        golomb_codeword(3, 0)
    data, nbits = encode_all([100], 7)
    with pytest.raises(EOFError):
        golomb_decode(7, BitReader(data, nbits - 1))
