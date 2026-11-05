# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-depth-first-search/. The authors are listed in prov/FP6REQ.jsonl.

import random
import sys

from iterative_depth_first_search import iterative_depth_first_search


def recursive_dfs(adj: list[list[int]]) -> tuple[list[int], list[int], list[int | None]]:
    """Independent oracle: the recursive DFS of CLRS, on small graphs."""
    n = len(adj)
    d = [0] * n
    f = [0] * n
    parent: list[int | None] = [None] * n
    clock = [0]

    def visit(u: int) -> None:
        clock[0] += 1
        d[u] = clock[0]
        for v in adj[u]:
            if d[v] == 0:
                parent[v] = u
                visit(v)
        clock[0] += 1
        f[u] = clock[0]

    for u in range(n):
        if d[u] == 0:
            visit(u)
    return d, f, parent


def test_example_directed() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], [5]]
    d, f, parent = iterative_depth_first_search(adj)
    assert d == [1, 2, 3, 6, 7, 11, 12]
    assert f == [10, 5, 4, 9, 8, 14, 13]
    assert parent == [None, 0, 1, 0, 3, None, 5]


def test_example_undirected() -> None:
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)]
    adj: list[list[int]] = [[] for _ in range(8)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for lst in adj:
        lst.sort()
    d, f, parent = iterative_depth_first_search(adj)
    assert sorted(range(8), key=lambda v: d[v]) == [0, 1, 3, 2, 4, 5, 6, 7]
    assert parent == [None, 0, 3, 1, 2, 4, 5, None]


def test_small_cases() -> None:
    assert iterative_depth_first_search([]) == ([], [], [])
    assert iterative_depth_first_search([[]]) == ([1], [2], [None])
    assert iterative_depth_first_search([[0]]) == ([1], [2], [None])


def test_long_path() -> None:
    n = 100000
    adj = [[i + 1] for i in range(n - 1)] + [[]]
    d, f, parent = iterative_depth_first_search(adj)
    assert d == list(range(1, n + 1))
    assert f == list(range(2 * n, n, -1))
    assert parent[n - 1] == n - 2


def test_random_against_recursive() -> None:
    rng = random.Random(7310)
    sys.setrecursionlimit(10000)
    for trial in range(600):
        n = rng.randint(1, 12)
        m = rng.randint(0, 3 * n)
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(m):
            a, b = rng.randrange(n), rng.randrange(n)
            adj[a].append(b)
            if trial % 2 == 1:
                adj[b].append(a)
        assert iterative_depth_first_search(adj) == recursive_dfs(adj)
