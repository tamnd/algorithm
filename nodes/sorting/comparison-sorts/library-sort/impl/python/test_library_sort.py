# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/library-sort/. The authors are listed in prov/QMZWKB.jsonl.

import itertools
import random

import library_sort as module
from library_sort import library_sort


class Key:
    def __init__(self, k: int, tag: int) -> None:
        self.k, self.tag = k, tag

    def __lt__(self, other: "Key") -> bool:
        return self.k < other.k


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 0, 3, 6]
    library_sort(a, 1.0, None)
    assert a == [0, 1, 2, 3, 4, 5, 6, 8]


def test_example_slots() -> None:
    s = module._spread([(1, 0), (2, 1), (4, 2), (5, 3)], 17)
    assert [i for i, x in enumerate(s) if x is not None] == [2, 6, 10, 14]
    for p, x in ((4, 8), (5, 0), (6, 3), (7, 6)):
        module._insert(s, x, p)
    assert ["_" if x is None else x[0] for x in s] == [0, "_", 1, "_", "_", "_", 2, "_", 3, "_", 4, "_", "_", "_", 5, 6, 8]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [2**63 - 1, 0, -(2**63), 2**63 - 1]):
        for seed in (None, 7):
            b = list(a)
            library_sort(b, 1.0, seed)
            assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            library_sort(b)
            assert b == list(range(n))


def test_small_eps_and_no_shuffle() -> None:
    rng = random.Random(3)
    for eps in (0.05, 0.25, 3.0):
        for seed in (None, 11):
            a = [rng.randint(0, 50) for _ in range(500)]
            b = list(a)
            library_sort(b, eps, seed)
            assert b == sorted(a)


def test_stable() -> None:
    rng = random.Random(2006)
    for top in (0, 3, 1000):
        a = [Key(rng.randint(0, top), i) for i in range(400)]
        library_sort(a)
        assert [(e.k, e.tag) for e in a] == sorted((e.k, e.tag) for e in a)


def test_random_against_sorted() -> None:
    rng = random.Random(2004)
    for _ in range(600):
        a = [rng.randint(-40, 40) for _ in range(rng.randint(0, 120))]
        b = list(a)
        library_sort(b, 1.0, rng.randrange(1000))
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"]
    library_sort(a)
    assert a == ["apple", "fig", "fig", "kiwi", "pear"]
