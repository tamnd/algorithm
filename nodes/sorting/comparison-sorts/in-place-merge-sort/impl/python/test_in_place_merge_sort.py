# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/in-place-merge-sort/. The authors are listed in prov/JZA43S.jsonl.

import itertools
import random

from in_place_merge_sort import in_place_merge_sort, merge_in_place, rotate


class Key:
    def __init__(self, k: int, tag: int) -> None:
        self.k, self.tag = k, tag

    def __lt__(self, other: "Key") -> bool:
        return self.k < other.k


def test_example() -> None:
    a = [1, 4, 6, 8, 2, 3, 5, 7]
    merge_in_place(a, 0, 4, 8)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]
    b = [5, 1, 4, 2, 8, 0, 3, 6]
    in_place_merge_sort(b)
    assert b == [0, 1, 2, 3, 4, 5, 6, 8]


def test_rotate() -> None:
    a = [6, 8, 2, 3, 5]
    rotate(a, 0, 2, 5)
    assert a == [2, 3, 5, 6, 8]
    b = [1, 2, 3]
    rotate(b, 0, 0, 3)
    rotate(b, 0, 3, 3)
    assert b == [1, 2, 3]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [2**63 - 1, 0, -(2**63), 2**63 - 1]):
        b = list(a)
        in_place_merge_sort(b)
        assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            in_place_merge_sort(b)
            assert b == list(range(n))


def test_merge_of_all_run_lengths() -> None:
    rng = random.Random(5)
    for l1 in range(12):
        for l2 in range(12):
            x = sorted(rng.randint(0, 5) for _ in range(l1))
            y = sorted(rng.randint(0, 5) for _ in range(l2))
            a = [Key(v, i) for i, v in enumerate(x + y)]
            merge_in_place(a, 0, l1, l1 + l2)
            assert [(e.k, e.tag) for e in a] == sorted((e.k, e.tag) for e in a)


def test_stable() -> None:
    rng = random.Random(2004)
    for _ in range(200):
        a = [Key(rng.randint(0, 4), i) for i in range(rng.randint(0, 60))]
        in_place_merge_sort(a)
        assert [(e.k, e.tag) for e in a] == sorted((e.k, e.tag) for e in a)


def test_random_against_sorted() -> None:
    rng = random.Random(1981)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 80))]
        b = list(a)
        in_place_merge_sort(b)
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"]
    in_place_merge_sort(a)
    assert a == ["apple", "fig", "fig", "kiwi", "pear"]
