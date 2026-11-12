# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gpsr/. The authors are listed in prov/8QEP75.jsonl.

import random

from gpsr import (
    components,
    crossing,
    dist2,
    gabriel_graph,
    gpsr,
    relative_neighborhood_graph,
    unit_disk_graph,
)


def scene(seed, n=60, r=0.2):
    rng = random.Random(seed)
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    return pts, unit_disk_graph(pts, r)


def edges(adj):
    return {(u, v) for u in range(len(adj)) for v in adj[u] if u < v}


def mst_edges(points, adj):
    """Prim's algorithm on each component of the unit disk graph."""
    n = len(points)
    done = [False] * n
    out = set()
    for root in range(n):
        if done[root]:
            continue
        best = {root: (0, None)}
        while best:
            u = min(best, key=lambda k: (best[k][0], k))
            _, parent = best.pop(u)
            done[u] = True
            if parent is not None:
                out.add((min(u, parent), max(u, parent)))
            for v in adj[u]:
                if not done[v]:
                    d = dist2(points[u], points[v])
                    if v not in best or d < best[v][0]:
                        best[v] = (d, u)
    return out


def test_planar_subgraphs_are_planar_symmetric_and_keep_connectivity():
    for seed in range(8):
        pts, adj = scene(seed)
        gg = gabriel_graph(pts, adj)
        rng_g = relative_neighborhood_graph(pts, adj)
        for g in (gg, rng_g):
            assert all(u in g[v] for u in range(len(g)) for v in g[u])
            es = sorted(edges(g))
            for i, (a, b) in enumerate(es):
                for c, d in es[i + 1:]:
                    if len({a, b, c, d}) == 4:
                        assert crossing(pts[a], pts[b], pts[c], pts[d]) is None
            assert components(g) == components(adj)
        assert mst_edges(pts, adj) <= edges(rng_g) <= edges(gg) <= edges(adj)


def test_every_connected_pair_is_delivered():
    perimeter_used = 0
    for seed in range(12):
        pts, adj = scene(seed)
        comp = components(adj)
        for planar in (gabriel_graph(pts, adj), relative_neighborhood_graph(pts, adj)):
            for s in range(0, len(pts), 4):
                for d in range(len(pts)):
                    if s != d and comp[s] == comp[d]:
                        ok, path, g, p = gpsr(pts, adj, planar, s, d)
                        assert ok and path[0] == s and path[-1] == d
                        assert all(path[i + 1] in adj[path[i]] for i in range(len(path) - 1))
                        perimeter_used += p > 0
    assert perimeter_used > 0


def greedy_only(points, adj, s, d):
    x = s
    while x != d:
        y = min(adj[x], key=lambda z: dist2(points[z], points[d]), default=None)
        if y is None or dist2(points[y], points[d]) >= dist2(points[x], points[d]):
            return False
        x = y
    return True


def test_greedy_alone_gets_stuck():
    stuck = 0
    for seed in range(5):
        pts, adj = scene(seed)
        comp = components(adj)
        for s in range(len(pts)):
            for d in range(len(pts)):
                if s != d and comp[s] == comp[d] and not greedy_only(pts, adj, s, d):
                    stuck += 1
    assert stuck > 0


def test_unreachable_destination_is_dropped():
    for seed in range(5):
        pts, adj = scene(seed, n=40, r=0.15)
        comp = components(adj)
        gg = gabriel_graph(pts, adj)
        pairs = [(s, d) for s in range(40) for d in range(40) if comp[s] != comp[d]]
        assert pairs
        for s, d in pairs[:50]:
            ok, path, _, _ = gpsr(pts, adj, gg, s, d)
            assert not ok and all(comp[x] == comp[s] for x in path)


def test_dead_end_example():
    # S, F, A, B, C, E, D; range 1.2. Greedy goes S -> F and is stuck there.
    pts = [(0, 0), (0.9, -0.2), (0, 1), (1, 1.5), (2, 1.5), (2.6, 0.7), (2.6, -0.3)]
    adj = unit_disk_graph(pts, 1.2)
    assert edges(adj) == {(0, 1), (0, 2), (2, 3), (3, 4), (4, 5), (5, 6)}
    ok, path, g, p = gpsr(pts, adj, gabriel_graph(pts, adj), 0, 6)
    assert ok and path == [0, 1, 0, 2, 3, 4, 5, 6]
    assert (g, p) == (2, 5)
