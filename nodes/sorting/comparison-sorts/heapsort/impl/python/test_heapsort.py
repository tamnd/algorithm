# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heapsort/. The authors are listed in prov/CSPR1S.jsonl.

import itertools
import random

from heapsort import heapsort, sift_down


def test_example() -> None:
    a = [6, 5, 3, 1, 8, 7, 2, 4]
    heapsort(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_build_heap_of_example() -> None:
    a = [6, 5, 3, 1, 8, 7, 2, 4]
    for i in range(len(a) // 2 - 1, -1, -1):
        sift_down(a, i, len(a))
    assert a == [8, 6, 7, 4, 5, 3, 2, 1]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 2], [1, 1, 1], [3, 2, 1], [5, 5, 1, 5], [-(2**63), 2**63 - 1, 0]):
        b = list(a)
        heapsort(b)
        assert b == sorted(a)


def test_all_permutations() -> None:
    for n in range(7):
        for p in itertools.permutations(range(n)):
            b = list(p)
            heapsort(b)
            assert b == list(range(n))


def test_not_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(1, "a"), Key(1, "b")]
    heapsort(a)
    assert [x.tag for x in a] == ["b", "a"]


def test_random_against_sorted() -> None:
    rng = random.Random(1964)
    for _ in range(600):
        a = [rng.randint(-40, 40) for _ in range(rng.randint(0, 70))]
        b = list(a)
        heapsort(b)
        assert b == sorted(a)
