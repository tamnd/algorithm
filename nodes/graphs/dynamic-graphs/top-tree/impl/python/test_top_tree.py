# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-tree/. The authors are listed in prov/YS9H4Q.jsonl.

import random

import pytest

from top_tree import NEG, Cluster, TopTreeForest


def _path(adj: list[dict[int, int]], s: int, t: int):
    """Weights on the tree path from s to t, or None, by iterative DFS."""
    prev = {s: (None, 0)}
    st = [s]
    while st:
        x = st.pop()
        for y, w in adj[x].items():
            if y not in prev:
                prev[y] = (x, w)
                st.append(y)
    if t not in prev:
        return None
    ws = []
    while t != s:
        t, w = prev[t]
        ws.append(w)
    return ws


def _check(root: Cluster, u: int, v: int, n_edges: int) -> None:
    """The top tree is binary above the edges, has the right root boundary and covers every edge once."""
    assert set(root.bound) == {u, v}
    if n_edges == 0:
        assert root.kind == "empty"
        return
    leaves, st = 0, [root]
    while st:
        c = st.pop()
        assert len(c.bound) <= 2
        if c.kind == "edge":
            assert not c.children
            leaves += 1
        else:
            assert len(c.children) == 2
            st.extend(c.children)
    assert leaves == n_edges


def test_example() -> None:
    f = TopTreeForest(7, seed=3)
    for u, v, w in [(0, 1, 4), (1, 2, 1), (2, 3, 7), (1, 4, 2), (4, 5, 3), (5, 6, 5)]:
        f.link(u, v, w)
    assert f.path_sum(3, 6) == 18 and f.path_max(3, 6) == 7
    assert f.tree_total(0) == 22
    f.cut(2, 3)
    assert f.path_sum(3, 6) is None and f.tree_total(3) == 0
    assert f.path_max(0, 6) == 5


def test_cycle_rejected() -> None:
    f = TopTreeForest(3)
    f.link(0, 1, 1)
    f.link(1, 2, 1)
    with pytest.raises(ValueError):
        f.link(0, 2, 1)


def test_random_against_static() -> None:
    rng = random.Random(9)
    for _ in range(500):
        n = rng.randint(1, 12)
        f = TopTreeForest(n, seed=rng.randrange(1 << 20))
        adj: list[dict[int, int]] = [dict() for _ in range(n)]
        for _ in range(rng.randint(1, 18)):
            edges = [(a, b) for a in range(n) for b in adj[a] if a < b]
            if edges and rng.random() < 0.35:
                a, b = rng.choice(edges)
                del adj[a][b], adj[b][a]
                f.cut(a, b)
            else:
                a, b = rng.randrange(n), rng.randrange(n)
                if a == b or _path(adj, a, b) is not None:
                    continue
                w = rng.randint(-5, 9)
                adj[a][b] = adj[b][a] = w
                f.link(a, b, w)
            for _ in range(4):
                a, b = rng.randrange(n), rng.randrange(n)
                ws = _path(adj, a, b)
                if ws is None:
                    assert f.path_sum(a, b) is None and not f.connected(a, b)
                    continue
                assert f.path_sum(a, b) == sum(ws)
                assert f.path_max(a, b) == (max(ws) if ws else NEG)
                comp = _path_component_edges(adj, a)
                assert f.tree_total(a) == sum(comp)
                _check(f.expose(a, b), a, b, len(comp))


def _path_component_edges(adj: list[dict[int, int]], s: int) -> list[int]:
    seen, st, ws = {s}, [s], []
    while st:
        x = st.pop()
        for y, w in adj[x].items():
            if y not in seen:
                seen.add(y)
                st.append(y)
    for x in seen:
        ws.extend(w for y, w in adj[x].items() if x < y)
    return ws


def test_long_path() -> None:
    n = 1000
    f = TopTreeForest(n, seed=5)
    for i in range(n - 1):
        f.link(i, i + 1, i % 7)
    assert f.path_sum(10, n - 5) == sum(i % 7 for i in range(10, n - 5))
    assert f.path_max(0, n - 1) == 6
