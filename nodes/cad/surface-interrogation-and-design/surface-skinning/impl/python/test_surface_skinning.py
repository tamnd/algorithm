# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-skinning/. The authors are listed in prov/5J15FM.jsonl.

import random
import unittest
from fractions import Fraction as Fr

from si3spline import curve_point, iso_curve_v, refine, surface_point
from surface_skinning import chord_parameters, surface_skinning

H = [0, 0, 0, Fr(1, 2), 1, 1, 1]
B = [0, 0, 0, 1, 1, 1]
C0 = (B, [(0, 0, 0), (1, 0, 0), (2, 0, 0)])
C1 = (H, [(0, 1, 0), (Fr(1, 2), 1, 2), (Fr(3, 2), 1, 0), (2, 1, 0)])
C2 = (B, [(0, 2, 1), (1, 2, 1), (2, 2, 1)])


def random_section(rng, p, y):
    """A random B-spline section of degree p near the plane y = const."""
    n = p + rng.randint(0, 4)
    inner = sorted(Fr(rng.randint(1, 19), 20) for _ in range(n - p))
    while any(inner.count(t) > p for t in inner):
        inner = sorted(Fr(rng.randint(1, 19), 20) for _ in range(n - p))
    knots = [Fr(0)] * (p + 1) + inner + [Fr(1)] * (p + 1)
    ctrl = [(Fr(rng.randint(-20, 20), 4), Fr(y) + Fr(rng.randint(-2, 2), 8), Fr(rng.randint(-20, 20), 4))
            for _ in range(n + 1)]
    return knots, ctrl


class TestSurfaceSkinning(unittest.TestCase):
    def assert_interpolates(self, sections, S, rng):
        U, V, p, q, P = S
        k = len(sections) - 1
        vs = self.params
        for (kn, ctrl), v in zip(sections, vs):
            # the iso-curve at v_k and the section on the same knots: equal nets
            self.assertEqual(iso_curve_v(V, q, P, v), refine(kn, p, ctrl, U)[1])
            t = Fr(rng.randint(0, 1000), 1000)
            self.assertEqual(surface_point(U, V, p, q, P, t, v), curve_point(kn, p, ctrl, t))
        self.assertEqual(len(vs), k + 1)

    def skin(self, sections, q=3, vs=None):
        S = surface_skinning(sections, q, vs)
        if vs is None:
            U, _, p, _, _ = S
            vs = chord_parameters([refine(kn, p, c, U)[1] for kn, c in sections])
        self.params = vs
        return S

    def test_example(self):
        S = self.skin([C0, C1, C2], q=2, vs=[Fr(0), Fr(1, 2), Fr(1)])
        U, V, p, q, P = S
        self.assertEqual((U, V, p, q), (H, B, 2, 2))
        middle = [row[1] for row in P]
        self.assertEqual(middle, [(0, 1, Fr(-1, 2)), (Fr(1, 2), 1, Fr(7, 2)),
                                  (Fr(3, 2), 1, Fr(-1, 2)), (2, 1, Fr(-1, 2))])
        self.assertEqual(surface_point(*S, Fr(1, 4), Fr(1, 2)), (Fr(1, 2), 1, Fr(5, 4)))
        self.assertEqual(surface_point(*S, Fr(1, 4), Fr(1, 4)), (Fr(1, 2), Fr(1, 2), Fr(13, 16)))
        self.assert_interpolates([C0, C1, C2], S, random.Random(1))

    def test_example_chord_parameters(self):
        S = self.skin([C0, C1, C2], q=2)
        v1 = float(self.params[1])
        expected = (3 / (1 + 2 ** 0.5) + 5 ** 0.5 / (5 ** 0.5 + 2 ** 0.5)) / 4
        self.assertAlmostEqual(v1, expected, places=12)
        self.assert_interpolates([C0, C1, C2], S, random.Random(2))

    def test_random_sections_are_interpolated(self):
        rng = random.Random(11)
        for trial in range(15):
            p = rng.randint(1, 3)
            K = rng.randint(1, 5)
            sections = [random_section(rng, p, 3 * k) for k in range(K + 1)]
            q = rng.randint(1, 3)
            if trial % 2:
                vs = sorted(rng.sample([Fr(j, 30) for j in range(1, 30)], K - 1)) if K > 1 else []
                vs = [Fr(0)] + vs + [Fr(1)]
                S = self.skin(sections, q, vs)
            else:
                S = self.skin(sections, q)
            self.assertEqual(S[3], min(q, K))
            self.assert_interpolates(sections, S, rng)

    def test_two_sections_give_a_ruled_surface(self):
        S = self.skin([C0, C2], q=3, vs=[Fr(0), Fr(1)])
        self.assertEqual(S[3], 1)
        u, v = Fr(1, 3), Fr(2, 5)
        a = curve_point(C0[0], 2, C0[1], u)
        b = curve_point(C2[0], 2, C2[1], u)
        self.assertEqual(surface_point(*S, u, v), tuple((1 - v) * x + v * y for x, y in zip(a, b)))

    def test_rejections(self):
        with self.assertRaises(ValueError):
            surface_skinning([C0, C0, C2], 2)            # equal sections: parameters do not increase
        with self.assertRaises(ValueError):
            surface_skinning([C0, ([0, 0, 1, 1], [(0, 0, 0), (1, 1, 1)])], 1)   # two degrees
        with self.assertRaises(ValueError):
            surface_skinning([C0], 1)


if __name__ == "__main__":
    unittest.main()
