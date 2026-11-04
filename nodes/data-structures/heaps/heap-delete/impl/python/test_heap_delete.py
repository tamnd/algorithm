# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-delete/. The authors are listed in prov/8TNZV0.jsonl.

import random

import pytest

from heap_delete import heap_delete, max_heapify


def is_max_heap(a: list[int]) -> bool:
    return all(a[(j - 1) // 2] >= a[j] for j in range(1, len(a)))


def build(keys: list[int]) -> list[int]:
    a = list(keys)
    for i in range(len(a) // 2 - 1, -1, -1):
        max_heapify(a, len(a), i)
    return a


def test_examples() -> None:
    a = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
    assert heap_delete(a, 1) == 14
    assert a == [16, 8, 10, 4, 7, 9, 3, 2, 1]
    b = [100, 50, 90, 40, 45, 80, 85]
    assert heap_delete(b, 3) == 40
    assert b == [100, 85, 90, 50, 45, 80]


def test_edges() -> None:
    with pytest.raises(IndexError):
        heap_delete([], 0)
    with pytest.raises(IndexError):
        heap_delete([3, 2], 2)
    a = [7]
    assert heap_delete(a, 0) == 7 and a == []
    a = [7, 5, 6]
    assert heap_delete(a, 2) == 6 and a == [7, 5]
    a = [7, 5, 6]
    assert heap_delete(a, 0) == 7 and a == [6, 5]


def test_sift_down_only_is_wrong() -> None:
    b = [100, 50, 90, 40, 45, 80, 85]
    b[3] = b.pop()
    max_heapify(b, len(b), 3)
    assert not is_max_heap(b)


def test_random() -> None:
    rng = random.Random(8)
    for _ in range(1000):
        a = build([rng.randint(-20, 20) for _ in range(rng.randint(1, 35))])
        while a:
            i = rng.randrange(len(a))
            expect = sorted(a[:i] + a[i + 1 :])
            x = a[i]
            assert heap_delete(a, i) == x
            assert is_max_heap(a)
            assert sorted(a) == expect
