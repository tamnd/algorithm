# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsukiyama-algorithm/. The authors are listed in prov/32F5MK.jsonl.

import itertools
import random

import pytest

from tsukiyama_algorithm import count_maximal_independent_sets, maximal_independent_sets


def brute_force(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    out = []
    for mask in range(1 << n):
        s = {v for v in range(n) if mask >> v & 1}
        if any(adj[v] & s for v in s):
            continue
        if all(v in s or adj[v] & s for v in range(n)):
            out.append(sorted(s))
    return sorted(out)


def random_graph(rng, n, p):
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def test_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(400):
        n = rng.randrange(0, 11)
        edges = random_graph(rng, n, rng.random())
        got = list(maximal_independent_sets(n, edges))
        assert len(got) == len({tuple(s) for s in got})
        assert sorted(got) == brute_force(n, edges)


def test_small_graphs() -> None:
    assert list(maximal_independent_sets(0, [])) == [[]]
    assert list(maximal_independent_sets(3, [])) == [[0, 1, 2]]
    # A path 0 - 1 - 2 - 3.
    assert sorted(maximal_independent_sets(4, [(0, 1), (1, 2), (2, 3)])) == [[0, 2], [0, 3], [1, 3]]
    # The complete graph has its vertices as singletons.
    k5 = list(itertools.combinations(range(5), 2))
    assert sorted(maximal_independent_sets(5, k5)) == [[v] for v in range(5)]


def test_moon_moser_bound() -> None:
    # Disjoint triangles reach 3^(n/3).
    for k in range(1, 6):
        tri = [(3 * j + a, 3 * j + b) for j in range(k) for a, b in [(0, 1), (1, 2), (0, 2)]]
        assert count_maximal_independent_sets(3 * k, tri) == 3**k
    # The largest count over all graphs with n vertices, for n up to 5.
    expected = {1: 1, 2: 2, 3: 3, 4: 4, 5: 6}
    for n, best in expected.items():
        pairs = list(itertools.combinations(range(n), 2))
        top = 0
        for mask in range(1 << len(pairs)):
            edges = [pairs[k] for k in range(len(pairs)) if mask >> k & 1]
            top = max(top, count_maximal_independent_sets(n, edges))
        assert top == best


def test_duplicate_edges_and_errors() -> None:
    assert sorted(maximal_independent_sets(2, [(0, 1), (1, 0)])) == [[0], [1]]
    with pytest.raises(ValueError):
        list(maximal_independent_sets(2, [(0, 0)]))
    with pytest.raises(ValueError):
        list(maximal_independent_sets(2, [(0, 2)]))
    with pytest.raises(ValueError):
        list(maximal_independent_sets(-1, []))


def test_larger_graph() -> None:
    rng = random.Random(9)
    n = 40
    edges = random_graph(rng, n, 0.2)
    sols = list(maximal_independent_sets(n, edges))
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    assert len(sols) == len({tuple(s) for s in sols})
    for s in sols:
        t = set(s)
        assert not any(adj[v] & t for v in t)
        assert all(v in t or adj[v] & t for v in range(n))
