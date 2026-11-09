# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-combination-generation/. The authors are listed in prov/PHDE76.jsonl.

import itertools
import math
import random

from recursive_combination_generation import count_calls, rec_combinations


def test_example() -> None:
    got = list(rec_combinations(5, 3))
    assert got == [
        (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5),
        (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 5),
    ]
    assert count_calls(5, 3) == 39


def test_edges() -> None:
    assert list(rec_combinations(0, 0)) == [()]
    assert list(rec_combinations(3, 0)) == [()]
    assert list(rec_combinations(3, 3)) == [(1, 2, 3)]
    assert list(rec_combinations(2, 3)) == []
    assert list(rec_combinations(3, -1)) == []
    assert count_calls(3, 0) == 1


def test_against_itertools() -> None:
    for n in range(0, 11):
        for k in range(0, n + 2):
            got = list(rec_combinations(n, k))
            assert got == list(itertools.combinations(range(1, n + 1), k))
            assert len(set(got)) == len(got) == (math.comb(n, k) if k <= n else 0)


def test_call_count() -> None:
    for n in range(0, 13):
        for k in range(1, n + 1):
            want = 2 * math.comb(n, k) - 1 + 2 * math.comb(n, k - 1)
            assert count_calls(n, k) == want
    assert count_calls(20, 17) == 11969


def test_random_positions() -> None:
    rng = random.Random(7)
    lists = {}
    for _ in range(600):
        n = rng.randint(0, 12)
        k = rng.randint(0, n)
        if (n, k) not in lists:
            lists[n, k] = (list(rec_combinations(n, k)), list(itertools.combinations(range(1, n + 1), k)))
        got, ref = lists[n, k]
        s = tuple(sorted(rng.sample(range(1, n + 1), k)))
        assert got.index(s) == ref.index(s)
