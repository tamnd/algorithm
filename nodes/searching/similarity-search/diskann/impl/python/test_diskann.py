# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diskann/. The authors are listed in prov/KR79N8.jsonl.

import math
import random

from diskann import Vamana

PTS = [(0, 0), (2, 0), (4, 0), (6, 0), (0, 3), (3, 3), (6, 3), (1, 6), (5, 6)]


def test_example() -> None:
    v = Vamana(PTS)
    assert v.start == 5
    v.build_full(1.5)
    assert v.adj[0] == [1, 4, 5]
    assert v.adj[5] == [4, 6, 1, 7, 8, 3]
    res, visited = v.greedy_search((5.5, 5), 1, 1, start=0)
    assert res == [8] and visited == {0, 5, 8}


def test_edge_cases() -> None:
    v = Vamana([])
    assert v.start == -1
    v = Vamana([(1, 1)])
    v.build(R=3, L=5, alpha=1.2, rng=random.Random(0))
    assert v.adj == [[]]
    assert v.greedy_search((0, 0), 1, 3) == ([0], {0})


def test_alpha_shortcut_and_approximation() -> None:
    rng = random.Random(79)
    for _ in range(500):
        n = rng.randint(2, 14)
        pts = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]
        alpha = rng.choice([1.2, 1.5, 2.0, 3.0])
        v = Vamana(pts)
        v.build_full(alpha)
        # alpha-shortcut property of full robust pruning
        for p in range(n):
            for x in range(n):
                if x != p and x not in v.adj[p]:
                    assert any(alpha * math.dist(pts[y], pts[x]) <= math.dist(pts[p], pts[x])
                               for y in v.adj[p])
        # Theorem: greedy search with L = 1 is (alpha + 1)/(alpha - 1)-approximate.
        q = (rng.uniform(-2, 12), rng.uniform(-2, 12))
        best = min(math.dist(q, p) for p in pts)
        res, _ = v.greedy_search(q, 1, 1, start=rng.randrange(n))
        assert math.dist(q, pts[res[0]]) <= (alpha + 1) / (alpha - 1) * best + 1e-9


def test_vamana_build() -> None:
    rng = random.Random(8)
    pts = [(rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(300)]
    v = Vamana(pts)
    v.build(R=8, L=20, alpha=1.2, rng=rng)
    assert all(len(a) <= 8 and len(set(a)) == len(a) and i not in a for i, a in enumerate(v.adj))
    hits = 0
    for _ in range(100):
        q = (rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))
        want = min(range(300), key=lambda i: math.dist(q, pts[i]))
        res, visited = v.greedy_search(q, 1, 20)
        hits += res == [want]
        assert len(visited) < 300
    assert hits >= 90
