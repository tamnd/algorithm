# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-heap/. The authors are listed in prov/1QKQ6A.jsonl.

import random

import pytest

from binary_heap import BinaryHeap


def test_example() -> None:
    h: BinaryHeap[int] = BinaryHeap()
    h.build([5, 3, 8, 1, 9, 2])
    assert h.a == [1, 3, 2, 5, 9, 8]
    h.insert(4)
    assert h.a == [1, 3, 2, 5, 9, 8, 4]
    h.insert(0)
    assert h.a == [0, 1, 2, 3, 9, 8, 4, 5]
    assert h.extract_min() == 0
    assert h.a == [1, 3, 2, 5, 9, 8, 4]
    h.decrease_key(4, 0)
    assert h.a == [0, 1, 2, 5, 3, 8, 4]
    assert h.extract_min() == 0
    assert h.a == [1, 3, 2, 5, 4, 8]
    h.check_invariant()


def test_edges() -> None:
    h: BinaryHeap[int] = BinaryHeap()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.extract_min()
    h.build([])
    assert len(h) == 0
    h.insert(7)
    assert h.find_min() == 7
    assert h.extract_min() == 7
    assert len(h) == 0
    h.build([2, 2, 2, 2])
    assert [h.extract_min() for _ in range(4)] == [2, 2, 2, 2]
    h.build([3, 1])
    with pytest.raises(ValueError):
        h.decrease_key(1, 5)
    h.build([1, 2, 3])
    h.decrease_key(2, 3)
    h.check_invariant()


def test_sorted_and_reversed() -> None:
    for keys in (list(range(50)), list(range(50, 0, -1))):
        h: BinaryHeap[int] = BinaryHeap()
        for k in keys:
            h.insert(k)
            h.check_invariant()
        assert [h.extract_min() for _ in keys] == sorted(keys)


def test_random_against_model() -> None:
    rng = random.Random(6121)
    for _ in range(500):
        h: BinaryHeap[int] = BinaryHeap()
        model: list[int] = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        h.build(model)
        h.check_invariant()
        for _ in range(rng.randint(0, 40)):
            op = rng.random()
            if op < 0.4:
                k = rng.randint(-20, 20)
                h.insert(k)
                model.append(k)
            elif op < 0.75:
                if model:
                    want = min(model)
                    assert h.find_min() == want
                    assert h.extract_min() == want
                    model.remove(want)
                else:
                    with pytest.raises(IndexError):
                        h.extract_min()
            elif model:
                i = rng.randrange(len(h))
                old = h.a[i]
                k = old - rng.randint(0, 10)
                h.decrease_key(i, k)
                model.remove(old)
                model.append(k)
            h.check_invariant()
            assert sorted(h.a) == sorted(model)
