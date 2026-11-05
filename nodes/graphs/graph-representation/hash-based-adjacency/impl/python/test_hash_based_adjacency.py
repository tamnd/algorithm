# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-based-adjacency/. The authors are listed in prov/NZ1XVJ.jsonl.

import random

import pytest

from hash_based_adjacency import HashAdjacency


def table(g: HashAdjacency) -> dict:
    return {u: sorted(s) for u, s in g.succ.items()}


def test_example() -> None:
    g = HashAdjacency()
    for x in range(4):
        g.add_vertex(x)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(3, 1)
    assert table(g) == {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    g.add_edge(1, 0)
    assert table(g) == {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    assert g.adjacent(0, 2) and not g.adjacent(0, 3)
    assert sorted(g.neighbors(1)) == [0, 2, 3] and g.degree(1) == 3
    g.remove_edge(1, 0)
    assert table(g) == {0: [2], 1: [2, 3], 2: [0, 1], 3: [1]}
    g.remove_vertex(2)
    assert table(g) == {0: [], 1: [3], 3: [1]}
    g.check_invariant()


def test_directed_example() -> None:
    g = HashAdjacency(directed=True)
    for u, v in [(0, 1), (0, 2), (1, 2), (2, 3), (3, 1), (3, 4)]:
        g.add_edge(u, v)
    assert table(g) == {0: [1, 2], 1: [2], 2: [3], 3: [1, 4], 4: []}
    assert {v: sorted(p) for v, p in g.pred.items()} == {0: [], 1: [0, 3], 2: [0, 1], 3: [2], 4: [3]}
    g.remove_vertex(3)
    assert table(g) == {0: [1, 2], 1: [2], 2: [], 4: []}
    assert {v: sorted(p) for v, p in g.pred.items()} == {0: [], 1: [0], 2: [0, 1], 4: []}
    g.check_invariant()


def test_edge_cases() -> None:
    g = HashAdjacency()
    assert g.edges() == set() and not g.adjacent("a", "b")
    with pytest.raises(ValueError):
        g.add_edge("a", "a")
    g.add_edge("a", ("b", 1))
    assert g.adjacent(("b", 1), "a")
    g.remove_edge("a", "zzz")
    g.remove_vertex("zzz")
    d = HashAdjacency(directed=True)
    d.add_edge("x", "x")
    assert d.adjacent("x", "x") and d.in_neighbors("x") == ["x"]
    d.remove_vertex("x")
    assert d.vertices() == [] and d.pred == {}
    d.check_invariant()


@pytest.mark.parametrize("directed", [False, True])
def test_random_against_set_model(directed: bool) -> None:
    rng = random.Random(1117)
    for _ in range(300):
        g = HashAdjacency(directed)
        verts: set[int] = set()
        model: set = set()

        def key(a: int, b: int):
            return (a, b) if directed else frozenset((a, b))

        for _ in range(rng.randint(0, 50)):
            op = rng.random()
            u, v = rng.randrange(8), rng.randrange(8)
            if op < 0.1:
                g.add_vertex(u)
                verts.add(u)
            elif op < 0.15:
                g.remove_vertex(u)
                verts.discard(u)
                model = {e for e in model if u not in (e if not directed else e)}
            elif op < 0.6:
                if not directed and u == v:
                    continue
                g.add_edge(u, v)
                verts |= {u, v}
                model.add(key(u, v))
            elif op < 0.8:
                g.remove_edge(u, v)
                model.discard(key(u, v))
            else:
                assert g.adjacent(u, v) == (key(u, v) in model)
            g.check_invariant()
        assert set(g.vertices()) == verts
        assert g.edges() == model
        for u in verts:
            if directed:
                nb = {b for a, b in model if a == u}
                ins = {a for a, b in model if b == u}
                assert set(g.in_neighbors(u)) == ins
            else:
                nb = {x for e in model if u in e for x in e if x != u}
            assert set(g.neighbors(u)) == nb and g.degree(u) == len(nb)
