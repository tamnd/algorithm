# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mitchell-guillotine-ptas/. The authors are listed in prov/XPPZ2J.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, dist, sqrt

from mitchell_guillotine_ptas import (crossings, general_position, guillotine_tour, least_bridges, m_span,
                                      side_signature, tour_edges, tour_length, windows_of, with_bridges)

# A(0,6) B(3,2) C(4,1) D(1,0) E(2,4) F(5,5)
POINTS = [(0, 6), (3, 2), (4, 1), (1, 0), (2, 4), (5, 5)]
OPT_ORDER = [0, 4, 3, 2, 1, 5]  # A E D C B F


def all_tours(n):
    return [[0] + list(p) for p in permutations(range(1, n)) if n < 3 or p[0] < p[-1]]


def opt_tour(points):
    return min((tour_length(points, o), o) for o in all_tours(len(points)))


def random_points(rng, n, size):
    return list(zip(rng.sample(range(size), n), rng.sample(range(size), n)))


def connected(pieces):
    adj = {}
    for p, q in pieces:
        adj.setdefault(p, []).append(q)
        adj.setdefault(q, []).append(p)
    start = next(iter(adj))
    seen, stack = {start}, [start]
    while stack:
        for q in adj[stack.pop()]:
            if q not in seen:
                seen.add(q)
                stack.append(q)
    return len(seen) == len(adj)


def k_mst(points, k):
    """The least spanning tree over all k-subsets, by Prim on each subset."""
    best = None
    for sub in combinations(points, k):
        inside, rest, edges, total = [sub[0]], list(sub[1:]), [], 0.0
        while rest:
            d, p, q = min((dist(p, q), p, q) for p in inside for q in rest)
            edges.append((p, q))
            total += d
            inside.append(q)
            rest.remove(q)
        if best is None or total < best[0]:
            best = (total, edges, list(sub))
    return best


def exhaustive_bridges(points, edges, m):
    """The least bridge length over all cut trees, by plain recursion without a table."""
    xs, ys = sorted(p[0] for p in points), sorted(p[1] for p in points)

    def rec(i0, i1, j0, j1):
        w = (xs[i0], xs[i1], ys[j0], ys[j1])
        if not any(w[0] < p[0] < w[1] and w[2] < p[1] < w[3] for p in points):
            return 0
        out = []
        for i in range(i0 + 1, i1):
            sp = m_span(crossings(edges, w, "x", xs[i]), m)
            out.append((0 if sp is None else sp[1] - sp[0]) + rec(i0, i, j0, j1) + rec(i, i1, j0, j1))
        for j in range(j0 + 1, j1):
            sp = m_span(crossings(edges, w, "y", ys[j]), m)
            out.append((0 if sp is None else sp[1] - sp[0]) + rec(i0, i1, j0, j) + rec(i0, i1, j, j1))
        return min(out)

    return rec(0, len(xs) - 1, 0, len(ys) - 1)


def test_example() -> None:
    length, order = opt_tour(POINTS)
    assert order == OPT_ORDER and abs(length - 20.2326) < 1e-4
    edges = tour_edges(POINTS, OPT_ORDER)
    root = (0, 5, 0, 6)
    assert m_span(crossings(edges, root, "x", 3), 1) == (Fraction(2, 3), Fraction(27, 5))
    assert m_span(crossings(edges, root, "y", 5), 1) == (1, 1)  # one part: the cut y = 5 is free
    stats = {}
    total, bridges = least_bridges(POINTS, edges, 1, stats)
    assert total == Fraction(4, 3) and bridges == [("x", 3, Fraction(2, 3), 2, (1, 5, 0, 5))]
    assert stats == {"windows": 225, "transitions": 290}
    new, graph, b = guillotine_tour(POINTS, OPT_ORDER, 1)
    assert new == [0, 4, 3, 1, 2, 5] and abs(graph - (length + Fraction(8, 3))) < 1e-9
    assert abs(tour_length(POINTS, new) - 20.4163) < 1e-4
    assert least_bridges(POINTS, edges, 2)[0] == 0 and guillotine_tour(POINTS, OPT_ORDER, 2)[0] == OPT_ORDER


