# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topological-map/. The authors are listed in prov/KYBFGV.jsonl.

import math
import random

import pytest

from topological_map import TopologicalMap

OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}


def floor_map():
    """The map of the page: a 2 by 3 block of corridors and one dead end.

    A(corner) - B(T) - C(corner)
    |           |      |
    D(T) ----- E(T) - F(corner)
    |
    G(dead end)
    """
    m = TopologicalMap()
    ids = {}
    for name, sig in [("A", "corner"), ("B", "T"), ("C", "corner"), ("D", "T"), ("E", "T"), ("F", "corner"), ("G", "end")]:
        ids[name] = m.add_place(sig)
    for u, a, v, length in [("A", "E", "B", 5), ("B", "E", "C", 4), ("A", "S", "D", 3), ("B", "S", "E", 3),
                            ("C", "S", "F", 3), ("D", "E", "E", 4), ("E", "E", "F", 4), ("D", "S", "G", 2)]:
        m.add_edge(ids[u], a, ids[v], OPP[a], length)
    return m, ids


def test_route_on_the_page_map():
    m, ids = floor_map()
    length, places, actions = m.route(ids["A"], ids["F"])
    assert length == 11
    assert places == [ids["A"], ids["D"], ids["E"], ids["F"]]
    assert actions == ["S", "E", "E"]
    assert m.route(ids["G"], ids["G"]) == (0, [ids["G"]], [])


def test_localize_on_the_page_map():
    m, ids = floor_map()
    assert m.localize("T", []) == {ids["B"], ids["D"], ids["E"]}
    assert m.localize("T", [("E", "corner")]) == {ids["C"], ids["F"]}
    assert m.localize("T", [("E", "corner"), ("S", "corner")]) == {ids["F"]}
    assert m.localize("T", [("W", "corner")]) == {ids["A"]}  # from B, the only T with a corner to its west
    assert m.localize("T", [("N", "T")]) == {ids["B"]}  # from E
    assert m.localize("T", [("N", "end")]) == set()  # inconsistent with the map


def test_symmetric_ring_cannot_be_resolved():
    # four corners in a square: every action sequence leaves all four candidates
    m = TopologicalMap()
    v = [m.add_place("corner") for _ in range(4)]
    for k in range(4):
        m.add_edge(v[k], "left", v[(k + 1) % 4], "right", 1)
    rng = random.Random(0)
    steps = [(rng.choice(["left", "right"]), "corner") for _ in range(20)]
    assert m.localize("corner", steps) == set(v)


def random_map(rng, n, labels):
    m = TopologicalMap()
    for _ in range(n):
        m.add_place(rng.randrange(3))
    for _ in range(3 * n):
        u, v = rng.randrange(n), rng.randrange(n)
        a, b = rng.choice(labels), rng.choice(labels)
        try:
            m.add_edge(u, a, v, b, rng.randint(0, 9))
        except ValueError:
            pass
    return m


def floyd_warshall(m):
    n = len(m.sig)
    d = [[math.inf] * n for _ in range(n)]
    for u in range(n):
        d[u][u] = 0
        for v, length in m.out[u].values():
            d[u][v] = min(d[u][v], length)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def test_route_matches_floyd_warshall():
    rng = random.Random(5)
    for _ in range(20):
        m = random_map(rng, 12, ["a", "b", "c", "d"])
        d = floyd_warshall(m)
        for s in range(12):
            for t in range(12):
                r = m.route(s, t)
                if d[s][t] == math.inf:
                    assert r is None
                    continue
                length, places, actions = r
                assert length == d[s][t]
                # the actions replay the route and add up to its length
                v, total = s, 0
                for a, w in zip(actions, places[1:]):
                    nxt, l = m.out[v][a]
                    assert nxt == w
                    v, total = w, total + l
                assert v == t and total == length


def test_localize_matches_brute_force():
    rng = random.Random(9)
    labels = ["a", "b", "c"]
    for _ in range(40):
        m = random_map(rng, 10, labels)
        start = rng.randrange(10)
        v, steps = start, []
        for _ in range(rng.randrange(6)):
            a = rng.choice(labels)
            w = m.step(v, a)
            if w is None:
                break
            steps.append((a, m.sig[w]))
            v = w
        got = m.localize(m.sig[start], steps)
        want = set()
        for v0 in range(10):
            if m.sig[v0] != m.sig[start]:
                continue
            v, ok = v0, True
            for a, z in steps:
                w = m.step(v, a)
                if w is None or m.sig[w] != z:
                    ok = False
                    break
                v = w
            if ok:
                want.add(v)
        assert got == want
        # the true place is always a candidate
        true_v = start
        for a, _ in steps:
            true_v = m.step(true_v, a)
        assert true_v in got


def test_errors():
    m = TopologicalMap()
    a = m.add_place("x")
    b = m.add_place("y")
    m.add_edge(a, "E", b, "W", 1)
    with pytest.raises(ValueError):
        m.add_edge(a, "E", b, "N", 1)  # E is taken at a
    with pytest.raises(ValueError):
        m.add_edge(a, "N", 5, "S", 1)
    with pytest.raises(ValueError):
        m.add_edge(a, "N", b, "S", -1)
    with pytest.raises(ValueError):
        m.add_edge(a, "loop", a, "loop", 1)
    assert m.route(b, a) == (1, [b, a], ["W"])
    c = m.add_place("z")
    assert m.route(a, c) is None
