# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/back-face-culling/. The authors are listed in prov/CT7W19.jsonl.

import random
from fractions import Fraction

from back_face_culling import back_face_cull

W, H = 6, 5
BOX = ((-1, 7), (-1, 6), (-9, -1))


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def hit(tri, e, s):
    """Parameter t > 0 where the ray e + t (s - e) meets the closed triangle, by Cramer's rule."""
    a, b, c = tri
    d = [-(s[k] - e[k]) for k in range(3)]
    e1 = [b[k] - a[k] for k in range(3)]
    e2 = [c[k] - a[k] for k in range(3)]
    r = [e[k] - a[k] for k in range(3)]
    m = det3(e1, e2, d)
    if m == 0:
        return None
    u, v, t = Fraction(det3(r, e2, d), m), Fraction(det3(e1, r, d), m), Fraction(det3(e1, e2, r), m)
    return t if u >= 0 and v >= 0 and u + v <= 1 and t > 0 else None


def nearest(faces, idx, e, s):
    ts = [t for k in idx if (t := hit(faces[k], e, s)) is not None]
    return min(ts) if ts else None


def outward(tri, inner):
    """Order the triangle so that its normal points away from the point `inner`."""
    a, b, c = tri
    n = [(b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1]),
         (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2]),
         (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])]
    side = sum(n[k] * (inner[k] - a[k]) for k in range(3))
    assert side != 0
    return [a, b, c] if side < 0 else [a, c, b]


def tetrahedron(rng, xlo=0, xhi=6):
    while True:
        p = [(rng.randint(xlo, xhi), rng.randint(0, 5), rng.randint(-8, -2)) for _ in range(4)]
        if det3([p[1][k] - p[0][k] for k in range(3)], [p[2][k] - p[0][k] for k in range(3)],
                [p[3][k] - p[0][k] for k in range(3)]) != 0:
            return [outward([p[a] for a in range(4) if a != o], p[o]) for o in range(4)]


def scene(rng, case):
    """A convex tetrahedron, a star-shaped octahedron, or two disjoint tetrahedra."""
    kind = case % 3
    if kind == 0:
        return tetrahedron(rng), True
    if kind == 1:
        return star(rng, (Fraction(3), Fraction(5, 2), Fraction(-5))), False
    return tetrahedron(rng, 0, 2) + tetrahedron(rng, 4, 6), False


def star(rng, c):
    """A closed octahedron that is star shaped about c, convex or not."""
    r = [Fraction(rng.randint(2, 6), 2) for _ in range(6)]
    tips = {}
    for axis in range(3):
        for sgn, ri in ((1, r[2 * axis]), (-1, r[2 * axis + 1])):
            p = list(c)
            p[axis] += sgn * ri
            tips[(axis, sgn)] = tuple(p)
    return [outward([tips[(0, sx)], tips[(1, sy)], tips[(2, sz)]], c)
            for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]


def eye_outside(rng):
    while True:
        e = tuple(Fraction(rng.randint(-60, 60), 4) for _ in range(3))
        if not all(lo <= e[k] <= hi for k, (lo, hi) in enumerate(BOX)):
            return e


def pixels():
    return [(Fraction(2 * i + 1, 2), Fraction(2 * j + 1, 2), Fraction(0)) for j in range(H) for i in range(W)]


def targets(rng, n):
    return [tuple(Fraction(rng.randint(4 * lo, 4 * hi), 4) for lo, hi in BOX) for _ in range(n)]


def centroid(tri):
    return tuple(Fraction(sum(p[k] for p in tri), 3) for k in range(3))


def visible_point(faces, k, e):
    """Is the centroid of face k seen from e? No face meets the open segment from e first."""
    g = centroid(faces[k])
    for q, tri in enumerate(faces):
        if q != k:
            t = hit(tri, e, g)
            if t is not None and t < 1:
                return False
    a, b, c = faces[k]
    n = [(b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1]),
         (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2]),
         (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])]
    return sum(n[m] * (e[m] - a[m]) for m in range(3)) != 0  # an edge-on face is not seen


