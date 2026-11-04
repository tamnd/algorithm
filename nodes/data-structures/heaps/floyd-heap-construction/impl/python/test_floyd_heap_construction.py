# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-heap-construction/. The authors are listed in prov/ADHNWH.jsonl.

import itertools
import random

from floyd_heap_construction import floyd_heap_construction, max_heapify


def is_max_heap(a: list[int]) -> bool:
    return all(a[(j - 1) // 2] >= a[j] for j in range(1, len(a)))


def test_example() -> None:
    a = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    floyd_heap_construction(a)
    assert a == [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]


def test_edges() -> None:
    for a in ([], [1], [1, 2], [2, 1], [5, 5, 5, 5], [1, 2, 3, 4], list(range(20))):
        b = list(a)
        floyd_heap_construction(b)
        assert is_max_heap(b)
        assert sorted(b) == sorted(a)


def test_wrong_order_pitfall() -> None:
    a = [1, 2, 3, 4]
    n = len(a)
    for i in range(0, n // 2):
        max_heapify(a, n, i)
    assert a == [3, 4, 1, 2] and not is_max_heap(a)
    b = [1, 2, 3, 4]
    floyd_heap_construction(b)
    assert is_max_heap(b)


def test_all_permutations() -> None:
    for n in range(8):
        for p in itertools.permutations(range(n)):
            b = list(p)
            floyd_heap_construction(b)
            assert is_max_heap(b) and sorted(b) == list(range(n))


def test_random_against_sorted() -> None:
    rng = random.Random(1964)
    for _ in range(600):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 70))]
        b = list(a)
        floyd_heap_construction(b)
        assert is_max_heap(b)
        assert sorted(b) == sorted(a)
