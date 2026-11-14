# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knot-removal-fairing/. The authors are listed in prov/GM71P6.jsonl.

import random
import unittest
from fractions import Fraction as Fr

from knot_removal_fairing import (curvature_sign_changes, fair_by_knot_removal, fairness,
                                  kappa_jump, max_move_squared, remove_and_reinsert)
from si3spline import curve_point, derivative_curve, sub

UNIFORM = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6, 6]
PARABOLA = [(i, Fr((i - 4) ** 2, 4)) for i in range(9)]


def dented():
    c = list(PARABOLA)
    c[4] = (4, Fr(1, 2))
    return c


def third_derivative_sides(knots, ctrl, r):
    d = derivative_curve(*derivative_curve(*derivative_curve(knots, 3, ctrl)))
    t = knots[r]
    return (curve_point(*d, (knots[r - 1] + t) / 2), curve_point(*d, (t + knots[r + 1]) / 2))


def random_curve(rng, uniform):
    n = rng.randint(6, 10)
    m = n - 2
    if uniform:
        inner = list(range(1, m))
    else:
        inner = [Fr(x, 4) for x in sorted(rng.sample(range(1, 4 * m), m - 1))]
    knots = [0] * 4 + inner + [m] * 4
    ctrl = [(Fr(i), Fr((2 * i - n) ** 2, 8)) for i in range(n + 1)]
    return knots, ctrl


def dist2(a, b):
    d = sub(a, b)
    return d[0] * d[0] + d[1] * d[1]


