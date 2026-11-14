# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rectilinear-minimum-spanning-tree/. The authors are listed in prov/53V9N5.jsonl.

import random

from rectilinear_minimum_spanning_tree import l1, octant_graph, rectilinear_minimum_spanning_tree


def prim_length(pts: list[tuple[int, int]]) -> int:
    """Prim's algorithm on the complete graph with L1 lengths, O(n^2)."""
    n = len(pts)
    if n == 0:
        return 0
    best = [l1(pts[0], p) for p in pts]
    used = [False] * n
    used[0] = True
    total = 0
    for _ in range(n - 1):
        j = min((i for i in range(n) if not used[i]), key=lambda i: best[i])
        used[j] = True
        total += best[j]
        for i in range(n):
            if not used[i]:
                best[i] = min(best[i], l1(pts[j], pts[i]))
    return total


def is_spanning_tree(n: int, edges: list[tuple[int, int, int]]) -> bool:
    if len(edges) != max(n - 1, 0):
        return False
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            a = parent[a]
        return a

    for _, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True


EXAMPLE = [(0, 0), (4, 1), (1, 4), (5, 5), (2, 3)]


def test_example() -> None:
    tree = rectilinear_minimum_spanning_tree(EXAMPLE)
    assert sum(d for d, _, _ in tree) == 16
    assert is_spanning_tree(5, tree)
    assert len(octant_graph(EXAMPLE)) <= 4 * 5


def test_edges() -> None:
    assert rectilinear_minimum_spanning_tree([]) == []
    assert rectilinear_minimum_spanning_tree([(3, 3)]) == []
    assert rectilinear_minimum_spanning_tree([(1, 1), (1, 1)]) == [(0, 0, 1)]
    plus = [(1, 0), (0, 1), (2, 1), (1, 2)]
    assert sum(d for d, _, _ in rectilinear_minimum_spanning_tree(plus)) == 6
    line = [(i, 0) for i in range(6)]
    assert sum(d for d, _, _ in rectilinear_minimum_spanning_tree(line)) == 5


def test_against_prim(seed: int = 19) -> None:
    rng = random.Random(seed)
    for _ in range(600):
        n = rng.randint(1, 30)
        span = rng.choice([3, 6, 20, 1000])
        pts = [(rng.randint(-span, span), rng.randint(-span, span)) for _ in range(n)]
        tree = rectilinear_minimum_spanning_tree(pts)
        assert is_spanning_tree(n, tree)
        assert all(d == l1(pts[a], pts[b]) for d, a, b in tree)
        assert sum(d for d, _, _ in tree) == prim_length(pts)
