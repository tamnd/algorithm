# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bipartiteness-testing/. The authors are listed in prov/S82K2H.jsonl.

import itertools
import random

from bipartiteness_testing import bipartiteness_testing


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if u != v:
            adj[v].append(u)
    return adj


def brute_two_colorable(n: int, edges: list[tuple[int, int]]) -> bool:
    return any(all(c[u] != c[v] for u, v in edges) for c in itertools.product((0, 1), repeat=n))


def check(n: int, edges: list[tuple[int, int]]) -> bool:
    ok, out = bipartiteness_testing(make(n, edges))
    es = {frozenset(e) for e in edges}
    if ok:
        assert len(out) == n and all(out[u] != out[v] for u, v in edges)
    else:
        k = len(out)
        assert k % 2 == 1
        assert all(frozenset((out[i], out[(i + 1) % k])) in es for i in range(k))
        if all(u != v for u, v in edges):
            assert len(set(out)) == k  # a simple cycle
    return ok


EXAMPLE = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6)]


def test_example() -> None:
    adj = make(7, EXAMPLE)
    assert bipartiteness_testing(adj) == (True, [0, 1, 1, 0, 0, 1, 0])
    adj = make(7, EXAMPLE[:4] + [(3, 5), (3, 4), (4, 5), (5, 6)])
    assert bipartiteness_testing(adj) == (False, [3, 1, 0, 2, 4])


def test_edges() -> None:
    assert bipartiteness_testing([]) == (True, [])
    assert bipartiteness_testing([[]]) == (True, [0])
    assert bipartiteness_testing(make(1, [(0, 0)])) == (False, [0])
    for k in range(2, 9):
        assert check(k, [(i, (i + 1) % k) for i in range(k)] if k > 2 else [(0, 1)]) == (k % 2 == 0 or k == 2)
        complete = list(itertools.combinations(range(k), 2))
        assert check(k, complete) == (k <= 2)
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    assert check(6, k33)
    petersen = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    assert not check(10, petersen)


def test_random_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(1500):
        n = rng.randrange(0, 9)
        p = rng.random() * 0.6
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        rng.shuffle(edges)
        assert check(n, edges) == brute_two_colorable(n, edges)
