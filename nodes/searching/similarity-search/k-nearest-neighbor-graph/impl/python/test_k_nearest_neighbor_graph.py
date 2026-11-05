# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-nearest-neighbor-graph/. The authors are listed in prov/CST612.jsonl.

import math
import random

from k_nearest_neighbor_graph import KNNGraph

LINE = [(0, 0), (1, 0), (3, 0), (6, 0), (10, 0), (11, 0)]


def oracle_lists(points, k):
    out = []
    for i, p in enumerate(points):
        others = sorted((math.dist(p, x), j) for j, x in enumerate(points) if j != i)
        out.append([j for _, j in others[:k]])
    return out


def reachable(adj, starts):
    seen = set(starts)
    stack = list(starts)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def test_example() -> None:
    g = KNNGraph(LINE, 2)
    assert g.adj == [[1, 2], [0, 2], [1, 0], [2, 4], [5, 3], [4, 3]]
    assert [sorted(r) for r in g.reverse()] == [[1, 2], [0, 2], [0, 1, 3], [4, 5], [3, 5], [4]]
    assert g.search((9, 0), 1, ef=2, starts=[0]) == [(6.0, 2)]
    assert g.search((9, 0), 1, ef=2, starts=[5]) == [(1.0, 4)]
    assert reachable(g.adj, [0]) == {0, 1, 2}


def test_edge_cases() -> None:
    assert KNNGraph([], 3).adj == []
    assert KNNGraph([(0, 0)], 3).adj == [[]]
    assert KNNGraph([(0, 0), (1, 1)], 5).adj == [[1], [0]]


def test_random_against_oracle() -> None:
    rng = random.Random(612)
    for _ in range(500):
        n = rng.randint(1, 18)
        dim = rng.randint(1, 3)
        pts = [tuple(rng.randint(0, 6) for _ in range(dim)) for _ in range(n)]
        k = rng.randint(1, 5)
        g = KNNGraph(pts, k)
        assert g.adj == oracle_lists(pts, k)
        q = tuple(rng.uniform(-1, 7) for _ in range(dim))
        starts = rng.sample(range(n), rng.randint(1, min(3, n)))
        kk = rng.randint(1, 4)
        # Theorem: with ef >= n the search is exact on the reachable set.
        got = g.search(q, kk, ef=n, starts=starts)
        reach = reachable(g.adj, starts)
        want = sorted((math.dist(q, pts[j]), j) for j in reach)[:kk]
        assert got == want
        # Lemma: with any ef the first answer is a local minimum.
        ef = rng.randint(1, 4)
        res = g.search(q, kk, ef=ef, starts=starts)
        d0, w = res[0]
        assert all(math.dist(q, pts[e]) >= d0 for e in g.adj[w])
        assert 1 <= len(res) <= min(kk, ef) and res == sorted(res)
