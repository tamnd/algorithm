# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-largest-first/. The authors are listed in prov/8E77R4.jsonl.

import itertools
import random

from recursive_largest_first import recursive_largest_first


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


def reference(adj: list[list[int]]) -> list[int]:
    """Direct transcription of RLF with sets, recounting at every step."""
    n = len(adj)
    nb = [set(a) for a in adj]
    c = [0] * n
    u = set(range(n))
    k = 0
    while u:
        k += 1
        p, w = set(u), set()
        v = min(p, key=lambda x: (-len(nb[x] & u), x))
        while True:
            c[v] = k
            p.discard(v)
            u.discard(v)
            moved = nb[v] & p
            p -= moved
            w |= moved
            if not p:
                break
            v = min(p, key=lambda x: (-len(nb[x] & w), len(nb[x] & p), x))
    return c


def check(adj: list[list[int]]) -> list[int]:
    c = recursive_largest_first(adj)
    n = len(adj)
    assert c == reference(adj)
    assert proper(adj, c)
    k = max(c, default=0)
    assert set(c) == set(range(1, k + 1))
    for v in range(n):
        # every class is maximal in what was left: v has a neighbour in each earlier class
        assert {c[w] for w in adj[v] if c[w] < c[v]} == set(range(1, c[v]))
        assert c[v] <= len(adj[v]) + 1
    return c


EXAMPLE = [(0, 2), (0, 4), (0, 5), (0, 6), (1, 3), (2, 3), (2, 4), (3, 4), (4, 6)]


def test_example() -> None:
    assert check(make(7, EXAMPLE)) == [1, 2, 3, 1, 2, 2, 3]


def test_edges() -> None:
    assert recursive_largest_first([]) == []
    assert recursive_largest_first([[]]) == [1]
    assert recursive_largest_first([[], [], []]) == [1, 1, 1]
    for n in range(1, 8):
        kn = make(n, [(i, j) for i in range(n) for j in range(i + 1, n)])
        assert sorted(check(kn)) == list(range(1, n + 1))
    for n in (3, 5, 7, 9):
        assert max(check(make(n, [(i, (i + 1) % n) for i in range(n)]))) == 3
    for n in (4, 6, 8):
        assert max(check(make(n, [(i, (i + 1) % n) for i in range(n)]))) == 2


def test_bipartite() -> None:
    kmn = make(7, [(i, j) for i in range(3) for j in range(3, 7)])
    assert max(check(kmn)) == 2
    t = 5
    crown = make(2 * t, [(2 * i, 2 * j + 1) for i in range(t) for j in range(t) if i != j])
    assert max(check(crown)) == 2


def test_random_against_brute_force() -> None:
    rng = random.Random(8779)
    for _ in range(600):
        n = rng.randint(0, 7)
        p = rng.random()
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        adj = make(n, edges)
        c = check(adj)
        assert max(c, default=0) >= chi(adj)


def test_random_larger() -> None:
    rng = random.Random(2201)
    for _ in range(100):
        n = rng.randint(8, 30)
        p = rng.random()
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        check(make(n, edges))
