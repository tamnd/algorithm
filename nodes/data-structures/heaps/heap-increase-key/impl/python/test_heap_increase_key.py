# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-increase-key/. The authors are listed in prov/ZN9K6H.jsonl.

import random

import pytest

from heap_increase_key import heap_increase_key, max_heap_insert


def is_max_heap(a: list[int]) -> bool:
    return all(a[(j - 1) // 2] >= a[j] for j in range(1, len(a)))


def test_clrs_example() -> None:
    a = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
    heap_increase_key(a, 8, 15)
    assert a == [16, 15, 10, 14, 7, 9, 3, 2, 8, 1]


def test_edges() -> None:
    a = [5, 3, 4]
    with pytest.raises(ValueError):
        heap_increase_key(a, 1, 2)
    with pytest.raises(IndexError):
        heap_increase_key(a, 3, 9)
    heap_increase_key(a, 1, 3)
    assert a == [5, 3, 4]
    heap_increase_key(a, 0, 6)
    assert a == [6, 3, 4]
    heap_increase_key(a, 2, 6)
    assert a == [6, 3, 6]
    b: list[int] = []
    for k in [3, 1, 4, 1, 5, 9, 2, 6]:
        max_heap_insert(b, k)
        assert is_max_heap(b)
    assert b[0] == 9


def test_random() -> None:
    rng = random.Random(1964)
    for _ in range(1000):
        a: list[int] = []
        for _ in range(rng.randint(1, 30)):
            max_heap_insert(a, rng.randint(-50, 50))
        for _ in range(10):
            i = rng.randrange(len(a))
            k = a[i] + rng.randint(0, 60)
            expect = sorted(a[:i] + [k] + a[i + 1 :])
            heap_increase_key(a, i, k)
            assert is_max_heap(a)
            assert sorted(a) == expect
