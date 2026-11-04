# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-memory-priority-queue/. The authors are listed in prov/Z1W9D1.jsonl.

import heapq
import math
import random

import pytest

from external_memory_priority_queue import ExternalMemoryPriorityQueue, Leaf, Node


def shape(x: "Node | Leaf") -> str:
    if isinstance(x, Leaf):
        return "[" + " ".join(str(i[0]) for i in x.items) + "]"
    inner = " ".join(shape(c) for c in x.children)
    return "<" + " ".join(str(r[0]) for r in x.routing) + "|" + str(len(x.buf)) + ">(" + inner + ")"


def mem(q: ExternalMemoryPriorityQueue[int]) -> list[int]:
    return [i[0] for i in q.mem]


def test_example() -> None:
    q: ExternalMemoryPriorityQueue[int] = ExternalMemoryPriorityQueue(block_size=2, fanout=4)
    for k in [50, 20, 80, 10, 60, 30, 70, 40, 90]:
        q.insert(k)
    assert shape(q.root) == "<70|0>(<30 50|0>([10 20] [30 40] [50 60]) <90|0>([70 80] [90]))"
    for k in [15, 25, 35, 45, 55, 65, 75, 85, 5]:
        q.insert(k)
    assert shape(q.root) == "<70|0>(<30 50|7>([10 20] [30 40] [50 60]) <90|2>([70 80] [90]))"
    q.check_invariant()
    assert q.delete_min() == 5
    assert mem(q) == [10, 15, 20, 25, 30, 35, 40]
    assert shape(q.root) == "<70|0>(<55 65|0>([45 50] [55 60] [65]) <90|2>([70 80] [90]))"
    assert q.delete_min() == 10
    assert q.delete_min() == 15
    q.insert(12)
    assert mem(q) == [12, 20, 25, 30, 35]
    q.insert(1)
    assert mem(q) == [1, 12, 20, 25, 30]
    assert len(q.root.buf) == 2
    q.check_invariant()
    out = [q.delete_min() for _ in range(len(q))]
    assert out == [1, 12, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
    assert q.ios == 75
    q.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        ExternalMemoryPriorityQueue(0, 4)
    q: ExternalMemoryPriorityQueue[int] = ExternalMemoryPriorityQueue(1, 4)
    with pytest.raises(IndexError):
        q.delete_min()
    with pytest.raises(IndexError):
        q.find_min()
    for _ in range(10):
        q.insert(7)
    q.insert(3)
    assert q.find_min() == 3
    assert [q.delete_min() for _ in range(11)] == [3] + [7] * 10
    assert len(q) == 0
    q.check_invariant()


def test_against_heapq() -> None:
    rng = random.Random(5)
    for _ in range(500):
        B = rng.randrange(1, 4)
        m = rng.randrange(4, 7)
        q: ExternalMemoryPriorityQueue[int] = ExternalMemoryPriorityQueue(B, m)
        h: list[int] = []
        for i in range(rng.randrange(1, 300)):
            if h and rng.random() < 0.4:
                assert q.delete_min() == heapq.heappop(h)
            else:
                k = rng.randrange(60)
                q.insert(k)
                heapq.heappush(h, k)
            assert len(q) == len(h)
            if i % 29 == 0:
                q.check_invariant()
        q.check_invariant()
        assert [q.delete_min() for _ in range(len(h))] == sorted(h)


def test_io_bound() -> None:
    B, m = 16, 8
    q: ExternalMemoryPriorityQueue[int] = ExternalMemoryPriorityQueue(B, m)
    rng = random.Random(11)
    N = 30000
    keys = [rng.randrange(10**9) for _ in range(N)]
    for k in keys:
        q.insert(k)
    assert [q.delete_min() for _ in range(N)] == sorted(keys)
    n = N / B
    bound = n * math.log(n, m)
    # 2N operations; a binary heap on disk would pay about one I/O per level
    assert q.ios <= 8 * bound
    assert q.ios < N
