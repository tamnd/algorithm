# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/length-limited-prefix-code/. The authors are listed in prov/D5F6KM.jsonl.

import random

import pytest

from length_limited_prefix_code import (
    adjust_bits,
    brute_force_lengths,
    cost,
    exact_lengths,
    huffman_lengths,
    jpeg_lengths,
    kraft_sum,
)

# Moffat (2019), Section 4.1 and Figure 6.
MOFFAT = [20, 17, 6, 3, 2, 2, 2, 1, 1, 1]


def test_moffat_example() -> None:
    assert cost(MOFFAT, huffman_lengths(MOFFAT)) == 140
    assert exact_lengths(MOFFAT, 5) == [2, 2, 3, 4, 4, 4, 4, 4, 5, 5]
    assert cost(MOFFAT, exact_lengths(MOFFAT, 5)) == 142
    assert cost(MOFFAT, exact_lengths(MOFFAT, 4)) == 146
    with pytest.raises(ValueError):
        exact_lengths(MOFFAT, 3)


def test_jpeg_adjustment_on_the_example() -> None:
    # Huffman counts by length: 1:1, 2:1, 4:1, 5:5, 6:2. The two codewords
    # of length 6 go to length 5, and the leaf of length 4 becomes a prefix.
    assert adjust_bits([0, 1, 1, 0, 1, 5, 2], 5) == [0, 1, 1, 0, 0, 8]
    lengths = jpeg_lengths(MOFFAT, 5)
    assert sorted(lengths) == [1, 2] + [5] * 8
    assert cost(MOFFAT, lengths) == 144


def test_exact_dp_matches_brute_force() -> None:
    rng = random.Random(31)
    for _ in range(150):
        n = rng.randint(2, 7)
        limit = rng.randint((n - 1).bit_length(), 6)
        w = [rng.randint(1, 40) for _ in range(n)]
        e = exact_lengths(w, limit)
        assert max(e) <= limit and kraft_sum(e) <= 1
        assert cost(w, e) == cost(w, brute_force_lengths(w, limit))


def test_large_limit_gives_huffman_cost() -> None:
    rng = random.Random(32)
    for _ in range(50):
        n = rng.randint(2, 20)
        w = [rng.randint(1, 100) for _ in range(n)]
        assert cost(w, exact_lengths(w, n - 1)) == cost(w, huffman_lengths(w))


def test_jpeg_heuristic_is_feasible_and_close() -> None:
    rng = random.Random(33)
    gaps = []
    for _ in range(80):
        n = rng.randint(8, 30)
        w = [int(1 + 1000 * rng.random() ** 6) for _ in range(n)]
        h = huffman_lengths(w)
        limit = max((n - 1).bit_length(), max(h) - rng.randint(1, 3))
        for reserve in (False, True):
            if reserve and 2**limit < n + 1:
                continue
            j = jpeg_lengths(w, limit, reserve)
            assert max(j) <= limit
            assert kraft_sum(j) <= 1 if not reserve else kraft_sum(j) < 1
        j = jpeg_lengths(w, limit)
        e = exact_lengths(w, limit)
        assert cost(w, j) >= cost(w, e)
        gaps.append((cost(w, j) - cost(w, e)) / cost(w, e))
    # The heuristic is not optimal, but the loss is small on these inputs.
    assert max(gaps) > 0
    assert sum(gaps) / len(gaps) < 0.02


def test_jpeg_reserve_leaves_all_ones_free() -> None:
    w = [50, 20, 10, 5, 5, 4, 3, 2, 1]
    j = jpeg_lengths(w, 16, reserve=True)
    assert kraft_sum(j) == 1 - kraft_sum([max(j)])
