# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pancake-sort/. The authors are listed in prov/NCD5YW.jsonl.

import itertools
import random

from pancake_sort import flip, pancake_sort


def test_example() -> None:
    a = [3, 6, 1, 5, 2, 4]
    flips: list[int] = []
    pancake_sort(a, flips)
    assert a == [1, 2, 3, 4, 5, 6]
    assert flips == [2, 6, 3, 5, 3, 4, 2, 3]


def test_flip() -> None:
    a = [1, 2, 3, 4, 5]
    flip(a, 2)
    assert a == [3, 2, 1, 4, 5]
    flip(a, 0)
    assert a == [3, 2, 1, 4, 5]


def test_flips_replay() -> None:
    # Only prefix reversals are used: replaying the recorded flips sorts a copy.
    rng = random.Random(6)
    for _ in range(200):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 30))]
        b = list(a)
        flips: list[int] = []
        pancake_sort(b, flips)
        assert b == sorted(a)
        for size in flips:
            a[:size] = a[:size][::-1]
        assert a == b


def test_at_most_2n_minus_3_flips() -> None:
    for n in range(2, 8):
        for p in itertools.permutations(range(n)):
            a = list(p)
            flips: list[int] = []
            pancake_sort(a, flips)
            assert a == list(range(n))
            assert len(flips) <= 2 * n - 3


def test_edges() -> None:
    for a in ([], [1], [1, 1], [2, 1], [5, 5, 1]):
        b = list(a)
        pancake_sort(b)
        assert b == sorted(a)


def test_sorted_needs_no_flip() -> None:
    a = list(range(100))
    flips: list[int] = []
    pancake_sort(a, flips)
    assert flips == []
