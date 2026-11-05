# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frt-tree-embedding/. The authors are listed in prov/CF4M1Y.jsonl.

import math
import random

import pytest

from frt_tree_embedding import FrtTree


def line_metric(pos: list[float]) -> list[list[float]]:
    return [[abs(a - b) for b in pos] for a in pos]


def graph_metric(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]]:
    inf = float("inf")
    d = [[0.0 if i == j else inf for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        d[a][b] = min(d[a][b], w)
        d[b][a] = min(d[b][a], w)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            row = d[i]
            for j in range(n):
                if dik + dk[j] < row[j]:
                    row[j] = dik + dk[j]
    return d


def brute_partitions(dist: list[list[float]], perm: list[int], beta: float) -> list[list[frozenset[int]]]:
    """Refine clusters level by level, scanning centers in order for each cluster."""
    n = len(dist)
    pairs = [dist[i][j] for i in range(n) for j in range(i + 1, n)]
    dmin = min(pairs, default=1.0)
    top = 0
    if n > 1:
        top = 1
        while 2.0**top * dmin < max(pairs):
            top += 1
    clusters = [frozenset(range(n))]
    out = [clusters]
    for i in range(top - 1, -1, -1):
        radius = beta * 2.0 ** (i - 1) * dmin
        nxt = []
        for cl in clusters:
            left = set(cl)
            for w in perm:
                part = {x for x in left if dist[w][x] <= radius}
                if part:
                    nxt.append(frozenset(part))
                    left -= part
        clusters = nxt
        out.append(clusters)
    return out


def tree_partitions(t: FrtTree) -> list[list[frozenset[int]]]:
    out = []
    for lev in range(t.top, -1, -1):
        out.append(sorted((frozenset(t.members[v]) for v in range(len(t.parent)) if t.level[v] == lev), key=sorted))
    return out


def test_page_example() -> None:
    d = line_metric([0, 1, 3, 7, 8])
    t = FrtTree(d, perm=[2, 0, 4, 1, 3], beta=1.5)
    assert t.top == 3
    parts = tree_partitions(t)
    assert parts[1] == [frozenset({0, 1, 2}), frozenset({3, 4})]
    assert parts[2] == [frozenset({0, 1}), frozenset({2}), frozenset({3, 4})]
    assert all(len(c) == 1 for c in parts[3])
    assert t.tree_distance(0, 1) == 4
    assert t.tree_distance(0, 2) == 12
    assert t.tree_distance(0, 3) == 28
    assert t.tree_distance(3, 4) == 4
    assert t.tree_distance(2, 2) == 0


def test_single_point() -> None:
    t = FrtTree([[0]], seed=1)
    assert t.top == 0 and t.leaf == [0] and t.parent == [-1]
    assert t.tree_distance(0, 0) == 0


def test_two_points() -> None:
    t = FrtTree([[0, 5], [5, 0]], seed=3)
    assert t.top == 1 and t.leaf[0] != t.leaf[1]
    assert t.tree_distance(0, 1) == 20


def test_star_metric() -> None:
    # the shortest-path metric of a star with unit edges: leaves are 2 apart
    n = 9
    d = graph_metric(n, [(0, i, 1.0) for i in range(1, n)])
    for seed in range(20):
        t = FrtTree(d, seed=seed)
        for u in range(n):
            for v in range(n):
                assert t.tree_distance(u, v) >= d[u][v]


def test_long_path_metric() -> None:
    # a path of 10^5 points would need a 10^10-entry matrix; the tree build is
    # quadratic by design, so the long test uses 1500 points on a line
    n = 1500
    d = line_metric(list(range(n)))
    t = FrtTree(d, seed=4)
    assert t.top == math.ceil(math.log2(n - 1))
    rng = random.Random(4)
    for _ in range(3000):
        u, v = rng.randrange(n), rng.randrange(n)
        assert t.tree_distance(u, v) >= d[u][v]
    assert len(set(t.leaf)) == n


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        FrtTree([])
    with pytest.raises(ValueError):
        FrtTree([[0, 1], [2, 0]])
    with pytest.raises(ValueError):
        FrtTree([[0, 0], [0, 0]])
    with pytest.raises(ValueError):
        FrtTree([[0, 1], [1, 0]], beta=3.0)
    with pytest.raises(ValueError):
        FrtTree([[0, 1], [1, 0]], beta=2.0)
    with pytest.raises(ValueError):
        FrtTree([[0, 1], [1, 0]], perm=[0, 0])
    t = FrtTree([[0, 1], [1, 0]], seed=0)
    with pytest.raises(IndexError):
        t.tree_distance(0, 2)


def test_expected_stretch() -> None:
    n = 24
    d = line_metric(list(range(n)))
    harmonic = sum(1 / s for s in range(1, n + 1))
    total = [[0.0] * n for _ in range(n)]
    trials = 300
    for seed in range(trials):
        t = FrtTree(d, seed=seed)
        for u in range(n):
            for v in range(u + 1, n):
                total[u][v] += t.tree_distance(u, v)
    for u in range(n):
        for v in range(u + 1, n):
            assert total[u][v] / trials <= 16 * harmonic * d[u][v]


def test_random_against_brute_force() -> None:
    rng = random.Random(23)
    for case in range(600):
        n = rng.randint(1, 10)
        if case % 2:
            d = line_metric([rng.randint(0, 60) * 1.0 + i * 1e-3 for i in range(n)])
        else:
            edges = [(i, rng.randrange(i), float(rng.randint(1, 9))) for i in range(1, n)]
            edges += [(rng.randrange(n), rng.randrange(n), float(rng.randint(1, 9))) for _ in range(n)]
            edges = [e for e in edges if e[0] != e[1]]
            d = graph_metric(n, edges)
        perm = list(range(n))
        rng.shuffle(perm)
        beta = rng.uniform(1.0, 2.0)
        t = FrtTree(d, perm=perm, beta=beta)
        expect = brute_partitions(d, perm, beta)
        got = tree_partitions(t)
        assert [sorted(level, key=sorted) for level in expect] == got
        for lev, level in zip(range(t.top, -1, -1), got):
            for cl in level:
                if lev < t.top:
                    assert max(d[a][b] for a in cl for b in cl) <= 2 * beta * 2.0 ** (lev - 1) * t.scale + 1e-9
        for u in range(n):
            for v in range(n):
                assert t.tree_distance(u, v) >= d[u][v] - 1e-9
