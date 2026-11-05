# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-mst/. The authors are listed in prov/T77RVB.jsonl.

import itertools
import random

from chazelle_mst import SoftHeap, chazelle_mst

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def kruskal_oracle(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    out = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i)):
        u, v, _ = edges[i]
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.append(i)
    return sorted(out)


def components(n, edges, chosen):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in chosen:
        parent[find(edges[i][0])] = find(edges[i][1])
    return len({find(x) for x in range(n)})


def brute_force_weight(n, edges):
    """Least weight of a spanning forest with as many edges as possible."""
    k = n - components(n, edges, range(len(edges)))
    best = None
    for c in itertools.combinations(range(len(edges)), k):
        if components(n, edges, c) == n - k:
            w = sum(edges[i][2] for i in c)
            best = w if best is None or w < best else best
    return best if best is not None else 0


def test_example():
    for s, t in ((2, 0), (3, 0), (4, 1), (8, 2), (3, 10)):
        assert chazelle_mst(6, EXAMPLE, piece_size=s, t=t, base=0) == [1, 2, 3, 5, 8]


def test_example_trace_with_corruption():
    log = []
    assert chazelle_mst(6, EXAMPLE, piece_size=3, t=0, base=0, log=log) == [1, 2, 3, 5, 8]
    assert log == [(6, 9, 2, 6)]


def test_soft_heap_contract():
    rng = random.Random(7)
    for t in (0, 1, 3):
        for _ in range(60):
            heap = SoftHeap(t)
            ckey_seen = {}
            inserted = 0
            for _ in range(rng.randint(1, 120)):
                if heap and rng.random() < 0.4:
                    key, p, ckey = heap.delete_min()
                    assert ckey >= key
                    assert ckey >= ckey_seen.get(p, key)
                    rest = heap.remaining()
                    assert all(c >= ckey for _, _, c in rest)
                    for k2, p2, c2 in rest:
                        assert c2 >= k2 and c2 >= ckey_seen.get(p2, k2)
                        ckey_seen[p2] = c2
                else:
                    heap.insert((rng.random(), inserted), inserted)
                    inserted += 1


def test_soft_heap_exact_when_threshold_large():
    rng = random.Random(3)
    keys = [rng.random() for _ in range(200)]
    heap = SoftHeap(10)
    for i, k in enumerate(keys):
        heap.insert(k, i)
    out = []
    while heap:
        key, _, ckey = heap.delete_min()
        assert key == ckey
        out.append(key)
    assert out == sorted(keys)


def test_soft_heap_corrupts_with_small_threshold():
    heap = SoftHeap(0)
    for i in range(64):
        heap.insert(i, i)
    assert sum(1 for k, _, c in heap.remaining() if c != k) > 0


def test_disconnected_gives_forest():
    edges = [(0, 1, 5), (1, 2, 1), (0, 2, 2), (3, 4, 7), (4, 5, 1), (3, 5, 1)]
    for t in (0, 2):
        got = chazelle_mst(7, edges, piece_size=2, t=t, base=0)
        assert got == kruskal_oracle(7, edges) == [1, 2, 4, 5]


def test_ties_parallel_edges_and_loops():
    edges = [(0, 1, 1), (0, 1, 1), (1, 2, 1), (2, 0, 1), (2, 2, 0), (2, 3, 1), (3, 0, 1)]
    for t in (0, 1, 5):
        assert chazelle_mst(4, edges, piece_size=2, t=t, base=0) == kruskal_oracle(4, edges) == [0, 2, 5]


def test_trivial_inputs():
    assert chazelle_mst(0, []) == []
    assert chazelle_mst(1, [(0, 0, 3)]) == []
    assert chazelle_mst(3, []) == []


def test_random_against_kruskal():
    rng = random.Random(20261105)
    for _ in range(700):
        n = rng.randint(1, 40)
        m = rng.randint(0, 120)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 6)) for _ in range(m)]
        expect = kruskal_oracle(n, edges)
        got = chazelle_mst(n, edges, piece_size=rng.choice([2, 3, 5, 8]), t=rng.choice([0, 1, 2, 4]),
                           base=rng.choice([0, 3, 8]))
        assert got == expect


def test_random_small_against_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 6)
        m = rng.randint(0, 8)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 4)) for _ in range(m)]
        got = chazelle_mst(n, edges, piece_size=2, t=0, base=0)
        assert components(n, edges, got) == components(n, edges, range(m))
        assert len(got) == n - components(n, edges, got)
        assert sum(edges[i][2] for i in got) == brute_force_weight(n, edges)
