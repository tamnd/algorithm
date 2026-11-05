# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/succinct-graph-representation/. The authors are listed in prov/M16F3Q.jsonl.

import math
import random

from succinct_graph_representation import SuccinctGraph

EXAMPLE = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]


def test_example() -> None:
    g = SuccinctGraph(4, EXAMPLE)
    g.check_invariant()
    assert g.l == 1
    assert [g.access(i) for i in range(6)] == [1, 2, 6, 8, 11, 15]
    assert g.high.length == 6 + 8 + 1
    assert g.bits() == 21
    assert g.adjacent(2, 3) and not g.adjacent(3, 2) and g.adjacent(3, 3)
    assert [g.degree(u) for u in range(4)] == [2, 1, 2, 1]
    assert g.neighbors(2) == [0, 3]
    assert g.neighbor(0, 1) == 2


def test_empty_and_single() -> None:
    g = SuccinctGraph(0, [])
    assert g.m == 0 and g.bits() == 1
    g = SuccinctGraph(1, [])
    assert not g.adjacent(0, 0) and g.degree(0) == 0
    g = SuccinctGraph(1, [(0, 0)])
    assert g.adjacent(0, 0) and g.neighbors(0) == [0]


def test_complete_graph_and_duplicates() -> None:
    n = 9
    arcs = [(u, v) for u in range(n) for v in range(n)]
    g = SuccinctGraph(n, arcs + arcs[:5])
    g.check_invariant()
    assert g.m == n * n and g.l == 0
    assert all(g.degree(u) == n for u in range(n))


def test_space_is_near_the_bound() -> None:
    rng = random.Random(7)
    n, m = 200, 1000
    arcs = set()
    while len(arcs) < m:
        arcs.add((rng.randrange(n), rng.randrange(n)))
    g = SuccinctGraph(n, arcs)
    bound = math.log2(math.comb(n * n, m))
    assert bound <= g.bits() <= bound + 2 * m


def test_random_against_sets() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n = rng.randrange(0, 12)
        arcs = [(rng.randrange(n), rng.randrange(n))
                for _ in range(rng.randrange(0, n * n + 1))] if n else []
        g = SuccinctGraph(n, arcs)
        g.check_invariant()
        s = set(arcs)
        assert g.m == len(s)
        for u in range(n):
            nb = sorted(v for (a, v) in s if a == u)
            assert g.degree(u) == len(nb)
            assert g.neighbors(u) == nb
            for v in range(n):
                assert g.adjacent(u, v) == ((u, v) in s)
