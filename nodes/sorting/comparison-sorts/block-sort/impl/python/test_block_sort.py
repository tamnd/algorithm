# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-sort/. The authors are listed in prov/0XYD20.jsonl.

import itertools
import random

import block_sort as module
from block_sort import block_sort


class Key:
    def __init__(self, k: int, tag: int) -> None:
        self.k, self.tag = k, tag

    def __lt__(self, other: "Key") -> bool:
        return self.k < other.k


def pairs(a: list[Key]) -> list[tuple[int, int]]:
    return [(e.k, e.tag) for e in a]


def test_example() -> None:
    left = list(range(18)) + [20, 22, 24, 26, 28, 30, 41, 43, 45, 47, 49, 51]
    right = [5, 10, 15, 19, 21, 23, 25, 27, 29, 31, 33, 35, 36, 37, 38, 39, 39, 40, 40, 40, 42, 44]
    a = [Key(v, i) for i, v in enumerate(left + right)]
    saved = module.SMALL_MERGE
    module.SMALL_MERGE = 0
    try:
        module._block_merge(a, 0, 30, 52)
    finally:
        module.SMALL_MERGE = saved
    assert pairs(a) == sorted(pairs(a))


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], [2**63 - 1, 0, -(2**63), 2**63 - 1]):
        b = list(a)
        block_sort(b)
        assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            block_sort(b)
            assert b == list(range(n))


def test_buffered_merges_directly() -> None:
    rng = random.Random(1992)
    for _ in range(400):
        m = rng.randint(64, 300)
        m2 = rng.randint(1, m)
        top = rng.choice([3, 40, 200, 10**6])
        x = sorted(rng.randint(0, top) for _ in range(m))
        y = sorted(rng.randint(0, top) for _ in range(m2))
        a = [Key(v, i) for i, v in enumerate(x + y)]
        module._block_merge(a, 0, m, m + m2)
        assert pairs(a) == sorted(pairs(a))


def test_stable_with_many_and_few_keys() -> None:
    rng = random.Random(1977)
    for top in (1, 5, 60, 10**6):
        for n in (100, 700, 1500):
            a = [Key(rng.randint(0, top), i) for i in range(n)]
            block_sort(a)
            assert pairs(a) == sorted(pairs(a))


def test_patterns() -> None:
    n = 2000
    for a in (list(range(n)), list(range(n, 0, -1)), [7] * n, [i % 3 for i in range(n)], list(range(n // 2)) + list(range(n // 2, 0, -1))):
        b = list(a)
        block_sort(b)
        assert b == sorted(a)


def test_random_against_sorted() -> None:
    rng = random.Random(1969)
    for _ in range(600):
        a = [rng.randint(-200, 200) for _ in range(rng.randint(0, 300))]
        b = list(a)
        block_sort(b)
        assert b == sorted(a)


def test_strings() -> None:
    a = ["pear", "fig", "apple", "fig", "kiwi"] * 30
    block_sort(a)
    assert a == sorted(["pear", "fig", "apple", "fig", "kiwi"] * 30)
