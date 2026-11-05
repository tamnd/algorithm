# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-diameter-double-sweep/. The authors are listed in prov/EZ41AA.jsonl.

import random

from tree_diameter_double_sweep import tree_diameter


def brute(n: int, edges: list[tuple[int, int, int]]) -> int:
    # Distances by repeated relaxation over the edge list from every source.
    best = 0
    for s in range(n):
        d: list[int | None] = [None] * n
        d[s] = 0
        changed = True
        while changed:
            changed = False
            for u, v, w in edges:
                for x, y in ((u, v), (v, u)):
                    if d[x] is not None and d[y] is None:
                        d[y] = d[x] + w
                        changed = True
        best = max(best, max(x for x in d if x is not None))
    return best


def path_length(edges: list[tuple[int, int, int]], path: list[int]) -> int:
    w = {}
    for u, v, x in edges:
        w[(u, v)] = w[(v, u)] = x
    assert len(set(path)) == len(path)
    return sum(w[(path[i], path[i + 1])] for i in range(len(path) - 1))


def test_example() -> None:
    edges = [(0, 1, 1), (0, 2, 1), (1, 3, 1), (1, 4, 1), (2, 5, 1), (4, 6, 1), (4, 7, 1)]
    d, path = tree_diameter(8, edges)
    assert d == 5
    assert path in ([6, 4, 1, 0, 2, 5], [5, 2, 0, 1, 4, 6], [7, 4, 1, 0, 2, 5], [5, 2, 0, 1, 4, 7])


def test_weighted_example() -> None:
    edges = [(0, 1, 2), (1, 2, 7), (1, 3, 3), (0, 4, 4), (4, 5, 1), (4, 6, 5)]
    d, path = tree_diameter(7, edges)
    assert d == 18
    assert path_length(edges, path) == 18


def test_single_vertex() -> None:
    assert tree_diameter(1, []) == (0, [0])


def test_path_long() -> None:
    n = 100_000
    edges = [(i, i + 1, 1) for i in range(n - 1)]
    d, path = tree_diameter(n, edges)
    assert d == n - 1
    assert path == list(range(n - 1, -1, -1))


def test_star() -> None:
    n = 30
    d, path = tree_diameter(n, [(0, i, 1) for i in range(1, n)])
    assert d == 2 and path[1] == 0 and len(path) == 3
    assert tree_diameter(2, [(0, 1, 5)])[0] == 5


def test_zero_weights() -> None:
    assert tree_diameter(3, [(0, 1, 0), (1, 2, 0)])[0] == 0


def test_random_against_brute_force() -> None:
    rng = random.Random(9124)
    for _ in range(600):
        n = rng.randint(1, 25)
        perm = list(range(n))
        rng.shuffle(perm)
        edges = [(perm[i], perm[rng.randrange(i)], rng.randint(0, 9)) for i in range(1, n)]
        d, path = tree_diameter(n, edges)
        assert d == brute(n, edges)
        assert path_length(edges, path) == d
