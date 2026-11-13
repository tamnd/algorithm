# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mirtich-polyhedral-mass-properties/. The authors are listed in prov/JVZRYG.jsonl.

import random
import unittest
from fractions import Fraction

from mirtich_polyhedral_mass_properties import mass_properties, volume_integrals


def tetra_sums(faces):
    """Brute force: fan each face into triangles and sum signed tetrahedra with the origin."""
    t0 = Fraction(0)
    t1 = [Fraction(0)] * 3
    t2 = [Fraction(0)] * 3
    tp = [Fraction(0)] * 3
    for face in faces:
        for k in range(1, len(face) - 1):
            a, b, c = face[0], face[k], face[k + 1]
            det = (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
                   + a[2] * (b[0] * c[1] - b[1] * c[0]))
            v = Fraction(det, 6)
            t0 += v
            s = [a[i] + b[i] + c[i] for i in range(3)]
            for i in range(3):
                t1[i] += v * s[i] / 4
                t2[i] += v / 20 * (a[i] * a[i] + b[i] * b[i] + c[i] * c[i] + s[i] * s[i])
            for i in range(3):
                j = (i + 1) % 3
                tp[i] += v / 20 * (a[i] * a[j] + b[i] * b[j] + c[i] * c[j] + s[i] * s[j])
    return t0, tuple(t1), tuple(t2), tuple(tp)


def box(x0, y0, z0, x1, y1, z1):
    v = lambda i, j, k: ((x0, x1)[i], (y0, y1)[j], (z0, z1)[k])
    return [
        [v(0, 0, 0), v(0, 1, 0), v(1, 1, 0), v(1, 0, 0)],
        [v(0, 0, 1), v(1, 0, 1), v(1, 1, 1), v(0, 1, 1)],
        [v(0, 0, 0), v(1, 0, 0), v(1, 0, 1), v(0, 0, 1)],
        [v(0, 1, 0), v(0, 1, 1), v(1, 1, 1), v(1, 1, 0)],
        [v(0, 0, 0), v(0, 0, 1), v(0, 1, 1), v(0, 1, 0)],
        [v(1, 0, 0), v(1, 1, 0), v(1, 1, 1), v(1, 0, 1)],
    ]


def tetra(o, a, b, c):
    return [[o, b, a], [o, a, c], [o, c, b], [a, b, c]]


DIRS = sorted({(x, y) for x in range(-3, 4) for y in range(-3, 4) if (x, y) != (0, 0)},
              key=lambda d: __import__("math").atan2(d[1], d[0]))


def star_prism(rng):
    """A prism over a random star-shaped polygon (often not convex)."""
    while True:
        dirs = sorted(rng.sample(DIRS, rng.randint(3, 8)), key=DIRS.index)
        poly = [(r * dx, r * dy) for (dx, dy), r in zip(dirs, [rng.randint(1, 4) for _ in dirs])]
        area2 = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                    for i in range(len(poly)))
        ok = all(dirs[(i + 1) % len(dirs)][0] * dirs[i][1] - dirs[(i + 1) % len(dirs)][1] * dirs[i][0] < 0
                 for i in range(len(dirs)))
        if area2 > 0 and ok:
            break
    h = rng.randint(1, 5)
    bottom = [(x, y, 0) for x, y in reversed(poly)]
    top = [(x, y, h) for x, y in poly]
    sides = []
    k = len(poly)
    for i in range(k):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % k]
        sides.append([(x0, y0, 0), (x1, y1, 0), (x1, y1, h), (x0, y0, h)])
    return [bottom, top] + sides


def transform(faces, m, t):
    f = lambda p: tuple(sum(m[i][j] * p[j] for j in range(3)) + t[i] for i in range(3))
    return [[f(p) for p in face] for face in faces]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


class TestMirtich(unittest.TestCase):
    def test_worked_example(self):
        faces = tetra((0, 0, 0), (2, 0, 0), (0, 3, 0), (0, 0, 4))
        T = volume_integrals(faces)
        self.assertEqual(T.t0, 4)
        self.assertEqual(T.t1, (2, 3, 4))
        mp = mass_properties(faces)
        self.assertEqual(mp.center, (Fraction(1, 2), Fraction(3, 4), Fraction(1)))
        self.assertEqual(tuple(T), tuple(tetra_sums(faces)))

    def test_unit_cube(self):
        mp = mass_properties(box(0, 0, 0, 1, 1, 1))
        self.assertEqual(mp.mass, 1)
        self.assertEqual(mp.center, (Fraction(1, 2),) * 3)
        z, s = Fraction(0), Fraction(1, 6)
        self.assertEqual(mp.inertia, ((s, z, z), (z, s, z), (z, z, s)))

    def test_box_density(self):
        mp = mass_properties(box(1, 2, 3, 4, 4, 4), density=3)
        self.assertEqual(mp.mass, 18)
        self.assertEqual(mp.center, (Fraction(5, 2), Fraction(3), Fraction(7, 2)))
        # I_xx = m (b^2 + c^2) / 12 with a = 3, b = 2, c = 1.
        self.assertEqual(mp.inertia[0][0], Fraction(18 * 5, 12))
        self.assertEqual(mp.inertia[0][1], 0)

    def test_reversed_orientation_negates(self):
        faces = box(0, 0, 0, 2, 3, 5)
        rev = [list(reversed(f)) for f in faces]
        self.assertEqual(volume_integrals(rev).t0, -30)

    def test_zero_volume_raises(self):
        flat = [[(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 0, 0), (0, 1, 0), (1, 0, 0)]]
        with self.assertRaises(ValueError):
            mass_properties(flat)

    def test_random_against_tetrahedra(self):
        rng = random.Random(20261114)
        for trial in range(600):
            kind = trial % 3
            if kind == 0:
                faces = star_prism(rng)
            elif kind == 1:
                x0, y0, z0 = (rng.randint(-5, 5) for _ in range(3))
                faces = box(x0, y0, z0, x0 + rng.randint(1, 4), y0 + rng.randint(1, 4), z0 + rng.randint(1, 4))
            else:
                pts = [tuple(rng.randint(-6, 6) for _ in range(3)) for _ in range(4)]
                o, a, b, c = pts
                d = det3([[a[i] - o[i] for i in range(3)], [b[i] - o[i] for i in range(3)],
                          [c[i] - o[i] for i in range(3)]])
                if d == 0:
                    continue
                faces = tetra(o, a, b, c) if d > 0 else tetra(o, b, a, c)
            while True:
                m = [[rng.randint(-2, 2) for _ in range(3)] for _ in range(3)]
                if det3(m) > 0:
                    break
            t = [Fraction(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(3)]
            faces = transform(faces, m, t)
            T = volume_integrals(faces)
            self.assertEqual(tuple(T), tuple(tetra_sums(faces)))
            self.assertGreater(T.t0, 0)


if __name__ == "__main__":
    unittest.main()
