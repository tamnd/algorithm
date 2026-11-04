# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-heap/. The authors are listed in prov/XN8WFN.jsonl.

import random

import pytest

from interval_heap import IntervalHeap


def test_example() -> None:
    h: IntervalHeap[int] = IntervalHeap()
    for x in [5, 2, 8, 6, 1, 9, 3]:
        h.insert(x)
        h.check_invariant()
    assert h.nodes() == [(1, 9), (3, 6), (2, 8), (5,)]
    h.insert(7)
    assert h.nodes() == [(1, 9), (3, 7), (2, 8), (5, 6)]
    assert h.extract_min() == 1
    assert h.nodes() == [(2, 9), (3, 7), (6, 8), (5,)]
    assert h.extract_max() == 9
    assert h.nodes() == [(2, 8), (3, 7), (5, 6)]
    assert (h.find_min(), h.find_max()) == (2, 8)
    h.check_invariant()


def test_edges() -> None:
    h: IntervalHeap[int] = IntervalHeap()
    for f in (h.find_min, h.find_max, h.extract_min, h.extract_max):
        with pytest.raises(IndexError):
            f()
    h.insert(4)
    assert (h.find_min(), h.find_max()) == (4, 4)
    assert h.extract_max() == 4
    h.insert(4)
    assert h.extract_min() == 4
    h = IntervalHeap([3, 1])
    assert h.extract_min() == 1
    assert h.extract_max() == 3
    assert len(h) == 0


def test_duplicates() -> None:
    h = IntervalHeap([2, 2, 2, 1, 1, 3, 3])
    h.check_invariant()
    out = [h.extract_min() for _ in range(7)]
    assert out == [1, 1, 2, 2, 2, 3, 3]


def test_random_against_model() -> None:
    rng = random.Random(31)
    for _ in range(500):
        h: IntervalHeap[int] = IntervalHeap()
        model: list[int] = []
        for _ in range(rng.randrange(1, 60)):
            op = rng.randrange(3)
            if op == 0 or not model:
                x = rng.randrange(20)
                h.insert(x)
                model.append(x)
            elif op == 1:
                m = min(model)
                model.remove(m)
                assert h.extract_min() == m
            else:
                m = max(model)
                model.remove(m)
                assert h.extract_max() == m
            h.check_invariant()
            assert sorted(h.a) == sorted(model)
            if model:
                assert h.find_min() == min(model)
                assert h.find_max() == max(model)
