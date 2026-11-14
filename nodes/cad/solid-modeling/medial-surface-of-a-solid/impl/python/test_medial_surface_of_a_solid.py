# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/medial-surface-of-a-solid/. The authors are listed in prov/B7FYY7.jsonl.

import itertools
import random
import unittest
from fractions import Fraction as Fr

from medial_surface_of_a_solid import (ConvexPolyhedron, cross, dot, in_convex_hull_planar, medial_seams,
                                       sheet_points, sub)

AXES = [((1, 0, 0), 1), ((-1, 0, 0), 1), ((0, 1, 0), 1), ((0, -1, 0), 1), ((0, 0, 1), 1), ((0, 0, -1), 1)]


def rational_unit_normals():
    """Unit vectors with rational coordinates from Pythagorean quadruples."""
    out = set()
    for (a, b, c), d in [((1, 2, 2), 3), ((2, 3, 6), 7), ((1, 4, 8), 9), ((4, 4, 7), 9), ((2, 6, 9), 11),
                         ((6, 6, 7), 11)]:
        for p in itertools.permutations((a, b, c)):
            for s in itertools.product((1, -1), repeat=3):
                out.add(tuple(Fr(s[k] * p[k], d) for k in range(3)))
    return sorted(out)


NORMALS = rational_unit_normals()


def box(a, b, c):
    return ConvexPolyhedron([((1, 0, 0), a), ((-1, 0, 0), 0), ((0, 1, 0), b), ((0, -1, 0), 0),
                             ((0, 0, 1), c), ((0, 0, -1), 0)])


def random_polyhedron(rng):
    planes = [(n, Fr(rng.randrange(6, 13), 3)) for n, _ in AXES]
    for n in rng.sample(NORMALS, rng.randrange(2, 7)):
        planes.append((n, Fr(rng.randrange(3, 10), 3)))
    return ConvexPolyhedron(planes)


def solve(rows, rhs):
    """Gaussian elimination over Fractions; None if singular."""
    m = [list(r) + [v] for r, v in zip(rows, rhs)]
    k = len(m)
    for c in range(k):
        p = next((r for r in range(c, k) if m[r][c] != 0), None)
        if p is None:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[r][k] / m[r][r] for r in range(k)]


def brute_junctions(P):
    """Every interior point where four faces with independent equations tie
    for nearest: solve b_l - n_l . x = rho for each 4-subset."""
    out = set()
    for quad in itertools.combinations(P.faces, 4):
        s = solve([list(P.planes[l][0]) + [Fr(1)] for l in quad], [P.planes[l][1] for l in quad])
        if s is None:
            continue
        x, rho = (s[0], s[1], s[2]), s[3]
        if rho > 0 and P.inside(x) and set(quad) <= P.nearest(x)[1]:
            out.add(x)
    return out


def brute_seam_interval(P, i, j, k):
    """The parameter interval on the line equidistant from faces i, j, k on
    which all three are nearest, by checking each other face in turn."""
    ni, nj, nk = (P.planes[l][0] for l in (i, j, k))
    w = cross(sub(ni, nj), sub(ni, nk))
    x0 = solve([list(sub(ni, nj)), list(sub(ni, nk)), list(w)],
               [P.planes[i][1] - P.planes[j][1], P.planes[i][1] - P.planes[k][1], Fr(0)])
    x0 = tuple(x0)
    lo, hi = None, None
    # constraints of the form a + t c >= 0
    cons = [(P.dist(i, x0), -dot(ni, w))]
    for l in P.faces:
        cons.append((P.dist(l, x0) - P.dist(i, x0), -dot(P.planes[l][0], w) + dot(ni, w)))
    for a, c in cons:
        if c == 0:
            if a < 0:
                return None
        elif c > 0:
            t = -a / c
            lo = t if lo is None else max(lo, t)
        else:
            t = -a / c
            hi = t if hi is None else min(hi, t)
    if lo is None or hi is None or lo >= hi:
        return None
    return x0, w, lo, hi


def param(x0, w, y):
    return dot(sub(y, x0), w) / dot(w, w)


