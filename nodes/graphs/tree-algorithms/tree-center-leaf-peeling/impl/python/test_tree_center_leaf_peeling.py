# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-center-leaf-peeling/. The authors are listed in prov/R9M66X.jsonl.

import random
from collections import deque

from tree_center_leaf_peeling import tree_center


def eccentricities(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    out = []
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    q.append(v)
        out.append(max(dist))
    return out


def check(n: int, edges: list[tuple[int, int]]) -> None:
    ecc = eccentricities(n, edges)
    rad = min(ecc)
    centre, rounds = tree_center(n, edges)
    assert centre == [v for v in range(n) if ecc[v] == rad]
    if n >= 2:
        assert rad == (rounds if len(centre) == 1 else rounds + 1)
        diameter = max(ecc)
        assert diameter == 2 * rounds + len(centre) - 1


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (4, 7)]
    assert tree_center(8, edges) == ([0, 1], 2)


def test_small() -> None:
    assert tree_center(1, []) == ([0], 0)
    assert tree_center(2, [(0, 1)]) == ([0, 1], 0)
    assert tree_center(3, [(0, 1), (1, 2)]) == ([1], 1)


def test_star() -> None:
    n = 40
    assert tree_center(n, [(0, i) for i in range(1, n)]) == ([0], 1)
    assert tree_center(n, [(n - 1, i) for i in range(n - 1)]) == ([n - 1], 1)


def test_path_long() -> None:
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]
    assert tree_center(n, edges) == ([n // 2 - 1, n // 2], n // 2 - 1)
    assert tree_center(n + 1, edges + [(n - 1, n)]) == ([n // 2], n // 2)


def test_random_against_brute_force() -> None:
    rng = random.Random(5150)
    for _ in range(700):
        n = rng.randint(1, 30)
        perm = list(range(n))
        rng.shuffle(perm)
        edges = [(perm[i], perm[rng.randrange(i)]) for i in range(1, n)]
        check(n, edges)
