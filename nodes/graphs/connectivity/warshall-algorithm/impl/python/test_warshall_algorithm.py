# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warshall-algorithm/. The authors are listed in prov/036P3Q.jsonl.

import random

from warshall_algorithm import warshall_algorithm


def oracle(adj: list[list[int]]) -> list[list[bool]]:
    """R[u][v] by a search from the successors of u (walks of length at least 1)."""
    n = len(adj)
    out = []
    for u in range(n):
        seen = set(adj[u])
        todo = list(seen)
        while todo:
            x = todo.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    todo.append(y)
        out.append([v in seen for v in range(n)])
    return out


def test_example() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], [5]]
    r = warshall_algorithm(adj)
    a = [True] * 5 + [False] * 2
    assert r[:4] == [a] * 4
    assert r[4] == [False] * 7
    assert r[5] == r[6] == [False] * 4 + [True] * 3
    assert sum(map(sum, r)) == 26


def test_edges() -> None:
    assert warshall_algorithm([]) == []
    assert warshall_algorithm([[]]) == [[False]]
    assert warshall_algorithm([[0]]) == [[True]]
    assert warshall_algorithm([[1, 1], []]) == [[False, True], [False, False]]
    # 3-cycle listed so that the wrong loop order (i outside k) misses R[0][0]
    assert warshall_algorithm([[2], [0], [1]]) == [[True] * 3] * 3
    # undirected path 0 - 1 - 2 given with both arcs: one component, full matrix
    assert warshall_algorithm([[1], [0, 2], [1]]) == [[True] * 3] * 3


def test_path() -> None:
    n = 40
    adj = [[i + 1] for i in range(n - 1)] + [[]]
    r = warshall_algorithm(adj)
    assert all(r[u][v] == (u < v) for u in range(n) for v in range(n))


def test_random() -> None:
    rng = random.Random(36)
    for _ in range(700):
        n = rng.randrange(1, 10)
        m = rng.randrange(0, 3 * n)
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(m):
            adj[rng.randrange(n)].append(rng.randrange(n))
        assert warshall_algorithm(adj) == oracle(adj)
