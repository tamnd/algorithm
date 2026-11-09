# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relative-neighborhood-graph/. The authors are listed in prov/5F7BZ4.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from relative_neighborhood_graph import RelativeNeighborhoodGraph, dist2

EXAMPLE = [(1, 3), (1, 11), (2, 8), (5, 1), (9, 6), (11, 1), (11, 4)]


def oracle(P):
    """Independent reference: p and q are joined when the two open disks of radius |pq|,
    centered at p and at q, share no other point."""
    n = len(P)
    out = set()
    for i, j in itertools.combinations(range(n), 2):
        d = dist2(P[i], P[j])
        near_i = {k for k in range(n) if k not in (i, j) and dist2(P[i], P[k]) < d}
        near_j = {k for k in range(n) if k not in (i, j) and dist2(P[j], P[k]) < d}
        if not near_i & near_j:
            out.add((i, j))
    return out


def gabriel(P):
    n = len(P)
    return {
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if all(
            (P[i][0] - P[k][0]) * (P[j][0] - P[k][0]) + (P[i][1] - P[k][1]) * (P[j][1] - P[k][1]) > 0
            for k in range(n)
            if k not in (i, j)
        )
    }


def kruskal_all_msts_union(P):
    """Edges that lie in some minimum spanning tree: pq is in some MST iff p and q are not
    connected by edges strictly shorter than |pq| (cycle property)."""
    n = len(P)
    pairs = sorted((dist2(P[i], P[j]), i, j) for i, j in itertools.combinations(range(n), 2))
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = set()
    t = 0
    while t < len(pairs):
        u = t
        while u < len(pairs) and pairs[u][0] == pairs[t][0]:
            u += 1
        group = pairs[t:u]
        for _, i, j in group:
            if find(i) != find(j):
                out.add((i, j))
        for _, i, j in group:
            parent[find(i)] = find(j)
        t = u
    return out


def test_example() -> None:
    g = RelativeNeighborhoodGraph(EXAMPLE)
    g.check_invariant()
    assert g.edges() == [(0, 2), (0, 3), (1, 2), (2, 4), (3, 5), (4, 6), (5, 6)]
    assert not g.has_edge(3, 4)  # (11,1) is in the lune of (5,1) and (9,6)
    assert g.neighbors(2) == [0, 1, 4]


def test_small_cases() -> None:
    assert RelativeNeighborhoodGraph([]).edges() == []
    assert RelativeNeighborhoodGraph([(2, 2)]).edges() == []
    assert RelativeNeighborhoodGraph([(0, 0), (3, 4)]).edges() == [(0, 1)]
    with pytest.raises(ValueError):
        RelativeNeighborhoodGraph([(0, 0), (1, 1), (0, 0)])


def test_ties_and_square() -> None:
    # Ties keep edges: the open lune excludes points at exactly distance |pq|.
    # |(0,0)(5,0)|^2 = 25 = |(0,0)(3,4)|^2, so (3,4) is on the boundary of the lune.
    tie = RelativeNeighborhoodGraph([(0, 0), (5, 0), (3, 4)])
    assert tie.edges() == [(0, 1), (0, 2), (1, 2)]
    # Square: each diagonal has the other corners strictly closer to both ends.
    sq = RelativeNeighborhoodGraph([(0, 0), (1, 0), (1, 1), (0, 1)])
    assert sq.edges() == [(0, 1), (0, 3), (1, 2), (2, 3)]
    # Unit-distance lattice: RNG keeps every unit edge, so it has cycles.
    grid = [(x, y) for x in range(3) for y in range(3)]
    assert len(RelativeNeighborhoodGraph(grid).edges()) == 12


def test_collinear_gives_a_path() -> None:
    pts = [(0, 0), (5, 5), (2, 2), (9, 9), (3, 3)]
    order = sorted(range(len(pts)), key=lambda i: pts[i])
    want = sorted(tuple(sorted(e)) for e in zip(order, order[1:]))
    assert RelativeNeighborhoodGraph(pts).edges() == want


def test_random_against_oracle_and_chain() -> None:
    rng = random.Random(1980)
    for trial in range(600):
        n = rng.randint(0, 12)
        r = rng.choice([2, 4, 10, 100])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        rng.shuffle(pts)
        g = RelativeNeighborhoodGraph(pts)
        E = set(g.edges())
        assert E == oracle(pts)
        if trial % 4 == 0:
            g.check_invariant()
        assert kruskal_all_msts_union(pts) <= E <= gabriel(pts)


def test_fractions() -> None:
    p, q = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))
    near = (Fraction(1, 2), Fraction(866, 1000))  # just inside the lune
    far = (Fraction(1, 2), Fraction(867, 1000))  # just outside
    assert not RelativeNeighborhoodGraph([p, q, near]).has_edge(0, 1)
    assert RelativeNeighborhoodGraph([p, q, far]).has_edge(0, 1)
