# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isomap/. The authors are listed in prov/HKAVDA.jsonl.

import math
import random

import pytest

from isomap import dijkstra, geodesic_distances, isomap, neighbor_graph


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0] * len(xs)
    for pos, i in enumerate(order):
        r[i] = pos
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))


def test_dijkstra_small_graph():
    adj = [{1: 1.0, 2: 4.0}, {0: 1.0, 2: 2.0}, {0: 4.0, 1: 2.0, 3: 1.0}, {2: 1.0}]
    assert dijkstra(adj, 0) == [0.0, 1.0, 3.0, 4.0]


def test_arc_is_unrolled_exactly():
    # Points on an arc with gaps 0.06 to 0.12. The radius 0.15 joins each point
    # only to the next point on each side, so the graph is a path.
    ts = [0.1 * i + 0.02 * (i % 3) for i in range(25)]
    pts = [(math.cos(t), math.sin(t), 0.0) for t in ts]
    y, lam = isomap(pts, 1, eps=0.15)
    chord = [0.0]
    for p, q in zip(pts, pts[1:]):
        chord.append(chord[-1] + math.dist(p, q))
    sign = 1.0 if y[-1][0] > y[0][0] else -1.0
    shift = sum(chord) / len(chord)
    for (v,), c in zip(y, chord):
        assert abs(sign * v - (c - shift)) < 1e-9
    assert abs(lam[1]) < 1e-9 * lam[0]


def test_complete_graph_equals_classical_mds():
    rng = random.Random(3)
    pts = [(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(12)]
    y, _ = isomap(pts, 2, k=11)
    for i in range(12):
        for j in range(12):
            assert abs(math.dist(y[i], y[j]) - math.dist(pts[i], pts[j])) < 1e-9


def test_swiss_roll_strip_is_unrolled():
    # One full turn of the roll, t in [1.5 pi, 3.5 pi], height in [0, 1]. The density
    # of t is proportional to t, so the points are close to uniform in arc length.
    rng = random.Random(7)
    ts, pts = [], []
    for _ in range(70):
        t = math.sqrt(rng.uniform((1.5 * math.pi) ** 2, (3.5 * math.pi) ** 2))
        h = rng.uniform(0.0, 1.0)
        ts.append(t)
        pts.append((t * math.cos(t), h, t * math.sin(t)))
    y, _ = isomap(pts, 1, k=6)
    rho = spearman([v for (v,) in y], ts)
    assert abs(rho) > 0.99
    # Without the graph, classical MDS on straight-line distances folds the roll.
    flat = isomap(pts, 1, k=69)[0]
    assert abs(spearman([v for (v,) in flat], ts)) < 0.9


def test_disconnected_graph_is_rejected():
    pts = [(0.0, 0.0), (0.1, 0.0), (0.2, 0.0), (10.0, 0.0), (10.1, 0.0), (10.2, 0.0)]
    with pytest.raises(ValueError):
        geodesic_distances(pts, k=2)


def test_epsilon_graph():
    pts = [(float(i), 0.0) for i in range(6)]
    adj = neighbor_graph(pts, eps=1.0)
    assert sorted(adj[2]) == [1, 3]
    assert geodesic_distances(pts, eps=1.0)[0][5] == 5.0
