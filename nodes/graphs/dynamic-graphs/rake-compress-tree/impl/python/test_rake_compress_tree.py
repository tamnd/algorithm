# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rake-compress-tree/. The authors are listed in prov/0SFSXB.jsonl.

import random

import pytest

from rake_compress_tree import RCForest


def _path_weight(n: int, edges: dict[tuple[int, int], int], s: int, t: int):
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for (a, b), w in edges.items():
        adj[a].append((b, w))
        adj[b].append((a, w))
    dist = {s: 0}
    st = [s]
    while st:
        x = st.pop()
        for y, w in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + w
                st.append(y)
    return dist.get(t)


def _check_clusters(f: RCForest) -> None:
    """Every edge is in exactly one leaf cluster, and boundaries are sane."""
    for v in range(f.n):
        c = f.cluster[v]
        assert c.rep == v and len(c.bound) <= 2 and v not in c.bound
        if c.parent is not None:
            assert c.parent.rep in c.bound


def test_example() -> None:
    f = RCForest(7)
    for u, v, w in [(0, 1, 4), (1, 2, 1), (2, 3, 7), (1, 4, 2), (4, 5, 3), (5, 6, 5)]:
        f.link(u, v, w)
    assert f.path_weight(3, 6) == 7 + 1 + 2 + 3 + 5
    assert f.path_weight(0, 0) == 0
    f.cut(1, 4)
    assert not f.connected(3, 6) and f.path_weight(3, 6) is None
    f.link(3, 6, 1)
    assert f.path_weight(0, 4) == 4 + 1 + 7 + 1 + 5 + 3


def test_cycle_rejected() -> None:
    f = RCForest(3)
    f.link(0, 1, 1)
    f.link(1, 2, 1)
    with pytest.raises(ValueError):
        f.link(2, 0, 1)


def test_random_against_static() -> None:
    rng = random.Random(6)
    for _ in range(500):
        n = rng.randint(1, 12)
        f = RCForest(n, seed=rng.randrange(1 << 20))
        edges: dict[tuple[int, int], int] = {}
        for _ in range(rng.randint(1, 20)):
            if edges and rng.random() < 0.35:
                e = rng.choice(list(edges))
                del edges[e]
                f.cut(*e)
            else:
                u, v = rng.randrange(n), rng.randrange(n)
                if u == v or _path_weight(n, edges, u, v) is not None:
                    continue
                w = rng.randint(1, 9)
                edges[(min(u, v), max(u, v))] = w
                f.link(u, v, w)
            _check_clusters(f)
            for _ in range(5):
                a, b = rng.randrange(n), rng.randrange(n)
                assert f.path_weight(a, b) == _path_weight(n, edges, a, b)
                assert f.connected(a, b) == (_path_weight(n, edges, a, b) is not None)


def test_depth_is_logarithmic() -> None:
    n = 2000
    f = RCForest(n, seed=7)
    f.edges = {(i, i + 1): 1 for i in range(n - 1)}
    f._build()
    assert f.depth() <= 60 and f.rounds <= 60
    assert f.path_weight(0, n - 1) == n - 1
    rng = random.Random(1)
    f.edges = {}
    for v in range(1, n):
        u = rng.randrange(v)
        f.edges[(u, v)] = 1
    f._build()
    assert f.rounds <= 60
