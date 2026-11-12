# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compact-routing/. The authors are listed in prov/CZ5P8G.jsonl.

import math
import random

from compact_routing import CompactRouting, TreeRouting, dijkstra


def random_graph(rng, n, extra, maxw):
    g = {u: {} for u in range(n)}
    for v in range(1, n):
        u = rng.randrange(v)
        g[u][v] = g[v][u] = rng.randint(1, maxw)
    for _ in range(extra):
        u, v = rng.sample(range(n), 2)
        g[u][v] = g[v][u] = rng.randint(1, maxw)
    return g


def check_all_pairs(g, cr):
    worst = 1.0
    for u in g:
        for v in g:
            path = cr.route(u, v)
            assert path[0] == u and path[-1] == v
            for a, b in zip(path, path[1:]):
                assert b in g[a]
            d = cr.dist[u][0][v]
            L = cr.length(path)
            assert L <= 3 * d
            if d:
                worst = max(worst, L / d)
    return worst


def test_tree_routing_follows_the_tree_path():
    for seed in range(30):
        rng = random.Random(seed)
        n = rng.randint(1, 60)
        par = {0: None}
        for v in range(1, n):
            par[v] = rng.randrange(v)
        t = TreeRouting(par, 0)
        for x in par:
            # the label has at most log2(n) light-edge ports
            assert len(t.label[x][1]) <= math.log2(n) if n > 1 else True
        anc = {}
        for v in par:
            a, chain = v, []
            while a is not None:
                chain.append(a)
                a = par[a]
            anc[v] = chain
        for u in par:
            for v in par:
                lca = next(a for a in anc[u] if a in set(anc[v]))
                expect = anc[u][:anc[u].index(lca) + 1]
                expect += list(reversed(anc[v][:anc[v].index(lca)]))
                path, x = [u], u
                while True:
                    y = t.next_hop(x, t.label[v])
                    if y is None:
                        break
                    path.append(y)
                    x = y
                assert path == expect


def test_stretch_at_most_three_on_all_pairs():
    worst = 1.0
    for seed in range(12):
        rng = random.Random(100 + seed)
        n = rng.randint(2, 70)
        g = random_graph(rng, n, rng.randint(0, 2 * n), rng.choice([1, 3, 10]))
        cr = CompactRouting(g, random.Random(seed))
        worst = max(worst, check_all_pairs(g, cr))
    assert 1.0 < worst <= 3.0


def test_clusters_are_small_and_landmarks_are_reached_exactly():
    rng = random.Random(7)
    n = 120
    g = random_graph(rng, n, 150, 10)
    s = math.sqrt(n / math.log(n))
    cr = CompactRouting(g, random.Random(8), s=s)
    for u in g:
        assert len(cr.direct[u]) <= 4 * n / s
    for a in cr.A:
        for u in g:
            assert cr.length(cr.route(u, a)) == cr.dist[u][0][a]


def test_direct_entries_close_under_next_hops():
    # if v is in C(u), it is in the cluster of every vertex on the way
    rng = random.Random(11)
    g = random_graph(rng, 80, 100, 5)
    cr = CompactRouting(g, random.Random(12))
    for u in g:
        for v in cr.direct[u]:
            x = cr.direct[u][v]
            if x is not None:
                assert v in cr.direct[x]


def test_tables_are_smaller_than_full_tables():
    rng = random.Random(3)
    n = 400
    g = random_graph(rng, n, 2 * n, 10)
    cr = CompactRouting(g, random.Random(4))
    words = [cr.table_words(u) for u in g]
    labels = [cr.label_words(v) for v in g]
    # a full table has n entries of 2 words
    assert sum(words) / n < 2 * n / 3
    assert max(labels) <= 3 + math.log2(n)
    for u in rng.sample(range(n), 25):
        for v in rng.sample(range(n), 25):
            assert cr.length(cr.route(u, v)) <= 3 * cr.dist[u][0][v]


def test_dijkstra_helper():
    g = {0: {1: 2, 2: 5}, 1: {0: 2, 2: 2}, 2: {0: 5, 1: 2}}
    dist, par = dijkstra(g, 0)
    assert dist == {0: 0, 1: 2, 2: 4} and par[2] == 1