class TestHandCases(unittest.TestCase):
    def test_cube(self):
        P = box(2, 2, 2)
        J, S = medial_seams(P)
        inner = {x: v for x, v in J.items() if v[0] > 0}
        self.assertEqual(list(inner), [(1, 1, 1)])
        self.assertEqual(inner[(1, 1, 1)], (1, frozenset(range(6))))
        self.assertEqual(len(S), 8)
        self.assertTrue(all(len(s[2]) == 3 for s in S))

    def test_long_box(self):
        P = box(4, 2, 2)
        J, S = medial_seams(P)
        inner = sorted(x for x, v in J.items() if v[0] > 0)
        self.assertEqual(inner, [(1, 1, 1), (3, 1, 1)])
        self.assertEqual(len(S), 9)
        mid = [s for s in S if len(s[2]) == 4]
        self.assertEqual(len(mid), 1)
        self.assertEqual(mid[0][2], frozenset({2, 3, 4, 5}))

    def test_sheet_of_cube(self):
        P = box(2, 2, 2)
        J, _ = medial_seams(P)
        # the sheet of faces x = 2 and y = 2 is the triangle (2,2,0), (2,2,2), (1,1,1)
        self.assertEqual(sheet_points(J, 0, 2), sorted([(2, 2, 0), (2, 2, 2), (1, 1, 1)]))


class TestRandom(unittest.TestCase):
    def test_seams_are_equidistant(self):
        """Every rational point inside a traced seam has exactly the seam's
        faces as nearest, and they number three or more."""
        rng = random.Random(1)
        checked = 0
        for _ in range(30):
            P = random_polyhedron(rng)
            J, S = medial_seams(P)
            for a, b, faces in S:
                self.assertGreaterEqual(len(faces), 3)
                for _ in range(4):
                    t = Fr(rng.randrange(1, 100), 100)
                    x = tuple(a[q] + t * (b[q] - a[q]) for q in range(3))
                    self.assertTrue(P.inside(x))
                    self.assertEqual(P.nearest(x)[1], faces)
                    checked += 1
            for x, (rho, T) in J.items():
                self.assertEqual(P.nearest(x), (rho, T))
        self.assertGreater(checked, 500)

    def test_junctions_against_brute_force(self):
        rng = random.Random(2)
        for _ in range(18):
            P = random_polyhedron(rng)
            J, _ = medial_seams(P)
            self.assertEqual({x for x, v in J.items() if v[0] > 0}, brute_junctions(P))
            self.assertEqual({x for x, v in J.items() if v[0] == 0}, set(P.vertices))

    def test_seams_against_brute_force(self):
        """For every triple of faces, the traced seams that contain it tile
        exactly the interval of the bisector line where the three are nearest."""
        rng = random.Random(3)
        for _ in range(18):
            P = random_polyhedron(rng)
            _, S = medial_seams(P)
            for tri in itertools.combinations(P.faces, 3):
                got = [s for s in S if set(tri) <= s[2]]
                want = brute_seam_interval(P, *tri)
                if want is None:
                    self.assertEqual(got, [])
                    continue
                x0, w, lo, hi = want
                ivs = sorted(tuple(sorted((param(x0, w, a), param(x0, w, b)))) for a, b, _ in got)
                self.assertTrue(ivs)
                self.assertEqual(ivs[0][0], lo)
                self.assertEqual(ivs[-1][1], hi)
                for p, q in zip(ivs, ivs[1:]):
                    self.assertEqual(p[1], q[0])

    def test_sheets_against_nearest_faces(self):
        """A rational point of the bisector plane of faces i and j is in the
        hull of the traced sheet corners exactly when i and j are nearest."""
        rng = random.Random(4)
        checked = 0
        for _ in range(20):
            P = random_polyhedron(rng)
            J, _ = medial_seams(P)
            for i, j in itertools.combinations(P.faces, 2):
                pts = sheet_points(J, i, j)
                if len(pts) < 3:
                    continue
                m = sub(P.planes[i][0], P.planes[j][0])
                e = next(cross(m, a) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1)) if cross(m, a) != (0, 0, 0))
                f = cross(m, e)
                c = tuple(sum(p[q] for p in pts) / len(pts) for q in range(3))
                for _ in range(6):
                    s, t = Fr(rng.randrange(-40, 41), 20), Fr(rng.randrange(-40, 41), 20)
                    x = tuple(c[q] + s * e[q] + t * f[q] for q in range(3))
                    want = P.inside(x) and {i, j} <= P.nearest(x)[1]
                    self.assertEqual(in_convex_hull_planar(pts, x), want)
                    checked += 1
        self.assertGreater(checked, 500)


if __name__ == "__main__":
    unittest.main()