def test_table_equals_exhaustive_search() -> None:
    rng = random.Random(1996)
    for _ in range(12):
        n = rng.randint(3, 5)
        points = random_points(rng, n, 8)
        order = rng.sample(range(n), n)
        edges = tour_edges(points, order)
        for m in (1, 2):
            assert least_bridges(points, edges, m)[0] == exhaustive_bridges(points, edges, m)


def test_tours_for_several_m() -> None:
    rng = random.Random(1999)
    for trial in range(16):
        n = rng.randint(4, 6)
        points = random_points(rng, n, 10)
        assert general_position(points)
        opt, best = opt_tour(points)
        for order in (best, rng.sample(range(n), n)):
            length = tour_length(points, order)
            for m in (1, 2, 3):
                stats = {}
                new, graph, bridges = guillotine_tour(points, order, m, stats)
                assert sorted(new) == list(range(n))
                assert bridges <= sqrt(2) * length / m  # the bound of the length theorem
                assert abs(graph - (length + 2 * bridges)) < 1e-9
                assert opt - 1e-9 <= tour_length(points, new) <= graph + 1e-9
                if order is best:
                    assert tour_length(points, new) <= (1 + 2 * sqrt(2) / m) * opt + 1e-9
                windows = stats["windows"]
                assert windows == comb(n, 2) ** 2 and stats["transitions"] <= windows * (2 * n - 4)


def test_bridges_end_on_the_network_inside_their_windows() -> None:
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randint(4, 7)
        points = random_points(rng, n, 12)
        edges = tour_edges(points, rng.sample(range(n), n))
        for m in (1, 2):
            _, bridges = least_bridges(points, edges, m)
            for axis, c, lo, hi, w in bridges:
                ends = [t for t, _ in crossings(edges, w, axis, c)]
                assert lo in ends and hi in ends  # the ends are old points of the network
                a, b = (w[2], w[3]) if axis == "x" else (w[0], w[1])
                assert a < lo < hi < b
            for (a1, c1, l1, h1, _), (a2, c2, l2, h2, _) in combinations(bridges, 2):
                if a1 == a2:
                    assert c1 != c2 or h1 < l2 or h2 < l1
                else:
                    assert not (l1 <= c2 <= h1 and l2 <= c1 <= h2)  # no two bridges meet


def test_k_mst_networks() -> None:
    rng = random.Random(2009)
    for _ in range(12):
        n = rng.randint(5, 7)
        points = random_points(rng, n, 10)
        k = rng.randint(3, n - 1)
        opt, edges, sub = k_mst(points, k)
        for m in (1, 2, 3):
            bridges, found = least_bridges(sub, edges, m)
            assert bridges <= sqrt(2) * opt / m
            pieces = with_bridges(sub, edges, found, 1)
            assert connected(pieces) and abs(sum(dist(p, q) for p, q in pieces) - (opt + bridges)) < 1e-9


def test_boundary_states() -> None:
    points = [(0, 3), (2, 0), (4, 2), (1, 4), (3, 1)]
    n = len(points)
    xs, ys, ws = windows_of(points)
    parts = comb(n, 2) + n * comb(n - 1, 2)  # a part is one edge, or a point with two of its edges
    for m in (1, 2):
        seen, most = {}, 0
        for order in all_tours(n):
            edges = tour_edges(points, order)
            for i0, i1, j0, j1 in ws:
                w = (xs[i0], xs[i1], ys[j0], ys[j1])
                for side, axis, c in (("left", "x", w[0]), ("right", "x", w[1]),
                                      ("bottom", "y", w[2]), ("top", "y", w[3])):
                    sig = side_signature(edges, w, side, m)
                    assert len(sig) <= 2 * m + 1
                    seen.setdefault((w, side), set()).add(sig)
                    most = max(most, len(crossings(edges, w, axis, c)))
        assert max(len(s) for s in seen.values()) <= 2 * (parts + 1) ** (2 * m)
        assert most > 2 * m or m == 2  # a side can have more parts than its state keeps
