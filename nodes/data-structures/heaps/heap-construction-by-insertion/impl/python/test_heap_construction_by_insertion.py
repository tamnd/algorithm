# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-construction-by-insertion/. The authors are listed in prov/0PQJ7X.jsonl.

import itertools
import random
from collections import Counter

from heap_construction_by_insertion import heap_construction_by_insertion, sift_up


class C:
    count = 0

    def __init__(self, v: int) -> None:
        self.v = v

    def __lt__(self, other: "C") -> bool:
        C.count += 1
        return self.v < other.v


def is_max_heap(a: list[int]) -> bool:
    return all(a[(j - 1) // 2] >= a[j] for j in range(1, len(a)))


def test_clrs_input() -> None:
    a = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    heap_construction_by_insertion(a)
    assert a == [16, 14, 10, 8, 7, 3, 9, 1, 4, 2]
    C.count = 0
    b = [C(v) for v in [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]]
    heap_construction_by_insertion(b)
    assert C.count == 17


def test_prefix_is_heap() -> None:
    a = [3, 9, 2, 7, 7, 8, 1, 10]
    for j in range(1, len(a)):
        sift_up(a, j)
        assert is_max_heap(a[: j + 1])


def test_worst_case_count() -> None:
    for n in range(1, 200):
        C.count = 0
        b = [C(v) for v in range(n)]
        heap_construction_by_insertion(b)
        assert C.count == sum(j.bit_length() - 1 for j in range(1, n + 1))
        assert b[0].v == n - 1


def test_edges() -> None:
    for a in ([], [1], [1, 1, 1], [2, 1], [1, 2]):
        b = list(a)
        heap_construction_by_insertion(b)
        assert is_max_heap(b) and sorted(b) == sorted(a)


def test_all_permutations_small() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            heap_construction_by_insertion(b)
            assert is_max_heap(b) and sorted(b) == list(range(n))


def test_random() -> None:
    rng = random.Random(1991)
    for _ in range(600):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 60))]
        b = list(a)
        heap_construction_by_insertion(b)
        assert is_max_heap(b)
        assert Counter(b) == Counter(a)
