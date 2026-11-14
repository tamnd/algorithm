# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blossom-quad/. The authors are listed in prov/ZDC65T.jsonl.

import random
from fractions import Fraction as F

from blossom_quad import blossom_quad, dual_graph, max_weight_matching, min_cost_perfect_matching
from mg3geom import boundary_edges, is_valid_planar_mesh, orient2d


def all_matchings(n, edges, perfect):
    """Every matching (perfect only, if asked) as a tuple of edge indices, by brute force."""
    out = []

    def go(v, used, chosen):
        while v < n and v in used:
            v += 1
        if v == n:
            out.append(tuple(chosen))
            return
        if not perfect:
            go(v + 1, used, chosen)
        for k, (i, j, _) in enumerate(edges):
            if (i == v and j not in used and j != v) or (j == v and i not in used and i != v):
                w = j if i == v else i
                go(v + 1, used | {v, w}, chosen + [k])
    go(0, frozenset(), [])
    return out


def partner_of(n, edges, chosen):
    p = [-1] * n
    for k in chosen:
        i, j, _ = edges[k]
        p[i], p[j] = j, i
    return p


def random_graph(rng, n, density, wmax):
    return [(i, j, rng.randint(1, wmax)) for i in range(n) for j in range(i + 1, n) if rng.random() < density]


def test_weighted_blossom_against_brute_force():
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randint(1, 9)
        edges = random_graph(rng, n, rng.uniform(0.2, 0.8), rng.choice((3, 20, 1000)))
        every = all_matchings(n, edges, perfect=False)
        weight = lambda ch: sum(edges[k][2] for k in ch)
        for maxcard in (False, True):
            p = max_weight_matching(n, edges, max_cardinality=maxcard)
            assert all(p[p[v]] == v for v in range(n) if p[v] >= 0)
            chosen = [k for k, (i, j, _) in enumerate(edges) if p[i] == j]
            assert len(chosen) == sum(1 for v in range(n) if p[v] >= 0) // 2
            if maxcard:
                size = max(len(ch) for ch in every)
                assert len(chosen) == size
                assert weight(chosen) == max(weight(ch) for ch in every if len(ch) == size)
            else:
                assert weight(chosen) == max(weight(ch) for ch in every)


def test_min_cost_perfect_matching_against_brute_force():
    rng = random.Random(2)
    found = 0
    for _ in range(150):
        n = 2 * rng.randint(1, 5)
        edges = random_graph(rng, n, rng.uniform(0.3, 0.9), 50)
        every = all_matchings(n, edges, perfect=True)
        p = min_cost_perfect_matching(n, edges)
        if not every:
            assert p is None
            continue
        found += 1
        best = min(sum(edges[k][2] for k in ch) for ch in every)
        assert p is not None and all(p[v] >= 0 and p[p[v]] == v for v in range(n))
        cost = sum(c for i, j, c in edges if p[i] == j)
        assert cost == best
    assert found >= 80


def grid_mesh(rng, W, H):
    P = []
    for j in range(H + 1):
        for i in range(W + 1):
            x = F(i) + (F(rng.randint(-30, 30), 100) if 0 < i < W else 0)
            y = F(j) + (F(rng.randint(-30, 30), 100) if 0 < j < H else 0)
            P.append((x, y))
    v = lambda i, j: j * (W + 1) + i
    tris = []
    for j in range(H):
        for i in range(W):
            a, b, c, d = v(i, j), v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)
            tris += [(a, b, c), (a, c, d)] if rng.random() < 0.5 else [(a, b, d), (b, c, d)]
    return P, tris


def fan_mesh(rng, k):
    """k triangles around a centre, with jittered rim points on a circle-like polygon."""
    import math
    P = [(F(0), F(0))]
    for s in range(k):
        t = 2 * math.pi * (s + rng.uniform(-0.2, 0.2)) / k
        r = rng.uniform(0.8, 1.2)
        P.append((F(round(1000 * r * math.cos(t)), 1000), F(round(1000 * r * math.sin(t)), 1000)))
    return P, [(0, 1 + s, 1 + (s + 1) % k) for s in range(k)]


def area(P, cells):
    return sum(sum(orient2d(P[c[0]], P[c[s]], P[c[s + 1]]) for s in range(1, len(c) - 1)) for c in cells)


def test_blossom_quad_against_all_perfect_matchings():
    rng = random.Random(3)
    meshes = []
    for W, H in ((1, 1), (2, 1), (3, 1), (2, 2), (3, 2), (2, 3)):
        for _ in range(6):
            meshes.append(grid_mesh(rng, W, H))
    for k in (4, 6, 8, 10, 12):
        for _ in range(4):
            meshes.append(fan_mesh(rng, k))
    unique = solved = 0
    for P, tris in meshes:
        assert len(tris) <= 12 and is_valid_planar_mesh(P, tris)
        dual = dual_graph(P, tris)
        edges = [(t1, t2, c) for t1, t2, c, _ in dual]
        every = all_matchings(len(tris), edges, perfect=True)
        quads, cost = blossom_quad(P, tris)
        if not every:
            assert quads is None and "no perfect matching" in cost
            continue
        solved += 1
        costs = sorted(sum(edges[k][2] for k in ch) for ch in every)
        assert cost == costs[0]
        if len(costs) == 1 or costs[1] > costs[0]:
            unique += 1
            best = next(ch for ch in every if sum(edges[k][2] for k in ch) == costs[0])
            assert sorted(quads) == sorted(dual[k][3] for k in best)
        # a perfect matching gives a conforming quad mesh of the same region
        assert 2 * len(quads) == len(tris)
        assert is_valid_planar_mesh(P, quads)
        assert area(P, quads) == area(P, tris)
        assert set(boundary_edges(quads)) == set(boundary_edges(tris))
        assert len(boundary_edges(quads)) % 2 == 0
    assert solved >= 40 and unique >= 30


def test_failures_and_parity():
    # odd number of triangles
    P = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(2), F(1))]
    quads, why = blossom_quad(P, [(0, 1, 2), (1, 3, 2), (1, 4, 3)])
    assert quads is None and "odd" in why
    # a centre triangle with three ears: the dual graph is a star, which has no perfect matching
    P = [(F(0), F(0)), (F(4), F(0)), (F(2), F(4)), (F(2), F(-2)), (F(5), F(3)), (F(-1), F(3))]
    tris = [(0, 1, 2), (0, 3, 1), (1, 4, 2), (2, 5, 0)]
    assert is_valid_planar_mesh(P, tris) and len(dual_graph(P, tris)) == 3
    quads, why = blossom_quad(P, tris)
    assert quads is None and "no perfect matching" in why
    # a boundary of odd length cannot bound a quad mesh: 4 Q = 2 E_int + E_bnd
    assert len(boundary_edges(tris)) == 6
    rng = random.Random(4)
    for _ in range(20):
        P, tris = grid_mesh(rng, rng.randint(1, 4), rng.randint(1, 3))
        quads, cost = blossom_quad(P, tris)
        if quads is not None:
            sides = {}
            for q in quads:
                for s in range(4):
                    e = frozenset((q[s], q[(s + 1) % 4]))
                    sides[e] = sides.get(e, 0) + 1
            assert 4 * len(quads) == 2 * sum(v == 2 for v in sides.values()) + sum(v == 1 for v in sides.values())
