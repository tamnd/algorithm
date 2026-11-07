# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graeffe-method/. The authors are listed in prov/4YAGDA.jsonl.

import math
import random
import unittest
from decimal import Decimal

from graeffe_method import graeffe, square_step


def poly(roots):
    c = [1.0]
    for r in roots:
        c = [x - r * y for x, y in zip(c + [0.0], [0.0] + c)]
    return c


class TestGraeffe(unittest.TestCase):
    def test_square_step_squares_roots(self):
        b = square_step([Decimal(x) for x in poly([1, 2, 3])])
        self.assertEqual(b, [Decimal(1), Decimal(-14), Decimal(49), Decimal(-36)])
        b = square_step(b)
        self.assertEqual(b, [Decimal(1), Decimal(-98), Decimal(1393), Decimal(-1296)])

    def test_example_converges(self):
        r = graeffe(poly([1, 2, 3]))
        self.assertEqual(r.status, "separated")
        self.assertEqual(r.steps, 8)
        for x, y in zip(r.roots, [3.0, 2.0, 1.0]):
            self.assertAlmostEqual(x, y, delta=1e-14)

    def test_signs_of_real_roots(self):
        r = graeffe(poly([1, -2, 3, -4.5]))
        for x, y in zip(sorted(r.roots), [-4.5, -2.0, 1.0, 3.0]):
            self.assertAlmostEqual(x, y, delta=1e-14)

    def test_quadratic_convergence_of_deviation(self):
        # the deviation (-1)^j c_j / b_j^2 - 1 roughly squares at every step
        b = [Decimal(x) for x in poly([1, 2, 3])]
        devs = []
        for _ in range(6):
            c = square_step(b)
            devs.append(abs(float(c[2] / (b[2] * b[2])) - 1))  # j = 2 is even
            b = c
        ratios = [math.log(devs[k + 1]) / math.log(devs[k]) for k in range(3, 5)]
        for q in ratios:
            self.assertGreater(q, 1.8)
            self.assertLess(q, 3.0)

    def test_complex_pair_gives_group(self):
        r = graeffe([1, 0, 3, 6, 10])  # roots -1 +- i and 1 +- 2i
        self.assertEqual(r.status, "max-iter")
        self.assertEqual(len(r.groups), 2)
        self.assertAlmostEqual(r.groups[0][0], math.sqrt(5), delta=1e-14)
        self.assertAlmostEqual(r.groups[1][0], math.sqrt(2), delta=1e-14)
        self.assertEqual([g[1] for g in r.groups], [2, 2])
        self.assertEqual(r.roots, [])

    def test_no_real_root(self):
        r = graeffe([1, 0, 1])
        self.assertEqual(r.groups, [(1.0, 2)])
        self.assertEqual(r.roots, [])

    def test_opposite_roots_and_multiple_roots(self):
        self.assertEqual(graeffe([1, 0, -4]).groups, [(2.0, 2)])
        for m in (2, 3, 4):
            r = graeffe(poly([1.5] * m + [0.5]))
            self.assertEqual([g[1] for g in r.groups], [m, 1])
            self.assertAlmostEqual(r.groups[0][0], 1.5, delta=1e-14)
            self.assertAlmostEqual(r.roots[0], 0.5, delta=1e-15)

    def test_root_exactly_zero(self):
        r = graeffe(poly([1, -2, 3, 0, 0]))
        self.assertEqual(r.groups[-1], (0.0, 2))
        for x, y in zip(sorted(r.roots), [-2.0, 0.0, 0.0, 1.0, 3.0]):
            self.assertAlmostEqual(x, y, delta=1e-14)

    def test_close_moduli(self):
        r = graeffe(poly([1.0, 1.01]))
        self.assertEqual(r.status, "separated")
        self.assertAlmostEqual(r.roots[0], 1.01, delta=1e-12)
        self.assertAlmostEqual(r.roots[1], 1.0, delta=1e-12)

    def test_max_iter(self):
        r = graeffe(poly([1, 2, 3]), max_iter=3)
        self.assertEqual(r.status, "max-iter")
        self.assertEqual(r.steps, 3)
        self.assertEqual(r.groups[0][1], 3)  # not yet separated: one group

    def test_wilkinson_20(self):
        r = graeffe(poly(range(1, 21)))
        self.assertEqual(r.status, "separated")
        self.assertEqual(r.steps, 11)
        err = max(abs(x - k) / k for x, k in zip(sorted(r.roots), range(1, 21)))
        self.assertLess(err, 1e-4)  # the rounded coefficients move the roots this much

    def test_degenerate_inputs(self):
        self.assertEqual(graeffe([0, 0, 2, -4]).roots, [2.0])
        self.assertEqual(graeffe([5]).groups, [])
        with self.assertRaises(ValueError):
            graeffe([0, 0])
        with self.assertRaises(ValueError):
            graeffe([1, float("nan"), 1])
        with self.assertRaises(ValueError):
            graeffe([1, float("inf")])

    def test_random_distinct_moduli(self):
        rng = random.Random(20240601)
        worst, steps = 0.0, 0
        for _ in range(500):
            n = rng.randint(1, 10)
            while True:
                mods = sorted(rng.uniform(0.1, 10) for _ in range(n))
                if all(mods[i + 1] / mods[i] > 1.05 for i in range(n - 1)):
                    break
            roots = [m * rng.choice([-1, 1]) for m in mods]
            r = graeffe(poly(roots))
            self.assertEqual(r.status, "separated")
            self.assertEqual(len(r.roots), n)
            steps += r.steps
            for x, y in zip(sorted(r.roots), sorted(roots)):
                worst = max(worst, abs(x - y) / abs(y))
        self.assertLess(worst, 1e-9)
        self.assertLess(steps / 500, 12)


if __name__ == "__main__":
    unittest.main()
