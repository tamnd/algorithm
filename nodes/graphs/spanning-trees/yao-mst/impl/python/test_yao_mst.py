# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-mst/. The authors are listed in prov/CXZBFW.jsonl.

import itertools
import random

from yao_mst import _split, yao_mst

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def kruskal_oracle(n, edges):
    """The unique minimum spanning forest for the order (w, index)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    out = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i)):
        a, b = find(edges[i][0]), find(edges[i][1])
        if a != b:
            parent[a] = b
            out.append(i)
    return sorted(out)


def components(n, edges, idx):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in idx:
        parent[find(edges[i][0])] = find(edges[i][1])
    return len({find(x) for x in range(n)})


def brute_min_weight(n, edges):
    """Least weight of a spanning forest with the components of the graph, by trying all edge sets."""
    target = components(n, edges, range(len(edges)))
    size = n - target
    best = None
    for sub in itertools.combinations(range(len(edges)), size):
        if components(n, edges, sub) == target:
            w = sum(edges[i][2] for i in sub)
            best = w if best is None or w < best else best
    return best


def weight(edges, idx):
    return sum(edges[i][2] for i in idx)


def test_example_all_phase_counts():
    for p in (0, 1, 2, 3):
        assert yao_mst(6, EXAMPLE, phases=p) == [1, 2, 3, 5, 8]
    assert yao_mst(6, EXAMPLE) == [1, 2, 3, 5, 8]


def test_example_groups():
    key = lambda i: (EXAMPLE[i][2], i)
    assert _split([1, 2, 4, 5], 3, key) == [[2], [1], [4, 5]]


def test_split_is_ordered_and_balanced():
    rng = random.Random(7)
    for _ in range(300):
        d = rng.randint(0, 40)
        k = rng.randint(1, 9)
        keys = [rng.randint(0, 5) for _ in range(d)]
        key = lambda i: (keys[i], i)
        gs = _split(list(range(d)), k, key)
        assert len(gs) == k
        assert sorted(x for g in gs for x in g) == list(range(d))
        for g, h in zip(gs, gs[1:]):
            if g and h:
                assert max(map(key, g)) < min(map(key, h))
        assert max(len(g) for g in gs) <= -(-d // k) + 1


def test_empty_and_single():
    assert yao_mst(0, []) == []
    assert yao_mst(1, []) == []
    assert yao_mst(1, [(0, 0, 5)]) == []
    assert yao_mst(2, [(0, 1, 3)]) == [0]


def test_ties_all_equal():
    k4 = [(a, b, 1) for a, b in itertools.combinations(range(4), 2)]
    for p in (0, 1, 2):
        assert yao_mst(4, k4, phases=p) == kruskal_oracle(4, k4)


def test_parallel_edges_and_loops():
    edges = [(0, 1, 5), (0, 1, 2), (1, 1, -9), (1, 2, 2), (2, 0, 2)]
    assert yao_mst(3, edges, phases=0) == [1, 3]


def test_negative_weights():
    edges = [(0, 1, -3), (1, 2, -1), (0, 2, -2)]
    assert yao_mst(3, edges, phases=0) == [0, 2]


def test_disconnected():
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (3, 4, 1), (4, 5, 1), (3, 5, 1)]
    for p in (0, 1, 5):
        out = yao_mst(7, edges, phases=p)
        assert out == kruskal_oracle(7, edges)
        assert len(out) == 7 - 3


def test_random_against_brute_force():
    rng = random.Random(1975)
    for _ in range(600):
        n = rng.randint(1, 7)
        m = rng.randint(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 4)) for _ in range(m)]
        p = rng.choice([None, 0, 1, 2])
        out = yao_mst(n, edges, phases=p)
        assert out == kruskal_oracle(n, edges)
        assert len(out) == n - components(n, edges, range(m))
        assert weight(edges, out) == brute_min_weight(n, edges)


def test_random_large_against_kruskal():
    rng = random.Random(23)
    for _ in range(60):
        n = rng.randint(2, 120)
        m = rng.randint(0, 400)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 20)) for _ in range(m)]
        for p in (None, 0):
            assert yao_mst(n, edges, phases=p) == kruskal_oracle(n, edges)