def test_worked_example():
    # The unit cube [0, 2]^3 as 12 outward triangles, seen from E = (5, 1, 4).
    cube = []
    c = (1, 1, 1)
    for axis in range(3):
        for val in (0, 2):
            q = [[0, 0], [2, 0], [2, 2], [0, 2]]
            pts = []
            for u, v in q:
                p = [0, 0, 0]
                p[axis] = val
                p[(axis + 1) % 3], p[(axis + 2) % 3] = u, v
                pts.append(tuple(p))
            cube.append(outward([pts[0], pts[1], pts[2]], c))
            cube.append(outward([pts[0], pts[2], pts[3]], c))
    # Order of the sides: x = 0, x = 2, y = 0, y = 2, z = 0, z = 2, two triangles each.
    # Only the sides x = 2 and z = 2 have the viewer on their outer side.
    assert back_face_cull(cube, (5, 1, 4)) == [2, 3, 10, 11]
    # From E = (5, 1, 1), between the planes z = 0 and z = 2, only the side x = 2 is kept.
    assert back_face_cull(cube, (5, 1, 1)) == [2, 3]
    # From E = (5, 2, 1) the side y = 2 is edge on (E is in its plane) and is culled.
    assert back_face_cull(cube, (5, 2, 1)) == [2, 3]
    # From a corner direction three sides face the viewer.
    assert back_face_cull(cube, (4, 5, 6)) == [2, 3, 6, 7, 10, 11]


def test_closed_meshes_never_lose_a_visible_face():
    rng = random.Random(31)
    for case in range(500):
        faces, _ = scene(rng, case)
        e = eye_outside(rng)
        kept = back_face_cull(faces, e)
        allf = range(len(faces))
        for s in targets(rng, 12):
            assert nearest(faces, kept, e, s) == nearest(faces, allf, e, s)
        if e[2] > 0:
            for s in pixels():
                assert nearest(faces, kept, e, s) == nearest(faces, allf, e, s)


def test_convex_is_exact_and_nonconvex_is_not():
    rng = random.Random(32)
    extra = 0
    for case in range(500):
        faces, convex = scene(rng, case)
        e = eye_outside(rng)
        kept = set(back_face_cull(faces, e))
        for k in range(len(faces)):
            seen = visible_point(faces, k, e)
            if seen:
                assert k in kept
            elif k in kept:
                assert not convex  # a convex solid has no front face whose centroid is hidden
                extra += 1
    assert extra > 0


def test_eye_inside_culls_visible_faces():
    faces = tetrahedron(random.Random(33))
    inside = tuple(sum(centroid(f)[k] for f in faces) / 4 for k in range(3))
    assert back_face_cull(faces, inside) == []
    assert nearest(faces, range(4), inside, (Fraction(0), Fraction(0), Fraction(0))) is not None


def test_view_direction_test_is_wrong_under_perspective():
    # A face with outward normal (1, 0, 0) at x = 0, seen from E = (3, 1, 2): E - v0 has x = 3 > 0.
    face = [(0, 0, -4), (0, 3, -4), (0, 0, -1)]
    face = outward(face, (-1, 1, -2))
    assert back_face_cull([face], (3, 1, 2)) == [0]
    # The test with the view direction (0, 0, -1) uses only n_z, which is 0 here: it drops the face.
    a, b, c = face
    nz = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    assert not nz > 0
    assert hit(face, (3, 1, 2), (Fraction(1, 2), Fraction(1), Fraction(-2))) is not None


def test_open_surface_loses_a_visible_face():
    tri = [(0, 0, -2), (4, 0, -2), (0, 4, -2)]  # normal (0, 0, 16), up
    assert back_face_cull([tri], (1, 1, 5)) == [0]
    assert back_face_cull([tri], (1, 1, -9)) == []  # seen from below, still visible
    assert hit(tri, (1, 1, -9), (Fraction(1), Fraction(1), Fraction(0))) is not None


def test_edges():
    assert back_face_cull([], (0, 0, 0)) == []
    tri = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    assert back_face_cull([tri], (5, 5, 0)) == []  # edge on
    assert back_face_cull([[(Fraction(0), 0, 0), (1, 0, 0), (0, 1, 0)]], (0, 0, Fraction(1, 3))) == [0]
