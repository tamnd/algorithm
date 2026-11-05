# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-first-search/. The authors are listed in prov/Q8B7W6.jsonl.

import random
import sys

from depth_first_search import depth_first_search


def recursive_dfs(adj: list[list[int]]) -> tuple[list[int], list[int], list[int | None]]:
    """The textbook recursive procedure, used as the oracle on small graphs."""
    n = len(adj)
    seen = [False] * n
    d, f = [0] * n, [0] * n
    parent: list[int | None] = [None] * n
    clock = [0]

    def visit(u: int) -> None:
        clock[0] += 1
        d[u] = clock[0]
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                parent[v] = u
                visit(v)
        clock[0] += 1
        f[u] = clock[0]

    for u in range(n):
        if not seen[u]:
            visit(u)
    return d, f, parent


def reachable(adj: list[list[int]], s: int) -> set[int]:
    seen, todo = {s}, [s]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


def test_example() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], [5]]
    d, f, parent = depth_first_search(adj)
    assert d == [1, 2, 3, 6, 7, 11, 12]
    assert f == [10, 5, 4, 9, 8, 14, 13]
    assert parent == [None, 0, 1, 0, 3, None, 5]


def test_edges() -> None:
    assert depth_first_search([]) == ([], [], [])
    assert depth_first_search([[0]]) == ([1], [2], [None])
    assert depth_first_search([[], []]) == ([1, 3], [2, 4], [None, None])


def test_long_path() -> None:
    n = 100000
    adj = [[i + 1] for i in range(n - 1)] + [[]]
    d, f, _ = depth_first_search(adj)
    assert d[n - 1] == n and f[n - 1] == n + 1 and f[0] == 2 * n


def test_random_against_recursive() -> None:
    sys.setrecursionlimit(10000)
    rng = random.Random(7781)
    for _ in range(600):
        n = rng.randint(1, 12)
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 3 * n)):
            adj[rng.randrange(n)].append(rng.randrange(n))
        d, f, parent = depth_first_search(adj)
        assert (d, f, parent) == recursive_dfs(adj)
        assert sorted(d + f) == list(range(1, 2 * n + 1))
        for u in range(n):
            for v in range(n):
                nested = d[u] < d[v] < f[v] < f[u]
                disjoint = f[u] < d[v] or f[v] < d[u]
                assert u == v or nested or disjoint or d[v] < d[u] < f[u] < f[v]
        for r in range(n):
            if parent[r] is None:
                tree = {v for v in range(n) if d[r] <= d[v] and f[v] <= f[r]}
                assert tree <= reachable(adj, r)
