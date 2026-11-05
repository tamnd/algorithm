# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-dynamic-connectivity/. The authors are listed in prov/DAB5AT.jsonl.

import random

from offline_dynamic_connectivity import offline_dynamic_connectivity


def _naive(n: int, ops: list[tuple]) -> list:
    """Recompute components from scratch by DFS at each query."""
    edges: list[tuple[int, int]] = []
    out = []
    for op in ops:
        if op[0] == "add":
            edges.append((op[1], op[2]))
        elif op[0] == "remove":
            u, v = op[1], op[2]
            for i, (a, b) in enumerate(edges):
                if (a, b) in ((u, v), (v, u)):
                    edges.pop(i)
                    break
        else:
            adj: list[list[int]] = [[] for _ in range(n)]
            for a, b in edges:
                adj[a].append(b)
                adj[b].append(a)
            comp = [-1] * n
            c = 0
            for s in range(n):
                if comp[s] == -1:
                    comp[s] = c
                    stack = [s]
                    while stack:
                        x = stack.pop()
                        for y in adj[x]:
                            if comp[y] == -1:
                                comp[y] = c
                                stack.append(y)
                    c += 1
            if op[0] == "query":
                out.append(comp[op[1]] == comp[op[2]])
            else:
                out.append(c)
    return out


def test_example() -> None:
    ops = [
        ("add", 0, 1), ("add", 1, 2), ("query", 0, 2), ("remove", 0, 1),
        ("query", 0, 2), ("add", 2, 3), ("add", 0, 3), ("query", 0, 1),
        ("remove", 1, 2), ("count",),
    ]
    assert offline_dynamic_connectivity(4, ops) == [True, False, True, 2]


def test_empty() -> None:
    assert offline_dynamic_connectivity(3, []) == []
    assert offline_dynamic_connectivity(3, [("count",)]) == [3]


def test_random_against_naive() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(1, 7)
        ops: list[tuple] = []
        alive: list[tuple[int, int]] = []
        for _ in range(rng.randint(0, 40)):
            r = rng.random()
            if r < 0.35:
                u, v = rng.randrange(n), rng.randrange(n)
                ops.append(("add", u, v))
                alive.append((u, v))
            elif r < 0.55 and alive:
                u, v = alive.pop(rng.randrange(len(alive)))
                ops.append(("remove", v, u) if rng.random() < 0.5 else ("remove", u, v))
            else:
                ops.append(("count",))
            # a query after every update, as in the brief
            ops.append(("query", rng.randrange(n), rng.randrange(n)))
        assert offline_dynamic_connectivity(n, ops) == _naive(n, ops)


def test_long_sequence() -> None:
    n = 2000
    ops: list[tuple] = [("add", i, i + 1) for i in range(n - 1)]
    ops += [("query", 0, n - 1), ("remove", 500, 501), ("query", 0, n - 1), ("count",)]
    assert offline_dynamic_connectivity(n, ops) == [True, False, 2]