class TestKnotRemovalFairing(unittest.TestCase):
    def test_example(self):
        c = dented()
        self.assertEqual(curvature_sign_changes(UNIFORM, PARABOLA), 0)
        self.assertEqual(curvature_sign_changes(UNIFORM, c), 2)
        self.assertEqual(kappa_jump(UNIFORM, c, 6), 9)
        self.assertEqual(kappa_jump(UNIFORM, PARABOLA, 6), 0)
        new, done = fair_by_knot_removal(UNIFORM, c, tol=1)
        self.assertEqual(done, [6])
        self.assertEqual(new, PARABOLA)
        self.assertEqual(curvature_sign_changes(UNIFORM, new), 0)
        self.assertLess(fairness(UNIFORM, new), fairness(UNIFORM, c))
        self.assertEqual(curve_point(UNIFORM, 3, c, 3), (4, Fr(5, 12)))
        self.assertEqual(curve_point(UNIFORM, 3, new, 3), (4, Fr(1, 12)))
        self.assertEqual(max_move_squared(c, new), Fr(1, 4))

    def test_tight_tolerance_stops_early(self):
        c = dented()
        new, done = fair_by_knot_removal(UNIFORM, c, tol=Fr(1, 4))
        self.assertEqual(done, [5, 7, 6, 5])
        self.assertNotIn(new, (c, PARABOLA))
        self.assertEqual(curvature_sign_changes(UNIFORM, new), 0)
        self.assertLess(fairness(UNIFORM, PARABOLA), fairness(UNIFORM, new))
        self.assertLessEqual(max_move_squared(c, new), Fr(1, 16))
        new0, done0 = fair_by_knot_removal(UNIFORM, c, tol=0)
        self.assertEqual((new0, done0), (c, []))

    def test_one_step_makes_the_knot_removable(self):
        rng = random.Random(3)
        for _ in range(40):
            knots, ctrl = random_curve(rng, uniform=False)
            ctrl = [(x + Fr(rng.randint(-4, 4), 8), y + Fr(rng.randint(-4, 4), 8)) for x, y in ctrl]
            r = rng.randint(4, len(ctrl) - 1)
            new = remove_and_reinsert(knots, ctrl, r)
            changed = [i for i in range(len(ctrl)) if new[i] != ctrl[i]]
            self.assertLessEqual(len(changed), 1)
            if changed:
                self.assertEqual(changed, [r - 2])
            left, right = third_derivative_sides(knots, new, r)
            self.assertEqual(left, right)
            self.assertIn(kappa_jump(knots, new, r), (0, None))

    def test_dents_lose_inflections(self):
        # a dent near the bottom of the parabola, where the curve is flat
        rng = random.Random(7)
        cases = 0
        for _ in range(60):
            knots, ctrl = random_curve(rng, uniform=True)
            n = len(ctrl) - 1
            j = rng.randint(max(3, (n - 2) // 2), min(n - 3, (n + 3) // 2))
            ctrl[j] = (ctrl[j][0], ctrl[j][1] + Fr(rng.randint(2, 6), 8))
            before = curvature_sign_changes(knots, ctrl)
            if before == 0:
                continue
            cases += 1
            new, _ = fair_by_knot_removal(knots, ctrl, tol=1, rounds=12)
            self.assertLess(curvature_sign_changes(knots, new), before)
            self.assertLessEqual(max_move_squared(ctrl, new), 1)
        self.assertGreaterEqual(cases, 10)

    def test_lower_measure_is_not_fewer_inflections(self):
        # a dent on the steep side: the measure drops, the two inflections stay
        knots = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8]
        ctrl = [(Fr(i), Fr((2 * i - 10) ** 2, 8)) for i in range(11)]
        ctrl[3] = (3, Fr(2) + Fr(3, 4))
        new, done = fair_by_knot_removal(knots, ctrl, tol=2)
        self.assertEqual(done, [7])
        self.assertLess(fairness(knots, new), fairness(knots, ctrl))
        self.assertEqual(curvature_sign_changes(knots, ctrl), 2)
        self.assertEqual(curvature_sign_changes(knots, new), 2)

    def test_curve_moves_less_than_the_tolerance(self):
        rng = random.Random(11)
        for _ in range(25):
            knots, ctrl = random_curve(rng, uniform=rng.random() < 0.5)
            ctrl = [(x + Fr(rng.randint(-6, 6), 8), y + Fr(rng.randint(-6, 6), 8)) for x, y in ctrl]
            tol = Fr(rng.randint(1, 8), 8)
            new, done = fair_by_knot_removal(knots, ctrl, tol=tol, rounds=8)
            self.assertEqual(len(new), len(ctrl))
            self.assertLessEqual(max_move_squared(ctrl, new), tol * tol)
            self.assertLessEqual(fairness(knots, new), fairness(knots, ctrl))
            for _ in range(10):
                t = Fr(rng.randint(0, 1000), 1000) * knots[-1]
                self.assertLessEqual(dist2(curve_point(knots, 3, new, t), curve_point(knots, 3, ctrl, t)), tol * tol)

    def test_sign_change_counter(self):
        bezier = [0, 0, 0, 0, 1, 1, 1, 1]
        self.assertEqual(curvature_sign_changes(bezier, [(0, 0), (1, 1), (2, -1), (3, 0)]), 1)
        self.assertEqual(curvature_sign_changes(bezier, [(0, 0), (1, 1), (2, 1), (3, 0)]), 0)
        # random curves: a dense sample never sees more sign changes than the exact count
        rng = random.Random(5)
        for _ in range(30):
            knots, ctrl = random_curve(rng, uniform=False)
            ctrl = [(x, y + Fr(rng.randint(-8, 8), 4)) for x, y in ctrl]
            exact = curvature_sign_changes(knots, ctrl)
            d1 = derivative_curve(knots, 3, ctrl)
            d2 = derivative_curve(*d1)
            signs = []
            for s in range(0, 801):
                t = Fr(s, 800) * knots[-1]
                a, b = curve_point(*d1, t), curve_point(*d2, t)
                f = a[0] * b[1] - a[1] * b[0]
                if f:
                    signs.append(f > 0)
            sampled = sum(1 for x, y in zip(signs, signs[1:]) if x != y)
            self.assertLessEqual(sampled, exact)
            self.assertEqual(exact % 2, (signs[0] != signs[-1]) % 2)

    def test_rejections(self):
        with self.assertRaises(ValueError):
            fair_by_knot_removal(UNIFORM, [(x, y, 0) for x, y in PARABOLA], 1)
        double = [0, 0, 0, 0, 1, 2, 2, 4, 5, 6, 6, 6, 6]
        with self.assertRaises(ValueError):
            fair_by_knot_removal(double, PARABOLA, 1)


if __name__ == "__main__":
    unittest.main()
