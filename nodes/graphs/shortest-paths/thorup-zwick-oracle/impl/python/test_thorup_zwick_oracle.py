# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thorup-zwick-oracle/. The authors are listed in prov/Q2T1JE.jsonl.

import heapq
import math
import random

import pytest

from thorup_zwick_oracle import ThorupZwickOracle

A, B, C, D, E, F = range(6)
EXAMPLE = [(A, B, 2), (B, C, 2), (C, D, 1), (D, E, 2), (E, F, 1), (F, A, 3), (B, E, 4)]


def all_pairs(n, edges):
    """Independent oracle: Dijkstra from every vertex."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    table = []
    for s in range(n):
        dist = [math.inf] * n
        heap = [(0, s)]
        while heap:
            d, u = heapq.heappop(heap)
            if dist[u] <= d:
                continue
            dist[u] = d
            for v, w in adj[u]:
                heapq.heappush(heap, (d + w, v))
        table.append(dist)
    return table


def test_example():
    o = ThorupZwickOracle(6, EXAMPLE, 2, levels=[{C, F}])
    assert o.bunch[A] == {A: 0, B: 2, C: 4, F: 3}
    assert o.bunch[B] == {B: 0, C: 2, F: 5}
    assert o.query(A, B) == 6  # stretch exactly 3 = 2k - 1
    assert o.query(B, A) == 2  # the answer depends on the order
    assert o.query(C, D) == 1
    assert o.size() == 17


def test_k1_is_exact():
    o = ThorupZwickOracle(6, EXAMPLE, 1)
    d = all_pairs(6, EXAMPLE)
    assert all(o.query(u, v) == d[u][v] for u in range(6) for v in range(6))


def test_unreachable_and_single_vertex():
    edges = [(0, 1, 1.5), (2, 3, 0)]
    for k in (1, 2, 3):
        for seed in range(5):
            o = ThorupZwickOracle(4, edges, k, seed=seed)
            assert o.query(0, 2) == math.inf and o.query(3, 1) == math.inf
            assert o.query(2, 3) == 0
    assert ThorupZwickOracle(1, [], 3).query(0, 0) == 0


def test_rejects_bad_input():
    for bad in (-1, -0.5, math.inf, math.nan, "2", True):
        with pytest.raises(ValueError):
            ThorupZwickOracle(2, [(0, 1, bad)], 2)
    for k in (0, -1, 1.5):
        with pytest.raises(ValueError):
            ThorupZwickOracle(2, [(0, 1, 1)], k)
    with pytest.raises(ValueError):
        ThorupZwickOracle(3, [], 3, levels=[{0}, {1}])


def test_random_stretch_and_bunches():
    rng = random.Random(20261105)
    for case in range(600):
        n = rng.randint(1, 14)
        m = rng.randint(0, 3 * n)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 2, 3, 5, 8, 2.5]))
                 for _ in range(m)]
        k = rng.randint(1, 4)
        o = ThorupZwickOracle(n, edges, k, seed=case)
        d = all_pairs(n, edges)
        A = o.levels
        for v in range(n):
            # the bunch matches its definition, computed from the exact table
            expect = {}
            for i in range(k):
                bound = min((d[a][v] for a in A[i + 1]), default=math.inf)
                for w in A[i] - A[i + 1]:
                    if d[w][v] < bound:
                        expect[w] = d[w][v]
            assert o.bunch[v] == expect
        for u in range(n):
            for v in range(n):
                e = o.query(u, v)
                if d[u][v] == math.inf:
                    assert e == math.inf
                else:
                    assert d[u][v] <= e <= (2 * k - 1) * d[u][v]
                    if k == 1:
                        assert e == d[u][v]
