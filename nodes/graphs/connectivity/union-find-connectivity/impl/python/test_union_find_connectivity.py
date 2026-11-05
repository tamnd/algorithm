# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/union-find-connectivity/. The authors are listed in prov/TDTBHE.jsonl.

import random

from union_find_connectivity import union_find_connectivity


def bfs_components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    label = [-1] * n
    for s in range(n):
        if label[s] == -1:
            label[s] = s
            queue = [s]
            for x in queue:
                for y in adj[x]:
                    if label[y] == -1:
                        label[y] = s
                        queue.append(y)
    return label


def same_partition(a: list[int], b: list[int]) -> bool:
    n = len(a)
    return len(b) == n and all((a[i] == a[j]) == (b[i] == b[j]) for i in range(n) for j in range(n))


def test_example() -> None:
    edges = [(0, 1), (2, 3), (1, 2), (4, 5), (3, 0), (6, 6), (5, 4), (1, 3)]
    assert union_find_connectivity(8, edges) == [0, 0, 0, 0, 4, 4, 6, 7]


def test_edges() -> None:
    assert union_find_connectivity(0, []) == []
    assert union_find_connectivity(1, []) == [0]
    assert union_find_connectivity(1, [(0, 0), (0, 0)]) == [0]
    assert union_find_connectivity(3, [(0, 1), (1, 0), (0, 1)]) == [0, 0, 2]
    assert union_find_connectivity(3, [(2, 1)]) == [0, 2, 2]


def test_long_chain() -> None:
    n = 50000
    comp = union_find_connectivity(n, [(i + 1, i) for i in range(n - 1)])
    assert len(set(comp)) == 1


def test_random() -> None:
    rng = random.Random(33)
    for _ in range(600):
        n = rng.randrange(0, 10)
        m = rng.randrange(0, 2 * n + 1) if n else 0
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        comp = union_find_connectivity(n, edges)
        assert same_partition(comp, bfs_components(n, edges))
        assert all(comp[comp[v]] == comp[v] for v in range(n))
