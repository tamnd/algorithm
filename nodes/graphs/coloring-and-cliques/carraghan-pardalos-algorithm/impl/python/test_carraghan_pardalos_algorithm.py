# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carraghan-pardalos-algorithm/. The authors are listed in prov/F3SXV2.jsonl.

import itertools
import random

from carraghan_pardalos_algorithm import carraghan_pardalos_algorithm


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def is_clique(k: list[int], edges: list[tuple[int, int]]) -> bool:
    es = {frozenset(e) for e in edges}
    return all(frozenset(p) in es for p in itertools.combinations(k, 2))


def omega(n: int, edges: list[tuple[int, int]]) -> int:
    for r in range(n, 0, -1):
        if any(is_clique(list(s), edges) for s in itertools.combinations(range(n), r)):
            return r
    return 0


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (0, 6), (5, 6),
             (1, 4), (6, 7)]
    assert carraghan_pardalos_algorithm(make(8, edges)) == [1, 2, 3, 4]


def test_edges() -> None:
    assert carraghan_pardalos_algorithm([]) == []
    assert carraghan_pardalos_algorithm([[]]) == [0]
    assert carraghan_pardalos_algorithm(make(4, [])) == [0]
    assert carraghan_pardalos_algorithm(make(2, [(0, 1)])) == [0, 1]
    for n in range(1, 9):
        assert carraghan_pardalos_algorithm(make(n, list(itertools.combinations(range(n), 2)))) == list(range(n))
    for n in range(4, 10):
        got = carraghan_pardalos_algorithm(make(n, [(i, (i + 1) % n) for i in range(n)]))
        assert len(got) == 2
    k333 = [(u, v) for u, v in itertools.combinations(range(9), 2) if u // 3 != v // 3]
    got = carraghan_pardalos_algorithm(make(9, k333))
    assert len(got) == 3 and is_clique(got, k333)


def test_random_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(700):
        n = rng.randrange(0, 10)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        got = carraghan_pardalos_algorithm(make(n, edges))
        assert got == sorted(set(got))
        assert all(0 <= v < n for v in got)
        assert is_clique(got, edges)
        assert len(got) == omega(n, edges)
