# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-memory-bank-conflicts/.

import random

from shared_memory_bank_conflicts import column_degree, degree, strided_degree, transpose_tile


def test_stride_degree_is_the_gcd():
    for stride in range(1, 130):
        assert degree([stride * l for l in range(32)]) == strided_degree(stride)
    assert [strided_degree(s) for s in (1, 2, 3, 4, 8, 16, 32, 33)] == [1, 2, 1, 4, 8, 16, 32, 1]


def test_broadcast_and_same_word():
    assert degree([7] * 32) == 1
    assert degree([0] * 16 + [32] * 16) == 2  # two words in bank 0
    assert degree([l // 2 for l in range(32)]) == 1  # pairs share a word


def test_column_of_a_32_wide_tile_and_padding():
    for col in range(32):
        assert column_degree(32, col=col) == 32
        assert column_degree(33, col=col) == 1
    for width in range(1, 80):
        from math import gcd
        assert column_degree(width) == gcd(width, 32)


def test_padded_transpose_is_correct_and_conflict_free():
    rng = random.Random(9)
    tile = [[rng.randrange(1000) for _ in range(32)] for _ in range(32)]
    expect = [list(row) for row in zip(*tile)]
    out, d1, d2 = transpose_tile(tile, pad=0)
    assert out == expect and set(d1) == {1} and set(d2) == {32}
    out, d1, d2 = transpose_tile(tile, pad=1)
    assert out == expect and set(d1) == {1} and set(d2) == {1}
