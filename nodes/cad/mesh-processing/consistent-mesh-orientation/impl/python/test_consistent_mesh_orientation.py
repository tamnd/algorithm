# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-mesh-orientation/. The authors are listed in prov/A5KM8D.jsonl.

import itertools
import random
from fractions import Fraction

from consistent_mesh_orientation import orient

# ---- brute force: try every vector of flips ----


def directed_ok(faces):
    seen = set()
    for f in faces:
        for i in range(len(f)):
            e = (f[i], f[(i + 1) % len(f)])
            if e in seen:
                return False
            seen.add(e)
    return True


def brute_components(faces):
    comp = list(range(len(faces)))

    def find(x):
        while comp[x] != x:
            x = comp[x]
        return x

    def edges(f):
        return {frozenset((f[i], f[(i + 1) % len(f)])) for i in range(len(f))}

    for i, j in itertools.combinations(range(len(faces)), 2):
        if edges(faces[i]) & edges(faces[j]):
            comp[find(i)] = find(j)
    groups = {}
    for i in range(len(faces)):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def brute_consistent_flips(faces, members):
    out = []
    for bits in itertools.product((0, 1), repeat=len(members)):
        sub = [faces[f][::-1] if b else faces[f] for f, b in zip(members, bits)]
        if directed_ok(sub):
            out.append(bits)
    return out


def outward_on_convex(points, face, centre):
    """For a convex polytope: the right-hand normal points away from an interior point."""
    a, b, c = (points[v] for v in face[:3])
    u = [b[k] - a[k] for k in range(3)]
    w = [c[k] - a[k] for k in range(3)]
    n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
    return sum(n[k] * (a[k] - centre[k]) for k in range(3)) > 0


# ---- shapes (faces oriented outward for the given points) ----


def tetra(rng):
    while True:
        pts = [tuple(rng.randint(-5, 5) for _ in range(3)) for _ in range(4)]
        faces = [(0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2)]
        a, b, c, d = pts
        det = sum(
            (b[i] - a[i]) * ((c[(i + 1) % 3] - a[(i + 1) % 3]) * (d[(i + 2) % 3] - a[(i + 2) % 3])
                             - (c[(i + 2) % 3] - a[(i + 2) % 3]) * (d[(i + 1) % 3] - a[(i + 1) % 3]))
            for i in range(3))
        if det != 0:
            return pts, faces, True


def octahedron(rng):
    a, b, c = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5)
    pts = [(0, 0, c), (0, 0, -c), (a, 0, 0), (0, b, 0), (-a, 0, 0), (0, -b, 0)]
    eq = [2, 3, 4, 5]
    faces = []
    for i in range(4):
        x, y = eq[i], eq[(i + 1) % 4]
        faces += [(0, x, y), (1, y, x)]
    return pts, faces, True


def cube(rng):
    s = rng.randint(1, 4)
    pts = [(x * s, y * s, z * s) for z in (0, 1) for y in (0, 1) for x in (0, 1)]
    # index = x + 2y + 4z
    faces = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (1, 3, 7, 5), (3, 2, 6, 7), (2, 0, 4, 6)]
    return pts, faces, True


def bipyramid(rng):
    h, k = rng.randint(1, 5), rng.randint(1, 5)
    pts = [(3, 0, 0), (-2, 2, 0), (-2, -2, 0), (0, 0, h), (0, 0, -k)]
    faces = [(0, 1, 3), (1, 2, 3), (2, 0, 3), (1, 0, 4), (2, 1, 4), (0, 2, 4)]
    return pts, faces, True


def moebius(rng):
    return None, [(i, (i + 1) % 5, (i + 2) % 5) for i in range(5)], False


def disk(rng):
    faces = []
    for i in range(2):
        for j in range(2):
            p, q, r, s = 3 * i + j, 3 * (i + 1) + j, 3 * (i + 1) + j + 1, 3 * i + j + 1
            faces += [(p, q, r), (p, r, s)]
    return None, faces, False


SHAPES = [tetra, octahedron, cube, bipyramid, moebius, disk]


def scramble(rng, faces):
    out = []
    for f in faces:
        k = rng.randrange(len(f))
        f = f[k:] + f[:k]
        out.append(f[::-1] if rng.random() < 0.5 else f)
    return out


def make_case(rng):
    parts = rng.sample(SHAPES, rng.choice((1, 1, 2)))
    pts_all, faces_all, convex_parts, base = [], [], [], 0
    for shape in parts:
        pts, faces, convex = shape(rng)
        nv = max(max(f) for f in faces) + 1
        shift = (100 * len(convex_parts), 0, 0)
        pts = pts or [(0, 0, 0)] * nv
        pts_all += [tuple(p[k] + shift[k] for k in range(3)) for p in pts]
        faces_all += [tuple(v + base for v in f) for f in faces]
        if convex:
            centre = tuple(Fraction(sum(p[k] for p in pts), len(pts)) + shift[k] for k in range(3))
            convex_parts.append((set(range(len(faces_all) - len(faces), len(faces_all))), centre))
        base += nv
    return pts_all, scramble(rng, faces_all), convex_parts


# ---- tests ----


def test_page_example():
    # a square of two triangles, the second one flipped
    r = orient([(0, 1, 2), (0, 3, 2)])
    assert r.faces == [(0, 1, 2), (2, 3, 0)] and r.flipped == [False, True]
    assert r.orientable == [True] and r.closed == [False]
    pts = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    r = orient([(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)], pts)  # every face points in some way
    assert directed_ok(r.faces) and r.volume6 == [1]
    assert r.faces == [(2, 1, 0), (0, 1, 3), (1, 2, 3), (3, 2, 0)]


def test_moebius_is_not_orientable():
    r = orient([(i, (i + 1) % 5, (i + 2) % 5) for i in range(5)])
    assert r.orientable == [False] and r.closed == [False]


def test_three_faces_on_an_edge_is_rejected():
    try:
        orient([(0, 1, 2), (1, 0, 3), (0, 1, 4)])
    except ValueError:
        return
    raise AssertionError("accepted a non-manifold edge")


def test_against_brute_force_random():
    rng = random.Random(1880)
    for _ in range(600):
        pts, faces, convex_parts = make_case(rng)
        r = orient(faces, pts)
        for members in brute_components(faces):
            cid = r.component[members[0]]
            assert all(r.component[f] == cid for f in members)
            assert sum(1 for c in r.component if c == cid) == len(members)
            flips = brute_consistent_flips(faces, members)
            assert r.orientable[cid] == bool(flips)
            if flips:
                assert len(flips) == 2  # one orientation and its reverse
                got = tuple(int(r.flipped[f]) for f in members)
                assert got in flips
        for face_set, centre in convex_parts:
            for f in face_set:
                assert outward_on_convex(pts, r.faces[f], centre)


def test_large_torus():
    rng = random.Random(5)
    a, b = 6, 7
    faces = []
    for i in range(a):
        for j in range(b):
            p, q = i * b + j, ((i + 1) % a) * b + j
            r_, s = ((i + 1) % a) * b + (j + 1) % b, i * b + (j + 1) % b
            faces += [(p, q, r_), (p, r_, s)]
    res = orient(scramble(rng, faces))
    assert res.orientable == [True] and res.closed == [True]
    assert directed_ok(res.faces)
