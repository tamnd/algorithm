# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-component-growing/. The authors are listed in prov/753N4R.jsonl.

import random

from generic_component_growing import components


def build(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if u != v:
            adj[v].append(u)
    return adj


def oracle(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Labels by repeated relaxation of the reachability relation."""
    reach = [[u == v for v in range(n)] for u in range(n)]
    for u, v in edges:
        reach[u][v] = reach[v][u] = True
    for w in range(n):
        for u in range(n):
            if reach[u][w]:
                for v in range(n):
                    if reach[w][v]:
                        reach[u][v] = True
    label: list[int] = [-1] * n
    k = 0
    for s in range(n):
        if label[s] == -1:
            for v in range(n):
                if reach[s][v]:
                    label[v] = k
            k += 1
    return label


def check(n: int, edges: list[tuple[int, int]], pick=None) -> None:
    adj = build(n, edges)
    comp, parent, k = components(adj) if pick is None else components(adj, pick)
    want = oracle(n, edges)
    assert comp == want
    assert k == (max(want) + 1 if n else 0)
    roots = 0
    for v in range(n):
        p = parent[v]
        if p is None:
            roots += 1
            assert all(comp[u] != comp[v] for u in range(v))  # the root is the smallest
        else:
            assert v in adj[p] and comp[p] == comp[v]
        seen = set()
        x: int | None = v
        while x is not None:  # the parent pointers have no cycle
            assert x not in seen
            seen.add(x)
            x = parent[x]
    assert roots == k


def test_example() -> None:
    edges = [(0, 1), (1, 2), (2, 0), (3, 4), (3, 4), (5, 6), (6, 7), (5, 7), (8, 8)]
    comp, parent, k = components(build(9, edges))
    assert comp == [0, 0, 0, 1, 1, 2, 2, 2, 3]
    assert k == 4
    assert sum(p is not None for p in parent) == 9 - 4
    check(9, edges)
    check(9, edges, pick=lambda size: 0)


def test_edges() -> None:
    assert components([]) == ([], [], 0)
    check(1, [])
    check(1, [(0, 0)])
    check(1, [(0, 0), (0, 0)])
    check(2, [(0, 1), (0, 1), (1, 0)])
    check(5, [])
    check(4, [(0, 3), (3, 3)])


def test_long_path() -> None:
    n = 20000
    edges = [(i, i + 1) for i in range(n - 1)]
    comp, parent, k = components(build(n, edges))
    assert k == 1 and comp == [0] * n


def test_random() -> None:
    rng = random.Random(753)
    for t in range(600):
        n = rng.randint(0, 9)
        m = rng.randint(0, 12) if n else 0
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        mode = t % 3
        if mode == 0:
            check(n, edges)
        elif mode == 1:
            check(n, edges, pick=lambda size: 0)
        else:
            r = random.Random(t)
            check(n, edges, pick=lambda size: r.randrange(size))
