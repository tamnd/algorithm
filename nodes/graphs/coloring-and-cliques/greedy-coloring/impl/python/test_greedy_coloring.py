# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-coloring/. The authors are listed in prov/PM9EGC.jsonl.

import itertools
import random

from greedy_coloring import greedy_coloring


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


def cycle(n: int) -> list[tuple[int, int]]:
    return [(i, (i + 1) % n) for i in range(n)]


def test_example_crown() -> None:
    # a1, b1, a2, b2, a3, b3 are 0 .. 5; a_i ~ b_j when i != j
    adj = make(6, [(0, 3), (0, 5), (2, 1), (2, 5), (4, 1), (4, 3)])
    assert greedy_coloring(adj) == [1, 1, 2, 2, 3, 3]
    assert greedy_coloring(adj, [0, 2, 4, 1, 3, 5]) == [1, 2, 1, 2, 1, 2]


def test_edges() -> None:
    assert greedy_coloring([]) == []
    assert greedy_coloring([[]]) == [1]
    assert greedy_coloring(make(4, [])) == [1, 1, 1, 1]
    k5 = make(5, list(itertools.combinations(range(5), 2)))
    assert sorted(greedy_coloring(k5)) == [1, 2, 3, 4, 5]
    assert greedy_coloring(make(5, cycle(5))) == [1, 2, 1, 2, 3]
    assert max(greedy_coloring(make(6, cycle(6)))) == 2
    k33 = make(6, [(i, j) for i in range(3) for j in range(3, 6)])
    assert max(greedy_coloring(k33)) == 2


def test_crown_is_bad() -> None:
    for k in range(1, 7):
        edges = [(2 * i, 2 * j + 1) for i in range(k) for j in range(k) if i != j]
        assert max(greedy_coloring(make(2 * k, edges)), default=0) == k


def test_random_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(0, 7)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        adj = make(n, edges)
        order = list(range(n))
        rng.shuffle(order)
        c = greedy_coloring(adj, order)
        assert proper(adj, c)
        delta = max((len(a) for a in adj), default=0)
        assert max(c, default=0) <= delta + 1
        for v in range(n):  # each color k > 1 has neighbours of colors 1 .. k-1
            assert {c[w] for w in adj[v]} >= set(range(1, c[v]))
        if n <= 6:
            best = min((max(greedy_coloring(adj, list(q)), default=0) for q in itertools.permutations(range(n))), default=0)
            assert best == chi(adj)
