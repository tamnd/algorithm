# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sift-down/. The authors are listed in prov/MFM3MX.jsonl.

import heapq
import random

import pytest

from sift_down import build_heap, extract_min, increase_key, sift_down


def is_min_heap(a: list[int]) -> bool:
    return all(not a[i] < a[(i - 1) // 2] for i in range(1, len(a)))


def test_example() -> None:
    a = [1, 2, 3, 4, 9, 5, 8, 7]
    assert extract_min(a) == 1
    assert a == [2, 4, 3, 7, 9, 5, 8]


def test_build_example() -> None:
    a = [9, 4, 7, 1, 8, 2, 6, 3, 5]
    build_heap(a)
    assert a == [1, 3, 2, 4, 8, 7, 6, 9, 5]


def test_edges() -> None:
    a = [5]
    assert extract_min(a) == 5 and a == []
    with pytest.raises(IndexError):
        extract_min(a)
    b = [2, 2, 2, 2]
    assert sift_down(b, 0) == 0  # equal keys do not move
    c = [1, 5, 3]
    assert increase_key(c, 0, 9) == 2 and c == [3, 5, 9]
    with pytest.raises(ValueError):
        increase_key(c, 0, 0)
    d = [4, 1, 2]
    assert sift_down(d, 0, 1) == 0 and d == [4, 1, 2]  # n limits the heap


def test_random_against_heapq() -> None:
    rng = random.Random(1964)
    for _ in range(600):
        items = [rng.randint(-30, 30) for _ in range(rng.randint(0, 40))]
        a = list(items)
        build_heap(a)
        assert is_min_heap(a) and sorted(a) == sorted(items)
        out = []
        while a:
            out.append(extract_min(a))
            assert is_min_heap(a)
        assert out == sorted(items)


def test_random_increase_key() -> None:
    rng = random.Random(8)
    for _ in range(600):
        a = [rng.randint(0, 50) for _ in range(rng.randint(1, 30))]
        heapq.heapify(a)
        i = rng.randrange(len(a))
        new = a[i] + rng.randint(0, 60)
        want = sorted(a[:i] + [new] + a[i + 1 :])
        j = increase_key(a, i, new)
        assert a[j] == new
        assert is_min_heap(a) and sorted(a) == want


def test_subtree_only() -> None:
    rng = random.Random(9)
    for _ in range(300):
        a = [rng.randint(0, 20) for _ in range(rng.randint(1, 31))]
        i = rng.randrange(len(a))
        # make every subtree below i a heap, then sift i down
        sub = []
        stack = [i]
        while stack:
            j = stack.pop()
            if j < len(a):
                sub.append(j)
                stack += [2 * j + 1, 2 * j + 2]
        for j in sorted(sub, reverse=True):
            if j != i:
                sift_down(a, j)
        before = list(a)
        sift_down(a, i)
        for j in range(len(a)):
            if j not in sub:
                assert a[j] == before[j]
        for j in sub:
            if j != i:
                assert not a[j] < a[(j - 1) // 2]
