# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baker-planar-ptas/. The authors are listed in prov/N8D9ER.jsonl.

import random

from baker_planar_ptas import (baker_independent_set, baker_vertex_cover, bfs_levels, elimination,
                               max_independent_set)


def grid_graph(a, b, rng=None, keep=1.0):
    """An a x b grid with one diagonal per cell (down-right, or random if rng is given): a planar graph."""
    adj = [set() for _ in range(a * b)]

    def add(u, v):
        if rng is None or rng.random() < keep:
            adj[u].add(v)
            adj[v].add(u)
    for i in range(a):
        for j in range(b):
            v = i * b + j
            if j + 1 < b:
                add(v, v + 1)
            if i + 1 < a:
                add(v, v + b)
            if i + 1 < a and j + 1 < b:
                if rng is None or rng.random() < 0.5:
                    add(v, v + b + 1)
                else:
                    add(v + 1, v + b)
    return adj


def brute_mis(adj):
    n = len(adj)
    nb = [sum(1 << u for u in adj[v]) for v in range(n)]
    best = 0
    for mask in range(1 << n):
        c = bin(mask).count("1")
        if c > best and all(not (mask >> v & 1) or not (nb[v] & mask) for v in range(n)):
            best = c
    return best


def independent(adj, s):
    return all(u not in adj[v] for v in s for u in s)


def is_cover(adj, s):
    return all(u in s or v in s for u in range(len(adj)) for v in adj[u])


def test_example() -> None:
    adj = grid_graph(4, 4)
    assert bfs_levels(adj) == [max(i, j) for i in range(4) for j in range(4)]
    assert brute_mis(adj) == 6
    st = {}
    s = baker_independent_set(adj, 2, st)
    assert st["values"] == [6, 4] and s == {1, 3, 4, 11, 12, 14} and independent(adj, s)
    assert st["states"] == 28 and st["width"] == 1
    st = {}
    s = baker_independent_set(adj, 3, st)
    assert st["values"] == [3, 6, 6] and len(s) == 6
    st = {}
    c = baker_vertex_cover(adj, 2, st)
    assert st["values"] == [12, 10] and len(c) == 10 and is_cover(adj, c)


def test_tree_decomposition_is_valid() -> None:
    rng = random.Random(41)
    for _ in range(40):
        adj = grid_graph(rng.randint(1, 5), rng.randint(1, 5), rng, 0.8)
        vs = [v for v in range(len(adj)) if rng.random() < 0.8]
        order, later = elimination(adj, vs)
        assert sorted(order) == sorted(vs)
        pos = {v: i for i, v in enumerate(order)}
        bags = [later[v] | {v} for v in order]
        keep = set(vs)
        for u in vs:
            for v in adj[u] & keep:
                assert any(u in b and v in b for b in bags)
        # the later neighbours of v lie in the bag of its parent: the running intersection property
        for v in order:
            if later[v]:
                p = min(later[v], key=pos.__getitem__)
                assert later[v] - {p} <= later[p]


def test_dp_is_exact_and_state_count() -> None:
    rng = random.Random(1983)
    for _ in range(60):
        adj = grid_graph(rng.randint(1, 4), rng.randint(1, 4), rng, 0.85)
        st = {}
        s = max_independent_set(adj, list(range(len(adj))), st)
        assert independent(adj, s) and len(s) == brute_mis(adj)
        assert st["states"] <= st["bound"] <= len(adj) * 2 ** st["width"]


def test_ratios_for_several_k() -> None:
    rng = random.Random(1994)
    for _ in range(30):
        adj = grid_graph(rng.randint(2, 4), rng.randint(2, 4), rng, 0.9)
        n = len(adj)
        opt = brute_mis(adj)
        for k in (1, 2, 3, 4):
            s = baker_independent_set(adj, k)
            assert independent(adj, s) and len(s) * k >= (k - 1) * opt
            c = baker_vertex_cover(adj, k)
            assert is_cover(adj, c) and len(c) * k <= (k + 1) * (n - opt)


def test_bands_have_small_width() -> None:
    # bands of k - 1 levels of the triangulated grid: the elimination widths stay bounded as the grid grows
    for size in (4, 6, 8):
        adj = grid_graph(size, size)
        for k in (2, 3):
            st = {}
            baker_independent_set(adj, k, st)
            assert st["width"] <= 3 * k
