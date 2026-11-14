# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-loop-closure/. The authors are listed in prov/V3P14V.jsonl.

import math
import random
import unittest
from fractions import Fraction

from vector_loop_closure import (
    fourbar_positions,
    fourbar_residual,
    fourbar_velocities,
    freudenstein_k,
    grashof_class,
    input_turns_by_sweep,
    joint_turns_fully,
    slider_crank_positions,
    slider_crank_residual,
    slider_crank_velocity,
)


def closes(lengths):
    """The loop can be assembled with some angles: the longest link is at most the sum of the others."""
    return 2 * max(lengths) <= sum(lengths)


def joint_turns_by_sweep(links, k, steps=720):
    """Sweep the joint between links[k] and links[k + 1] of the cycle (d, a, b, c)."""
    g, i, cpl, o = (links[(k + j) % 4] for j in range(4))
    return input_turns_by_sweep(i, cpl, o, g, steps)


class TestFourBarPositions(unittest.TestCase):
    def test_exact_half_angle_example(self):
        # a = 2, b = 7, c = 5, d = 6 at theta2 = 0: A = -12/5, B = 0, C = 8/5, so t^2 = 2/3
        k1, k2, k3 = freudenstein_k(Fraction(2), Fraction(7), Fraction(5), Fraction(6))
        self.assertEqual((k1, k2, k3), (Fraction(3), Fraction(6, 5), Fraction(4, 5)))
        qa, qb, qc = 1 - k1 - k2 + k3, 0, k1 - (k2 + 1) + k3
        self.assertEqual((qa, qc), (Fraction(-12, 5), Fraction(8, 5)))
        self.assertEqual(-qc / qa, Fraction(2, 3))
        ps = fourbar_positions(2, 7, 5, 6, 0.0)
        self.assertEqual([p[2] for p in ps], [1, -1])
        self.assertAlmostEqual(math.tan(ps[0][1] / 2), math.sqrt(2 / 3), places=12)
        self.assertAlmostEqual(math.tan(ps[1][1] / 2), -math.sqrt(2 / 3), places=12)
        # B = (7, 2 sqrt 6) on the open branch
        self.assertAlmostEqual(6 + 5 * math.cos(ps[0][1]), 7.0, places=12)
        self.assertAlmostEqual(5 * math.sin(ps[0][1]), 2 * math.sqrt(6), places=12)

    def test_residual_random(self):
        rng = random.Random(20261114)
        count = 0
        for _ in range(3000):
            a, b, c, d = (rng.uniform(0.2, 10.0) for _ in range(4))
            theta2 = rng.uniform(-math.pi, math.pi)
            for t3, t4, br in fourbar_positions(a, b, c, d, theta2):
                self.assertLess(fourbar_residual(a, b, c, d, theta2, t3, t4), 1e-9 * (a + b + c + d))
                count += 1
        self.assertGreater(count, 2000)

    def test_two_assemblies_are_mirror_images(self):
        rng = random.Random(7)
        for _ in range(500):
            a, b, c, d = (rng.uniform(0.5, 6.0) for _ in range(4))
            theta2 = rng.uniform(0, 2 * math.pi)
            ps = fourbar_positions(a, b, c, d, theta2)
            if len(ps) != 2:
                continue
            self.assertEqual({ps[0][2], ps[1][2]}, {1, -1})
            ax, ay = a * math.cos(theta2), a * math.sin(theta2)
            pts = [(d + c * math.cos(t4), c * math.sin(t4)) for _, t4, _ in ps]
            # both B are at distance b from A and c from O4, so they are mirror images in line A O4
            for bx, by in pts:
                self.assertAlmostEqual(math.hypot(bx - ax, by - ay), b, delta=1e-9 * (a + b + c + d))
                self.assertAlmostEqual(math.hypot(bx - d, by), c, delta=1e-9 * (a + b + c + d))

    def test_no_assembly_when_triangle_fails(self):
        # a = 2, d = 6, b = 3, c = 2: the diagonal is between 4 and 8, but b + c = 5
        self.assertEqual(fourbar_positions(2, 3, 2, 6, math.pi), [])
        self.assertTrue(fourbar_positions(2, 3, 2, 6, 0.0))

    def test_velocities_against_finite_differences(self):
        rng = random.Random(11)
        h = 1e-6
        tested = 0
        for _ in range(400):
            a, b, c, d = (rng.uniform(0.5, 6.0) for _ in range(4))
            theta2 = rng.uniform(0, 2 * math.pi)
            ps = fourbar_positions(a, b, c, d, theta2)
            pm = fourbar_positions(a, b, c, d, theta2 - h)
            pp = fourbar_positions(a, b, c, d, theta2 + h)
            if len(ps) != 2 or len(pm) != 2 or len(pp) != 2:
                continue
            for k in range(2):
                t3, t4, br = ps[k]
                if abs(math.sin(t3 - t4)) < 0.05:
                    continue
                w3, w4 = fourbar_velocities(a, b, c, theta2, t3, t4, 1.0)
                fd3 = math.remainder(pp[k][0] - pm[k][0], 2 * math.pi) / (2 * h)
                fd4 = math.remainder(pp[k][1] - pm[k][1], 2 * math.pi) / (2 * h)
                self.assertAlmostEqual(w3, fd3, delta=1e-4 * (1 + abs(w3)))
                self.assertAlmostEqual(w4, fd4, delta=1e-4 * (1 + abs(w4)))
                tested += 1
        self.assertGreater(tested, 200)

    def test_toggle_velocity_raises(self):
        # at a toggle position the coupler and the output are in line, sin(theta3 - theta4) = 0,
        # and the loop derivative does not fix omega3 and omega4 (here a = 2, b = 4, c = 4, d = 6 at theta2 = pi)
        (t3, t4, _), = fourbar_positions(2, 4, 4, 6, math.pi)
        with self.assertRaises(ZeroDivisionError):
            fourbar_velocities(2, 4, 4, math.pi, t3, t4, 1.0)


