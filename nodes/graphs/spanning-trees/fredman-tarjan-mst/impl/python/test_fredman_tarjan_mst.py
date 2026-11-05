# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fredman-tarjan-mst/. The authors are listed in prov/37AZFW.jsonl.

import heapq
import random

from fredman_tarjan_mst import _FibHeap, fredman_tarjan_mst

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def kruskal_weight(n, edges):
    """The weight and the number of edges of a minimum spanning forest."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, count = 0, 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            total += w
            count += 1
    return total, count


def is_forest(n, edges, chosen):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in chosen:
        a, b = find(edges[i][0]), find(edges[i][1])
        if a == b:
            return False
        parent[a] = b
    return True


def check(n, edges, chosen):
    assert len(set(chosen)) == len(chosen)
    assert is_forest(n, edges, chosen)
    assert (sum(edges[i][2] for i in chosen), len(chosen)) == kruskal_weight(n, edges)


def test_example():
    assert fredman_tarjan_mst(6, EXAMPLE) == [1, 2, 3, 5, 8]


def test_example_two_phases():
    log = []
    assert fredman_tarjan_mst(6, EXAMPLE, heap_limit=1, log=log) == [1, 2, 3, 5, 8]
    assert [(t, m, trees) for t, m, _, trees in log] == [(6, 9, 2), (2, 1, 1)]


def test_trivial_graphs():
    assert fredman_tarjan_mst(0, []) == []
    assert fredman_tarjan_mst(1, []) == []
    assert fredman_tarjan_mst(1, [(0, 0, 3)]) == []
    assert fredman_tarjan_mst(3, []) == []


def test_parallel_edges_and_loops():
    edges = [(0, 1, 5), (0, 1, 2), (1, 1, -9), (1, 2, 2), (2, 1, 1)]
    assert fredman_tarjan_mst(3, edges) == [1, 4]


def test_ties_take_smaller_index():
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 1)]
    assert fredman_tarjan_mst(3, edges) == [0, 1]


def test_disconnected():
    edges = [(0, 1, 3), (2, 3, 1), (3, 4, 2), (2, 4, 0)]
    got = fredman_tarjan_mst(6, edges)
    check(6, edges, got)
    assert got == [0, 1, 3]


def test_fibonacci_heap_sorts():
    rng = random.Random(3)
    for _ in range(200):
        h = _FibHeap()
        ref = []
        nodes = []
        for j in range(rng.randint(1, 40)):
            key = rng.randint(0, 50)
            nodes.append([h.insert((key, j), j), key, j, True])
        for _ in range(rng.randint(0, 30)):
            entry = rng.choice(nodes)
            if entry[3]:
                if rng.random() < 0.5:
                    key, item = h.extract_min()
                    best = min((e for e in nodes if e[3]), key=lambda e: (e[1], e[2]))
                    assert key == (best[1], best[2]) and item == best[2]
                    best[3] = False
                else:
                    entry[1] = rng.randint(-20, entry[1])
                    h.decrease_key(entry[0], (entry[1], entry[2]))
        ref = sorted((e[1], e[2]) for e in nodes if e[3])
        out = [h.extract_min()[0] for _ in range(h.size)]
        assert out == ref
        assert heapq.nsmallest(len(ref), ref) == out


def test_random_against_kruskal():
    rng = random.Random(20261105)
    for trial in range(700):
        n = rng.randint(1, 12)
        m = rng.randint(0, 30)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 6)) for _ in range(m)]
        limit = None if trial % 3 == 0 else rng.randint(1, 4)
        check(n, edges, fredman_tarjan_mst(n, edges, heap_limit=limit))


def test_large_sparse_many_phases():
    rng = random.Random(11)
    for _ in range(20):
        n = rng.randint(50, 200)
        edges = [(v, rng.randrange(v), rng.randint(0, 10**6)) for v in range(1, n)]
        edges += [(rng.randrange(n), rng.randrange(n), rng.randint(0, 10**6)) for _ in range(n // 2)]
        log = []
        got = fredman_tarjan_mst(n, edges, log=log)
        check(n, edges, got)
        assert len(got) == n - 1
        for t, m, k, trees in log:
            assert trees <= max(1, 2 * m / k)
