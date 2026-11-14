# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/progressive-mesh/. The authors are listed in prov/WJ1E5T.jsonl.

import random
from fractions import Fraction

import pytest

from mx2geom import directed_edges, euler_characteristic
from progressive_mesh import Mesh, build, ecol, edges, link_condition, refine, vsplit

TET_V = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
TET_F = [(0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2)]
OCTA_V = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
OCTA_F = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
STRIP_V = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0)]
STRIP_F = [(0, 1, 4), (0, 4, 3), (1, 2, 5), (1, 5, 4)]


def subdivide(v, f):
    v = list(v)
    mid, out = {}, []

    def m(a, b):
        key = (min(a, b), max(a, b))
        if key not in mid:
            mid[key] = len(v)
            v.append(tuple(Fraction(x + y, 2) for x, y in zip(v[a], v[b])))
        return mid[key]

    for a, b, c in f:
        ab, bc, ca = m(a, b), m(b, c), m(c, a)
        out += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
    return v, out


def jitter(v, seed):
    rng = random.Random(seed)
    return [tuple(Fraction(x) + Fraction(rng.randint(-20, 20), 400) for x in p) for p in v]


def torus(r, c):
    idx = lambda i, j: (i % r) * c + (j % c)
    v = [(i, j, 0) for i in range(r) for j in range(c)]
    f = []
    for i in range(r):
        for j in range(c):
            f += [(idx(i, j), idx(i + 1, j), idx(i + 1, j + 1)), (idx(i, j), idx(i + 1, j + 1), idx(i, j + 1))]
    return v, f


def grid_disk(r, c):
    idx = lambda i, j: i * (c + 1) + j
    v = [(i, j, 0) for i in range(r + 1) for j in range(c + 1)]
    f = []
    for i in range(r):
        for j in range(c):
            f += [(idx(i, j), idx(i + 1, j), idx(i + 1, j + 1)), (idx(i, j), idx(i + 1, j + 1), idx(i, j + 1))]
    return v, f


def meshes():
    octa2 = subdivide(*subdivide(OCTA_V, OCTA_F))
    return [
        ("octahedron", OCTA_V, OCTA_F),
        ("octahedron subdivided twice", jitter(octa2[0], 1), octa2[1]),
        ("torus 5 x 6", jitter(torus(5, 6)[0], 2), torus(5, 6)[1]),
        ("grid disk 4 x 5", jitter(grid_disk(4, 5)[0], 3), grid_disk(4, 5)[1]),
        ("strip", STRIP_V, STRIP_F),
    ]


def is_manifold_surface(mesh):
    faces = list(mesh.faces.values())
    directed_edges(faces)  # raises if a directed edge is used twice
    assert len({frozenset(t) for t in faces}) == len(faces)
    for v, star in mesh.star.items():  # each vertex has one fan: a cycle or one path
        nxt = {}
        for f in star:
            t = mesh.faces[f]
            k = t.index(v)
            nxt[t[(k + 1) % 3]] = t[(k + 2) % 3]
        assert len(nxt) == len(star)
        starts = [a for a in nxt if a not in nxt.values()]
        assert len(starts) <= 1
        first = a = starts[0] if starts else next(iter(nxt))
        steps = 0
        while a in nxt and steps <= len(nxt):
            a = nxt[a]
            steps += 1
            if a == first:
                break
        assert steps == len(nxt)  # one walk visits every face at v


def test_every_legal_collapse_is_undone_exactly():
    for name, v, f in meshes():
        original = Mesh(v, f)
        chi = euler_characteristic(f)
        for a, b in edges(original):
            for vs, vt in ((a, b), (b, a)):
                mesh = original.copy()
                if not link_condition(mesh, vs, vt):
                    with pytest.raises(ValueError):
                        ecol(mesh, vs, vt, (0, 0, 0))
                    assert mesh.state() == original.state()
                    continue
                rec = ecol(mesh, vs, vt, (7, 7, 7))
                assert vt not in mesh.pos and mesh.pos[vs] == (7, 7, 7)
                is_manifold_surface(mesh)
                assert euler_characteristic(list(mesh.faces.values())) == chi
                vsplit(mesh, rec)
                assert mesh.state() == original.state(), (name, vs, vt)


def test_whole_sequence_restores_the_input_and_every_level():
    for name, v, f in meshes():
        original = Mesh(v, f)
        base, records = build(v, f, target=4)
        # Replay the collapses to get the mesh at every level.
        levels = [refine(base, records, k).state() for k in range(len(records) + 1)]
        assert levels[-1] == original.state(), name
        assert levels[0] == base.state()
        for k in range(len(records)):
            assert len(levels[k + 1][0]) == len(levels[k][0]) + 1


def test_link_condition_rejects_bad_collapses():
    tet = Mesh(TET_V, TET_F)
    for a, b in edges(tet):
        assert not link_condition(tet, a, b) and not link_condition(tet, b, a)
    strip = Mesh(STRIP_V, STRIP_F)
    assert not link_condition(strip, 1, 4)  # an inner edge between two boundary vertices: a pinch
    assert link_condition(strip, 0, 1)  # a boundary edge
    assert not link_condition(strip, 0, 5)  # not an edge


def test_simplification_keeps_the_topology():
    for name, v, f in meshes():
        chi = euler_characteristic(f)
        base, records = build(v, f, target=4)
        is_manifold_surface(base)
        assert euler_characteristic(list(base.faces.values())) == chi
        if name.startswith("octahedron"):
            assert len(base.pos) == 4 and len(base.faces) == 4  # a sphere ends as a tetrahedron


def test_record_is_small_and_ids_are_fresh():
    v, f = meshes()[1][1:]
    base, records = build(v, f, target=4)
    assert len(base.pos) + len(records) == len(v)
    created = [r.vt for r in records]
    assert len(set(created)) == len(created) and not set(created) & set(base.pos)
    for r in records:
        assert r.fl is not None and r.fr is not None  # a closed mesh: two faces per split


def test_random_orders_round_trip():
    for seed in range(4):
        rng = random.Random(seed)
        name, v, f = meshes()[seed % 4]
        mesh = Mesh(v, f)
        original = mesh.state()
        stack = []
        for _ in range(len(v)):
            legal = [(a, b) for a, b in edges(mesh) if link_condition(mesh, a, b)]
            if not legal:
                break
            a, b = rng.choice(legal)
            if rng.random() < 0.5:
                a, b = b, a
            stack.append(ecol(mesh, a, b, mesh.pos[rng.choice((a, b))]))
        while stack:
            vsplit(mesh, stack.pop())
        assert mesh.state() == original
