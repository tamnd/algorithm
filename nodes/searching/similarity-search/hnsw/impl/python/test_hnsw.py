# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hnsw/. The authors are listed in prov/ZFDM4P.jsonl.

import math
import random

from hnsw import HNSW, euclidean

PTS = [(0, 0), (4, 0), (8, 1), (1, 5), (5, 6), (9, 5), (2, 9), (7, 9)]
LEVELS = [2, 0, 1, 0, 1, 0, 0, 0]


def build_example() -> HNSW:
    h = HNSW(M=2, ef_construction=4, m_max0=3, heuristic=False)
    for p, lv in zip(PTS, LEVELS):
        h.insert(p, level=lv)
    return h


def test_example() -> None:
    h = build_example()
    assert h.entry == 0 and h.top == 2
    assert sorted(h.links[0][1]) == [2, 4]
    assert h.search((6, 7), 1, ef=2) == [(math.sqrt(2), 4)]


def test_level_distribution() -> None:
    h = HNSW(M=4, rng=random.Random(1))
    levels = [h.random_level() for _ in range(40000)]
    for j in range(4):
        frac = sum(lv >= j for lv in levels) / len(levels)
        assert abs(frac - 4.0**-j) < 0.01


def test_exact_without_pruning() -> None:
    rng = random.Random(21)
    for _ in range(500):
        n = rng.randint(1, 25)
        d = rng.randint(1, 3)
        pts = [tuple(rng.uniform(-5, 5) for _ in range(d)) for _ in range(n)]
        h = HNSW(M=rng.randint(2, 4), ef_construction=rng.randint(1, 8), m_max0=n, rng=rng,
                 heuristic=rng.random() < 0.5)
        for p in pts:
            h.insert(p)
        q = tuple(rng.uniform(-6, 6) for _ in range(d))
        k = rng.randint(1, 4)
        got = h.search(q, k, ef=n)
        assert [a for a, _ in got] == sorted(euclidean(q, p) for p in pts)[:k]


def test_invariants_and_recall() -> None:
    rng = random.Random(5)
    pts = [tuple(rng.random() for _ in range(4)) for _ in range(600)]
    h = HNSW(M=6, ef_construction=40, rng=rng)
    for p in pts:
        h.insert(p)
    for i, layers in enumerate(h.links):
        for lv, nb in enumerate(layers):
            assert len(nb) <= (h.m_max0 if lv == 0 else h.M)
            assert i not in nb
            assert all(len(h.links[e]) > lv for e in nb)
    hits = 0
    for _ in range(100):
        q = tuple(rng.random() for _ in range(4))
        want = {i for _, i in sorted((euclidean(q, p), i) for i, p in enumerate(pts))[:10]}
        hits += len(want & {i for _, i in h.search(q, 10, ef=50)})
    assert hits / 1000 >= 0.9
