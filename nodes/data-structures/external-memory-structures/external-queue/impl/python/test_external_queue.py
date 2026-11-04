# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-queue/. The authors are listed in prov/HQ3Q31.jsonl.

import random
from collections import deque

import pytest

from external_queue import ExternalQueue


def test_example() -> None:
    q: ExternalQueue[int] = ExternalQueue(3)
    for x in range(1, 8):
        q.enqueue(x)
        q.check_invariant()
    assert list(q.disk) == [[1, 2, 3], [4, 5, 6]] and q.tail == [7]
    assert q.writes == 2 and q.reads == 0
    assert q.dequeue() == 1
    assert q.reads == 1 and list(q.head) == [2, 3]
    q.enqueue(8)
    assert [q.dequeue() for _ in range(5)] == [2, 3, 4, 5, 6]
    assert q.reads == 2
    assert q.dequeue() == 7
    assert q.reads == 2 and list(q.head) == [8] and q.tail == []
    assert q.front() == 8 and len(q) == 1
    assert q.dequeue() == 8 and len(q) == 0
    assert (q.reads, q.writes) == (2, 2)


def test_edges() -> None:
    with pytest.raises(ValueError):
        ExternalQueue(0)
    q: ExternalQueue[str] = ExternalQueue(1)
    with pytest.raises(IndexError):
        q.dequeue()
    q.enqueue("a")
    assert q.writes == 1
    assert q.front() == "a" and q.dequeue() == "a"
    with pytest.raises(IndexError):
        q.front()


def test_alternating_is_free() -> None:
    q: ExternalQueue[int] = ExternalQueue(16)
    for x in range(1000):
        q.enqueue(x)
        assert q.dequeue() == x
    # each block of 16 items is written once and read once at most
    assert q.reads + q.writes <= 2 * 1000 // 16


def test_against_deque() -> None:
    rng = random.Random(11)
    for _ in range(500):
        B = rng.randrange(1, 6)
        q: ExternalQueue[int] = ExternalQueue(B)
        model: deque[int] = deque()
        n = rng.randrange(1, 200)
        p = rng.random()
        enq = 0
        for _ in range(n):
            if model and rng.random() < p:
                assert q.dequeue() == model.popleft()
            else:
                x = rng.randrange(1000)
                q.enqueue(x)
                model.append(x)
                enq += 1
            q.check_invariant()
            assert q.items() == list(model) and len(q) == len(model)
        assert q.writes <= enq // B
        assert q.reads <= q.writes
