# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-scc/. The authors are listed in prov/JH9ZVM.jsonl.

import random

from tarjan_scc import tarjan_scc


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
    comp = tarjan_scc(adj)
    r = [reach(adj, u) for u in range(n)]
    for u in range(n):
        for v in range(n):
            assert (comp[u] == comp[v]) == (v in r[u] and u in r[v])
    for u in range(n):
        for v in adj[u]:
            assert comp[u] >= comp[v]
    if n:
        assert sorted(set(comp)) == list(range(max(comp) + 1))


def test_example() -> None:
    adj = [[1, 3, 2], [2], [0], [2, 4], [], [4, 6], [5]]
    assert tarjan_scc(adj) == [1, 1, 1, 1, 0, 2, 2]


def test_edges() -> None:
    assert tarjan_scc([]) == []
    assert tarjan_scc([[]]) == [0]
    assert tarjan_scc([[0]]) == [0]
    assert tarjan_scc([[0, 0, 1], [1]]) == [1, 0]
    assert tarjan_scc([[1, 1], [0]]) == [0, 0]
    assert tarjan_scc([[1], [2], []]) == [2, 1, 0]
    assert tarjan_scc([[], [0], [1]]) == [0, 1, 2]
    cycle = [[(i + 1) % 6] for i in range(6)]
    assert tarjan_scc(cycle) == [0] * 6
    # undirected graph given with both arcs: components are connected components
    assert tarjan_scc([[1], [0], [3], [2]]) == [0, 0, 1, 1]


def test_cross_arc_to_stack() -> None:
    # 0 -> 1 -> 0 and 0 -> 2 -> 1: the cross arc 2 -> 1 goes to a vertex on the stack
    assert tarjan_scc([[1, 2], [0], [1]]) == [0, 0, 0]
    # cross arc 2 -> 1 into a finished component {1}
    assert tarjan_scc([[1, 2], [], [1]]) == [2, 0, 1]


def test_long_path() -> None:
    n = 20000
    path = [[i + 1] for i in range(n - 1)] + [[]]
    assert tarjan_scc(path) == list(range(n - 1, -1, -1))
    path[-1] = [0]
    assert tarjan_scc(path) == [0] * n


def test_random() -> None:
    rng = random.Random(21)
    for _ in range(600):
        n = rng.randrange(1, 9)
        m = rng.randrange(0, 3 * n)
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(m):
            adj[rng.randrange(n)].append(rng.randrange(n))
        check(adj)
