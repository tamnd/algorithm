# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-queue/. The authors are listed in prov/VVXG5M.jsonl.

import random

import pytest

from min_queue import MinQueue, MonotonicMinQueue


def test_page_example() -> None:
    q: MinQueue[int] = MinQueue()
    for x in [4, 2, 5]:
        q.enqueue(x)
    assert q.min() == 2
    assert q.inp.s == [(4, 4), (2, 2), (5, 2)]
    assert q.dequeue() == 4
    assert q.moves == 3
    assert q.out.s == [(5, 5), (2, 2)]
    assert q.min() == 2
    q.enqueue(1)
    assert q.min() == 1
    assert q.dequeue() == 2
    assert q.min() == 1
    assert q.dequeue() == 5
    assert q.min() == 1
    assert q.dequeue() == 1
    assert q.moves == 4
    assert len(q) == 0


def test_edges() -> None:
    q: MinQueue[int] = MinQueue()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.min()
    for x in [3, 3, 3]:
        q.enqueue(x)
    assert q.dequeue() == 3 and q.min() == 3


def test_amortized_moves() -> None:
    q: MinQueue[int] = MinQueue()
    rng = random.Random(5)
    enq = 0
    for _ in range(10000):
        if len(q) and rng.random() < 0.5:
            q.dequeue()
        else:
            q.enqueue(rng.randint(0, 100))
            enq += 1
    assert q.moves <= enq


def test_sliding_window_minimum() -> None:
    a = [5, 1, 4, 2, 6, 3, 0, 7]
    q: MinQueue[int] = MinQueue()
    out = []
    for i, x in enumerate(a):
        q.enqueue(x)
        if i >= 3:
            q.dequeue()
        if i >= 2:
            out.append(q.min())
    assert out == [min(a[i : i + 3]) for i in range(len(a) - 2)]


def test_random_against_model() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        q: MinQueue[int] = MinQueue()
        m: MonotonicMinQueue[int] = MonotonicMinQueue()
        model: list[int] = []
        for _ in range(60):
            if model and rng.random() < 0.45:
                want = model.pop(0)
                assert q.dequeue() == want
                assert m.dequeue() == want
            else:
                x = rng.randint(0, 6)
                q.enqueue(x)
                m.enqueue(x)
                model.append(x)
            assert q.to_list() == model
            if model:
                assert q.min() == min(model) == m.min()
