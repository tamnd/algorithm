# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parting-line-generation/. The authors are listed in prov/D4D190.jsonl.

import random
import unittest
from fractions import Fraction

from parting_line_generation import face_signs, newell_normal, parting_loops, silhouette_edges

# The square pyramid of the page: base [-1, 1]^2 at z = 0, apex (0, 0, 2).
PYR_V = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (0, 0, 2)]
PYR_F = [[0, 3, 2, 1], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]

BOX_V = [(0, 0, 0), (2, 0, 0), (2, 3, 0), (0, 3, 0), (0, 0, 1), (2, 0, 1), (2, 3, 1), (0, 3, 1)]
BOX_F = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def hull_2d(points):
    """Andrew's monotone chain, strict corners only, counterclockwise."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def strict_corners(poly):
    """Drop the points of a closed polygon that are collinear with their neighbours."""
    out = list(poly)
    changed = True
    while changed and len(out) > 2:
        changed = False
        for i in range(len(out)):
            a, b, c = out[i - 1], out[i], out[(i + 1) % len(out)]
            if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0:
                del out[i]
                changed = True
                break
    return out


def same_cycle(p, q):
    if len(p) != len(q):
        return False
    n = len(p)
    for r in (q, q[::-1]):
        for s in range(n):
            if all(p[i] == r[(i + s) % n] for i in range(n)):
                return True
    return False


def random_convex_polygon(rng, around_origin):
    while True:
        pts = [(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(rng.randint(3, 14))]
        h = hull_2d(pts)
        if len(h) < 3:
            continue
        if around_origin:
            k = len(h)
            if not all((h[(i + 1) % k][0] - h[i][0]) * (0 - h[i][1]) - (h[(i + 1) % k][1] - h[i][1]) * (0 - h[i][0]) > 0 for i in range(k)):
                continue
        return h


def prism(poly, h):
    k = len(poly)
    verts = [(x, y, 0) for x, y in poly] + [(x, y, h) for x, y in poly]
    faces = [list(range(k - 1, -1, -1)), list(range(k, 2 * k))]
    for i in range(k):
        j = (i + 1) % k
        faces.append([i, j, k + j, k + i])
    return verts, faces


def bipyramid(poly, h):
    k = len(poly)
    verts = [(x, y, 0) for x, y in poly] + [(0, 0, h), (0, 0, -h)]
    faces = []
    for i in range(k):
        j = (i + 1) % k
        faces.append([i, j, k])
        faces.append([j, i, k + 1])
    return verts, faces


def terrain(rng, nx, ny, hmax):
    """A closed heightfield block: triangulated top, walls and bottom."""
    def top(i, j):
        return i * (ny + 1) + j

    def bot(i, j):
        return (nx + 1) * (ny + 1) + top(i, j)

    verts = [(i, j, rng.randint(1, hmax)) for i in range(nx + 1) for j in range(ny + 1)]
    verts += [(i, j, 0) for i in range(nx + 1) for j in range(ny + 1)]
    faces = []
    for i in range(nx):
        for j in range(ny):
            a, b, c, e = top(i, j), top(i + 1, j), top(i + 1, j + 1), top(i, j + 1)
            faces += [[a, b, c], [a, c, e]]
            a, b, c, e = bot(i, j), bot(i + 1, j), bot(i + 1, j + 1), bot(i, j + 1)
            faces += [[a, c, b], [a, e, c]]
    quads = []
    for i in range(nx):
        quads.append((bot(i, 0), bot(i + 1, 0), top(i + 1, 0), top(i, 0)))
        quads.append((bot(i + 1, ny), bot(i, ny), top(i, ny), top(i + 1, ny)))
    for j in range(ny):
        quads.append((bot(0, j + 1), bot(0, j), top(0, j), top(0, j + 1)))
        quads.append((bot(nx, j), bot(nx, j + 1), top(nx, j + 1), top(nx, j)))
    for a, b, c, e in quads:
        faces += [[a, b, c], [a, c, e]]
    return verts, faces


def linear_map(rng, verts, faces):
    while True:
        m = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        det = dot(m[0], cross(m[1], m[2]))
        if det != 0:
            break
    nv = [tuple(dot(row, v) for row in m) for v in verts]
    nf = [list(f) if det > 0 else list(reversed(f)) for f in faces]
    return nv, nf


def volume6(verts, faces):
    total = 0
    for f in faces:
        for i in range(1, len(f) - 1):
            total += dot(verts[f[0]], cross(verts[f[i]], verts[f[i + 1]]))
    return total


def brute_signs(verts, faces, d, zero_side):
    """Face signs from the cross product of the first three vertices, in Fraction."""
    out = []
    for f in faces:
        p0, p1, p2 = ([Fraction(c) for c in verts[i]] for i in f[:3])
        n = cross(sub(p1, p0), sub(p2, p0))
        s = dot(n, [Fraction(c) for c in d])
        out.append(1 if s > 0 else -1 if s < 0 else zero_side)
    return out


def brute_silhouette(verts, faces, d, zero_side=-1):
    """Compare every pair of faces: an edge is on the silhouette if its two faces differ in sign."""
    signs = brute_signs(verts, faces, d, zero_side)
    edges = [set(frozenset((f[i], f[(i + 1) % len(f)])) for i in range(len(f))) for f in faces]
    out = set()
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            if signs[i] != signs[j]:
                for e in edges[i] & edges[j]:
                    out.add(tuple(sorted(e)))
    return out


def projection_basis(d):
    axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    e = min(axes, key=lambda a: abs(dot(a, d)))
    a = cross(d, e)
    b = cross(d, a)
    return a, b


class TestPartingLines(unittest.TestCase):
    def check_loops(self, verts, faces, d, zero_side=-1):
        loops = parting_loops(verts, faces, d, zero_side)
        signs = face_signs(verts, faces, d, zero_side)
        upper_half_edges = set()
        for fi, f in enumerate(faces):
            if signs[fi] > 0:
                upper_half_edges |= {(f[i], f[(i + 1) % len(f)]) for i in range(len(f))}
        seen = []
        for loop in loops:
            for i in range(len(loop)):
                h = (loop[i], loop[(i + 1) % len(loop)])
                self.assertIn(h, upper_half_edges)
                seen.append(tuple(sorted(h)))
        expected = brute_silhouette(verts, faces, d, zero_side)
        self.assertEqual(len(seen), len(set(seen)))
        self.assertEqual(set(seen), expected)
        self.assertEqual(silhouette_edges(verts, faces, d, zero_side), expected)
        return loops

    def test_pyramid_trace(self):
        d = (1, 0, 1)
        self.assertEqual([newell_normal(PYR_V, f) for f in PYR_F], [(0, 0, -8), (0, -4, 2), (4, 0, 2), (0, 4, 2), (-4, 0, 2)])
        self.assertEqual(face_signs(PYR_V, PYR_F, d), [-1, 1, 1, 1, -1])
        self.assertEqual(parting_loops(PYR_V, PYR_F, d), [[0, 1, 2, 3, 4]])
        self.check_loops(PYR_V, PYR_F, d)

    def test_box_vertical_faces(self):
        # d = z: the four walls have n . d = 0, and zero_side decides where they go.
        d = (0, 0, 1)
        self.assertEqual(parting_loops(BOX_V, BOX_F, d, -1), [[4, 5, 6, 7]])
        self.assertEqual(parting_loops(BOX_V, BOX_F, d, 1), [[0, 1, 2, 3]])
        self.check_loops(BOX_V, BOX_F, d, -1)
        self.check_loops(BOX_V, BOX_F, d, 1)

    def test_box_tilted(self):
        loops = self.check_loops(BOX_V, BOX_F, (1, 1, 1))
        self.assertEqual(len(loops), 1)
        self.assertEqual(len(loops[0]), 6)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            parting_loops(PYR_V, PYR_F[:-1], (0, 0, 1))
        with self.assertRaises(ValueError):
            face_signs(PYR_V, PYR_F, (0, 0, 1), 0)

    def test_random_convex(self):
        rng = random.Random(20261115)
        done = 0
        while done < 150:
            poly = random_convex_polygon(rng, around_origin=True)
            maker = prism if done % 2 == 0 else bipyramid
            verts, faces = maker(poly, rng.randint(1, 15))
            verts, faces = linear_map(rng, verts, faces)
            self.assertGreater(volume6(verts, faces), 0)
            d = (rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-5, 5))
            if d == (0, 0, 0):
                continue
            if any(dot(newell_normal(verts, f), d) == 0 for f in faces):
                continue  # not in general position; the theorem needs n . d != 0
            loops = self.check_loops(verts, faces, d)
            self.assertEqual(len(loops), 1)
            loop = loops[0]
            self.assertEqual(len(loop), len(set(loop)))
            a, b = projection_basis(d)
            proj = [(dot(a, verts[v]), dot(b, verts[v])) for v in loop]
            hull = hull_2d([(dot(a, v), dot(b, v)) for v in verts])
            self.assertTrue(same_cycle(strict_corners(proj), hull))
            done += 1

    def test_random_terrain(self):
        rng = random.Random(7)
        for trial in range(40):
            verts, faces = terrain(rng, rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6))
            self.assertGreater(volume6(verts, faces), 0)
            d = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(1, 4))
            for zero_side in (-1, 1):
                self.check_loops(verts, faces, d, zero_side)

    def test_flat_terrain_is_one_loop(self):
        # A terrain with a constant height and d = z: the top face set is the upper region.
        rng = random.Random(3)
        verts, faces = terrain(rng, 3, 2, 1)
        loops = self.check_loops(verts, faces, (0, 0, 1))
        self.assertEqual(len(loops), 1)
        self.assertEqual(len(loops[0]), 2 * (3 + 2))


if __name__ == "__main__":
    unittest.main()
