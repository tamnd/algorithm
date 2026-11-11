# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parity-bit/. The authors are listed in prov/XJCSTS.jsonl.

import itertools
import random

from parity_bit import (
    add_parity_7bit, check_8bit, decode_2d, encode_2d, even_parity, odd_parity, parity_block, rebuild,
    syndromes_2d,
)


def test_ascii_examples() -> None:
    # 'A' = 0x41 = 100 0001 has two 1 bits; 'C' = 0x43 has three.
    assert add_parity_7bit(0x41) == 0x41 and add_parity_7bit(0x41, odd=True) == 0xC1
    assert add_parity_7bit(0x43) == 0xC3 and add_parity_7bit(0x43, odd=True) == 0x43
    assert even_parity(0) == 0 and odd_parity(0) == 1


def test_single_parity_detects_exactly_odd_errors() -> None:
    for ch in range(128):
        for odd in (False, True):
            frame = add_parity_7bit(ch, odd)
            assert check_8bit(frame, odd)
            for e in range(1, 256):
                assert check_8bit(frame ^ e, odd) == (e.bit_count() % 2 == 0)


def flip(word: list[list[int]], cells) -> list[list[int]]:
    out = [row[:] for row in word]
    for i, j in cells:
        out[i][j] ^= 1
    return out


def test_2d_parity_exhaustive_on_3_by_4() -> None:
    k_rows, k_cols = 3, 4
    words = []
    for bits in range(1 << (k_rows * k_cols)):
        block = [[(bits >> (i * k_cols + j)) & 1 for j in range(k_cols)] for i in range(k_rows)]
        words.append(encode_2d(block))
    # Minimum distance 4: the least weight of a nonzero codeword.
    assert min(sum(map(sum, w)) for w in words[1:]) == 4
    rng = random.Random(5)
    cells = list(itertools.product(range(k_rows + 1), range(k_cols + 1)))
    for w in rng.sample(words, 40):
        for c in cells:  # every single error is corrected
            assert decode_2d(flip(w, [c])) == ("corrected", w)
        for pair in itertools.combinations(cells, 2):  # every double error is detected
            assert decode_2d(flip(w, pair))[0] == "error"
        for triple in itertools.combinations(cells, 3):  # every triple error has a nonzero syndrome
            assert syndromes_2d(flip(w, triple)) != ([], [])


def test_2d_parity_limits() -> None:
    w = encode_2d([[1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0]])
    # Four errors on the corners of a rectangle are not seen.
    rect = [(0, 1), (0, 3), (2, 1), (2, 3)]
    assert decode_2d(flip(w, rect)) == ("ok", flip(w, rect))
    # Three errors in an L shape point at the fourth corner: miscorrection.
    status, out = decode_2d(flip(w, rect[:3]))
    assert status == "corrected" and out == flip(w, rect) and out != w


def test_raid_xor_parity() -> None:
    rng = random.Random(4)
    data = [rng.randbytes(16) for _ in range(5)]
    p = parity_block(data)
    assert parity_block([*data, p]) == bytes(16)  # all blocks XOR to zero
    for lost in range(5):
        blocks = [None if i == lost else b for i, b in enumerate(data)]
        assert rebuild(blocks, p) == data
