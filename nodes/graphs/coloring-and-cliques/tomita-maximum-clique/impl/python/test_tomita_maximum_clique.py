# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tomita-maximum-clique/. The authors are listed in prov/B53EJC.jsonl.

import itertools
import random

from tomita_maximum_clique import number_sort, tomita_maximum_clique


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def is_clique(adj: list[list[int]], s: list[int]) -> bool:
    return all(v in adj[u] for u, v in itertools.combinations(s, 2))


def omega(adj: list[list[int]]) -> int:
    n = len(adj)
    for k in range(n, 0, -1):
        if any(is_clique(adj, list(s)) for s in itertools.combinations(range(n), k)):
            return k
    return 0


def check(adj: list[list[int]]) -> list[int]:
    q = tomita_maximum_clique(adj)
    assert q == sorted(set(q))
    assert all(0 <= v < len(adj) for v in q)
    assert is_clique(adj, q)
    assert len(q) == omega(adj)
    return q


def complement(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    es = {frozenset(e) for e in edges}
    return [(i, j) for i in range(n) for j in range(i + 1, n) if frozenset((i, j)) not in es]


def cyc(n: int) -> list[tuple[int, int]]:
    return [(i, (i + 1) % n) for i in range(n)]


EXAMPLE = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 6), (4, 5), (5, 6)]


def test_example() -> None:
    assert check(make(7, EXAMPLE)) == [0, 1, 2, 3]


def test_number_sort() -> None:
    adj = make(5, cyc(5))
    nbr = [set(a) for a in adj]
    order, col = number_sort([0, 1, 2, 3, 4], nbr)
    assert order == [0, 2, 1, 3, 4] and col == [1, 1, 2, 2, 3]


def test_edges() -> None:
    assert tomita_maximum_clique([]) == []
    assert tomita_maximum_clique([[]]) == [0]
    assert len(tomita_maximum_clique([[], [], []])) == 1
    for n in range(1, 9):
        kn = make(n, [(i, j) for i in range(n) for j in range(i + 1, n)])
        assert check(kn) == list(range(n))
    for n in (3, 5, 7, 9):
        assert len(check(make(n, cyc(n)))) == (3 if n == 3 else 2)
    for n in (5, 6, 7, 8):
        assert len(check(make(n, complement(n, cyc(n))))) == n // 2


def test_bipartite_and_multipartite() -> None:
    kmn = make(7, [(i, j) for i in range(3) for j in range(3, 7)])
    assert len(check(kmn)) == 2
    k333 = make(9, [(i, j) for i in range(9) for j in range(i + 1, 9) if i // 3 != j // 3])
    assert len(check(k333)) == 3


def test_random_against_brute_force() -> None:
    rng = random.Random(6061)
    for _ in range(700):
        n = rng.randint(0, 10)
        p = rng.random()
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        check(make(n, edges))


def test_planted() -> None:
    rng = random.Random(77)
    for _ in range(30):
        n = 40
        edges = {(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3}
        plant = sorted(rng.sample(range(n), 9))
        edges |= set(itertools.combinations(plant, 2))
        q = tomita_maximum_clique(make(n, sorted(edges)))
        assert len(q) >= 9 and is_clique(make(n, sorted(edges)), q)
