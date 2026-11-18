# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-dependent-refinement/. The authors are listed in prov/TRTDD8.jsonl.

import random
from math import pi, sqrt

from view_dependent_refinement import (
    ProgressiveMesh,
    SelectiveMesh,
    cross,
    deltas,
    dot,
    grid_mesh,
    make_qrefine,
    orient,
    screen_error_exceeds,
    sub,
    vertex_bounds,
)

G = 6


def build(seed):
    rng = random.Random(seed)
    pos, faces, border = grid_mesh(rng, G)
    return ProgressiveMesh(rng, pos, faces, border)


def valid(sm):
    pm = sm.pm
    fs = sm.faces()
    directed = set()
    undirected = {}
    area2 = 0
    for c in fs.values():
        area2 += orient(*(pm.pos[v] for v in c))
        for k in range(3):
            a, b = c[k], c[(k + 1) % 3]
            if (a, b) in directed:
                return False
            directed.add((a, b))
            undirected[frozenset((a, b))] = undirected.get(frozenset((a, b)), 0) + 1
    for e, n in undirected.items():
        if n == 1:
            p, q = (pm.pos[v] for v in e)
            on_border = (p[0] == q[0] and p[0] in (0, G)) or (p[2] == q[2] and p[2] in (0, G))
            if not on_border:
                return False
    used = {v for c in fs.values() for v in c}
    if used != sm.active:
        return False
    return len(used) - len(undirected) + len(fs) == 1 and area2 == 2 * G * G


def test_full_refinement_and_full_coarsening():
    for seed in range(3):
        pm = build(seed)
        assert len(pm.order) >= 15
        sm = SelectiveMesh(pm)
        assert sm.faces() == pm.base_faces
        for v in pm.order:
            assert sm.vsplit_legal(v)
            sm.vsplit(v)
        assert sm.faces() == {f: c for f, c in enumerate(pm.faces)}
        for v in reversed(pm.order):
            assert sm.ecol_legal(v)
            sm.ecol(v)
        assert sm.faces() == pm.base_faces


def test_dependencies_come_earlier_in_the_vsplit_order():
    pm = build(4)
    for v in pm.order:
        i = pm.index[v]
        if v in pm.parent:
            assert pm.index[pm.parent[v]] < i
        for f in pm.rec[v][2]:
            if f in pm.creator:
                assert pm.index[pm.creator[f]] < i


def test_random_legal_operations_keep_the_mesh_valid():
    rng = random.Random(5)
    for seed in range(3):
        pm = build(seed)
        sm = SelectiveMesh(pm)
        done = 0
        for _ in range(400):
            ops = [("s", v) for v in sm.active if sm.vsplit_legal(v)]
            ops += [("c", v) for v in {pm.parent[w] for w in sm.active if w in pm.parent} if sm.ecol_legal(v)]
            kind, v = rng.choice(sorted(ops))
            if kind == "s":
                sm.vsplit(v)
            else:
                sm.ecol(v)
            done += 1
            assert valid(sm)
        assert done == 400


def test_force_vsplit_splits_the_vertex_and_keeps_the_mesh_valid():
    rng = random.Random(6)
    pm = build(7)
    for _ in range(40):
        sm = SelectiveMesh(pm)
        for _ in range(rng.randrange(0, 20)):
            ops = [v for v in sm.active if sm.vsplit_legal(v)]
            if ops:
                sm.vsplit(rng.choice(sorted(ops)))
        v = rng.choice(pm.order)
        sm.force_vsplit(v)
        assert sm.is_split(v)
        assert valid(sm)


def test_adapt_refinement_reaches_a_fixed_point():
    pm = build(8)
    bounds = vertex_bounds(pm, deltas(pm))
    rng = random.Random(9)
    sm = SelectiveMesh(pm)
    for _ in range(6):
        eye = (rng.uniform(-2, G + 2), rng.uniform(4, 8), rng.uniform(G + 1, G + 5))
        target = (rng.uniform(1, G - 1), 0.0, rng.uniform(1, G - 1))
        q = make_qrefine(pm, bounds, eye, sub(target, eye), pi / 3, rng.uniform(0.05, 0.4))
        for _ in range(50):
            if sm.adapt_refinement(q) == 0:
                break
        assert sm.adapt_refinement(q) == 0
        assert valid(sm)
        for v in sm.active:
            assert not (v in pm.children and q(v))
            if v in pm.parent:
                p = pm.parent[v]
                assert not (sm.ecol_legal(p) and not q(p))


def test_squared_screen_error_test_equals_the_projected_radius_form():
    rng = random.Random(10)
    checked = 0
    for _ in range(5000):
        mu, delta = rng.uniform(0, 0.2), rng.uniform(0, 1)
        n = tuple(rng.uniform(-1, 1) for _ in range(3))
        ln = sqrt(dot(n, n))
        n = tuple(x / ln for x in n)
        p = tuple(rng.uniform(-5, 5) for _ in range(3))
        e = tuple(rng.uniform(-5, 5) for _ in range(3))
        kappa = rng.uniform(0.001, 0.2)
        w = sub(p, e)
        d = sqrt(dot(w, w))
        c = cross(n, w)
        radius = max(mu, delta * sqrt(dot(c, c)) / d) / d
        if abs(radius - kappa) < 1e-9:
            continue
        assert screen_error_exceeds(mu, delta, n, p, e, kappa) == (radius >= kappa)
        checked += 1
    assert checked > 4900
