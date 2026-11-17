# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-pseudotime/. The authors are listed in prov/MJ06W1.jsonl.

import itertools
import math
import random

import pytest

from mst_pseudotime import (
    adjacency,
    cell_pseudotime,
    cluster_pseudotime,
    diameter_path,
    dist,
    prim_mst,
    tree_distances,
)

R2 = math.sqrt(2)
PAGE = [(0, 0), (1, 0), (2, 0), (3, 1), (4, 2), (3, -1), (4, -2), (5, -3)]


def weight(edges):
    return sum(w for _, _, w in edges)


def kruskal_weight(points):
    n = len(points)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0.0
    for w, a, b in sorted((dist(points[a], points[b]), a, b) for a in range(n) for b in range(a + 1, n)):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += w
    return total


def prufer_trees(n):
    """All labeled trees on n vertices, from Pruefer sequences."""
    for seq in itertools.product(range(n), repeat=n - 2):
        degree = [1] * n
        for x in seq:
            degree[x] += 1
        edges = []
        for x in seq:
            leaf = min(v for v in range(n) if degree[v] == 1)
            edges.append((leaf, x))
            degree[leaf] -= 1
            degree[x] -= 1
        u, v = [v for v in range(n) if degree[v] == 1]
        edges.append((u, v))
        yield edges


def spearman(a, b):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for k, i in enumerate(order):
            r[i] = k
        return r

    ra, rb = ranks(a), ranks(b)
    n = len(a)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))


def test_page_example():
    out = cell_pseudotime(PAGE)
    assert sorted((min(a, b), max(a, b)) for a, b, _ in out["tree"]) == [(0, 1), (1, 2), (2, 3), (2, 5), (3, 4), (5, 6), (6, 7)]
    # The longest path runs from tip to tip, not from the start of the process.
    assert out["backbone"] == [7, 6, 5, 2, 3, 4]
    assert out["branch_points"] == [2]
    tau = cell_pseudotime(PAGE, root=0)["pseudotime"]
    want = [0, 1, 2, 2 + R2, 2 + 2 * R2, 2 + R2, 2 + 2 * R2, 2 + 3 * R2]
    assert all(math.isclose(a, b) for a, b in zip(tau, want))


def test_prim_matches_kruskal_and_exhaustive_search():
    rng = random.Random(1)
    for _ in range(30):
        n = rng.randint(2, 25)
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        edges = prim_mst(pts)
        assert len(edges) == n - 1
        assert math.isclose(weight(edges), kruskal_weight(pts))
    for n in range(2, 7):
        pts = [(rng.random(), rng.random(), rng.random()) for _ in range(n)]
        best = min(sum(dist(pts[a], pts[b]) for a, b in t) for t in prufer_trees(n))
        assert math.isclose(weight(prim_mst(pts)), best)


def test_diameter_matches_all_pairs():
    rng = random.Random(2)
    for _ in range(30):
        n = rng.randint(2, 20)
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        adj = adjacency(n, prim_mst(pts))
        path = diameter_path(adj, start=rng.randrange(n))
        length = sum(w for a, b in zip(path, path[1:]) for v, w in adj[a] if v == b)
        longest = max(max(tree_distances(adj, s)[0]) for s in range(n))
        assert math.isclose(length, longest)


def test_points_on_a_monotone_curve_are_ordered_exactly():
    """Distance strictly increasing in the gap of the parameter: the tree is the path of consecutive points."""
    rng = random.Random(3)
    for _ in range(10):
        t = sorted(rng.uniform(0, 2.5) for _ in range(30))
        pts = [(math.cos(s), math.sin(s), 0.3 * s) for s in t]  # a helix piece, chords grow with the gap
        order = list(range(30))
        rng.shuffle(order)
        shuffled = [pts[i] for i in order]
        tt = [t[i] for i in order]
        root = order.index(0)
        tau = cell_pseudotime(shuffled, root=root)["pseudotime"]
        assert sorted(range(30), key=lambda i: tau[i]) == sorted(range(30), key=lambda i: tt[i])
        arc = [0.0]
        for a, b in zip(pts, pts[1:]):
            arc.append(arc[-1] + dist(a, b))
        assert all(math.isclose(tau[j], arc[order[j]], abs_tol=1e-12) for j in range(30))


def test_noisy_line_measured():
    """A measurement: 200 cells near a line in 5 dimensions, noise 0.05 per coordinate."""
    rng = random.Random(4)
    t = [rng.random() for _ in range(200)]
    pts = [[s * 3, s * 2] + [rng.gauss(0, 0.05) for _ in range(3)] for s in t]
    pts = [[p[0] + rng.gauss(0, 0.05), p[1] + rng.gauss(0, 0.05)] + p[2:] for p in pts]
    root = min(range(200), key=lambda i: t[i])
    tau = cell_pseudotime(pts, root=root)["pseudotime"]
    assert spearman(tau, t) > 0.97


def test_cluster_version_on_a_line():
    rng = random.Random(5)
    pts, labels, t = [], [], []
    for c in range(5):
        for _ in range(20):
            s = c + rng.uniform(-0.4, 0.4)
            pts.append((s, rng.gauss(0, 0.1)))
            labels.append(c)
            t.append(s)
    out = cluster_pseudotime(pts, labels, root_cluster=0)
    assert out["path"] == [0, 1, 2, 3, 4]
    tau = out["pseudotime"]
    assert all(v is not None for v in tau)
    assert spearman(tau, t) > 0.97
    # A cell is placed between 0 and the length of the path of centers.
    c = out["centers"]
    length = sum(dist(c[i], c[i + 1]) for i in range(4))
    assert all(0 <= v <= length + 1e-12 for v in tau)


def test_cluster_version_off_path_cluster_gets_none():
    pts = [(0, 0), (0.1, 0), (1, 0), (1.1, 0), (2, 0), (2.1, 0), (1, 5), (1.1, 5)]
    labels = [0, 0, 1, 1, 2, 2, 3, 3]
    out = cluster_pseudotime(pts, labels, root_cluster=0)
    assert out["path"] == [0, 1, 3]
    assert out["pseudotime"][4] is None
    with pytest.raises(ValueError):
        cluster_pseudotime(pts, labels, root_cluster=9)


def test_branching_measured():
    """A measurement: a Y with three arms of 60 cells; one branch point lies near the junction."""
    rng = random.Random(6)
    pts = []
    for ang in (math.pi, math.pi / 4, -math.pi / 4):
        for _ in range(60):
            r = rng.uniform(0.05, 1.0)
            pts.append((r * math.cos(ang) + rng.gauss(0, 0.02), r * math.sin(ang) + rng.gauss(0, 0.02)))
    out = cell_pseudotime(pts)
    hubs = [v for v in out["branch_points"] if math.hypot(*pts[v]) < 0.3]
    assert hubs
    assert len(out["branch_points"]) > 3  # noise adds small side branches too


def test_errors():
    with pytest.raises(ValueError):
        cell_pseudotime([(0, 0)])
    with pytest.raises(ValueError):
        cell_pseudotime([(0, 0), (1, 1)], root=5)
