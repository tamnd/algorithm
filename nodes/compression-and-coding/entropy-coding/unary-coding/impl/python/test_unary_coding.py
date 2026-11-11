# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unary-coding/. The authors are listed in prov/KAJ1DT.jsonl.

import heapq
import random
from fractions import Fraction

import pytest

from unary_coding import BitReader, BitWriter, decode_all, encode_all, unary_codeword, unary_decode


def test_codewords() -> None:
    assert [unary_codeword(n) for n in range(5)] == ["0", "10", "110", "1110", "11110"]
    assert [unary_codeword(n, ones_first=False) for n in range(4)] == ["1", "01", "001", "0001"]


def test_length_is_n_plus_one() -> None:
    for n in range(200):
        assert len(unary_codeword(n)) == n + 1


def test_prefix_free() -> None:
    words = [unary_codeword(n) for n in range(40)]
    for a in words:
        for b in words:
            assert a == b or not b.startswith(a)


def test_round_trip_random() -> None:
    rng = random.Random(7)
    for ones_first in (True, False):
        for _ in range(500):
            values = [rng.randrange(20) for _ in range(rng.randrange(30))]
            data, nbits = encode_all(values, ones_first)
            assert nbits == sum(v + 1 for v in values)
            assert decode_all(data, nbits, ones_first) == values


def test_edge_cases() -> None:
    assert decode_all(*encode_all([])) == []
    assert decode_all(*encode_all([0] * 17)) == [0] * 17
    assert decode_all(*encode_all([1000])) == [1000]
    with pytest.raises(ValueError):
        unary_codeword(-1)
    r = BitReader(b"\xff", 8)
    with pytest.raises(EOFError):
        unary_decode(r)


def test_bit_writer_layout() -> None:
    w = BitWriter()
    w.write_bits(0b101, 3)
    w.write_bits(0b11110000, 8)
    assert w.bits() == "10111110000"
    data, nbits = w.getvalue()
    assert nbits == 11 and data == bytes([0b10111110, 0b00000000])


def huffman_lengths(weights: list[Fraction]) -> list[int]:
    """Codeword lengths of a Huffman code, built with a heap (an independent oracle)."""
    heap = [(w, i, [i]) for i, w in enumerate(weights)]
    heapq.heapify(heap)
    depth = [0] * len(weights)
    counter = len(weights)
    while len(heap) > 1:
        w1, _, s1 = heapq.heappop(heap)
        w2, _, s2 = heapq.heappop(heap)
        for i in s1 + s2:
            depth[i] += 1
        heapq.heappush(heap, (w1 + w2, counter, s1 + s2))
        counter += 1
    return depth


def test_optimal_for_geometric_one_half() -> None:
    # p(n) = 2^-(n+1). The ideal length -log2 p(n) is n + 1, the unary length.
    big = 30
    probs = [Fraction(1, 2 ** (n + 1)) for n in range(big)]
    tail = 1 - sum(probs)  # the mass of all n >= big, as one extra symbol
    assert tail == Fraction(1, 2**big)
    lengths = huffman_lengths(probs + [tail])
    assert lengths[:big] == [n + 1 for n in range(big)]
    # The expected unary length over the first terms has the closed form 2 - (N + 2) / 2^N.
    for m in range(1, 25):
        part = sum(Fraction(n + 1, 2 ** (n + 1)) for n in range(m))
        assert part == 2 - Fraction(m + 2, 2**m)


def test_not_optimal_for_other_geometric() -> None:
    # For theta = 3/4 Huffman beats unary on the first symbols of the source.
    theta = Fraction(3, 4)
    big = 40
    probs = [(1 - theta) * theta**n for n in range(big)]
    tail = 1 - sum(probs)
    lengths = huffman_lengths(probs + [tail])
    huff = sum(p * l for p, l in zip(probs, lengths))
    unary = sum(p * (n + 1) for n, p in enumerate(probs))
    assert huff < unary - Fraction(1, 2)
