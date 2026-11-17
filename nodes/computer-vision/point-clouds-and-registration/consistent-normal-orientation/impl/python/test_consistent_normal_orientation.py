# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-normal-orientation/. The authors are listed in prov/4CA5PS.jsonl.

import math
import random
from collections import deque

from consistent_normal_orientation import emst_edges, orient_normals, riemannian_graph


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def kruskal(n, edges):
    """Minimum spanning tree by Kruskal with union-find. edges: (w, i, j)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree = []
    for w, i, j in sorted(edges):
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            tree.append((w, i, j))
    return tree


def oracle(points, normals, k):
    """Kruskal on the same graph, then breadth-first propagation."""
    n = len(points)
    adj = riemannian_graph(points, k)
    edges = [(1.0 - abs(dot(normals[i], normals[j])), i, j) for i in adj for j in adj[i] if i < j]
    tree = kruskal(n, edges)
    nb = {i: [] for i in range(n)}
    for _, i, j in tree:
        nb[i].append(j)
        nb[j].append(i)
    root = max(range(n), key=lambda i: (points[i][2], -i))
    out = [tuple(m) for m in normals]
    if out[root][2] < 0:
        out[root] = tuple(-x for x in out[root])
    seen = {root}
    queue = deque([root])
    while queue:
        i = queue.popleft()
        for j in nb[i]:
            if j not in seen:
                seen.add(j)
                if dot(out[i], out[j]) < 0:
                    out[j] = tuple(-x for x in out[j])
                queue.append(j)
    return out


def sphere(rng, n, r=1.0):
    pts, nrm = [], []
    for _ in range(n):
        u = [rng.gauss(0, 1) for _ in range(3)]
        lu = math.sqrt(dot(u, u))
        u = [x / lu for x in u]
        pts.append(tuple(r * x for x in u))
        s = rng.choice([-1.0, 1.0])
        nrm.append(tuple(s * x for x in u))
    return pts, nrm


def test_example_arc() -> None:
    ts = [math.radians(a) for a in (90, 60, 30, 120, 150)]
    pts = [(math.cos(t), 0.0, math.sin(t)) for t in ts]
    signs = [1, -1, 1, 1, -1]
    nrm = [tuple(s * x for x in p) for s, p in zip(signs, pts)]
    out = orient_normals(pts, nrm, 2)
    for p, m in zip(pts, out):
        assert all(abs(a - b) < 1e-12 for a, b in zip(p, m))


def test_sphere_becomes_outward() -> None:
    rng = random.Random(31)
    pts, nrm = sphere(rng, 120)
    out = orient_normals(pts, nrm, 6)
    assert all(dot(p, m) > 0 for p, m in zip(pts, out))


def test_plane_and_paraboloid() -> None:
    rng = random.Random(32)
    pts, nrm = [], []
    for _ in range(80):
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        z = 0.3 * (x * x - y * y)
        g = (-0.6 * x, 0.6 * y, 1.0)
        lg = math.sqrt(dot(g, g))
        s = rng.choice([-1.0, 1.0])
        pts.append((x, y, z))
        nrm.append(tuple(s * c / lg for c in g))
    out = orient_normals(pts, nrm, 6)
    assert all(m[2] > 0 for m in out)


def test_matches_kruskal_oracle() -> None:
    rng = random.Random(33)
    for _ in range(5):
        pts, nrm = sphere(rng, 60, r=rng.uniform(0.5, 2.0))
        noisy = []
        for m in nrm:
            v = [x + rng.gauss(0, 0.05) for x in m]
            lv = math.sqrt(dot(v, v))
            noisy.append(tuple(x / lv for x in v))
        assert orient_normals(pts, noisy, 5) == oracle(pts, noisy, 5)


def test_output_does_not_depend_on_input_signs() -> None:
    rng = random.Random(34)
    pts, nrm = sphere(rng, 50)
    flipped = [tuple(-x for x in m) if rng.random() < 0.5 else m for m in nrm]
    assert orient_normals(pts, nrm, 5) == orient_normals(pts, flipped, 5)


def test_emst_is_minimum() -> None:
    rng = random.Random(35)
    for _ in range(5):
        pts = [tuple(rng.uniform(0, 1) for _ in range(3)) for _ in range(25)]
        e = emst_edges(pts)
        assert len(e) == 24
        total = sum(math.dist(pts[i], pts[j]) for i, j in e)
        allp = [(math.dist(pts[i], pts[j]), i, j) for i in range(25) for j in range(i + 1, 25)]
        best = sum(w for w, _, _ in kruskal(25, allp))
        assert abs(total - best) < 1e-12


def test_thin_plate_is_a_known_failure() -> None:
    # Two sheets 0.05 apart, the top and the bottom of a thin plate. The true
    # outward normals are +z on top and -z below, but every normal is
    # parallel to every other, so propagation gives all of them one sign.
    rng = random.Random(36)
    top = [(rng.uniform(0, 1), rng.uniform(0, 1), 0.05) for _ in range(30)]
    bottom = [(rng.uniform(0, 1), rng.uniform(0, 1), 0.0) for _ in range(30)]
    nrm = [(0.0, 0.0, rng.choice([-1.0, 1.0])) for _ in range(60)]
    out = orient_normals(top + bottom, nrm, 6)
    assert all(m == (0.0, 0.0, 1.0) for m in out)


def test_edges() -> None:
    assert orient_normals([], [], 3) == []
    assert orient_normals([(0.0, 0.0, 1.0)], [(0.0, 0.0, -1.0)], 3) == [(0.0, 0.0, 1.0)]
