# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bron-kerbosch/. The authors are listed in prov/SFJ221.jsonl.

import itertools
import random

from bron_kerbosch import bron_kerbosch


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def brute(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    es = {frozenset(e) for e in edges}
    cl = [
        set(s)
        for r in range(n + 1)
        for s in itertools.combinations(range(n), r)
        if all(frozenset(p) in es for p in itertools.combinations(s, 2))
    ]
    return sorted(sorted(c) for c in cl if not any(c < d for d in cl))


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (0, 6), (5, 6)]
    assert bron_kerbosch(make(7, edges)) == [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [5, 6], [0, 6]]


def test_edges() -> None:
    assert bron_kerbosch([]) == [[]]
    assert bron_kerbosch([[]]) == [[0]]
    assert sorted(bron_kerbosch(make(4, []))) == [[0], [1], [2], [3]]
    for n in range(1, 8):
        assert bron_kerbosch(make(n, list(itertools.combinations(range(n), 2)))) == [list(range(n))]
    for n in range(4, 10):
        cyc = [(i, (i + 1) % n) for i in range(n)]
        assert sorted(bron_kerbosch(make(n, cyc))) == sorted(sorted(e) for e in cyc)
    k333 = [(u, v) for u, v in itertools.combinations(range(9), 2) if u // 3 != v // 3]
    got = bron_kerbosch(make(9, k333))
    assert len(got) == 27 and sorted(got) == brute(9, k333)
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    assert sorted(bron_kerbosch(make(6, k33))) == sorted([i, j] for i, j in k33)


def test_random_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(600):
        n = rng.randrange(0, 9)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        got = bron_kerbosch(make(n, edges))
        assert len(got) == len({tuple(c) for c in got})
        assert sorted(got) == brute(n, edges)
