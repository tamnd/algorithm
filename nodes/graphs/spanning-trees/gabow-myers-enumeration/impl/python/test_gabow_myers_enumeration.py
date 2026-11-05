# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-myers-enumeration/. The authors are listed in prov/NE4VW0.jsonl.

import itertools
import random
from fractions import Fraction

from gabow_myers_enumeration import gabow_myers_enumeration

EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]


def is_spanning_tree(n, edges, chosen):
    if len(chosen) != n - 1:
        return False
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in chosen:
        a, b = find(edges[i][0]), find(edges[i][1])
        if a == b:
            return False
        parent[a] = b
    return True


def brute_force(n, edges):
    if n <= 0:
        return set()
    return {frozenset(c) for c in itertools.combinations(range(len(edges)), n - 1) if is_spanning_tree(n, edges, c)}


def kirchhoff(n, edges):
    """Number of spanning trees by the matrix-tree theorem, in exact arithmetic."""
    if n == 1:
        return 1
    lap = [[Fraction(0)] * n for _ in range(n)]
    for u, v in edges:
        if u != v:
            lap[u][u] += 1
            lap[v][v] += 1
            lap[u][v] -= 1
            lap[v][u] -= 1
    a = [row[1:] for row in lap[1:]]
    k = n - 1
    det = Fraction(1)
    for c in range(k):
        p = next((r for r in range(c, k) if a[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            a[c], a[p] = a[p], a[c]
            det = -det
        det *= a[c][c]
        for r in range(c + 1, k):
            f = a[r][c] / a[c][c]
            for j in range(c, k):
                a[r][j] -= f * a[c][j]
    return int(det)


def run(n, edges):
    out = list(gabow_myers_enumeration(n, edges))
    sets = [frozenset(t) for t in out]
    assert len(sets) == len(set(sets)), "a tree was listed twice"
    for t in out:
        assert is_spanning_tree(n, edges, t)
    return set(sets)


def test_example_has_55_trees():
    trees = run(6, EXAMPLE)
    assert len(trees) == 55
    assert trees == brute_force(6, EXAMPLE)
    assert frozenset([1, 2, 3, 5, 8]) in trees


def test_first_trees_of_example():
    out = list(gabow_myers_enumeration(6, EXAMPLE))
    assert out[:3] == [[1, 5, 8, 7, 3], [1, 5, 8, 7, 2], [1, 5, 8, 7, 0]]
    assert len(out) == 55


def test_complete_graphs_match_cayley():
    for n in range(1, 7):
        edges = list(itertools.combinations(range(n), 2))
        assert len(run(n, edges)) == (n ** (n - 2) if n >= 2 else 1)


def test_cycle():
    n = 7
    edges = [(i, (i + 1) % n) for i in range(n)]
    trees = run(n, edges)
    assert trees == {frozenset(set(range(n)) - {i}) for i in range(n)}


def test_tree_input_gives_itself():
    edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
    assert run(5, edges) == {frozenset(range(4))}


def test_single_vertex_and_empty():
    assert list(gabow_myers_enumeration(1, [])) == [[]]
    assert list(gabow_myers_enumeration(1, [(0, 0)])) == [[]]
    assert list(gabow_myers_enumeration(0, [])) == []


def test_disconnected_yields_nothing():
    assert list(gabow_myers_enumeration(4, [(0, 1), (2, 3)])) == []
    assert list(gabow_myers_enumeration(3, [(0, 1), (0, 1), (1, 1)])) == []


def test_parallel_edges_and_loops():
    edges = [(0, 1), (0, 1), (1, 2), (2, 2), (0, 2)]
    trees = run(3, edges)
    assert trees == {frozenset(s) for s in ([0, 2], [1, 2], [0, 4], [1, 4], [2, 4])}


def test_random_against_brute_force_and_kirchhoff():
    rng = random.Random(20261105)
    for _ in range(600):
        n = rng.randint(1, 6)
        m = rng.randint(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        trees = run(n, edges)
        assert trees == brute_force(n, edges)
        assert len(trees) == kirchhoff(n, edges)
