# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tremaux-traversal/. The authors are listed in prov/BKR094.jsonl.

import random
from collections import Counter

from tremaux_traversal import tremaux_traversal


def dfs_oracle(n: int, edges: list[tuple[int, int]], s: int) -> tuple[list[int], list[int | None]]:
    """Independent oracle: recursive DFS preorder and parents, lists in edge order."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        if b != a:
            adj[b].append(a)
    seen = [False] * n
    parent: list[int | None] = [None] * n
    order: list[int] = []

    def visit(u: int) -> None:
        seen[u] = True
        order.append(u)
        for w in adj[u]:
            if not seen[w]:
                parent[w] = u
                visit(w)

    visit(s)
    return order, parent


def check_walk(n: int, edges: list[tuple[int, int]], s: int, walk: list[int]) -> None:
    assert walk[0] == s and walk[-1] == s
    comp = set(walk)
    want = Counter()
    for a, b in edges:
        if a in comp:
            want[(min(a, b), max(a, b))] += 2
    used = Counter((min(x, y), max(x, y)) for x, y in zip(walk, walk[1:]))
    assert used == want  # each passage of the component is walked exactly twice


def first_visits(walk: list[int]) -> list[int]:
    seen: set[int] = set()
    out = []
    for v in walk:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)]
    walk, parent = tremaux_traversal(8, edges, 0)
    assert walk == [0, 1, 3, 2, 0, 2, 4, 5, 3, 5, 6, 5, 4, 2, 3, 1, 0]
    assert parent == [None, 0, 3, 1, 2, 4, 5, None]
    check_walk(8, edges, 0, walk)


def test_small_cases() -> None:
    assert tremaux_traversal(1, [], 0) == ([0], [None])
    assert tremaux_traversal(2, [(0, 1)], 0) == ([0, 1, 0], [None, 0])
    walk, _ = tremaux_traversal(1, [(0, 0)], 0)
    assert walk == [0, 0, 0]
    walk, parent = tremaux_traversal(2, [(0, 1), (1, 0)], 1)
    assert walk == [1, 0, 1, 0, 1] and parent == [1, None]


def test_long_path() -> None:
    n = 100000
    edges = [(i, i + 1) for i in range(n - 1)]
    walk, parent = tremaux_traversal(n, edges, 0)
    assert walk == list(range(n)) + list(range(n - 2, -1, -1))
    assert parent[n - 1] == n - 2


def test_random_against_dfs() -> None:
    rng = random.Random(1882)
    for _ in range(600):
        n = rng.randint(1, 10)
        m = rng.randint(0, 2 * n)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        s = rng.randrange(n)
        walk, parent = tremaux_traversal(n, edges, s)
        check_walk(n, edges, s, walk)
        order, want_parent = dfs_oracle(n, edges, s)
        assert first_visits(walk) == order
        assert parent == want_parent
