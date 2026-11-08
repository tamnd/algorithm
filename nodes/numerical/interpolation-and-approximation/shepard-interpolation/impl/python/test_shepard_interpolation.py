# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shepard-interpolation/. The authors are listed in prov/GAEMZW.jsonl.

import random
import unittest
from fractions import Fraction as F

from shepard_interpolation import shepard, shepard_weights


def rand_set(rng, n, dim):
    pts = [tuple(rng.uniform(-1, 1) for _ in range(dim)) for _ in range(n)]
    vals = [rng.uniform(-5, 5) for _ in range(n)]
    return pts, vals


class TestShepard(unittest.TestCase):
    def test_at_nodes(self):
        rng = random.Random(1)
        for trial in range(50):
            pts, vals = rand_set(rng, rng.randint(1, 30), rng.randint(1, 3))
            for p, v in zip(pts, vals):
                self.assertEqual(shepard(pts, vals, p, 2), v)
                self.assertEqual(shepard(pts, vals, p, 2, radius=0.5), v)

    def test_constants_exact(self):
        rng = random.Random(2)
        for trial in range(40):
            n = rng.randint(1, 12)
            pts = [(F(rng.randint(-20, 20), 7), F(rng.randint(-20, 20), 5))
                   for _ in range(n)]
            vals = [F(3, 4)] * n
            x = (F(rng.randint(-30, 30), 11), F(rng.randint(-30, 30), 13))
            for p in (2, 4, 6):
                self.assertEqual(shepard(pts, vals, x, p), F(3, 4))

    def test_convex_combination(self):
        rng = random.Random(3)
        for trial in range(300):
            pts, vals = rand_set(rng, rng.randint(1, 25), rng.randint(1, 3))
            x = tuple(rng.uniform(-1.5, 1.5) for _ in range(len(pts[0])))
            p = rng.choice([1, 2, 3, 2.5])
            s = shepard(pts, vals, x, p)
            self.assertLessEqual(min(vals) - 1e-12, s)
            self.assertLessEqual(s, max(vals) + 1e-12)
            w = shepard_weights(pts, x, p)
            self.assertAlmostEqual(sum(w), 1.0, places=12)
            self.assertTrue(all(wi >= 0 for wi in w))

    def test_single_node(self):
        for x in [(-3.0,), (0.0,), (0.25,), (7.0,)]:
            self.assertEqual(shepard([(0.25,)], [4.5], x), 4.5)

    def test_two_nodes_exact(self):
        # nodes 0 and 1, values 0 and 1, x = 1/3, p = 2: weights 9 and 9/4
        self.assertEqual(shepard([(F(0),), (F(1),)], [F(0), F(1)], (F(1, 3),)), F(1, 5))
        # midpoint gives the average for any power
        for p in (1, 2, 3, 4):
            self.assertAlmostEqual(shepard([(0.0,), (1.0,)], [2.0, 6.0], (0.5,), p), 4.0)

    def test_linear_data_not_reproduced(self):
        pts = [(F(0),), (F(1),), (F(2),)]
        vals = [F(0), F(1), F(2)]
        self.assertEqual(shepard(pts, vals, (F(1, 2),)), F(11, 19))

    def test_repeated_nodes(self):
        pts = [(F(0),), (F(0),), (F(1),)]
        vals = [F(1), F(3), F(10)]
        self.assertEqual(shepard(pts, vals, (F(0),)), F(2))
        # elsewhere a repeated node counts twice
        x = (F(1, 4),)
        w0 = 1 / F(1, 4) ** 2
        w1 = 1 / F(3, 4) ** 2
        expect = (w0 * 1 + w0 * 3 + w1 * 10) / (2 * w0 + w1)
        self.assertEqual(shepard(pts, vals, x), expect)
        w = shepard_weights(pts, (F(0),))
        self.assertEqual(w, [F(1, 2), F(1, 2), 0])

    def test_flat_spots(self):
        # p = 2: zero slope at nodes; p = 1: a corner with nonzero slope
        pts = [(0.0,), (1.0,), (2.0,)]
        vals = [0.0, 1.0, 4.0]
        for h in (1e-3, 1e-4):
            d2 = abs(shepard(pts, vals, (1.0 + h,), 2) - 1.0) / h
            d1 = abs(shepard(pts, vals, (1.0 + h,), 1) - 1.0) / h
            self.assertLess(d2, 20 * h)
            self.assertGreater(d1, 0.5)

    def test_jump_data(self):
        pts = [(i / 10,) for i in range(-10, 11)]
        vals = [0.0 if p[0] < 0 else 1.0 for p in pts]
        prev = None
        for k in range(-200, 201):
            s = shepard(pts, vals, (k / 200,), 2)
            self.assertTrue(-1e-15 <= s <= 1 + 1e-15)
            if prev is not None:
                self.assertLess(abs(s - prev), 0.2)
            prev = s

    def test_local_version(self):
        rng = random.Random(5)
        for trial in range(100):
            pts, vals = rand_set(rng, 30, 2)
            x = (rng.uniform(-1, 1), rng.uniform(-1, 1))
            R = 0.6
            try:
                s = shepard(pts, vals, x, radius=R)
            except ValueError:
                self.assertTrue(all(sum((a - b) ** 2 for a, b in zip(x, p)) >= R * R for p in pts))
                continue
            far = [i for i, p in enumerate(pts)
                   if sum((a - b) ** 2 for a, b in zip(x, p)) >= R * R]
            vals2 = list(vals)
            for i in far:
                vals2[i] = 1e6
            self.assertAlmostEqual(shepard(pts, vals2, x, radius=R), s, places=9)
            self.assertAlmostEqual(shepard(pts, [2.5] * 30, x, radius=R), 2.5, places=12)

    def test_errors(self):
        with self.assertRaises(ValueError):
            shepard([], [], (0.0,))
        with self.assertRaises(ValueError):
            shepard([(0.0,)], [1.0, 2.0], (0.0,))
        with self.assertRaises(ValueError):
            shepard([(0.0,)], [1.0], (0.5,), p=0)
        with self.assertRaises(ValueError):
            shepard([(0.0,)], [1.0], (5.0,), radius=1.0)


if __name__ == "__main__":
    unittest.main()
