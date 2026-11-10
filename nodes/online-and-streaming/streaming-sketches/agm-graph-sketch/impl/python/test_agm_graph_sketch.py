# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agm-graph-sketch/. The authors are listed in prov/25M25W.jsonl.

import random

from agm_graph_sketch import (
    EMPTY,
    AGMSketch,
    components_direct,
    components_from_forest,
    edge_index,
    edge_of,
    signed_incidence,
)

OPS = [(1, 2, 1), (2, 3, 1), (1, 3, 1), (4, 5, 1), (3, 4, 1), (3, 4, -1), (5, 6, 1)]
FINAL = [(1, 2), (2, 3), (1, 3), (4, 5), (5, 6)]


def test_worked_example() -> None:
    s = AGMSketch(6, random.Random(0))
    assert (s.levels, s.copies, s.rounds) == (8, 3, 14)
    for u, v, d in OPS:
        s.update(u, v, d)
    assert edge_index(6, 3, 4) == 16 and edge_of(6, 16) == (3, 4)
    assert signed_incidence(6, FINAL, 2) == {2: -1, 9: 1}
    # round 1: each vertex alone
    assert [s.sample_cut(0, [w]) for w in range(1, 7)] == [(1, 2), (1, 2), (1, 3), (4, 5), (5, 6), (5, 6)]
    # the sketch of {1, 2} returns an edge that leaves it; whole components give EMPTY
    assert s.sample_cut(0, [1, 2]) in [(1, 3), (2, 3)]
    assert s.sample_cut(1, [1, 2, 3]) == EMPTY and s.sample_cut(1, [4, 5, 6]) == EMPTY
    forest, stats = s.spanning_forest()
    assert forest == [(1, 2), (1, 3), (4, 5), (5, 6)]
    assert stats == {"rounds_used": 2, "fails": 0}
    assert components_from_forest(6, forest) == [frozenset({1, 2, 3}), frozenset({4, 5, 6})]


def test_cut_lemma_on_vectors() -> None:
    # The sum of a_w over S is supported exactly on the edges with one end in S.
    rng = random.Random(12)
    for _ in range(500):
        n = rng.randint(2, 9)
        pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
        edges = [e for e in pairs if rng.random() < 0.4]
        S = {w for w in range(1, n + 1) if rng.random() < 0.5}
        total: dict = {}
        for w in S:
            for e, s in signed_incidence(n, edges, w).items():
                total[e] = total.get(e, 0) + s
        support = {edge_of(n, e) for e, s in total.items() if s}
        cut = {(u, v) for u, v in edges if (u in S) != (v in S)}
        assert support == cut
        for e, s in total.items():
            u, v = edge_of(n, e)
            assert s == (u in S) - (v in S)


def test_edges() -> None:
    s = AGMSketch(1, random.Random(0))
    assert s.spanning_forest()[0] == []
    s = AGMSketch(4, random.Random(1))
    assert s.spanning_forest()[0] == []
    for u, v in [(1, 2), (2, 3), (3, 4)]:
        s.update(u, v, 1)
    for u, v in [(1, 2), (2, 3), (3, 4)]:
        s.update(v, u, -1)  # the order of the endpoints does not matter
    forest, _ = s.spanning_forest()
    assert forest == []
    try:
        s.update(2, 2, 1)
        raise AssertionError("loop accepted")
    except ValueError:
        pass


def test_random_dynamic_graphs() -> None:
    rng = random.Random(5)
    wrong = 0
    for trial in range(500):
        n = rng.randint(1, 9)
        sk = AGMSketch(n, random.Random(trial))
        E: set = set()
        for _ in range(rng.randint(0, 25)):
            if n < 2:
                break
            u, v = rng.sample(range(1, n + 1), 2)
            e = (min(u, v), max(u, v))
            if e in E and rng.random() < 0.5:
                E.remove(e)
                sk.update(u, v, -1)
            elif e not in E:
                E.add(e)
                sk.update(u, v, 1)
        forest, stats = sk.spanning_forest()
        assert all(e in E for e in forest)  # only real edges, so the forest is a subgraph
        assert len(forest) == n - len(components_from_forest(n, forest))  # acyclic
        assert stats["rounds_used"] <= sk.rounds
        if components_from_forest(n, forest) != components_direct(n, E):
            wrong += 1
    assert wrong <= 5  # the design failure probability is 0.01 per graph


def test_linearity_order_does_not_matter() -> None:
    rng = random.Random(77)
    ops = [(1, 2, 1), (3, 4, 1), (2, 3, 1), (1, 4, 1), (2, 3, -1), (5, 6, 1), (1, 4, -1)]
    a = AGMSketch(6, random.Random(3))
    b = AGMSketch(6, random.Random(3))
    for u, v, d in ops:
        a.update(u, v, d)
    shuffled = ops[:]
    rng.shuffle(shuffled)
    for u, v, d in shuffled:
        b.update(u, v, d)
    assert a.cells == b.cells
