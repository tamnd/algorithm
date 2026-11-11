# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canonical-huffman-code/. The authors are listed in prov/ZVDKR0.jsonl.

import heapq
import random

import pytest

from canonical_huffman_code import Decoder, assign_codes, code_strings, encode


def test_rfc1951_section_3_2_2_example() -> None:
    # RFC 1951, Section 3.2.2: alphabet ABCDEFGH with bit lengths
    # (3, 3, 3, 3, 3, 2, 4, 4) and the table of codes printed there.
    lengths = [3, 3, 3, 3, 3, 2, 4, 4]
    assert code_strings(lengths) == ["010", "011", "100", "101", "110", "00", "1110", "1111"]


def test_rfc1951_abcd_example() -> None:
    # RFC 1951, Section 3.2.2: lengths (2, 1, 3, 3) give A 10, B 0, C 110, D 111.
    assert code_strings([2, 1, 3, 3]) == ["10", "0", "110", "111"]


def test_rfc1951_fixed_literal_length_code() -> None:
    # RFC 1951, Section 3.2.6: the fixed Huffman code of the literal/length alphabet.
    lengths = [8] * 144 + [9] * 112 + [7] * 24 + [8] * 8
    words = code_strings(lengths)
    assert words[0] == "00110000" and words[143] == "10111111"
    assert words[144] == "110010000" and words[255] == "111111111"
    assert words[256] == "0000000" and words[279] == "0010111"
    assert words[280] == "11000000" and words[287] == "11000111"


def test_unused_symbols_and_kraft_check() -> None:
    assert code_strings([0, 1, 0, 1]) == [None, "0", None, "1"]
    with pytest.raises(ValueError):
        assign_codes([1, 1, 1])


def huffman_lengths(weights):
    heap = [(w, i, [i]) for i, w in enumerate(weights)]
    heapq.heapify(heap)
    lengths = [0] * len(weights)
    age = len(weights)
    while len(heap) > 1:
        w1, _, a = heapq.heappop(heap)
        w2, _, b = heapq.heappop(heap)
        for s in a + b:
            lengths[s] += 1
        heapq.heappush(heap, (w1 + w2, age, a + b))
        age += 1
    return lengths


def test_canonical_properties_and_round_trip() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(2, 60)
        weights = [rng.randint(0, 40) for _ in range(n)]
        used = [i for i in range(n) if weights[i] > 0]
        if len(used) < 2:
            continue
        hl = huffman_lengths([weights[i] for i in used])
        lengths = [0] * n
        for i, l in zip(used, hl):
            lengths[i] = l
        words = code_strings(lengths)
        live = [(lengths[i], i, words[i]) for i in used]
        # prefix free and the same lengths as the Huffman code
        for _, _, x in live:
            for _, _, y in live:
                assert x == y or not y.startswith(x)
        # sorted by (length, symbol), the codewords increase as binary fractions
        live.sort()
        for (_, _, x), (_, _, y) in zip(live, live[1:]):
            assert int(x, 2) / 2 ** len(x) < int(y, 2) / 2 ** len(y)
        msg = [rng.choice(used) for _ in range(300)]
        bits = encode(msg, lengths)
        dec = Decoder(lengths)
        assert dec.decode_bits(bits) == msg
        assert dec.decode_buffer(bits) == msg


def test_decoder_rejects_bad_input() -> None:
    dec = Decoder([1, 2, 0])  # codes 0, 10; "11" is not a codeword
    with pytest.raises(ValueError):
        dec.decode_bits("11")
    with pytest.raises(ValueError):
        dec.decode_bits("1")
    with pytest.raises(ValueError):
        dec.decode_buffer("11")
