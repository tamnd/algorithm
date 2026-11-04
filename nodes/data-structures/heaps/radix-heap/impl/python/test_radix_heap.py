# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-heap/. The authors are listed in prov/FZSDPB.jsonl.

import heapq
import random

import pytest

from radix_heap import RadixHeap


def contents(h: RadixHeap[None]) -> dict[int, list[int]]:
    return {i: sorted(k for k, _ in b) for i, b in enumerate(h.buckets) if b}


def test_example() -> None:
    h: RadixHeap[None] = RadixHeap()
    for k in [5, 1, 7, 6, 13]:
        h.insert(k)
    h.check_invariant()
    assert contents(h) == {1: [1], 3: [5, 6, 7], 4: [13]}
    assert h.extract_min()[0] == 1
    assert contents(h) == {3: [5, 6, 7], 4: [13]}
    assert h.extract_min()[0] == 5
    assert contents(h) == {2: [6, 7], 4: [13]}
    h.insert(8)
    assert contents(h) == {2: [6, 7], 4: [8, 13]}
    assert h.extract_min()[0] == 6
    assert contents(h) == {1: [7], 4: [8, 13]}
    assert h.extract_min()[0] == 7
    assert h.extract_min()[0] == 8
    assert contents(h) == {3: [13]}
    assert h.extract_min()[0] == 13
    assert h.is_empty()
    assert h.moves == 10
    h.check_invariant()


def test_edge_cases() -> None:
    h: RadixHeap[str] = RadixHeap()
    with pytest.raises(IndexError):
        h.extract_min()
    with pytest.raises(IndexError):
        h.find_min()
    h.insert(0, "a")
    h.insert(0, "b")
    assert h.find_min() == 0
    assert {h.extract_min()[1], h.extract_min()[1]} == {"a", "b"}
    h.insert(10, "c")
    assert h.extract_min() == (10, "c")
    with pytest.raises(ValueError):
        h.insert(9, "d")
    big = 2**70 + 3
    h.insert(big, "e")
    h.insert(10, "f")
    assert h.extract_min() == (10, "f")
    assert h.extract_min() == (big, "e")


def test_random_monotone_against_heapq() -> None:
    rng = random.Random(1990)
    for _ in range(600):
        h: RadixHeap[int] = RadixHeap()
        ref: list[int] = []
        last = 0
        inserts = 0
        top = 1 << rng.randrange(1, 20)
        for _ in range(rng.randrange(1, 80)):
            if rng.random() < 0.6 or not ref:
                k = last + rng.randrange(top)
                h.insert(k, k)
                heapq.heappush(ref, k)
                inserts += 1
            else:
                k, v = h.extract_min()
                assert k == v == heapq.heappop(ref)
                last = k
            h.check_invariant()
            assert len(h) == len(ref)
        bits = max(1, (last + top).bit_length())
        assert h.moves <= inserts * bits


def test_dijkstra() -> None:
    rng = random.Random(42)
    for _ in range(100):
        n = rng.randrange(2, 40)
        adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
        for _ in range(rng.randrange(0, 4 * n)):
            u, v = rng.randrange(n), rng.randrange(n)
            adj[u].append((v, rng.randrange(0, 100)))

        def run(use_radix: bool) -> list[float]:
            dist = [float("inf")] * n
            dist[0] = 0
            h: RadixHeap[int] = RadixHeap()
            q: list[tuple[int, int]] = []
            if use_radix:
                h.insert(0, 0)
            else:
                q.append((0, 0))
            while (len(h) if use_radix else len(q)):
                d, u = h.extract_min() if use_radix else heapq.heappop(q)
                assert u is not None
                if d > dist[u]:
                    continue
                for v, w in adj[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        if use_radix:
                            h.insert(d + w, v)
                        else:
                            heapq.heappush(q, (d + w, v))
            return dist

        assert run(True) == run(False)
