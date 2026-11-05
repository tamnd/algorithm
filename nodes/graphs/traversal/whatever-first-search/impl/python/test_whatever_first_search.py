# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whatever-first-search/. The authors are listed in prov/4TP999.jsonl.

import random
from collections import deque

import pytest

from whatever_first_search import whatever_first_search


def bfs_oracle(adj: list[list[int]], s: int) -> tuple[list[int], list[int | None]]:
    """Textbook BFS: mark on enqueue, parent set at discovery."""
    parent: list[int | None] = [None] * len(adj)
    seen = [False] * len(adj)
    seen[s] = True
    order, q = [], deque([s])
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                q.append(v)
    return order, parent


def dfs_oracle(adj: list[list[int]], s: int) -> tuple[list[int], list[int | None]]:
    """Textbook recursive DFS from s: preorder and parents."""
    parent: list[int | None] = [None] * len(adj)
    seen = [False] * len(adj)
    order: list[int] = []

    def visit(u: int) -> None:
        seen[u] = True
        order.append(u)
        for v in adj[u]:
            if not seen[v]:
                parent[v] = u
                visit(v)

    visit(s)
    return order, parent


def test_example() -> None:
    adj = [[1, 2], [0, 2], [0, 1, 3], [2]]
    assert whatever_first_search(adj, 0, "stack") == ([0, 1, 2, 3], [None, 0, 1, 2])
    assert whatever_first_search(adj, 0, "queue") == ([0, 1, 2, 3], [None, 0, 0, 2])


def test_larger_example() -> None:
    adj = [[1, 2], [0, 3], [0, 3, 4], [1, 2, 5], [2, 5], [3, 4, 6], [5], []]
    assert whatever_first_search(adj, 0, "stack") == (
        [0, 1, 3, 2, 4, 5, 6],
        [None, 0, 3, 1, 2, 4, 5, None],
    )
    assert whatever_first_search(adj, 0, "queue") == (
        [0, 1, 2, 3, 4, 5, 6],
        [None, 0, 0, 1, 2, 3, 5, None],
    )


def test_edge_cases() -> None:
    assert whatever_first_search([[]], 0) == ([0], [None])
    assert whatever_first_search([[0]], 0, "queue") == ([0], [None])
    assert whatever_first_search([[], []], 1) == ([1], [None, None])
    with pytest.raises(ValueError):
        whatever_first_search([[]], 0, "heap")


def test_long_path() -> None:
    n = 100000
    adj = [[i + 1] for i in range(n - 1)] + [[]]
    order, parent = whatever_first_search(adj, 0, "stack")
    assert order == list(range(n))
    assert parent[n - 1] == n - 2


def test_random_against_oracles() -> None:
    rng = random.Random(9137)
    for trial in range(600):
        n = rng.randint(1, 10)
        p = rng.random()
        adj: list[list[int]] = [[] for _ in range(n)]
        undirected = trial % 2 == 0
        for u in range(n):
            for v in range(n):
                if (not undirected or u < v) and rng.random() < p / 2:
                    adj[u].append(v)
                    if undirected and u != v:
                        adj[v].append(u)
        for lst in adj:
            rng.shuffle(lst)
        s = rng.randrange(n)
        assert whatever_first_search(adj, s, "queue") == bfs_oracle(adj, s)
        assert whatever_first_search(adj, s, "stack") == dfs_oracle(adj, s)
