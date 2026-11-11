# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-alphabetic-code/. The authors are listed in prov/GS71SB.jsonl.

import heapq
import math
import random

from optimal_alphabetic_code import (
    alphabetic_cubic,
    alphabetic_knuth,
    brute_force,
    codewords,
)


def huffman_cost(weights) -> int:
    h = list(weights)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


def test_examples() -> None:
    assert alphabetic_knuth([4, 1, 6, 2, 3])[:2] == (37, [2, 2, 2, 3, 3])
    assert alphabetic_knuth([1, 10, 1])[0] == 23
    assert huffman_cost([1, 10, 1]) == 14
    # Sorted weights: the order costs nothing, the result is a Huffman cost.
    assert alphabetic_knuth([1, 1, 2, 3, 5, 8])[0] == huffman_cost([1, 1, 2, 3, 5, 8])
    assert codewords([2, 2, 2, 3, 3]) == ["00", "01", "10", "110", "111"]


def test_knuth_equals_cubic_equals_brute_force() -> None:
    rng = random.Random(1971)
    for _ in range(300):
        n = rng.randint(1, 8)
        w = [rng.randint(1, 20) for _ in range(n)]
        cost, depths, _ = alphabetic_knuth(w)
        assert cost == alphabetic_cubic(w)[0] == brute_force(w)
        assert cost == sum(x * d for x, d in zip(w, depths))


def test_knuth_on_larger_inputs_and_monotone_splits() -> None:
    rng = random.Random(1980)
    for _ in range(40):
        n = rng.randint(10, 40)
        w = [rng.randint(1, 1000) for _ in range(n)]
        cost, depths, cut = alphabetic_knuth(w)
        assert cost == alphabetic_cubic(w)[0]
        for i in range(n):
            for j in range(i + 2, n):
                assert cut[i][j - 1] <= cut[i][j] <= cut[i + 1][j]
        words = codewords(depths)
        assert words == sorted(words)
        assert all(not b.startswith(a) for a, b in zip(words, words[1:]))
        assert sum(2.0 ** -d for d in depths) == 1.0


def test_bounds() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(2, 30)
        w = [rng.randint(1, 100) for _ in range(n)]
        t = sum(w)
        h = -sum(x / t * math.log2(x / t) for x in w)
        cost = alphabetic_knuth(w)[0]
        assert huffman_cost(w) <= cost
        assert h - 1e-12 <= cost / t < h + 2
