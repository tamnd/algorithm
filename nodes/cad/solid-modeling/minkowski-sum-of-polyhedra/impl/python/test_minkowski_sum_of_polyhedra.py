# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minkowski-sum-of-polyhedra/. The authors are listed in prov/EBNP81.jsonl.

import itertools
import random
import unittest

from minkowski_sum_of_polyhedra import (affine_dim, cross, dot, euler_characteristic, facet_normals,
                                         minkowski_sum_convex, sub, support, vertices_of)

DIRS2 = [w for w in itertools.product(range(-2, 3), repeat=3) if w != (0, 0, 0)]
DIRS4 = [w for w in itertools.product(range(-4, 5), repeat=3) if w != (0, 0, 0)]


def random_body(rng, k_lo=4, k_hi=8, r=3):
    while True:
        k = rng.randrange(k_lo, k_hi + 1)
        pts = list({tuple(rng.randrange(-r, r + 1) for _ in range(3)) for _ in range(k)})
        if len(pts) >= 4 and affine_dim(pts) == 3:
            return pts


def rank(vs):
    vs = [v for v in vs if v != (0, 0, 0)]
    if not vs:
        return 0
    a = vs[0]
    b = next((v for v in vs if cross(a, v) != (0, 0, 0)), None)
    if b is None:
        return 1
    n = cross(a, b)
    return 3 if any(dot(n, v) != 0 for v in vs) else 2


class TestHandCases(unittest.TestCase):
    def test_tetrahedron_plus_its_reflection(self):
        t = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        s = minkowski_sum_convex(t, [(-a, -b, -c) for a, b, c in t])
        self.assertEqual(len(s), 14)                       # cuboctahedron
        self.assertEqual(sorted(len(c) for c in s.values()), [3] * 8 + [4] * 6)
        self.assertEqual(len(vertices_of(s)), 12)

    def test_cube_plus_octahedron(self):
        c = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
        o = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        s = minkowski_sum_convex(c, o)
        self.assertEqual(len(s), 26)
        self.assertEqual(len(vertices_of(s)), 24)
        self.assertEqual(euler_characteristic(s), 2)

    def test_cube_plus_cube(self):
        c = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
        s = minkowski_sum_convex(c, c)
        self.assertEqual(len(s), 6)
        self.assertEqual(vertices_of(s), {(x, y, z) for x in (0, 2) for y in (0, 2) for z in (0, 2)})


class TestRandom(unittest.TestCase):
    def check_facets(self, P, Q, s):
        verts = vertices_of(s)
        for u, cyc in s.items():
            h = support(P, u) + support(Q, u)
            on = {v for v in verts if dot(u, v) == h}
            self.assertTrue(all(dot(u, v) <= h for v in verts))
            self.assertEqual(on, set(cyc))
            self.assertGreaterEqual(len(cyc), 3)
            for i in range(len(cyc)):
                a, b, c = cyc[i], cyc[(i + 1) % len(cyc)], cyc[(i + 2) % len(cyc)]
                n = cross(sub(b, a), sub(c, b))
                # a strict left turn seen from outside: n is a positive multiple of u
                self.assertEqual(cross(n, u), (0, 0, 0))
                self.assertGreater(dot(n, u), 0)

    def test_support_function_adds(self):
        rng = random.Random(1)
        for _ in range(500):
            P, Q = random_body(rng), random_body(rng)
            s = minkowski_sum_convex(P, Q)
            verts = vertices_of(s)
            for w in DIRS2:
                self.assertEqual(max(dot(w, v) for v in verts), support(P, w) + support(Q, w))
            self.check_facets(P, Q, s)
            self.assertEqual(euler_characteristic(s), 2)

    def test_support_function_many_directions(self):
        rng = random.Random(2)
        for _ in range(60):
            P, Q = random_body(rng, 6, 10, 5), random_body(rng, 6, 10, 5)
            s = minkowski_sum_convex(P, Q)
            verts = vertices_of(s)
            for w in DIRS4:
                self.assertEqual(max(dot(w, v) for v in verts), support(P, w) + support(Q, w))

    def test_against_hull_of_vertex_sums(self):
        """Brute force: the facets of the hull of all n m sums, by triples."""
        rng = random.Random(3)
        for _ in range(80):
            P, Q = random_body(rng, 4, 5), random_body(rng, 4, 5)
            s = minkowski_sum_convex(P, Q)
            sums = list({(p[0] + q[0], p[1] + q[1], p[2] + q[2]) for p in P for q in Q})
            normals = facet_normals(sums)
            self.assertEqual(set(s), normals)
            hs = {u: support(sums, u) for u in normals}
            want = {x for x in sums if rank([u for u in normals if dot(u, x) == hs[u]]) == 3}
            self.assertEqual(vertices_of(s), want)

    def test_facet_count_bound(self):
        """The facet bound 4 m n - 9 m - 9 n + 26 of Fogel, Halperin and
        Weibel for summands with m and n facets."""
        rng = random.Random(4)
        for _ in range(300):
            P, Q = random_body(rng), random_body(rng)
            m, n = len(facet_normals(P)), len(facet_normals(Q))
            self.assertLessEqual(len(minkowski_sum_convex(P, Q)), 4 * m * n - 9 * m - 9 * n + 26)


if __name__ == "__main__":
    unittest.main()
