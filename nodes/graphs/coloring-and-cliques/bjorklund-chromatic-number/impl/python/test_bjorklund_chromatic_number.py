# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bjorklund-chromatic-number/. The authors are listed in prov/X7DPRF.jsonl.

import itertools
import random

from bjorklund_chromatic_number import bjorklund_chromatic_number


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def chi_brute(n: int, edges: list[tuple[int, int]]) -> int:
    for k in range(n + 1):
        for col in itertools.product(range(k), repeat=n):
            if all(col[u] != col[v] for u, v in edges):
                return k
    return n


def test_example() -> None:
    c5 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    assert bjorklund_chromatic_number(make(5, c5)) == 3


def test_edges() -> None:
    assert bjorklund_chromatic_number([]) == 0
    assert bjorklund_chromatic_number([[]]) == 1
    assert bjorklund_chromatic_number(make(4, [])) == 1
    assert bjorklund_chromatic_number(make(2, [(0, 1)])) == 2
    k5 = list(itertools.combinations(range(5), 2))
    assert bjorklund_chromatic_number(make(5, k5)) == 5


def test_petersen() -> None:
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    assert bjorklund_chromatic_number(make(10, outer + spokes + inner)) == 3


def test_random_against_brute_force() -> None:
    rng = random.Random(2009)
    for _ in range(600):
        n = rng.randint(0, 7)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        assert bjorklund_chromatic_number(make(n, edges)) == chi_brute(n, edges)
