# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/degeneracy-ordering/. The authors are listed in prov/JTSFJW.jsonl.

import itertools
import random

from degeneracy_ordering import degeneracy_ordering


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def brute_degeneracy(n: int, edges: list[tuple[int, int]]) -> int:
    """max over non-empty vertex sets S of the minimum degree of G[S]."""
    best = 0
    for r in range(1, n + 1):
        for s in itertools.combinations(range(n), r):
            ss = set(s)
            deg = {v: 0 for v in s}
            for u, v in edges:
                if u in ss and v in ss:
                    deg[u] += 1
                    deg[v] += 1
            best = max(best, min(deg.values()))
    return best


def greedy(adj: list[list[int]], order: list[int]) -> list[int]:
    c = [0] * len(adj)
    for v in order:
        taken = {c[w] for w in adj[v]}
        k = 1
        while k in taken:
            k += 1
        c[v] = k
    return c


def check(n: int, edges: list[tuple[int, int]]) -> int:
    adj = make(n, edges)
    order, d = degeneracy_ordering(adj)
    assert sorted(order) == list(range(n))
    pos = {v: i for i, v in enumerate(order)}
    later = [sum(1 for w in adj[v] if pos[w] > pos[v]) for v in range(n)]
    assert max(later, default=0) == d
    c = greedy(adj, order[::-1])
    assert all(c[u] != c[v] for u, v in edges)
    assert max(c, default=0) <= d + 1
    return d


EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (0, 6), (5, 6)]


def test_example() -> None:
    order, d = degeneracy_ordering(make(7, EXAMPLE))
    assert (order, d) == ([6, 5, 4, 3, 2, 1, 0], 2)
    assert greedy(make(7, EXAMPLE), order[::-1]) == [1, 2, 3, 1, 2, 3, 2]


def test_edges() -> None:
    assert degeneracy_ordering([]) == ([], 0)
    assert degeneracy_ordering([[]]) == ([0], 0)
    for k in range(1, 8):
        assert check(k, list(itertools.combinations(range(k), 2))) == k - 1
    for k in range(3, 10):
        assert check(k, [(i, (i + 1) % k) for i in range(k)]) == 2
    assert check(6, [(i, j) for i in range(3) for j in range(3, 6)]) == 3
    assert check(10, [(0, i) for i in range(1, 10)]) == 1  # a star
    assert check(5, [(i, i + 1) for i in range(4)]) == 1  # a path


def test_random_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(700):
        n = rng.randrange(0, 9)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        rng.shuffle(edges)
        assert check(n, edges) == brute_degeneracy(n, edges)
