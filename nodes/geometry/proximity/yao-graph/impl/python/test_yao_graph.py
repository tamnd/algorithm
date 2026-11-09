# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-graph/. The authors are listed in prov/78899M.jsonl.

import heapq
import itertools
import math
import random

import pytest

from yao_graph import YaoGraph, dist2

EXAMPLE = [(1, 3), (1, 11), (2, 8), (5, 1), (9, 6), (11, 1), (11, 4)]
# Boundary directions of the eight cones, counterclockwise from the positive x-axis.
DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def oracle_cone(v, k):
    """Independent cone test: v is in cone j when it is on or left of boundary j and strictly
    right of boundary j + 1 (the cones are at most 90 degrees wide, so this is enough)."""
    step = 8 // k
    for j in range(k):
        a, b = DIRS[j * step], DIRS[((j + 1) * step) % 8]
        if cross(a, v) >= 0 and cross(b, v) < 0:
            return j
    raise AssertionError("no cone")


def oracle_edges(P, k):
    E = set()
    for i, p in enumerate(P):
        for c in range(k):
            cand = [(dist2(p, q), j) for j, q in enumerate(P) if j != i and oracle_cone((q[0] - p[0], q[1] - p[1]), k) == c]
            if cand:
                E.add(tuple(sorted((i, min(cand)[1]))))
    return E


def shortest_paths(P, E):
    n = len(P)
    adj = [[] for _ in range(n)]
    for i, j in E:
        w = math.dist(P[i], P[j])
        adj[i].append((j, w))
        adj[j].append((i, w))
    out = []
    for s in range(n):
        d = [math.inf] * n
        d[s] = 0.0
        h = [(0.0, s)]
        while h:
            du, u = heapq.heappop(h)
            if du > d[u]:
                continue
            for v, w in adj[u]:
                if du + w < d[v]:
                    d[v] = du + w
                    heapq.heappush(h, (d[v], v))
        out.append(d)
    return out


def mst_weight(P, E):
    """Kruskal on the given edges, with exact squared lengths for ordering and float sum."""
    parent = list(range(len(P)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, used = 0.0, 0
    for _, i, j in sorted((dist2(P[i], P[j]), i, j) for i, j in E):
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            total += math.dist(P[i], P[j])
            used += 1
    return total, used


T8 = 1 / (1 - 2 * math.sin(math.pi / 8))  # about 4.262


def test_example() -> None:
    g = YaoGraph(EXAMPLE)
    assert len(g.edges()) == 15
    assert g.out[0] == [4, 2, 1, None, None, None, None, 3]  # (1,3): (9,6), (2,8), (1,11), (5,1)
    assert g.has_edge(0, 4) and g.has_edge(2, 3)  # these two edges cross: not planar
    assert len(YaoGraph(EXAMPLE, 4).edges()) == 10


def test_small_and_errors() -> None:
    assert YaoGraph([]).edges() == []
    assert YaoGraph([(0, 0)]).edges() == []
    assert YaoGraph([(0, 0), (3, -7)]).edges() == [(0, 1)]
    with pytest.raises(ValueError):
        YaoGraph([(0, 0), (0, 0)])
    with pytest.raises(ValueError):
        YaoGraph([(0, 0)], 6)


def test_collinear_and_grid() -> None:
    line = [(3 * t, t) for t in range(8)]
    assert YaoGraph(line).edges() == [(t, t + 1) for t in range(7)]
    grid = [(x, y) for x in range(4) for y in range(4)]
    for k in (4, 8):
        assert set(YaoGraph(grid, k).edges()) == oracle_edges(grid, k)


def test_random_against_oracle_stretch_and_mst() -> None:
    rng = random.Random(1982)
    worst = 1.0
    for _ in range(500):
        n = rng.randint(0, 14)
        r = rng.choice([3, 10, 1000])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        complete = list(itertools.combinations(range(len(pts)), 2))
        for k in (4, 8):
            E = YaoGraph(pts, k).edges()
            assert set(E) == oracle_edges(pts, k)
            assert len(E) <= k * len(pts)
            if k == 8:
                d = shortest_paths(pts, E)
                for i, j in complete:
                    ratio = d[i][j] / math.dist(pts[i], pts[j])
                    assert ratio <= T8 + 1e-9
                    worst = max(worst, ratio)
                # Every Euclidean minimum spanning tree lies in the 8-cone Yao graph.
                w_all, _ = mst_weight(pts, complete)
                w_yao, used = mst_weight(pts, E)
                assert used == max(len(pts) - 1, 0)
                assert abs(w_all - w_yao) <= 1e-9 * max(1.0, w_all)
            else:
                assert mst_weight(pts, E)[1] == max(len(pts) - 1, 0)  # connected
    assert worst < T8
