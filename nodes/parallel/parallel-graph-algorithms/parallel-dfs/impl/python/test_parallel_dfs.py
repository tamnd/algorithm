# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-dfs/. The authors are listed in prov/A3D0QP.jsonl.

import random

from parallel_dfs import Cost, parallel_dfs


def stack_dfs(adj: list[list[int]], s: int) -> tuple[list[int], list[int | None], int]:
    """Sequential DFS with an explicit stack. Returns preorder, parent and the tree height."""
    n = len(adj)
    parent: list[int | None] = [None] * n
    depth = [0] * n
    parent[s] = s
    order = [s]
    stack = [(s, 0)]
    while stack:
        u, i = stack[-1]
        if i < len(adj[u]):
            stack[-1] = (u, i + 1)
            v = adj[u][i]
            if parent[v] is None:
                parent[v] = u
                depth[v] = depth[u] + 1
                order.append(v)
                stack.append((v, 0))
        else:
            stack.pop()
    return order, parent, max(depth[v] for v in order)


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def check(adj: list[list[int]], s: int) -> None:
    c = Cost()
    order, parent = parallel_dfs(adj, s, c)
    want_order, want_parent, h = stack_dfs(adj, s)
    assert order == want_order
    assert parent == want_parent
    assert c.rounds == h + 1


def test_example() -> None:
    adj = [[2, 1], [3], [1, 3], [0]]  # directed, with the cycle 0 -> 2 -> 1 -> 3 -> 0
    order, parent = parallel_dfs(adj, 0)
    assert order == [0, 2, 1, 3]
    assert parent == [0, 2, 0, 1]


def test_undirected_families() -> None:
    rng = random.Random(31)
    for n in (1, 2, 5, 12, 25):
        graphs = [
            undirected(n, []),
            undirected(n, [(i, i + 1) for i in range(n - 1)]),
            undirected(n, [(0, i) for i in range(1, n)]),
            undirected(n, [(i, j) for i in range(n) for j in range(i + 1, n)]),
        ]
        if n >= 3:
            graphs.append(undirected(n, [(i, (i + 1) % n) for i in range(n)]))
        for adj in graphs:
            for a in adj:
                rng.shuffle(a)
            for s in range(n):
                check(adj, s)


def test_random_directed_and_dags() -> None:
    rng = random.Random(32)
    for t in range(600):
        n = rng.randint(1, 14)
        p = rng.choice([0.1, 0.2, 0.35, 0.6])
        if t % 2 == 0:  # a DAG under a random order of the vertices
            perm = list(range(n))
            rng.shuffle(perm)
            rank = {v: r for r, v in enumerate(perm)}
            adj = [[v for v in range(n) if rank[u] < rank[v] and rng.random() < p] for u in range(n)]
        else:  # any directed graph, with cycles and self-loops
            adj = [[v for v in range(n) if rng.random() < p] for u in range(n)]
        for a in adj:
            rng.shuffle(a)
        check(adj, rng.randrange(n))


def test_random_undirected() -> None:
    rng = random.Random(33)
    for _ in range(300):
        n = rng.randint(1, 16)
        p = rng.choice([0.1, 0.25, 0.5])
        adj = undirected(n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p])
        for a in adj:
            rng.shuffle(a)
        check(adj, 0)


def test_path_needs_n_rounds() -> None:
    n = 30
    adj = [[i + 1] if i + 1 < n else [] for i in range(n)]
    c = Cost()
    parallel_dfs(adj, 0, c)
    assert c.rounds == n
