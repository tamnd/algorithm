# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twenty-questions-problem/. The authors are listed in prov/ZFP8QP.jsonl.

import itertools
import math
import random

from twenty_questions_problem import (alphabetic_cost, entropy, huffman_cost, one_lie_pelc,
                                      one_lie_search, subset_cost, worst_case)


def test_worst_case() -> None:
    assert [worst_case(n) for n in range(1, 10)] == [0, 1, 2, 2, 3, 3, 3, 3, 4]
    assert worst_case(2 ** 20) == 20 and worst_case(2 ** 20 + 1) == 21
    assert worst_case(10 ** 6) == 20


def test_huffman_is_optimal_over_all_trees() -> None:
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(1, 8)
        w = [rng.randint(1, 30) for _ in range(n)]
        assert huffman_cost(w) == subset_cost(w)


def test_alphabetic_against_all_orders_of_splits() -> None:
    rng = random.Random(6)
    for _ in range(60):
        n = rng.randint(1, 6)
        w = [rng.randint(1, 30) for _ in range(n)]
        a = alphabetic_cost(w)
        assert a >= huffman_cost(w)
        # some order of the objects makes comparison questions as good as any questions
        assert min(alphabetic_cost(list(p)) for p in itertools.permutations(w)) == huffman_cost(w)


def test_entropy_bounds() -> None:
    rng = random.Random(8)
    for _ in range(100):
        n = rng.randint(2, 30)
        w = [rng.randint(1, 100) for _ in range(n)]
        total = sum(w)
        h = entropy([x / total for x in w])
        avg = huffman_cost(w) / total
        assert h - 1e-9 <= avg < h + 1
        assert alphabetic_cost(w) / total < h + 2


def test_worked_example() -> None:
    w = [1, 1, 2, 4, 8]  # probabilities w / 16
    assert huffman_cost(w) == 30 and alphabetic_cost(w) == 30
    assert math.isclose(entropy([x / 16 for x in w]), 30 / 16)
    assert alphabetic_cost([8, 1, 4, 1, 2]) == 32


def test_one_lie_pelc_against_search() -> None:
    for n in range(1, 120):
        assert one_lie_search(n) == one_lie_pelc(n), n
    assert one_lie_pelc(10 ** 6) == 25
