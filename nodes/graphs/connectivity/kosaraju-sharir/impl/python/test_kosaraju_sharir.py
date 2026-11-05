# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kosaraju-sharir/. The authors are listed in prov/TA3TXZ.jsonl.

import random

from kosaraju_sharir import kosaraju_sharir


def reach(adj: list[list[int]], s: int) -> set[int]:
    seen, todo = {s}, [s]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


def check(adj: list[list[int]]) -> None:
    n = len(adj)
    comp = kosaraju_sharir(adj)
    r = [reach(adj, u) for u in range(n)]
    for u in range(n):
        for v in range(n):
            assert (comp[u] == comp[v]) == (v in r[u] and u in r[v])
    for u in range(n):
        for v in adj[u]:
            assert comp[u] <= comp[v]
    if n:
        assert sorted(set(comp)) == list(range(max(comp) + 1))


def test_example() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], [5]]
    assert kosaraju_sharir(adj) == [1, 1, 1, 1, 2, 0, 0]


def test_edges() -> None:
    assert kosaraju_sharir([]) == []
    assert kosaraju_sharir([[]]) == [0]
    assert kosaraju_sharir([[0]]) == [0]
    assert kosaraju_sharir([[1, 1], [0]]) == [0, 0]
    assert kosaraju_sharir([[1], [2], []]) == [0, 1, 2]
    assert kosaraju_sharir([[], [0], [1]]) == [2, 1, 0]
    cycle = [[(i + 1) % 6] for i in range(6)]
    assert kosaraju_sharir(cycle) == [0] * 6


def test_long_path() -> None:
    n = 20000
    path = [[i + 1] for i in range(n - 1)] + [[]]
    assert kosaraju_sharir(path) == list(range(n))
    path[-1] = [0]
    assert kosaraju_sharir(path) == [0] * n


def test_random() -> None:
    rng = random.Random(20)
    for _ in range(600):
        n = rng.randrange(1, 9)
        m = rng.randrange(0, 3 * n)
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(m):
            adj[rng.randrange(n)].append(rng.randrange(n))
        check(adj)
