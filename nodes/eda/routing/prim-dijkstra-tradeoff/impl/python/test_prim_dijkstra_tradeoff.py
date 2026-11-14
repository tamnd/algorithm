# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prim-dijkstra-tradeoff/. The authors are listed in prov/93CM0J.jsonl.

import random
from fractions import Fraction

from prim_dijkstra_tradeoff import l1, prim_dijkstra_tradeoff, tree_cost


def mst_length(pts: list[tuple[int, int]]) -> int:
    """Kruskal on all pairs, written apart from the tree builder."""
    n = len(pts)
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            a = parent[a]
        return a

    total = 0
    for d, i, j in sorted((l1(pts[i], pts[j]), i, j) for i in range(n) for j in range(i + 1, n)):
        if find(i) != find(j):
            parent[find(i)] = find(j)
            total += d
    return total


def is_tree_from(parent: list[int], source: int) -> bool:
    n = len(parent)
    if parent[source] != -1:
        return False
    for v in range(n):
        seen = set()
        while v != source:
            if v in seen or parent[v] < 0:
                return False
            seen.add(v)
            v = parent[v]
    return True


EXAMPLE = [(0, 0), (1, 3), (2, 6), (3, 9), (6, 9), (9, 9), (9, 6), (9, 3), (9, 0)]


def test_example() -> None:
    parent, d = prim_dijkstra_tradeoff(EXAMPLE, 0)
    assert tree_cost(EXAMPLE, parent) == 27 and max(d) == 27
    parent, d = prim_dijkstra_tradeoff(EXAMPLE, Fraction(1, 4))
    assert parent == [-1, 0, 1, 2, 3, 4, 5, 6, 0]
    assert tree_cost(EXAMPLE, parent) == 33 and max(d) == 24
    parent, d = prim_dijkstra_tradeoff(EXAMPLE, Fraction(1, 2))
    assert parent == [-1, 0, 1, 2, 3, 4, 7, 8, 0]
    assert tree_cost(EXAMPLE, parent) == 33 and max(d) == 18
    parent, d = prim_dijkstra_tradeoff(EXAMPLE, 1)
    assert d == [l1(EXAMPLE[0], p) for p in EXAMPLE]
    assert tree_cost(EXAMPLE, parent) == 93


def test_edges() -> None:
    assert prim_dijkstra_tradeoff([], 0) == ([], [])
    assert prim_dijkstra_tradeoff([(1, 1)], 1) == ([-1], [0])
    assert prim_dijkstra_tradeoff([(0, 0), (2, 2)], Fraction(1, 3)) == ([-1, 0], [0, 4])


def test_bounds(seed: int = 31) -> None:
    rng = random.Random(seed)
    for _ in range(300):
        n = rng.randint(1, 14)
        pts = [(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(n)]
        s = rng.randrange(n)
        parent, d = prim_dijkstra_tradeoff(pts, 0, s)
        assert is_tree_from(parent, s)
        assert tree_cost(pts, parent) == mst_length(pts)
        parent, d = prim_dijkstra_tradeoff(pts, 1, s)
        assert is_tree_from(parent, s)
        assert all(d[v] == l1(pts[s], pts[v]) for v in range(n))
        c = Fraction(rng.randint(1, 9), 10)
        parent, d = prim_dijkstra_tradeoff(pts, c, s)
        assert is_tree_from(parent, s)
        assert all(c * d[v] <= l1(pts[s], pts[v]) for v in range(n))
        assert all(d[v] == d[parent[v]] + l1(pts[v], pts[parent[v]]) for v in range(n) if v != s)
