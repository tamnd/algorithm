# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compact-forward-algorithm/. The authors are listed in prov/R006RZ.jsonl.

import random

from compact_forward_algorithm import compact_forward_algorithm


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def oracle(n: int, edges: list[tuple[int, int]]) -> set[frozenset[int]]:
    """All triangles, by testing every triple of vertices."""
    es = {frozenset(e) for e in edges}
    out: set[frozenset[int]] = set()
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                if {frozenset((a, b)), frozenset((a, c)), frozenset((b, c))} <= es:
                    out.add(frozenset((a, b, c)))
    return out


EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]


def test_example() -> None:
    tri = compact_forward_algorithm(undirected(7, EXAMPLE))
    assert tri == [(1, 2, 3), (1, 2, 0), (4, 5, 6)]


def test_edges() -> None:
    assert compact_forward_algorithm([]) == []
    assert compact_forward_algorithm([[]]) == []
    assert compact_forward_algorithm(undirected(3, [(0, 1), (1, 2)])) == []
    assert compact_forward_algorithm(undirected(3, [(0, 1), (1, 2), (0, 2)])) == [(0, 1, 2)]
    k5 = [(u, v) for u in range(5) for v in range(u + 1, 5)]
    assert len(compact_forward_algorithm(undirected(5, k5))) == 10
    star = undirected(6, [(0, v) for v in range(1, 6)])
    assert compact_forward_algorithm(star) == []


def test_random_against_oracle() -> None:
    rng = random.Random(31337)
    for _ in range(700):
        n = rng.randint(1, 11)
        p = rng.random()
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        rng.shuffle(edges)
        adj = undirected(n, edges)
        for lst in adj:
            rng.shuffle(lst)
        tri = compact_forward_algorithm(adj)
        sets = [frozenset(t) for t in tri]
        assert len(sets) == len(set(sets))
        assert all(len(s) == 3 for s in sets)
        assert set(sets) == oracle(n, edges)
