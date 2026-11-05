# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsatur/. The authors are listed in prov/4C0R37.jsonl.

import itertools
import random

from dsatur import dsatur


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def proper(adj: list[list[int]], c: list[int]) -> bool:
    return all(c[u] != c[v] for u in range(len(adj)) for v in adj[u])


def chi(adj: list[list[int]]) -> int:
    n = len(adj)
    for k in range(n + 1):
        for col in itertools.product(range(k), repeat=n):
            if proper(adj, list(col)):
                return k
    return n


def two_colorable(adj: list[list[int]]) -> bool:
    side = [-1] * len(adj)
    for s in range(len(adj)):
        if side[s] < 0:
            side[s] = 0
            stack = [s]
            while stack:
                u = stack.pop()
                for w in adj[u]:
                    if side[w] < 0:
                        side[w] = 1 - side[u]
                        stack.append(w)
                    elif side[w] == side[u]:
                        return False
    return True


def cycle(n: int) -> list[tuple[int, int]]:
    return [(i, (i + 1) % n) for i in range(n)]


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (0, 6), (5, 6)]
    assert dsatur(make(7, edges)) == [2, 3, 1, 2, 3, 1, 3]


def test_not_optimal() -> None:
    edges = [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 6), (2, 5), (3, 5), (3, 6), (4, 5), (4, 6)]
    adj = make(7, edges)
    assert dsatur(adj) == [2, 1, 3, 2, 3, 1, 4]
    assert chi(adj) == 3


def test_edges() -> None:
    assert dsatur([]) == []
    assert dsatur([[]]) == [1]
    assert dsatur(make(4, [])) == [1, 1, 1, 1]
    for n in range(1, 8):
        assert sorted(dsatur(make(n, list(itertools.combinations(range(n), 2))))) == list(range(1, n + 1))
    for n in range(3, 12):
        assert max(dsatur(make(n, cycle(n)))) == (2 if n % 2 == 0 else 3)
    for k in range(1, 7):  # crown graphs, where greedy in a bad order uses k colors
        edges = [(2 * i, 2 * j + 1) for i in range(k) for j in range(k) if i != j]
        assert max(dsatur(make(2 * k, edges))) <= 2
    for n in range(4, 10):  # wheels: hub n-1 joined to the cycle 0 .. n-2
        adj = make(n, cycle(n - 1) + [(i, n - 1) for i in range(n - 1)])
        assert max(dsatur(adj)) == (3 if (n - 1) % 2 == 0 else 4)


def test_random_bipartite_exact() -> None:
    rng = random.Random(11)
    for _ in range(500):
        a, b = rng.randrange(0, 8), rng.randrange(0, 8)
        p = rng.random()
        edges = [(i, a + j) for i in range(a) for j in range(b) if rng.random() < p]
        perm = list(range(a + b))
        rng.shuffle(perm)
        adj = make(a + b, [(perm[u], perm[v]) for u, v in edges])
        c = dsatur(adj)
        assert proper(adj, c)
        assert max(c, default=0) <= 2


def test_random_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(700):
        n = rng.randrange(0, 7)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        adj = make(n, edges)
        c = dsatur(adj)
        assert proper(adj, c)
        assert all(x >= 1 for x in c)
        for v in range(n):  # greedy property: colors 1 .. c[v]-1 all occur next to v
            assert {c[w] for w in adj[v]} >= set(range(1, c[v]))
        delta = max((len(x) for x in adj), default=0)
        assert max(c, default=0) <= delta + 1
        # with this tie-break DSATUR is optimal on every graph with at most 6 vertices
        assert max(c, default=0) == chi(adj)
        if two_colorable(adj):
            assert max(c, default=0) <= 2
