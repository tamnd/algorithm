# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-buffer/. The authors are listed in prov/9NS9WP.jsonl.

import random

import pytest

from circular_buffer import CircularBuffer


def test_page_example() -> None:
    B: CircularBuffer[int] = CircularBuffer(4)
    for x in (1, 2, 3):
        B.enqueue(x)
    assert B.dequeue() == 1 and B.h == 1
    B.enqueue(4)
    B.enqueue(5)
    assert B.a == [5, 2, 3, 4] and list(B) == [2, 3, 4, 5]
    with pytest.raises(OverflowError):
        B.enqueue(6)
    assert B.dequeue() == 2
    B.push_front(9)
    assert B.h == 1 and B.a == [5, 9, 3, 4] and list(B) == [9, 3, 4, 5]
    assert B.pop_back() == 5
    assert B.get(2) == 4 and list(B) == [9, 3, 4]
    B.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        CircularBuffer(0)
    B: CircularBuffer[str] = CircularBuffer(1)
    with pytest.raises(IndexError):
        B.dequeue()
    with pytest.raises(IndexError):
        B.pop_back()
    with pytest.raises(IndexError):
        B.get(0)
    B.push_front("a")
    assert B.is_full()
    with pytest.raises(OverflowError):
        B.push_front("b")
    assert B.pop_back() == "a" and len(B) == 0
    B.check_invariant()


def test_random_against_list() -> None:
    rng = random.Random(99)
    for _ in range(600):
        cap = rng.randrange(1, 8)
        B: CircularBuffer[int] = CircularBuffer(cap)
        model: list[int] = []
        for _ in range(rng.randrange(1, 50)):
            op = rng.randrange(5)
            x = rng.randrange(100)
            if op == 0:
                if len(model) == cap:
                    with pytest.raises(OverflowError):
                        B.enqueue(x)
                else:
                    B.enqueue(x); model.append(x)
            elif op == 1:
                if len(model) == cap:
                    with pytest.raises(OverflowError):
                        B.push_front(x)
                else:
                    B.push_front(x); model.insert(0, x)
            elif op == 2 and model:
                assert B.dequeue() == model.pop(0)
            elif op == 3 and model:
                assert B.pop_back() == model.pop()
            elif op == 4 and model:
                i = rng.randrange(len(model))
                assert B.get(i) == model[i]
            B.check_invariant()
            assert list(B) == model
