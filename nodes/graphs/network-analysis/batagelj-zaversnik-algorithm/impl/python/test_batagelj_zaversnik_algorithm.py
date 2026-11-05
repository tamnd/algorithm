# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batagelj-zaversnik-algorithm/. The authors are listed in prov/HTAYEM.jsonl.

import random

from batagelj_zaversnik_algorithm import batagelj_zaversnik_algorithm


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def oracle(adj: list[list[int]]) -> list[int]:
    """Core numbers from the definition: the best minimum degree over all vertex sets."""
    n = len(adj)
    core = [0] * n
    for mask in range(1, 1 << n):
        members = [v for v in range(n) if mask >> v & 1]
        low = min(sum(1 for u in adj[v] if mask >> u & 1) for v in members)
        for v in members:
            if low > core[v]:
                core[v] = low
    return core


EXAMPLE = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (4, 7)]


def test_example() -> None:
    adj = undirected(9, EXAMPLE)
    assert batagelj_zaversnik_algorithm(adj) == [3, 3, 3, 3, 2, 2, 2, 1, 0]


def test_edges() -> None:
    assert batagelj_zaversnik_algorithm([]) == []
    assert batagelj_zaversnik_algorithm([[]]) == [0]
    assert batagelj_zaversnik_algorithm(undirected(2, [(0, 1)])) == [1, 1]
    path = undirected(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    assert batagelj_zaversnik_algorithm(path) == [1] * 5
    k5 = undirected(5, [(u, v) for u in range(5) for v in range(u + 1, 5)])
    assert batagelj_zaversnik_algorithm(k5) == [4] * 5
    star = undirected(6, [(0, v) for v in range(1, 6)])
    assert batagelj_zaversnik_algorithm(star) == [1] * 6


def test_long_path_no_recursion() -> None:
    n = 100000
    adj = undirected(n, [(i, i + 1) for i in range(n - 1)])
    assert batagelj_zaversnik_algorithm(adj) == [1] * n


def test_random_against_oracle() -> None:
    rng = random.Random(7713)
    for _ in range(700):
        n = rng.randint(1, 10)
        p = rng.random()
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        rng.shuffle(edges)
        adj = undirected(n, edges)
        for lst in adj:
            rng.shuffle(lst)
        assert batagelj_zaversnik_algorithm(adj) == oracle(adj)
