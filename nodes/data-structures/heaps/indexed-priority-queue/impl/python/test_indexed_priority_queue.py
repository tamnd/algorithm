# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indexed-priority-queue/. The authors are listed in prov/QQ610A.jsonl.

import heapq
import random

import pytest

from indexed_priority_queue import IndexedMinPQ


def test_example() -> None:
    q: IndexedMinPQ[int] = IndexedMinPQ(6)
    for i, k in [(0, 50), (1, 30), (2, 40), (3, 10), (4, 60)]:
        q.insert(i, k)
    assert q.pq == [3, 1, 2, 0, 4]
    assert q.qp == [3, 1, 2, 0, 4, -1]
    q.decrease_key(4, 5)
    assert q.pq == [4, 3, 2, 0, 1]
    assert q.qp == [3, 4, 2, 1, 0, -1]
    assert q.delete(3) == 10
    assert q.pq == [4, 1, 2, 0]
    assert q.qp == [3, 1, 2, -1, 0, -1]
    assert q.extract_min() == (4, 5)
    assert q.pq == [1, 0, 2]
    q.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        IndexedMinPQ(-1)
    q: IndexedMinPQ[int] = IndexedMinPQ(2)
    with pytest.raises(IndexError):
        q.extract_min()
    with pytest.raises(IndexError):
        q.min_index()
    with pytest.raises(IndexError):
        q.insert(2, 0)
    q.insert(0, 5)
    with pytest.raises(KeyError):
        q.insert(0, 1)
    with pytest.raises(ValueError):
        q.decrease_key(0, 6)
    with pytest.raises(KeyError):
        q.delete(1)
    assert q.min_index() == 0
    assert q.delete(0) == 5
    assert len(q) == 0
    q.insert(0, 3)
    assert q.key_of(0) == 3
    q.check_invariant()


def test_delete_last_cell() -> None:
    q: IndexedMinPQ[int] = IndexedMinPQ(3)
    q.insert(0, 1)
    q.insert(1, 2)
    assert q.delete(1) == 2
    q.check_invariant()
    assert q.extract_min() == (0, 1)


def test_dijkstra() -> None:
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randrange(1, 15)
        adj = [[(rng.randrange(n), rng.randrange(10)) for _ in range(rng.randrange(4))] for _ in range(n)]
        dist = [None] * n
        q: IndexedMinPQ[int] = IndexedMinPQ(n)
        q.insert(0, 0)
        best = {0: 0}
        while len(q):
            u, d = q.extract_min()
            dist[u] = d
            for v, w in adj[u]:
                if dist[v] is None and (v not in best or d + w < best[v]):
                    if q.contains(v):
                        q.decrease_key(v, d + w)
                    else:
                        q.insert(v, d + w)
                    best[v] = d + w
        ref = [None] * n
        h = [(0, 0)]
        while h:
            d, u = heapq.heappop(h)
            if ref[u] is not None:
                continue
            ref[u] = d
            for v, w in adj[u]:
                if ref[v] is None:
                    heapq.heappush(h, (d + w, v))
        assert dist == ref


def test_random_against_model() -> None:
    rng = random.Random(99)
    for _ in range(500):
        m = rng.randrange(1, 15)
        q: IndexedMinPQ[int] = IndexedMinPQ(m)
        model: dict[int, int] = {}
        for _ in range(rng.randrange(1, 50)):
            op = rng.randrange(5)
            free = [i for i in range(m) if i not in model]
            if (op == 0 or not model) and free:
                i, k = rng.choice(free), rng.randrange(30)
                q.insert(i, k)
                model[i] = k
            elif not model:
                continue
            elif op == 1:
                i, k = q.extract_min()
                assert k == min(model.values())
                assert model.pop(i) == k
            elif op == 2:
                i = rng.choice(sorted(model))
                k = rng.randrange(model[i] + 1)
                q.decrease_key(i, k)
                model[i] = k
            elif op == 3:
                i = rng.choice(sorted(model))
                k = rng.randrange(30)
                q.change_key(i, k)
                model[i] = k
            else:
                i = rng.choice(sorted(model))
                assert q.delete(i) == model.pop(i)
            q.check_invariant()
            assert len(q) == len(model)
            for i in range(m):
                assert q.contains(i) == (i in model)
