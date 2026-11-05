# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/link-cut-tree/. The authors are listed in prov/45BF01.jsonl.

import random

from link_cut_tree import LinkCutForest


def _path(adj: list[set[int]], u: int, v: int) -> list[int] | None:
    prev = {u: -1}
    stack = [u]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in prev:
                prev[y] = x
                stack.append(y)
    if v not in prev:
        return None
    out = [v]
    while out[-1] != u:
        out.append(prev[out[-1]])
    return out


def _lca(adj: list[set[int]], r: int, u: int, v: int) -> int:
    pu = set(_path(adj, r, u))
    for x in _path(adj, r, v):  # the list runs from v up to r
        if x in pu:
            return x
    raise AssertionError


def test_example() -> None:
    f = LinkCutForest(7, [5, 3, 8, 1, 4, 7, 2])
    for u, v in [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (0, 6)]:
        f.link(u, v)
    assert f.path_sum(2, 5) == 8 + 3 + 1 + 4 + 7
    assert f.path_max(6, 4) == 5
    assert f.lca(0, 2, 5) == 1
    f.cut(1, 3)
    assert not f.connected(2, 5)
    assert f.path_sum(3, 5) == 12
    f.link(2, 5)
    assert f.path_sum(6, 3) == 2 + 5 + 3 + 8 + 7 + 4 + 1
    assert f.find_root(4) in range(7)


def test_errors() -> None:
    f = LinkCutForest(3)
    f.link(0, 1)
    try:
        f.link(1, 0)
        raise AssertionError
    except ValueError:
        pass
    try:
        f.cut(0, 2)
        raise AssertionError
    except ValueError:
        pass


def test_random_against_naive() -> None:
    rng = random.Random(2024)
    for _ in range(60):
        n = rng.randint(1, 12)
        vals = [rng.randint(-9, 9) for _ in range(n)]
        f = LinkCutForest(n, vals)
        adj: list[set[int]] = [set() for _ in range(n)]
        edges: list[tuple[int, int]] = []
        for _ in range(200):
            op = rng.random()
            u, v = rng.randrange(n), rng.randrange(n)
            if op < 0.3:
                if u != v and _path(adj, u, v) is None:
                    f.link(u, v)
                    adj[u].add(v)
                    adj[v].add(u)
                    edges.append((u, v))
            elif op < 0.45 and edges:
                a, b = edges.pop(rng.randrange(len(edges)))
                if rng.random() < 0.5:
                    a, b = b, a
                f.cut(a, b)
                adj[a].discard(b)
                adj[b].discard(a)
            elif op < 0.55:
                x = rng.randint(-9, 9)
                f.set_value(u, x)
                vals[u] = x
            p = _path(adj, u, v)
            assert f.connected(u, v) == (p is not None)
            if p is not None:
                assert f.path_sum(u, v) == sum(vals[x] for x in p)
                assert f.path_max(v, u) == max(vals[x] for x in p)
                r = rng.choice(p)
                assert f.lca(r, u, v) == r
                w = rng.randrange(n)
                if _path(adj, w, u) is not None:
                    assert f.lca(w, u, v) == _lca(adj, w, u, v)


def test_long_path_no_recursion_error() -> None:
    n = 5000
    f = LinkCutForest(n, list(range(n)))
    for i in range(n - 1):
        f.link(i, i + 1)
    assert f.path_sum(0, n - 1) == n * (n - 1) // 2
    f.cut(2500, 2499)
    assert not f.connected(0, n - 1)
    assert f.path_max(2500, n - 1) == n - 1
