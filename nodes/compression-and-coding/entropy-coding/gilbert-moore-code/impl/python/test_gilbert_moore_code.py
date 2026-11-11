# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-moore-code/. The authors are listed in prov/0R8C9C.jsonl.

import functools
import math
import random

import pytest

from gilbert_moore_code import (
    alphabetic_words,
    gilbert_moore_code,
    is_prefix_free,
    optimal_alphabetic_cost,
)


def entropy(counts) -> float:
    t = sum(counts)
    return -sum(w / t * math.log2(w / t) for w in counts)


def brute_alphabetic(weights) -> int:
    """Try every binary tree on the leaves in order."""

    @functools.lru_cache(maxsize=None)
    def best(i, j):
        if i == j:
            return 0
        return sum(weights[i : j + 1]) + min(best(i, k) + best(k + 1, j) for k in range(i, j))

    # An independent check by enumerating all trees for small n.
    def trees(i, j):
        if i == j:
            yield [0]
            return
        for k in range(i, j):
            for left in trees(i, k):
                for right in trees(k + 1, j):
                    yield [d + 1 for d in left] + [d + 1 for d in right]

    n = len(weights)
    if n <= 7:
        value = min(sum(w * d for w, d in zip(weights, depths)) for depths in trees(0, n - 1))
        assert value == best(0, n - 1)
        return value
    return best(0, n - 1)


def test_worked_example() -> None:
    w = [4, 1, 6, 2, 3]
    words = gilbert_moore_code(w)
    assert words == ["001", "01001", "100", "1100", "1110"]
    assert sum(x * len(c) for x, c in zip(w, words)) == 55
    cost, lengths = optimal_alphabetic_cost(w)
    assert (cost, lengths) == (37, [2, 2, 2, 3, 3])
    assert alphabetic_words(lengths) == ["00", "01", "10", "110", "111"]


def test_order_prefix_and_bound() -> None:
    rng = random.Random(1959)
    for _ in range(500):
        n = rng.randint(1, 14)
        w = [rng.randint(1, 40) for _ in range(n)]
        words = gilbert_moore_code(w)
        assert is_prefix_free(words)
        assert words == sorted(words)  # the code keeps the order of the symbols
        t = sum(w)
        mean = sum(x * len(c) for x, c in zip(w, words)) / t
        h = entropy(w)
        assert h + 1 - 1e-12 <= mean < h + 2


def test_dynamic_program_is_optimal_and_beats_the_code() -> None:
    rng = random.Random(33)
    for _ in range(150):
        n = rng.randint(1, 8)
        w = [rng.randint(1, 30) for _ in range(n)]
        cost, lengths = optimal_alphabetic_cost(w)
        assert cost == brute_alphabetic(w)
        assert cost == sum(x * l for x, l in zip(w, lengths))
        words = alphabetic_words(lengths)
        if n > 1:
            assert is_prefix_free(words) and words == sorted(words)
        assert cost <= sum(x * len(c) for x, c in zip(w, gilbert_moore_code(w)))
        # The optimal alphabetic code also has mean length below H + 2.
        assert cost / sum(w) < entropy(w) + 2


def test_order_has_a_price() -> None:
    # With the heavy symbol in the middle, an alphabetic code can not give
    # it a 1-bit codeword without also giving one to a light neighbour.
    assert optimal_alphabetic_cost([1, 10, 1])[0] == 23  # Huffman: 14


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        gilbert_moore_code([3, 0, 2])
    assert gilbert_moore_code([5]) == ["1"]
