# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/five-color-algorithm/. The authors are listed in prov/AFEY7W.jsonl.

import itertools
import random

from five_color_algorithm import five_color


def adj_from_edges(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def check(adj, color):
    """Independent oracle: a proper coloring with colors 0 to 4."""
    assert len(color) == len(adj)
    assert all(0 <= c <= 4 for c in color)
    for v, nb in enumerate(adj):
        for u in nb:
            assert color[u] != color[v]


def random_triangulation(rng, n, flips):
    """A random maximal planar graph: insert vertices into faces, then flip edges.

    Faces are oriented triangles of a sphere; each directed edge lies on one face.
    """
    faces = {0: (0, 1, 2), 1: (0, 2, 1)}
    where = {}
    for f, (a, b, c) in faces.items():
        where[(a, b)] = where[(b, c)] = where[(c, a)] = f
    nxt = 2
    adjset = [set() for _ in range(n)]
    for a, b in ((0, 1), (1, 2), (0, 2)):
        adjset[a].add(b)
        adjset[b].add(a)

    def put(f, tri):
        faces[f] = tri
        a, b, c = tri
        where[(a, b)] = where[(b, c)] = where[(c, a)] = f

    for w in range(3, n):
        f = rng.choice(list(faces))
        a, b, c = faces[f]
        put(f, (a, b, w))
        put(nxt, (b, c, w))
        put(nxt + 1, (c, a, w))
        nxt += 2
        for x in (a, b, c):
            adjset[x].add(w)
            adjset[w].add(x)
    keys = list(where)
    for _ in range(flips):
        a, b = rng.choice(keys)
        if (a, b) not in where:
            continue
        f1, f2 = where[(a, b)], where[(b, a)]
        c = next(x for x in faces[f1] if x not in (a, b))
        d = next(x for x in faces[f2] if x not in (a, b))
        if c == d or d in adjset[c] or len(adjset[a]) <= 3 or len(adjset[b]) <= 3:
            continue
        for e in ((a, b), (b, a)):
            del where[e]
        put(f1, (b, c, d))
        put(f2, (c, a, d))
        adjset[a].discard(b)
        adjset[b].discard(a)
        adjset[c].add(d)
        adjset[d].add(c)
        keys += [(c, d), (d, c)]
    return [sorted(s) for s in adjset]


ICOSAHEDRON_EDGES = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
    (1, 6), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8), (4, 9), (5, 9), (5, 10), (1, 10),
    (6, 7), (7, 8), (8, 9), (9, 10), (10, 6),
    (11, 6), (11, 7), (11, 8), (11, 9), (11, 10),
]


def test_page_example():
    # the wheel with a 5-cycle rim 1..5 and hub 0, and a vertex 6 joined to 1, 2, 3
    edges = [(0, i) for i in range(1, 6)] + [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (6, 1), (6, 2), (6, 3)]
    adj = adj_from_edges(7, edges)
    color = five_color(adj)
    check(adj, color)


def test_small_cases():
    assert five_color([]) == []
    assert five_color([[]]) == [0]
    k4 = adj_from_edges(4, list(itertools.combinations(range(4), 2)))
    c = five_color(k4)
    check(k4, c)
    assert len(set(c)) == 4
    k5 = adj_from_edges(5, list(itertools.combinations(range(5), 2)))
    c = five_color(k5)
    check(k5, c)
    k33 = adj_from_edges(6, [(a, b) for a in range(3) for b in range(3, 6)])
    check(k33, five_color(k33))
    tree = adj_from_edges(6, [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5)])
    check(tree, five_color(tree))


def test_icosahedron():
    adj = adj_from_edges(12, ICOSAHEDRON_EDGES)
    assert all(len(a) == 5 for a in adj)
    check(adj, five_color(adj))


def test_nonplanar_k6_and_k7_are_rejected():
    for n in (6, 7):
        adj = adj_from_edges(n, list(itertools.combinations(range(n), 2)))
        try:
            five_color(adj)
        except ValueError:
            continue
        raise AssertionError("K%d got a 5-coloring" % n)


def test_random_planar():
    rng = random.Random(7)
    stats = {}
    for _ in range(600):
        n = rng.randint(3, 30)
        adj = random_triangulation(rng, n, rng.randint(0, 4 * n))
        # delete a few edges at random to get non-maximal planar graphs
        if rng.random() < 0.3:
            for v in range(n):
                adj[v] = [u for u in adj[v] if (min(u, v) * 7 + max(u, v)) % 5 != 0]
        check(adj, five_color(adj, stats))
    assert stats.get("swaps", 0) > 0


def test_random_graphs_valid_or_rejected():
    rng = random.Random(8)
    for _ in range(500):
        n = rng.randint(0, 9)
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.6]
        adj = adj_from_edges(n, edges)
        try:
            color = five_color(adj)
        except ValueError:
            continue
        check(adj, color)


def test_large():
    rng = random.Random(9)
    adj = random_triangulation(rng, 3000, 9000)
    assert sum(len(a) for a in adj) == 2 * (3 * 3000 - 6)
    check(adj, five_color(adj))
