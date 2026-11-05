# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lawler-chromatic-number/. The authors are listed in prov/E447F2.jsonl.

import itertools
import random

from lawler_chromatic_number import lawler_chromatic_number, maximal_independent_sets


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


def check(adj: list[list[int]]) -> int:
    k, c = lawler_chromatic_number(adj)
    assert proper(adj, c)
    assert sorted(set(c)) == list(range(1, k + 1))
    return k


def cycle(n: int) -> list[list[int]]:
    return make(n, [(i, (i + 1) % n) for i in range(n)])


def complete(n: int) -> list[list[int]]:
    return make(n, [(i, j) for i in range(n) for j in range(i + 1, n)])


def test_example() -> None:
    assert check(cycle(5)) == 3
    nbr = [sum(1 << w for w in row) for row in cycle(5)]
    mis = sorted(sorted(v for v in range(5) if i >> v & 1) for i in maximal_independent_sets(nbr, 31))
    assert mis == [[0, 2], [0, 3], [1, 3], [1, 4], [2, 4]]


def test_edges() -> None:
    assert lawler_chromatic_number([]) == (0, [])
    assert check([[]]) == 1
    assert check([[], [], [], []]) == 1
    for n in range(1, 8):
        assert check(complete(n)) == n
    for n in (3, 5, 7, 9, 11):
        assert check(cycle(n)) == 3
    for n in (4, 6, 8, 10):
        assert check(cycle(n)) == 2


def test_named_graphs() -> None:
    kmn = make(7, [(i, j) for i in range(3) for j in range(3, 7)])
    assert check(kmn) == 2
    pet = make(10, [(i, (i + 1) % 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)])
    assert check(pet) == 3
    # Groetzsch graph: Mycielskian of C5, triangle-free with chi = 4
    e = [(i, (i + 1) % 5) for i in range(5)]
    e += [(5 + i, (i + 1) % 5) for i in range(5)] + [(5 + i, (i - 1) % 5) for i in range(5)]
    e += [(10, 5 + i) for i in range(5)]
    assert check(make(11, e)) == 4
    wheel = make(6, [(i, (i + 1) % 5) for i in range(5)] + [(5, i) for i in range(5)])
    assert check(wheel) == 4


def test_mis_count_moon_moser() -> None:
    adj = make(9, [(i, j) for i in range(9) for j in range(i + 1, 9) if i // 3 == j // 3])
    nbr = [sum(1 << w for w in row) for row in adj]
    assert len(list(maximal_independent_sets(nbr, (1 << 9) - 1))) == 27


def test_random_against_brute_force() -> None:
    rng = random.Random(9031)
    for _ in range(500):
        n = rng.randint(0, 7)
        p = rng.random()
        adj = make(n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p])
        assert check(adj) == chi(adj)
        nbr = [sum(1 << w for w in row) for row in adj]
        s = rng.randrange(1 << n)
        got = sorted(maximal_independent_sets(nbr, s))
        want = []
        verts = [v for v in range(n) if s >> v & 1]
        for k in range(len(verts) + 1):
            for sub in itertools.combinations(verts, k):
                m = sum(1 << v for v in sub)
                if any(nbr[v] & m for v in sub):
                    continue
                if all(nbr[v] & m for v in verts if not m >> v & 1):
                    want.append(m)
        assert got == sorted(want)
