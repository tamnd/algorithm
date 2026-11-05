# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnson-elementary-cycles-algorithm/. The authors are listed in prov/S5MRH3.jsonl.

import itertools
import random

from johnson_elementary_cycles_algorithm import johnson_elementary_cycles_algorithm


def brute_cycles(adj):
    """Independent oracle: every ordering of a vertex set that starts at its least vertex."""
    n = len(adj)
    arcs = {(u, v) for u in range(n) for v in adj[u]}
    found = set()
    for k in range(1, n + 1):
        for vs in itertools.combinations(range(n), k):
            for rest in itertools.permutations(vs[1:]):
                c = (vs[0],) + rest
                if all((c[i], c[(i + 1) % k]) in arcs for i in range(k)):
                    found.add(c)
    return found


EXAMPLE = [[1], [2, 3], [0, 3], [0, 4], [3, 4], []]


def test_example() -> None:
    got = johnson_elementary_cycles_algorithm(EXAMPLE)
    assert got == [[0, 1, 2], [0, 1, 2, 3], [0, 1, 3], [3, 4], [4]]


def test_unblock_needed() -> None:
    adj = [[1, 3], [2, 0], [1], [2]]
    got = johnson_elementary_cycles_algorithm(adj)
    assert got == [[0, 1], [0, 3, 2, 1], [1, 2]]


def test_small_cases() -> None:
    assert johnson_elementary_cycles_algorithm([]) == []
    assert johnson_elementary_cycles_algorithm([[]]) == []
    assert johnson_elementary_cycles_algorithm([[0]]) == [[0]]
    assert johnson_elementary_cycles_algorithm([[0, 0]]) == [[0]]
    assert johnson_elementary_cycles_algorithm([[1, 1], [0]]) == [[0, 1]]
    assert johnson_elementary_cycles_algorithm([[1], [2], []]) == []
    assert johnson_elementary_cycles_algorithm([[], [], []]) == []


def test_complete_digraph() -> None:
    for n, want in ((3, 5), (4, 20), (5, 84)):
        adj = [[v for v in range(n) if v != u] for u in range(n)]
        got = johnson_elementary_cycles_algorithm(adj)
        assert len(got) == want and len({tuple(c) for c in got}) == want


def test_long_cycle() -> None:
    n = 50000
    adj = [[(i + 1) % n] for i in range(n)]
    assert johnson_elementary_cycles_algorithm(adj) == [list(range(n))]


def test_random_against_brute_force() -> None:
    rng = random.Random(1975)
    for _ in range(600):
        n = rng.randint(0, 6)
        p = rng.random() * 0.6
        adj = [[v for v in range(n) if rng.random() < p] for _ in range(n)]
        for a in adj:
            if a and rng.random() < 0.2:
                a.append(a[0])
            rng.shuffle(a)
        got = johnson_elementary_cycles_algorithm(adj)
        tuples = [tuple(c) for c in got]
        assert len(tuples) == len(set(tuples))
        assert set(tuples) == brute_cycles(adj)
