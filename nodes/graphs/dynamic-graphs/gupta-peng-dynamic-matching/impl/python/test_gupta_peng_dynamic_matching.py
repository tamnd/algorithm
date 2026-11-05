# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gupta-peng-dynamic-matching/. The authors are listed in prov/PZK1QP.jsonl.

import random
from fractions import Fraction

from gupta_peng_dynamic_matching import DynamicMatching, _augment_to_maximum


def _nu(n: int, edges: set[tuple[int, int]]) -> int:
    """Maximum matching size by dynamic programming over vertex subsets."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    f = [0] * (1 << n)
    for mask in range(1, 1 << n):
        i = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << i)
        best = f[rest]
        nb = adj[i] & rest
        while nb:
            j = (nb & -nb).bit_length() - 1
            nb &= nb - 1
            best = max(best, 1 + f[rest & ~(1 << j)])
        f[mask] = best
    return f[(1 << n) - 1]


def test_blossom_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 9)
        edges = set()
        for _ in range(rng.randint(0, 20)):
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v:
                edges.add((min(u, v), max(u, v)))
        adj: list[set[int]] = [set() for _ in range(n)]
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        mate = [-1] * n
        _augment_to_maximum(n, adj, mate)
        assert all(mate[v] == -1 or (mate[mate[v]] == v and mate[v] in adj[v]) for v in range(n))
        assert sum(1 for v in range(n) if mate[v] > v) == _nu(n, edges)


def test_example() -> None:
    g = DynamicMatching(6, Fraction(1, 2))
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]:
        g.insert(u, v)
    assert len(g.matching()) == 3


def test_random_updates_against_brute_force() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(2, 9)
        eps = rng.choice([Fraction(1, 4), Fraction(1, 2), Fraction(1)])
        g = DynamicMatching(n, eps)
        edges: set[tuple[int, int]] = set()
        for _ in range(rng.randint(1, 40)):
            u, v = rng.randrange(n), rng.randrange(n)
            if u == v:
                continue
            e = (min(u, v), max(u, v))
            if e in edges and rng.random() < 0.5:
                edges.discard(e)
                g.delete(u, v)
            else:
                edges.add(e)
                g.insert(u, v)
            m = g.matching()
            used = [x for e2 in m for x in e2]
            assert len(used) == len(set(used))
            assert all(e2 in edges for e2 in m)
            assert len(m) == g.size
            assert (1 + eps) * len(m) >= _nu(n, edges)


def test_rebuilds_are_rare_on_large_matchings() -> None:
    n = 400
    g = DynamicMatching(n, Fraction(1, 2))
    for i in range(0, n, 2):
        g.insert(i, i + 1)
    for i in range(1, n - 1, 2):
        g.insert(i, i + 1)
    before = g.rebuilds
    for i in range(0, 80, 2):
        g.delete(i, i + 1)
    assert g.rebuilds - before <= 2
