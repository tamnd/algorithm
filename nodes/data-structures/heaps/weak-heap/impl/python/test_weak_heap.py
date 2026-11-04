# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-heap/. The authors are listed in prov/PYFMNC.jsonl.

import heapq
import math
import random

import pytest

from weak_heap import WeakHeap, weak_heapsort


def test_example_build() -> None:
    h = WeakHeap([8, 3, 6, 1, 5, 9, 2, 7])
    assert h.a == [1, 5, 6, 2, 8, 9, 3, 7]
    assert h.r == [0, 1, 0, 1, 1, 0, 1, 0]
    assert h.comparisons == 7
    h.check_invariant()


def test_example_delete_and_insert() -> None:
    h = WeakHeap([8, 3, 6, 1, 5, 9, 2, 7])
    h.comparisons = 0
    assert h.delete_min() == 1
    assert h.a == [2, 5, 6, 7, 8, 9, 3]
    assert h.r == [0, 1, 0, 0, 1, 0, 1]
    assert h.comparisons == 2
    h.comparisons = 0
    h.insert(4)
    assert h.a == [2, 5, 6, 4, 8, 9, 3, 7]
    assert h.r == [0, 1, 0, 0, 1, 0, 1, 1]
    assert h.comparisons == 2
    h.check_invariant()


def test_edge_cases() -> None:
    h: WeakHeap[int] = WeakHeap()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    h.insert(3)
    h.insert(1)
    assert h.find_min() == 1
    assert [h.delete_min(), h.delete_min()] == [1, 3]
    assert weak_heapsort([]) == ([], 0)
    assert weak_heapsort([5]) == ([5], 0)
    assert weak_heapsort([2, 2, 1, 2])[0] == [1, 2, 2, 2]


def test_sort_comparison_bound() -> None:
    rng = random.Random(1993)
    for n in range(2, 260):
        for _ in range(3):
            data = [rng.randrange(1000) for _ in range(n)]
            out, c = weak_heapsort(data)
            assert out == sorted(data)
            k = math.ceil(math.log2(n))
            assert c <= n * k - 2**k + n - 1


def test_random_against_heapq() -> None:
    rng = random.Random(2012)
    for _ in range(600):
        start = [rng.randrange(-30, 30) for _ in range(rng.randrange(0, 20))]
        h = WeakHeap(start)
        ref = list(start)
        heapq.heapify(ref)
        h.check_invariant()
        for _ in range(rng.randrange(1, 50)):
            if rng.random() < 0.55 or not ref:
                x = rng.randrange(-30, 30)
                h.insert(x)
                heapq.heappush(ref, x)
            else:
                assert h.find_min() == ref[0]
                n = len(h)
                h.comparisons = 0
                assert h.delete_min() == heapq.heappop(ref)
                assert h.comparisons <= max(0, math.ceil(math.log2(n)))
            h.check_invariant()
            assert sorted(h.a) == sorted(ref)
