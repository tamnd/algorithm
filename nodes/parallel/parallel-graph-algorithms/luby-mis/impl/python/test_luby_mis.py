# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luby-mis/. The authors are listed in prov/HV73GG.jsonl.

import math
import random

from luby_mis import Cost, luby_mis


def to_adj(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def is_mis(adj: list[list[int]], I: set[int]) -> bool:
    independent = all(u not in I for v in I for u in adj[v])
    maximal = all(v in I or any(u in I for u in adj[v]) for v in range(len(adj)))
    return independent and maximal


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
    adj = to_adj(7, [(i, i + 1) for i in range(6)])
    c = Cost()
    I = luby_mis(adj, random.Random(0), c, first=[6, 0, 2, 3, 4, 1, 5])
    assert I == {1, 3, 5}
    assert c.rounds == 2
    assert c.edges == [6, 0]


def test_mis_property() -> None:
    rng = random.Random(1)
    runs = 0
    for n, edges in family(rng):
        adj = to_adj(n, edges)
        for _ in range(3):
            c = Cost()
            I = luby_mis(adj, random.Random(rng.random()), c)
            assert is_mis(adj, I)
            assert c.rounds <= max(1, n)  # at least the vertex of least priority leaves in each round
            runs += 1
    assert runs >= 500


def test_edges_halve_in_expectation() -> None:
    # over many rounds, the live edges removed are at least half of the live edges, on average
    rng = random.Random(2)
    before = 0
    after = 0
    for _ in range(200):
        n = rng.randint(5, 60)
        p = rng.choice([0.05, 0.2, 0.5])
        adj = to_adj(n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p])
        c = Cost()
        luby_mis(adj, random.Random(rng.random()), c)
        for a, b in zip(c.edges, c.edges[1:] + [0]):
            before += a
            after += b
    assert after <= 0.5 * before


def test_mean_rounds() -> None:
    # c = 1: the mean number of rounds stays below log2 n on random graphs with average degree 8
    rng = random.Random(3)
    for n in (64, 256, 1024):
        total = 0
        for _ in range(10):
            edges = set()
            while len(edges) < 4 * n:
                u, v = rng.randrange(n), rng.randrange(n)
                if u != v:
                    edges.add((min(u, v), max(u, v)))
            c = Cost()
            luby_mis(to_adj(n, sorted(edges)), random.Random(rng.random()), c)
            total += c.rounds
        assert total / 10 <= math.log2(n)
