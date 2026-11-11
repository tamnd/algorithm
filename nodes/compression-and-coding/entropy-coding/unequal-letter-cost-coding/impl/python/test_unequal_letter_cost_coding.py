# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unequal-letter-cost-coding/. The authors are listed in prov/QF16XK.jsonl.

import heapq
import math
import random

import pytest

from unequal_letter_cost_coding import brute_force, capacity_root, optimal_cost


def huffman_cost(weights) -> int:
    h = list(weights)
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        x, y = heapq.heappop(h), heapq.heappop(h)
        total += x + y
        heapq.heappush(h, x + y)
    return total


def letter_cost(word: str, a: int, b: int) -> int:
    return sum(a if ch == "0" else b for ch in word)


def test_worked_example_costs_1_and_2() -> None:
    w = [4, 3, 2, 1]
    assert optimal_cost(w, 1, 2) == (27, [2, 3, 3, 4])
    # The codewords 00, 01, 10, 11 cost 2, 3, 3, 4.
    assert sum(x * letter_cost(c, 1, 2) for x, c in zip(w, ["00", "01", "10", "11"])) == 27
    # The Huffman tree 0, 10, 110, 111, with the cheap letter always on the
    # heavier side, costs more.
    assert sum(x * letter_cost(c, 1, 2) for x, c in zip(w, ["0", "10", "110", "111"])) == 29


def test_huffman_lengths_are_not_enough() -> None:
    # Weights 9, 8, 8, 6, 6 have the Huffman lengths 2, 2, 2, 3, 3.
    w = [9, 8, 8, 6, 6]
    assert optimal_cost(w, 1, 2) == (123, [3, 3, 3, 4, 4])
    best_with_huffman_lengths = sum(
        x * letter_cost(c, 1, 2) for x, c in zip(w, ["01", "10", "11", "000", "001"])
    )
    optimal_words = sum(x * letter_cost(c, 1, 2) for x, c in zip(w, ["01", "10", "000", "11", "001"]))
    assert (best_with_huffman_lengths, optimal_words) == (125, 123)


def test_dp_equals_brute_force() -> None:
    rng = random.Random(1961)
    for _ in range(250):
        n = rng.randint(1, 8)
        w = [rng.randint(1, 30) for _ in range(n)]
        for a, b in ((1, 2), (1, 3), (2, 3), (2, 5)):
            assert optimal_cost(w, a, b)[0] == brute_force(w, a, b), (w, a, b)


def test_equal_costs_give_huffman() -> None:
    rng = random.Random(1952)
    for _ in range(200):
        w = [rng.randint(1, 50) for _ in range(rng.randint(1, 20))]
        assert optimal_cost(w, 1, 1)[0] == huffman_cost(w)
        assert optimal_cost(w, 3, 3)[0] == 3 * huffman_cost(w)


def test_leaf_costs_match_the_total() -> None:
    rng = random.Random(4)
    for _ in range(100):
        w = [rng.randint(1, 40) for _ in range(rng.randint(2, 25))]
        total, levels = optimal_cost(w, 1, 2)
        assert total == sum(x * y for x, y in zip(sorted(w, reverse=True), levels))
        # The leaf costs of a full tree satisfy sum c^-cost = 1 for the capacity root c.
        c = capacity_root(1, 2)
        assert abs(sum(c**-y for y in levels) - 1) < 1e-9


def test_entropy_lower_bound_and_golden_ratio() -> None:
    c = capacity_root(1, 2)
    assert abs(c - (1 + math.sqrt(5)) / 2) < 1e-12
    rng = random.Random(8)
    for _ in range(100):
        w = [rng.randint(1, 100) for _ in range(rng.randint(2, 30))]
        t = sum(w)
        h = -sum(x / t * math.log2(x / t) for x in w)
        mean = optimal_cost(w, 1, 2)[0] / t
        assert mean >= h / math.log2(c) - 1e-9


def test_uniform_weights_and_bad_input() -> None:
    assert optimal_cost([1] * 5, 1, 2) == (17, [3, 3, 3, 4, 4])
    assert optimal_cost([9], 1, 2) == (0, [0])
    with pytest.raises(ValueError):
        optimal_cost([1, 2], 0, 1)
