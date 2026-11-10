# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jones-plassmann/. The authors are listed in prov/R3VG3J.jsonl.

import math
import random

from jones_plassmann import Cost, jones_plassmann


def to_adj(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def greedy(adj: list[list[int]], priority: list[int]) -> list[int]:
    color = [-1] * len(adj)
    for v in sorted(range(len(adj)), key=lambda v: -priority[v]):
        used = {color[u] for u in adj[v]}
        k = 0
        while k in used:
            k += 1
        color[v] = k
    return color


def longest_decreasing_path(adj: list[list[int]], priority: list[int]) -> int:
    depth = [1] * len(adj)
    for v in sorted(range(len(adj)), key=lambda v: -priority[v]):
        for u in adj[v]:
            if priority[u] > priority[v]:
                depth[v] = max(depth[v], depth[u] + 1)
    return max(depth, default=0)


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out = []
    for n in (1, 2, 7, 20, 41):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))
        out.append((n, [(0, i) for i in range(1, n)]))
        if n >= 3:
            out.append((n, [(i, (i + 1) % n) for i in range(n)]))
        out.append((n, [(i, j) for i in range(n) for j in range(i + 1, n)]))
    for _ in range(150):
        n = rng.randint(1, 80)
        p = rng.choice([0.01, 0.05, 0.1, 0.3, 0.8])
        out.append((n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]))
    return out


def test_example() -> None:
    adj = to_adj(5, [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (1, 4)])
    c = Cost()
    col = jones_plassmann(adj, cost=c, priority=[3, 5, 1, 4, 2])
    assert col == [1, 0, 2, 0, 1]
    assert c.rounds == 3


def test_against_greedy() -> None:
    rng = random.Random(4)
    runs = 0
    for n, edges in family(rng):
        adj = to_adj(n, edges)
        delta = max((len(a) for a in adj), default=0)
        for _ in range(3):
            pr = list(range(n))
            rng.shuffle(pr)
            c = Cost()
            col = jones_plassmann(adj, cost=c, priority=pr)
            assert all(col[u] != col[v] for u, v in edges)  # proper
            assert max(col, default=-1) + 1 <= delta + 1  # at most Delta + 1 colors
            assert col == greedy(adj, pr)  # the greedy coloring of the priority order
            assert c.rounds == longest_decreasing_path(adj, pr)
            runs += 1
    assert runs >= 500


def test_mean_rounds() -> None:
    # random graphs of average degree 4: c = 1.5, the mean number of rounds stays below 1.5 log2 n + 2
    rng = random.Random(5)
    for n in (64, 256, 1024):
        total = 0
        for _ in range(10):
            edges = set()
            while len(edges) < 2 * n:
                u, v = rng.randrange(n), rng.randrange(n)
                if u != v:
                    edges.add((min(u, v), max(u, v)))
            c = Cost()
            jones_plassmann(to_adj(n, sorted(edges)), random.Random(rng.random()), c)
            total += c.rounds
        assert total / 10 <= 1.5 * math.log2(n) + 2
