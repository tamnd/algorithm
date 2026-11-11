# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-fano-coding/. The authors are listed in prov/M37AW1.jsonl.

import heapq
import math
import random
from fractions import Fraction

import pytest

from shannon_fano_coding import cost, fano_code, is_prefix_free, shannon_code


def huffman_cost(weights) -> int:
    h = list(weights)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def entropy(weights) -> float:
    t = sum(weights)
    return -sum(w / t * math.log2(w / t) for w in weights)


def test_example_where_fano_loses_to_huffman() -> None:
    w = [15, 7, 6, 6, 5]
    assert fano_code(w) == ["00", "01", "10", "110", "111"]
    assert cost(w, fano_code(w)) == 89
    assert huffman_cost(w) == 87


def test_shannon_example() -> None:
    w = [15, 7, 6, 6, 5]
    words = shannon_code([Fraction(x, 39) for x in w])
    assert words == ["00", "011", "100", "101", "110"]
    assert cost(w, words) == 102


def test_dyadic_source_is_coded_exactly() -> None:
    p = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)]
    assert shannon_code(p) == ["0", "10", "110", "111"]
    assert fano_code([4, 2, 1, 1]) == ["0", "10", "110", "111"]


def test_prefix_free_and_bounds() -> None:
    rng = random.Random(51)
    for _ in range(400):
        n = rng.randint(2, 14)
        w = [rng.randint(1, 60) for _ in range(n)]
        t = sum(w)
        h = entropy(w)
        f = fano_code(w)
        s = shannon_code([Fraction(x, t) for x in w])
        assert is_prefix_free(f) and is_prefix_free(s)
        # Shannon's lengths ceil(log2 1/p) give H <= L < H + 1.
        assert h - 1e-12 <= cost(w, s) / t < h + 1
        # Fano's code is never better than Huffman's, and stays below H + 1 here.
        assert cost(w, f) >= huffman_cost(w)
        assert h - 1e-12 <= cost(w, f) / t < h + 1
        # Fano's code is a full tree, so its Kraft sum is 1.
        assert sum(Fraction(1, 2 ** len(c)) for c in f) == 1


def test_small_inputs() -> None:
    assert fano_code([7]) == ["0"]
    assert fano_code([3, 3]) == ["0", "1"]
    assert shannon_code([Fraction(1)]) == ["0"]
    with pytest.raises(ValueError):
        shannon_code([Fraction(1, 2), Fraction(1, 4)])
