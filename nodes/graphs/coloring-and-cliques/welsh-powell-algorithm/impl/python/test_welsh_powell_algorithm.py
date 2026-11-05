# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welsh-powell-algorithm/. The authors are listed in prov/NAP2ZB.jsonl.

import itertools
import random

from welsh_powell_algorithm import welsh_powell_algorithm


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


def first_fit(adj: list[list[int]], order: list[int]) -> list[int]:
    c = [0] * len(adj)
    for v in order:
        taken = {c[w] for w in adj[v]}
        k = 1
        while k in taken:
            k += 1
        c[v] = k
    return c


def wp_bound(adj: list[list[int]]) -> int:
    d = sorted((len(x) for x in adj), reverse=True)
    return max((min(d[i] + 1, i + 1) for i in range(len(d))), default=0)


def check(adj: list[list[int]]) -> list[int]:
    c = welsh_powell_algorithm(adj)
    n = len(adj)
    assert proper(adj, c)
    assert all(x >= 1 for x in c)
    k = max(c, default=0)
    assert set(c) == set(range(1, k + 1))
    assert k <= wp_bound(adj)
    order = sorted(range(n), key=lambda v: (-len(adj[v]), v))
    assert c == first_fit(adj, order)
    return c


EXAMPLE = [(0, 2), (0, 4), (0, 5), (0, 6), (1, 3), (2, 3), (2, 4), (3, 4), (4, 6)]


def test_example() -> None:
    adj = make(7, EXAMPLE)
    assert check(adj) == [1, 2, 3, 1, 2, 2, 3]
    assert wp_bound(adj) == 4
    assert max(first_fit(adj, list(range(7)))) == 4


def test_edges() -> None:
    assert welsh_powell_algorithm([]) == []
    assert welsh_powell_algorithm([[]]) == [1]
    assert welsh_powell_algorithm([[], [], []]) == [1, 1, 1]
    for n in range(1, 8):
        kn = make(n, [(i, j) for i in range(n) for j in range(i + 1, n)])
        assert sorted(check(kn)) == list(range(1, n + 1))
    for n in (3, 5, 7, 9):
        cyc = make(n, [(i, (i + 1) % n) for i in range(n)])
        assert max(check(cyc)) == 3
    star = make(6, [(0, i) for i in range(1, 6)])
    assert check(star) == [1, 2, 2, 2, 2, 2]


def test_bipartite() -> None:
    kmn = make(7, [(i, j) for i in range(3) for j in range(3, 7)])
    assert max(check(kmn)) == 2
    # crown graph: K_{t,t} minus a perfect matching, labelled so that ties go a1, b1, a2, b2, ...
    t = 5
    crown = make(2 * t, [(2 * i, 2 * j + 1) for i in range(t) for j in range(t) if i != j])
    assert max(check(crown)) == t


def test_random_against_brute_force() -> None:
    rng = random.Random(4157)
    for _ in range(600):
        n = rng.randint(0, 7)
        p = rng.random()
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        adj = make(n, edges)
        c = check(adj)
        assert max(c, default=0) >= chi(adj)
