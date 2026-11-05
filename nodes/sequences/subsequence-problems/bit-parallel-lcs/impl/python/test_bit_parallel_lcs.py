# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-parallel-lcs/. The authors are listed in prov/FSVMW5.jsonl.

import random

from bit_parallel_lcs import bit_parallel_columns, bit_parallel_lcs_length, match_masks


def lcs_table(x: str, y: str) -> list[list[int]]:
    c = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    return c


def test_example() -> None:
    x, y = "ABCBDAB", "BDCABA"
    assert match_masks(x)["B"] == 0b1001010
    cols = bit_parallel_columns(x, y)
    assert cols[0] == 0b1111111
    assert cols[1] == 0b1111101
    assert bit_parallel_lcs_length(x, y) == 4


def test_edges() -> None:
    assert bit_parallel_lcs_length("", "") == 0
    assert bit_parallel_lcs_length("abc", "") == 0
    assert bit_parallel_lcs_length("", "abc") == 0
    assert bit_parallel_lcs_length("abc", "xyz") == 0
    assert bit_parallel_lcs_length("abc", "abc") == 3
    assert bit_parallel_lcs_length("a" * 200, "a" * 150) == 150


def test_columns_match_table() -> None:
    rng = random.Random(1986)
    for _ in range(500):
        x = "".join(rng.choice("ACGT"[: rng.randint(1, 4)]) for _ in range(rng.randrange(20)))
        y = "".join(rng.choice("ACGT") for _ in range(rng.randrange(20)))
        c = lcs_table(x, y)
        for j, v in enumerate(bit_parallel_columns(x, y)):
            for i in range(1, len(x) + 1):
                step = c[i][j] - c[i - 1][j]
                assert ((v >> (i - 1)) & 1) == 1 - step
        assert bit_parallel_lcs_length(x, y) == c[len(x)][len(y)]


def test_long_inputs() -> None:
    rng = random.Random(7)
    x = "".join(rng.choice("ACGT") for _ in range(300))
    y = "".join(rng.choice("ACGT") for _ in range(250))
    assert bit_parallel_lcs_length(x, y) == lcs_table(x, y)[300][250]
