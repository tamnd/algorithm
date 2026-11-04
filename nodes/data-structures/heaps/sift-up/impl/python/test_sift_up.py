# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift-up/. The authors are listed in prov/9J3JJD.jsonl.

import heapq
import random

import pytest

from sift_up import decrease_key, heap_insert, sift_up


def is_min_heap(a: list[int]) -> bool:
    return all(not a[i] < a[(i - 1) // 2] for i in range(1, len(a)))


def test_example() -> None:
    a = [2, 4, 3, 7, 9, 5, 8]
    assert heap_insert(a, 1) == 0
    assert a == [1, 2, 3, 4, 9, 5, 8, 7]
    assert heap_insert(a, 3) == 3
    assert a == [1, 2, 3, 3, 9, 5, 8, 7, 4]


def test_edges() -> None:
    a: list[int] = []
    assert heap_insert(a, 5) == 0 and a == [5]
    assert sift_up(a, 0) == 0
    b = [1, 1, 1]
    assert heap_insert(b, 1) == 3  # an equal key does not move
    c = [3, 4, 5]
    assert decrease_key(c, 2, 0) == 0 and c == [0, 4, 3]
    with pytest.raises(ValueError):
        decrease_key(c, 0, 9)


def test_random_inserts_against_heapq() -> None:
    rng = random.Random(1964)
    for _ in range(600):
        a: list[int] = []
        items = [rng.randint(-30, 30) for _ in range(rng.randint(0, 40))]
        for x in items:
            heap_insert(a, x)
            assert is_min_heap(a)
        assert sorted(a) == sorted(items)
        out = []
        while a:
            out.append(heapq.heappop(a))
        assert out == sorted(items)


def test_random_decrease_key() -> None:
    rng = random.Random(7)
    for _ in range(600):
        a = [rng.randint(0, 50) for _ in range(rng.randint(1, 30))]
        heapq.heapify(a)
        i = rng.randrange(len(a))
        new = a[i] - rng.randint(0, 60)
        want = sorted(a[:i] + [new] + a[i + 1 :])
        j = decrease_key(a, i, new)
        assert a[j] == new
        assert is_min_heap(a)
        assert sorted(a) == want


def test_path_bound() -> None:
    a = list(range(1, 64))  # a sorted array is a min-heap
    j = heap_insert(a, 0)
    assert j == 0 and is_min_heap(a)