class TestGrashofAgainstSweep(unittest.TestCase):
    def test_each_joint_against_sweep(self):
        rng = random.Random(1875)
        seen = set()
        for _ in range(500):
            links = [rng.randint(1, 12) for _ in range(4)]  # cycle (d, a, b, c)
            if not closes(links) or 2 * max(links) == sum(links):
                continue
            d, a, b, c = links
            turns = [joint_turns_by_sweep(links, k, steps=360) for k in range(4)]
            for k in range(4):
                x, y, u, v = (links[(k + j) % 4] for j in range(4))
                self.assertEqual(turns[k], joint_turns_fully(x, y, u, v), (links, k))
            s, p, q, l = sorted(links)
            self.assertEqual(any(turns), s + l <= p + q, links)
            cls = grashof_class(a, b, c, d)
            seen.add(cls)
            if cls == "triple-rocker":
                self.assertFalse(any(turns))
            elif cls == "crank-rocker":
                self.assertEqual((turns[0], turns[3]), (True, False))
            elif cls == "rocker-crank":
                self.assertEqual((turns[0], turns[3]), (False, True))
            elif cls == "double-crank":
                self.assertEqual((turns[0], turns[3]), (True, True))
            elif cls == "grashof double-rocker":
                self.assertEqual((turns[0], turns[3]), (False, False))
                self.assertEqual((turns[1], turns[2]), (True, True))
            if cls not in ("triple-rocker", "change point"):
                # the shortest link turns fully against both neighbours, the other two joints rock
                ks = [k for k in range(4) if links[k] == s]
                if len(ks) == 1:
                    k = ks[0]
                    self.assertTrue(turns[(k - 1) % 4] and turns[k])
                    self.assertFalse(turns[(k + 1) % 4] or turns[(k + 2) % 4])
        self.assertGreaterEqual(len(seen), 5)

    def test_change_point(self):
        # s + l = p + q: 2 + 6 = 4 + 4; the linkage reaches a position with all links in line
        a, b, c, d = 2, 4, 4, 6
        self.assertEqual(grashof_class(a, b, c, d), "change point")
        ps = fourbar_positions(a, b, c, d, math.pi)
        self.assertEqual(len(ps), 1)
        t3, t4, br = ps[0]
        self.assertEqual(br, 0)
        self.assertAlmostEqual(math.sin(t3), 0.0, places=9)
        self.assertAlmostEqual(math.sin(t4), 0.0, places=9)
        self.assertTrue(input_turns_by_sweep(a, b, c, d))


class TestSliderCrank(unittest.TestCase):
    def test_residual_and_branches(self):
        rng = random.Random(3)
        for _ in range(2000):
            a, b = rng.uniform(0.2, 5.0), rng.uniform(0.2, 10.0)
            e = rng.uniform(-3.0, 3.0)
            theta2 = rng.uniform(0, 2 * math.pi)
            ps = slider_crank_positions(a, b, e, theta2)
            for x, t3, br in ps:
                self.assertLess(slider_crank_residual(a, b, e, theta2, x, t3), 1e-9 * (a + b + abs(e) + 1))
            if len(ps) == 2:
                self.assertGreater(ps[0][0], ps[1][0])

    def test_full_rotation_and_stroke(self):
        rng = random.Random(5)
        for _ in range(60):
            a, b, e = rng.randint(1, 6), rng.randint(1, 12), rng.randint(-4, 4)
            sweep = [slider_crank_positions(a, b, e, 2 * math.pi * k / 720) for k in range(720)]
            full = all(sweep)
            self.assertEqual(full, b >= a + abs(e), (a, b, e))
            if b > a + abs(e):
                xs = [p[0][0] for p in sweep]
                stroke = math.sqrt((a + b) ** 2 - e * e) - math.sqrt((b - a) ** 2 - e * e)
                self.assertAlmostEqual(max(xs) - min(xs), stroke, delta=1e-3 * stroke)
                if e == 0:
                    self.assertAlmostEqual(stroke, 2 * a, places=12)

    def test_slider_velocity_against_finite_differences(self):
        rng = random.Random(9)
        h = 1e-6
        for _ in range(300):
            a, b, e = rng.uniform(0.5, 3.0), rng.uniform(4.0, 8.0), rng.uniform(-1.0, 1.0)
            theta2 = rng.uniform(0, 2 * math.pi)
            x, t3, _ = slider_crank_positions(a, b, e, theta2)[0]
            w3, xdot = slider_crank_velocity(a, b, theta2, t3, 2.0)
            xp = slider_crank_positions(a, b, e, theta2 + h)[0][0]
            xm = slider_crank_positions(a, b, e, theta2 - h)[0][0]
            self.assertAlmostEqual(xdot, 2.0 * (xp - xm) / (2 * h), delta=1e-5 * (1 + abs(xdot)))


if __name__ == "__main__":
    unittest.main()
