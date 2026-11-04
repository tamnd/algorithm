# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-extract-max/. The authors are listed in prov/4GYGY9.jsonl.

import heapq
import random

import pytest

from heap_extract_max import heap_extract_max, max_heapify


def is_max_heap(a: list[int]) -> bool:
    return all(a[(j - 1) // 2] >= a[j] for j in range(1, len(a)))


def build(keys: list[int]) -> list[int]:
    a = list(keys)
    for i in range(len(a) // 2 - 1, -1, -1):
        max_heapify(a, len(a), i)
    return a


def test_clrs_example() -> None:
    a = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
    assert heap_extract_max(a) == 16
    assert a == [14, 8, 10, 4, 7, 9, 3, 2, 1]
    assert heap_extract_max(a) == 14
    assert a == [10, 8, 9, 4, 7, 1, 3, 2]


def test_edges() -> None:
    with pytest.raises(IndexError):
        heap_extract_max([])
    a = [5]
    assert heap_extract_max(a) == 5 and a == []
    a = [5, 5, 5]
    assert heap_extract_max(a) == 5 and a == [5, 5]
    a = [2, 1]
    assert heap_extract_max(a) == 2 and a == [1]


def test_random_against_heapq() -> None:
    rng = random.Random(64)
    for _ in range(800):
        keys = [rng.randint(-30, 30) for _ in range(rng.randint(1, 40))]
        a = build(keys)
        assert is_max_heap(a)
        model = [-k for k in keys]
        heapq.heapify(model)
        while a:
            assert heap_extract_max(a) == -heapq.heappop(model)
            assert is_max_heap(a)
            assert sorted(a) == sorted(-k for k in model)
