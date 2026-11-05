# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/demetrescu-italiano-apsp/. The authors are listed in prov/5HVW8R.jsonl.

import heapq
import math
import random

from demetrescu_italiano_apsp import DynamicAPSP


def static_dist(n, weights):
    """All distances by one Dijkstra run per source, from zero."""
    out = [[math.inf] * n for _ in range(n)]
    adj = [[] for _ in range(n)]
    for (a, b), w in weights.items():
        adj[a].append((b, w))
    for s in range(n):
        d = out[s]
        d[s] = 0
        h = [(0, s)]
        while h:
            du, u = heapq.heappop(h)
            if du > d[u]:
                continue
            for v, w in adj[u]:
                if du + w < d[v]:
                    d[v] = du + w
                    heapq.heappush(h, (d[v], v))
    return out


def check(g, weights):
    n = g.n
    want = static_dist(n, weights)
    for x in range(n):
        for y in range(n):
            assert g.dist(x, y) == want[x][y], (x, y, g.dist(x, y), want[x][y])
            p = g.path(x, y)
            if want[x][y] == math.inf:
                assert p is None
            else:
                assert p[0] == x and p[-1] == y and len(set(p)) == len(p)
                assert sum(weights[(a, b)] for a, b in zip(p, p[1:])) == want[x][y]


def test_example():
    g = DynamicAPSP(4)
    g.update(1, {(0, 1): 3, (1, 2): 1, (1, 3): 4})
    g.update(2, {(0, 2): 5, (2, 3): 1})
    assert [g.dist(0, y) for y in range(4)] == [0, 3, 4, 5]
    assert g.path(0, 3) == [0, 1, 2, 3]
    g.update(1, {(0, 1): None, (1, 3): 1})
    assert [g.dist(0, y) for y in range(4)] == [0, math.inf, 5, 6]
    assert g.path(0, 3) == [0, 2, 3]
    g.update(1, {(0, 1): 1})
    assert [g.dist(0, y) for y in range(4)] == [0, 1, 2, 2]
    assert g.path(0, 3) == [0, 1, 3]


def test_edges():
    g = DynamicAPSP(3)
    assert g.dist(0, 0) == 0 and g.dist(0, 1) == math.inf and g.path(0, 1) is None
    g.insert_edge(0, 1, 0)
    g.insert_edge(1, 0, 0)
    assert g.dist(0, 1) == 0 and g.dist(1, 0) == 0
    g.delete_edge(0, 1)
    assert g.dist(0, 1) == math.inf
    for bad in ({(1, 2): 1}, {(0, 0): 1}, {(0, 1): -1}):
        try:
            g.update(0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("no error")


def test_random_against_static():
    rng = random.Random(5)
    for trial in range(60):
        n = rng.randint(2, 7)
        g = DynamicAPSP(n)
        weights = {}
        for _ in range(40):
            v = rng.randrange(n)
            changes = {}
            for _ in range(rng.randint(1, 4)):
                u = rng.randrange(n)
                if u == v:
                    continue
                e = (v, u) if rng.random() < 0.5 else (u, v)
                changes[e] = None if rng.random() < 0.3 else rng.randint(0, 6)
            g.update(v, changes)
            for e, w in changes.items():
                if w is None:
                    weights.pop(e, None)
                else:
                    weights[e] = w
            check(g, weights)


def test_dense_ties():
    rng = random.Random(11)
    n = 6
    g = DynamicAPSP(n)
    weights = {}
    for _ in range(150):
        v = rng.randrange(n)
        changes = {}
        for u in range(n):
            if u != v and rng.random() < 0.6:
                changes[(v, u)] = rng.choice([None, 1, 1, 2])
                changes[(u, v)] = rng.choice([None, 1, 1, 2])
        g.update(v, changes)
        for e, w in changes.items():
            if w is None:
                weights.pop(e, None)
            else:
                weights[e] = w
        check(g, weights)
