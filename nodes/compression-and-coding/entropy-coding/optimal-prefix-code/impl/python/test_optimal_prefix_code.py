# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-prefix-code/. The authors are listed in prov/8V9YWA.jsonl.

import math
import random

from optimal_prefix_code import (
    brute_force_lengths,
    brute_force_minimax,
    cost,
    huffman_lengths,
    kraft_sum,
    minimax_lengths,
)


def test_examples_of_the_page() -> None:
    assert cost([5, 2, 1, 1], brute_force_lengths([5, 2, 1, 1])) == 15
    # Two optimal length lists with the same cost.
    assert cost([1, 1, 2, 2], [2, 2, 2, 2]) == cost([1, 1, 2, 2], [3, 3, 2, 1]) == 12
    assert cost([1, 1, 2, 2], brute_force_lengths([1, 1, 2, 2])) == 12
    # A skewed source: one bit per symbol, far above the entropy.
    assert brute_force_lengths([9, 1]) == [1, 1]


def test_huffman_matches_brute_force() -> None:
    rng = random.Random(21)
    for _ in range(150):
        n = rng.randint(1, 7)
        w = [rng.randint(0, 30) for _ in range(n)]
        bf = brute_force_lengths(w)
        hu = huffman_lengths(w)
        assert kraft_sum(bf) <= 1 and kraft_sum(hu) <= 1
        assert cost(w, hu) == cost(w, bf)


def test_entropy_bounds() -> None:
    rng = random.Random(22)
    for _ in range(100):
        n = rng.randint(2, 7)
        w = [rng.randint(1, 50) for _ in range(n)]
        total = sum(w)
        p = [x / total for x in w]
        h = -sum(q * math.log2(q) for q in p)
        avg = cost(p, brute_force_lengths(w))
        assert h - 1e-12 <= avg < h + 1


def test_minimax_greedy_matches_brute_force() -> None:
    rng = random.Random(23)
    for _ in range(150):
        n = rng.randint(1, 7)
        w = [rng.randint(0, 6) for _ in range(n)]
        ls = minimax_lengths(w)
        assert kraft_sum(ls) <= 1
        assert max(a + b for a, b in zip(w, ls)) == brute_force_minimax(w)
