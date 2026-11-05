# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pettie-ramachandran-mst/. The authors are listed in prov/BJQNXT.jsonl.

import itertools
import random

from pettie_ramachandran_mst import _kruskal, _partition, pettie_ramachandran_mst

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
    best = None
    for sub in itertools.combinations(range(len(edges)), n - target):
        if components(n, edges, sub) == target:
            w = sum(edges[i][2] for i in sub)
            best = w if best is None or w < best else best
    return best


def test_example():
    assert pettie_ramachandran_mst(6, EXAMPLE) == [1, 2, 3, 5, 8]
    assert pettie_ramachandran_mst(6, EXAMPLE, r=3) == [1, 2, 3, 5, 8]


def test_example_trace_with_corruption():
    es = [(u, v, w, i) for i, (u, v, w) in enumerate(EXAMPLE)]
    corrupt = lambda i: 5 if i == 2 else 0
    pieces, bad, links = _partition(6, es, 3, corrupt)
    assert pieces == [[0, 1, 2], [3], [4, 5]]
    assert bad == {2}
    assert sorted(e[3] for e in links) == [3, 5]
    assert pettie_ramachandran_mst(6, EXAMPLE, r=3, corrupt=corrupt) == [1, 2, 3, 5, 8]


def test_partition_forest_is_in_msf_without_corrupted():
    rng = random.Random(2002)
    for _ in range(300):
        n = rng.randint(1, 15)
        m = rng.randint(0, 40)
        es = [(rng.randrange(n), rng.randrange(n), rng.randint(-4, 6), i) for i in range(m)]
        es = [e for e in es if e[0] != e[1]]
        p = rng.random()
        corrupt = lambda i: rng.random() * 10 if rng.random() < p else 0
        r = rng.randint(1, 6)
        pieces, bad, links = _partition(n, es, r, corrupt)
        assert sorted(x for pc in pieces for x in pc) == list(range(n))
        assert all(len(pc) <= max(r, 1) for pc in pieces)
        clean = [e for e in es if e[3] not in bad]
        msf = {e[3] for e in _kruskal(n, clean)}
        assert all(e[3] in msf and e[3] not in bad for e in links)


def test_empty_and_small():
    assert pettie_ramachandran_mst(0, []) == []
    assert pettie_ramachandran_mst(1, [(0, 0, 1)]) == []
    assert pettie_ramachandran_mst(2, [(0, 1, 7)]) == [0]


def test_ties_all_equal():
    k5 = [(a, b, 1) for a, b in itertools.combinations(range(5), 2)]
    for r in (1, 2, 3):
        assert pettie_ramachandran_mst(5, k5, r=r) == kruskal_oracle(5, k5)


def test_parallel_loops_negative():
    edges = [(0, 1, 5), (0, 1, -2), (1, 1, -9), (1, 2, -2), (2, 0, -2)]
    assert pettie_ramachandran_mst(3, edges, r=2) == [1, 3]


def test_disconnected():
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (3, 4, 1), (4, 5, 1), (3, 5, 1)]
    out = pettie_ramachandran_mst(7, edges, r=2, corrupt=lambda i: 3 if i % 2 else 0)
    assert out == kruskal_oracle(7, edges)
    assert len(out) == 7 - 3


def test_all_corrupted():
    rng = random.Random(4)
    for _ in range(50):
        n = rng.randint(2, 12)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 5)) for _ in range(rng.randint(0, 30))]
        assert pettie_ramachandran_mst(n, edges, r=4, corrupt=lambda i: 100) == kruskal_oracle(n, edges)


def test_random_against_brute_force():
    rng = random.Random(2000)
    for _ in range(600):
        n = rng.randint(1, 7)
        m = rng.randint(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 4)) for _ in range(m)]
        p = rng.random()
        corrupt = lambda i: rng.random() * 8 if rng.random() < p else 0
        r = rng.choice([None, 1, 2, 3, 5])
        out = pettie_ramachandran_mst(n, edges, r=r, corrupt=corrupt)
        assert out == kruskal_oracle(n, edges)
        assert sum(edges[i][2] for i in out) == brute_min_weight(n, edges)


def test_random_large_against_kruskal():
    rng = random.Random(31)
    for _ in range(80):
        n = rng.randint(2, 150)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 30)) for _ in range(rng.randint(0, 500))]
        p = rng.random()
        corrupt = lambda i: rng.random() * 20 if rng.random() < p else 0
        assert pettie_ramachandran_mst(n, edges, r=rng.choice([None, 2, 4, 8]), corrupt=corrupt) == kruskal_oracle(n, edges)
