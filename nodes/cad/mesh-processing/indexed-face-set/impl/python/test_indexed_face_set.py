# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indexed-face-set/. The authors are listed in prov/A865QN.jsonl.

import random

from indexed_face_set import IndexedFaceSet, read_off

# ---- brute force: scan every face for every query ----


def scan_edges(face):
    k = len(face)
    return [(face[i], face[(i + 1) % k]) for i in range(k)]


def brute_edge_faces(faces, u, v):
    return [f for f, face in enumerate(faces) for a, b in scan_edges(face) if {a, b} == {u, v}]


def brute_neighbors(faces, f):
    mine = {frozenset(e) for e in scan_edges(faces[f])}
    return {g for g, face in enumerate(faces) if g != f and mine & {frozenset(e) for e in scan_edges(face)}}


def brute_vertex_faces(faces, v):
    return [f for f, face in enumerate(faces) if v in face]


def brute_edge_set(faces):
    return {frozenset(e) for face in faces for e in scan_edges(face)}


def rand_mesh(rng, n, nf):
    faces = []
    for _ in range(nf):
        k = rng.choice((3, 3, 3, 4, 5))
        faces.append(tuple(rng.sample(range(n), min(k, n))))
    verts = [(rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]
    return verts, faces


# ---- tests ----


def test_page_example_square():
    m = IndexedFaceSet([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [(0, 1, 2), (0, 2, 3)])
    assert m.edges[(0, 2)] == [(0, 2), (1, 0)]
    assert m.edge_faces(2, 0) == [0, 1]
    assert sorted(m.boundary_edges()) == [(0, 1), (0, 3), (1, 2), (2, 3)]
    assert m.face_neighbors(0) == [1]
    assert m.vertex_faces(0) == [0, 1]
    assert m.euler_characteristic() == 1


def test_page_example_soup():
    pts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 0), (1, 1, 0), (0, 1, 0)]
    m = IndexedFaceSet(pts, [(0, 1, 2), (3, 4, 5)])
    assert m.face_neighbors(0) == []
    assert len(m.boundary_edges()) == 6
    assert m.euler_characteristic() == 2


def test_closed_meshes():
    tet = IndexedFaceSet([(0, 0, 0)] * 4, [(0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2)])
    assert tet.euler_characteristic() == 2 and tet.boundary_edges() == []
    cube = IndexedFaceSet([(0, 0, 0)] * 8, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                                             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
    assert cube.euler_characteristic() == 2 and cube.boundary_edges() == []
    assert all(len(cube.face_neighbors(f)) == 4 for f in range(6))
    a, b = 4, 5
    faces = []
    for i in range(a):
        for j in range(b):
            p, q = i * b + j, ((i + 1) % a) * b + j
            r, s = ((i + 1) % a) * b + (j + 1) % b, i * b + (j + 1) % b
            faces += [(p, q, r), (p, r, s)]
    torus = IndexedFaceSet([(0, 0, 0)] * (a * b), faces)
    assert torus.euler_characteristic() == 0 and torus.boundary_edges() == []


def test_non_manifold_edge():
    # three triangles on one edge {0, 1}
    m = IndexedFaceSet([(0, 0, 0)] * 5, [(0, 1, 2), (1, 0, 3), (0, 1, 4)])
    assert m.non_manifold_edges() == [(0, 1)]
    assert sorted(m.edge_faces(0, 1)) == [0, 1, 2]


def test_invalid_faces():
    for bad in ([(0, 1)], [(0, 1, 1)], [(0, 1, 3)]):
        try:
            IndexedFaceSet([(0, 0, 0)] * 3, bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


def test_off_round_trip():
    text = "OFF\n# a square\n4 2 0\n0 0 0\n1 0 0\n1.5 1 0\n0 1 -2.25\n3 0 1 2\n3 0 2 3\n"
    m = read_off(text)
    assert m.vertices[2] == (1.5, 1, 0) and m.faces == [(0, 1, 2), (0, 2, 3)]
    m2 = read_off(m.to_off())
    assert m2.vertices == m.vertices and m2.faces == m.faces
    rng = random.Random(11)
    verts = [(rng.random(), rng.uniform(-1e9, 1e9), rng.randint(-5, 5)) for _ in range(20)]
    faces = [tuple(rng.sample(range(20), 3)) for _ in range(15)]
    m3 = read_off(IndexedFaceSet(verts, faces).to_off())
    assert m3.vertices == verts and m3.faces == faces


def test_against_brute_force_random():
    rng = random.Random(2024)
    for _ in range(600):
        n = rng.randint(3, 9)
        verts, faces = rand_mesh(rng, n, rng.randint(1, 10))
        m = IndexedFaceSet(verts, faces)
        for u in range(n):
            for v in range(n):
                if u != v:
                    assert sorted(m.edge_faces(u, v)) == sorted(brute_edge_faces(faces, u, v))
            assert m.vertex_faces(u) == brute_vertex_faces(faces, u)
        for f in range(len(faces)):
            got = m.face_neighbors(f)
            assert len(got) == len(set(got)) and set(got) == brute_neighbors(faces, f)
        edges = brute_edge_set(faces)
        counts = {e: sum(1 for face in faces for x in scan_edges(face) if frozenset(x) == e) for e in edges}
        assert {frozenset(e) for e in m.boundary_edges()} == {e for e, c in counts.items() if c == 1}
        assert {frozenset(e) for e in m.non_manifold_edges()} == {e for e, c in counts.items() if c >= 3}
        assert m.euler_characteristic() == n - len(edges) + len(faces)
        assert read_off(m.to_off()).faces == m.faces
