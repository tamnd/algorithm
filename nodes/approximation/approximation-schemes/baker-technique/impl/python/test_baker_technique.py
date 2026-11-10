# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baker-technique/. The authors are listed in prov/2A03SS.jsonl.

import random

from baker_technique import (baker_max, baker_min, bfs_levels, exact_independent_set,
                             exact_vertex_cover)


def grid_graph(rng, a, b, keep):
    """A planar graph: an a x b grid with one random diagonal per cell, each edge kept with probability keep."""
    adj = [set() for _ in range(a * b)]

    def add(u, v):
        if rng.random() < keep:
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
                if rng.random() < 0.5:
                    add(v, v + b + 1)
                else:
                    add(v + 1, v + b)
    return adj


def brute_mis(adj):
    n = len(adj)
    best = 0
    for mask in range(1 << n):
        if bin(mask).count("1") <= best:
            continue
        if all(not (mask >> u & 1 and mask >> v & 1) for u in range(n) for v in adj[u]):
            best = bin(mask).count("1")
    return best


def independent(adj, s):
    return all(u not in adj[v] for v in s for u in s)


def is_cover(adj, s):
    return all(u in s or v in s for u in range(len(adj)) for v in adj[u])


EXAMPLE = [set() for _ in range(9)]
for _u, _v in [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8),
               (0, 4), (4, 8), (2, 4), (4, 6)]:
    EXAMPLE[_u].add(_v)
    EXAMPLE[_v].add(_u)


def test_example() -> None:
    assert bfs_levels(EXAMPLE) == [0, 1, 2, 1, 1, 2, 2, 2, 2]
    st = {}
    s = baker_max(EXAMPLE, 2, exact_independent_set, st)
    assert brute_mis(EXAMPLE) == 4 and st["values"] == [2, 4] and s == {0, 2, 6, 8}
    st = {}
    c = baker_min(EXAMPLE, 2, exact_vertex_cover, st)
    assert st["values"] == [5, 5] and len(c) == 5 and is_cover(EXAMPLE, c)


def test_exact_solvers() -> None:
    rng = random.Random(1994)
    for _ in range(60):
        adj = grid_graph(rng, rng.randint(1, 3), rng.randint(1, 4), 0.8)
        s = exact_independent_set(adj, list(range(len(adj))))
        assert independent(adj, s) and len(s) == brute_mis(adj)
        c = exact_vertex_cover(adj, list(range(len(adj))))
        assert is_cover(adj, c) and len(c) == len(adj) - brute_mis(adj)


def test_levels_and_layer_lemma() -> None:
    rng = random.Random(153)
    for _ in range(60):
        adj = grid_graph(rng, rng.randint(1, 4), rng.randint(1, 4), 0.85)
        level = bfs_levels(adj)
        assert all(abs(level[u] - level[v]) <= 1 for u in range(len(adj)) for v in adj[u])
        opt = exact_independent_set(adj, list(range(len(adj))))
        for k in (2, 3, 4):
            loss = [sum(1 for v in opt if level[v] % k == r) for r in range(k)]
            assert sum(loss) == len(opt) and min(loss) * k <= len(opt)


def test_ratios_for_several_k() -> None:
    rng = random.Random(180)
    for _ in range(40):
        adj = grid_graph(rng, rng.randint(2, 4), rng.randint(2, 4), 0.85)
        n = len(adj)
        level = bfs_levels(adj)
        opt_is = exact_independent_set(adj, list(range(n)))
        opt_vc = set(range(n)) - opt_is
        for k in (1, 2, 3, 4):
            st = {}
            s = baker_max(adj, k, exact_independent_set, st)
            assert independent(adj, s)
            assert len(s) * k >= (k - 1) * len(opt_is)
            for r in range(k):
                assert st["values"][r] >= len(opt_is) - sum(1 for v in opt_is if level[v] % k == r)
            st = {}
            c = baker_min(adj, k, exact_vertex_cover, st)
            assert is_cover(adj, c)
            assert len(c) * k <= (k + 1) * len(opt_vc)
            for r in range(k):
                assert st["values"][r] <= len(opt_vc) + sum(1 for v in opt_vc if level[v] % k == r)
