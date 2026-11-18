# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roam-terrain/. The authors are listed in prov/5KAMME.jsonl.

import random
from fractions import Fraction

from roam_terrain import (
    Bintree,
    Mesh,
    base,
    contains,
    edges_of,
    interpolate,
    make_priority,
    random_heights,
    target,
    update,
)


def conforming(mesh):
    m = mesh.tree.m
    verts = {v for t in mesh.active for v in t}
    area2 = 0
    for t in mesh.active:
        a, b, c = t
        area2 += (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    if area2 != 2 * m * m:
        return False
    for e, ts in mesh.edges.items():
        p, q = tuple(e)
        border = (p[0] == q[0] and p[0] in (0, m)) or (p[1] == q[1] and p[1] in (0, m))
        if len(ts) != (1 if border else 2):
            return False
        for v in verts:
            if v in (p, q):
                continue
            cr = (q[0] - p[0]) * (v[1] - p[1]) - (q[1] - p[1]) * (v[0] - p[0])
            if cr == 0 and min(p[0], q[0]) <= v[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= v[1] <= max(p[1], q[1]):
                return False
    return True


def setup(rng, k):
    m = 2 ** k
    tree = Bintree(k, random_heights(rng, m))
    eye = (Fraction(rng.randint(0, 4 * m), 4), Fraction(rng.randint(0, 4 * m), 4))
    return tree, eye


def test_wedgie_bounds_the_true_surface():
    rng = random.Random(1)
    tree, _ = setup(rng, 3)
    pts = list(tree.h)
    for t in tree.all:
        worst = max(abs(tree.h[p] - interpolate(t, tree.h, p)) for p in pts if contains(t, p))
        assert worst <= tree.err[t]
        if t in tree.children:
            assert all(tree.err[u] <= tree.err[t] for u in tree.children[t])


def test_partner_is_in_the_tree_and_priorities_are_monotone():
    rng = random.Random(2)
    tree, eye = setup(rng, 4)
    prio = make_priority(tree, eye, 1)
    known = set(tree.all)
    for t in tree.all:
        u = tree.partner(t)
        if u is not None:
            assert u in known and base(u) == base(t) and tree.partner(u) == t
        for c in tree.children.get(t, ()):
            assert prio(c) <= prio(t)


def test_force_split_keeps_the_mesh_conforming():
    rng = random.Random(3)
    tree, _ = setup(rng, 4)
    mesh = Mesh(tree)
    for _ in range(60):
        t = rng.choice(sorted(t for t in mesh.active if t in tree.children))
        mesh.force_split(t)
        assert t not in mesh.active
        assert conforming(mesh)


def test_frame_reaches_the_closure_and_every_leaf_is_accurate():
    rng = random.Random(4)
    for _ in range(6):
        tree, eye = setup(rng, 4)
        eps = Fraction(rng.randint(1, 12), 8)
        prio = make_priority(tree, eye, 1)
        mesh = update(Mesh(tree), prio, eps)
        assert mesh.active == target(tree, prio, eps)
        assert conforming(mesh)
        assert all(prio(t) <= eps * eps for t in mesh.active)


def test_incremental_frames_equal_a_fresh_build():
    rng = random.Random(5)
    tree, eye = setup(rng, 4)
    mesh = Mesh(tree)
    eps = Fraction(1, 2)
    for _ in range(8):
        eye = (min(max(eye[0] + Fraction(rng.randint(-8, 8), 4), 0), 16),
               min(max(eye[1] + Fraction(rng.randint(-8, 8), 4), 0), 16))
        eps = min(max(eps + Fraction(rng.randint(-2, 2), 8), Fraction(1, 8)), Fraction(2))
        prio = make_priority(tree, eye, 1)
        update(mesh, prio, eps)
        fresh = update(Mesh(tree), prio, eps)
        assert mesh.active == fresh.active
        assert conforming(mesh)


def test_result_is_the_smallest_accurate_triangulation_by_enumeration():
    rng = random.Random(6)
    tree, eye = setup(rng, 2)
    start = frozenset(tree.roots)
    seen = {start}
    todo = [start]
    while todo:
        s = todo.pop()
        for t in s:
            if t in tree.children:
                mesh = Mesh(tree, s)
                mesh.force_split(t)
                n = frozenset(mesh.active)
                if n not in seen:
                    seen.add(n)
                    todo.append(n)
    assert len(seen) == 5489
    assert all(conforming(Mesh(tree, s)) for s in sorted(seen, key=sorted)[::25])
    for eps in (Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2)):
        prio = make_priority(tree, eye, 1)
        ok = [s for s in seen if all(prio(t) <= eps * eps for t in s)]
        best = min(len(s) for s in ok)
        winners = [s for s in ok if len(s) == best]
        got = frozenset(update(Mesh(tree), prio, eps).active)
        assert winners == [got]
