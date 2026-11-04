# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/comb-sort/. The authors are listed in prov/SYZVMD.jsonl.

import itertools
import random

from comb_sort import comb_sort


def test_example() -> None:
    a = [8, 4, 1, 5, 9, 2, 6, 3, 7, 0]
    assert comb_sort(a) == 6
    assert a == list(range(10))


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)]):
        b = list(a)
        comb_sort(b)
        assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(1, 8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            comb_sort(b)
            assert b == list(range(n))


def test_gap_sequence_on_sorted_input() -> None:
    # 1000 -> 769 -> 591 -> ... -> 1: the passes before gap 1, then one pass with gap 1.
    gaps = []
    g = 1000
    while g > 1:
        g = max(1, g * 10 // 13)
        gaps.append(g)
    assert comb_sort(list(range(1000))) == len(gaps)


def test_random_against_sorted() -> None:
    rng = random.Random(1980)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 60))]
        b = list(a)
        comb_sort(b)
        assert b == sorted(a)
