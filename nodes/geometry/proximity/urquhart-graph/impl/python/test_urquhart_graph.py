# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/urquhart-graph/. The authors are listed in prov/XMCR03.jsonl.

import itertools
import random

import pytest

from urquhart_graph import UrquhartGraph, dist2, orient

EXAMPLE = [(1, 3), (1, 11), (2, 8), (5, 1), (9, 6), (11, 1), (11, 4)]


def hull_twice_area(P):
    """Twice the area of the convex hull (monotone chain)."""
    pts = sorted(set(P))
    if len(pts) < 3:
        return 0

    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h

    hull = half(pts)[:-1] + half(pts[::-1])[:-1]
    return sum(hull[i][0] * hull[(i + 1) % len(hull)][1] - hull[(i + 1) % len(hull)][0] * hull[i][1] for i in range(len(hull)))


def rng_edges(P):
    n = len(P)
    return {
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if not any(max(dist2(P[i], P[k]), dist2(P[j], P[k])) < dist2(P[i], P[j]) for k in range(n) if k not in (i, j))
    }


def check(P):
    g = UrquhartGraph(P)
    T = g.triangles
    # The triangles tile the convex hull: their areas add up to the hull area, and each
    # has an empty circumcircle by construction, so together they are the Delaunay triangulation.
    assert sum(abs(orient(P[a], P[b], P[c])) for a, b, c in T) == hull_twice_area(P)
    D = {e for t in T for e in itertools.combinations(t, 2)}
    if not T and len(P) >= 2:
        order = sorted(range(len(P)), key=lambda i: P[i])
        D = {tuple(sorted(e)) for e in zip(order, order[1:])}
    # Reference: an edge is removed iff it is the strictly longest side of some triangle on it.
    removed = set()
    for t in T:
        for e in itertools.combinations(t, 2):
            others = [f for f in itertools.combinations(t, 2) if f != e]
            if all(dist2(P[e[0]], P[e[1]]) > dist2(P[f[0]], P[f[1]]) for f in others):
                removed.add(e)
    E = set(g.edges())
    assert E == D - removed
    assert rng_edges(P) <= E <= D
    for i in range(len(P)):
        for j in g.neighbors(i):
            assert g.has_edge(j, i)
    return g


def test_example() -> None:
    g = check(EXAMPLE)
    assert len(g.triangles) == 6
    # Removed: (1,3)(1,11), (2,8)(5,1), (1,11)(9,6), (5,1)(11,4). The result equals the Gabriel graph.
    assert g.edges() == [(0, 2), (0, 3), (1, 2), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)]
    assert g.has_edge(3, 4)  # (5,1)(9,6) survives although it is not an RNG edge


def test_small_and_collinear() -> None:
    assert UrquhartGraph([]).edges() == []
    assert UrquhartGraph([(1, 1)]).edges() == []
    assert UrquhartGraph([(0, 0), (4, 1)]).edges() == [(0, 1)]
    assert UrquhartGraph([(0, 0), (2, 2), (1, 1), (5, 5)]).edges() == [(0, 2), (1, 2), (1, 3)]
    with pytest.raises(ValueError):
        UrquhartGraph([(0, 0), (0, 0)])


def test_cocircular_is_rejected() -> None:
    with pytest.raises(ValueError):
        UrquhartGraph([(0, 0), (1, 0), (1, 1), (0, 1)])


def test_isosceles_keeps_both_long_sides() -> None:
    # Sides 25, 25, 10: the longest side is not unique, so nothing is removed,
    # and both long sides are RNG edges (the lune is open).
    g = check([(0, 0), (5, 0), (4, 3)])
    assert g.edges() == [(0, 1), (0, 2), (1, 2)]


def test_random_against_reference() -> None:
    rng = random.Random(1982)
    done = 0
    while done < 500:
        n = rng.randint(0, 10)
        r = rng.choice([3, 6, 20, 100])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        try:
            check(pts)
        except ValueError:
            continue
        done += 1
