# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-ary-heap/. The authors are listed in prov/Y99BAR.jsonl.

import heapq
import random

import pytest

from d_ary_heap import DaryHeap


def test_example_d3() -> None:
    h: DaryHeap[int] = DaryHeap(3)
    h.build([5, 3, 8, 1, 9, 2, 7, 6, 4])
    assert h.a == [1, 2, 4, 5, 9, 3, 7, 6, 8]
    h.insert(0)
    assert h.a == [0, 2, 1, 5, 9, 3, 7, 6, 8, 4]
    assert h.extract_min() == 0
    assert h.a == [1, 2, 4, 5, 9, 3, 7, 6, 8]
    h.decrease_key(7, 0)
    assert h.a == [0, 2, 1, 5, 9, 3, 7, 4, 8]
    h.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        DaryHeap(1)
    h: DaryHeap[int] = DaryHeap(2)
    with pytest.raises(IndexError):
        h.extract_min()
    with pytest.raises(IndexError):
        h.find_min()
    h.build([])
    assert len(h) == 0
    h.build([7])
    assert h.find_min() == 7
    with pytest.raises(ValueError):
        h.decrease_key(0, 8)
    with pytest.raises(IndexError):
        h.decrease_key(1, 0)
    assert h.extract_min() == 7 and len(h) == 0


def test_random_against_heapq() -> None:
    rng = random.Random(1975)
    for case in range(700):
        d = 2 + case % 6
        h: DaryHeap[int] = DaryHeap(d)
        model: list[int] = []
        if rng.random() < 0.5:
            keys = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
            h.build(keys)
            model = list(keys)
            heapq.heapify(model)
            h.check_invariant()
        for _ in range(rng.randint(0, 60)):
            op = rng.random()
            if op < 0.45:
                k = rng.randint(-50, 50)
                h.insert(k)
                heapq.heappush(model, k)
            elif op < 0.8:
                if model:
                    assert h.extract_min() == heapq.heappop(model)
            elif h.a:
                i = rng.randrange(len(h.a))
                old = h.a[i]
                k = old - rng.randint(0, 30)
                model.remove(old)
                heapq.heapify(model)
                heapq.heappush(model, k)
                h.decrease_key(i, k)
            h.check_invariant()
            assert sorted(h.a) == sorted(model)
            if model:
                assert h.find_min() == model[0]
