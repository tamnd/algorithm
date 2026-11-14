# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gear-generation-by-enveloping/. The authors are listed in prov/X68YYQ.jsonl.

import math
import random
import unittest

from gear_generation_by_enveloping import (
    envelope, involute, inv, meshing, rack_clearance, rack_flank, rack_motion, rot,
    shaper_flank, shaper_motion,
)


def polar(p):
    return math.hypot(p[0], p[1]), math.atan2(p[1], p[0])


def closed_involute_point(rb, theta0, t):
    """The flank theta + inv(alpha) = theta0 of the gear: the mirror of involute(rb, t), turned by theta0."""
    x, y = involute(rb, t)
    return rot(theta0, (x, -y))


def random_rack_case(rng, undercut_free=True):
    while True:
        m = rng.uniform(0.5, 10.0)
        phi = math.radians(rng.uniform(14.5, 30.0))
        z = rng.randint(8, 120)
        r = m * z / 2
        if not undercut_free or r * math.sin(phi) ** 2 >= m:
            return m, phi, z, r


class TestRackGeneration(unittest.TestCase):
    def test_root_and_point_match_closed_form_involute(self):
        rng = random.Random(1)
        for _ in range(600):
            m, phi, z, r = random_rack_case(rng, undercut_free=False)
            rb = r * math.cos(phi)
            theta0 = math.pi / 2 + inv(phi)
            limit = r * math.sin(phi) * math.tan(phi)
            u = rng.uniform(-min(m / math.cos(phi), limit), 1.25 * m / math.cos(phi))
            curve, normal = rack_flank(phi)
            pts = envelope(curve, normal, rack_motion(r), [u], -1.5, 1.5)
            self.assertEqual(len(pts), 1)
            _, psi, p = pts[0]
            self.assertAlmostEqual(psi, u / (r * math.sin(phi)), delta=1e-11)
            t = (r * math.sin(phi) + u / math.tan(phi)) / rb
            q = closed_involute_point(rb, theta0, t)
            self.assertLess(math.dist(p, q), 1e-9 * r)
            rho, theta = polar(p)
            self.assertGreaterEqual(rho, rb * (1 - 1e-12))
            self.assertAlmostEqual(theta + inv(math.acos(min(1.0, rb / rho))), theta0, delta=1e-7)

    def test_root_on_grid_node_is_found_once(self):
        curve, normal = rack_flank(math.radians(20))
        pts = envelope(curve, normal, rack_motion(40.0), [0.0], -1.0, 1.0, cells=64)
        self.assertEqual(len(pts), 1)
        self.assertEqual(pts[0][1], 0.0)
        self.assertLess(math.dist(pts[0][2], (0.0, 40.0)), 1e-12)

    def test_meshing_is_normal_part_of_relative_velocity(self):
        rng = random.Random(2)
        h = 1e-6
        for _ in range(300):
            m, phi, z, r = random_rack_case(rng, undercut_free=False)
            if rng.random() < 0.5:
                curve, normal = rack_flank(phi)
                motion = rack_motion(r)
                u = rng.uniform(-2 * m, 2 * m)
            else:
                rc = m * rng.randint(10, 40) / 2
                curve, normal = shaper_flank(rc, phi)
                motion = shaper_motion(r, rc)
                u = rng.uniform(0.0, 1.0)
            psi = rng.uniform(-0.5, 0.5)
            a = motion.apply(psi + h, curve(u))
            b = motion.apply(psi - h, curve(u))
            v = ((a[0] - b[0]) / (2 * h), (a[1] - b[1]) / (2 * h))
            n = rot(motion.a(psi), normal(u))
            expect = n[0] * v[0] + n[1] * v[1]
            self.assertAlmostEqual(meshing(curve, normal, motion, u, psi), expect,
                                   delta=1e-5 * (1 + abs(expect)) * r)

    def test_point_is_touched_but_not_cut_by_the_rack(self):
        rng = random.Random(3)
        for _ in range(60):
            m, phi, z, r = random_rack_case(rng)
            motion = rack_motion(r)
            curve, normal = rack_flank(phi)
            u = rng.uniform(-m / math.cos(phi), 1.25 * m / math.cos(phi))
            (_, psi, p), = envelope(curve, normal, motion, [u], -1.5, 1.5)
            c = rack_clearance(phi, motion, p, psi - 0.3, psi + 0.3, m, 600)
            self.assertGreater(c, -1e-9 * r)
            self.assertLess(c, 1e-9 * r)

    def test_brute_force_swept_boundary_is_the_involute(self):
        rng = random.Random(4)
        for _ in range(18):
            m, phi, z, r = random_rack_case(rng)
            z = max(z, 18)
            r = m * z / 2
            rb = r * math.cos(phi)
            theta0 = math.pi / 2 + inv(phi)
            motion = rack_motion(r)
            curve, normal = rack_flank(phi)
            (_, _, low), = envelope(curve, normal, motion, [-m / math.cos(phi)], -1.5, 1.5)
            rho = rng.uniform(math.hypot(*low) + 1e-3 * m, r + m)
            w = 6 * m / r

            def cleared(theta):
                p = (rho * math.cos(theta), rho * math.sin(theta))
                return rack_clearance(phi, motion, p, -w, w, m, 2000) >= 0

            expect = theta0 - inv(math.acos(rb / rho))
            lo, hi = expect - 0.5 * m / rho, expect + 0.5 * m / rho
            self.assertTrue(cleared(lo))
            self.assertFalse(cleared(hi))
            for _ in range(45):
                mid = 0.5 * (lo + hi)
                if cleared(mid):
                    lo = mid
                else:
                    hi = mid
            self.assertAlmostEqual(lo, expect, delta=1e-6)

    def test_undercut_iff_addendum_above_r_sin2_phi(self):
        rng = random.Random(5)
        seen = [0, 0]
        while min(seen) < 40:
            m = rng.uniform(1.0, 6.0)
            phi = math.radians(rng.uniform(14.5, 25.0))
            z = rng.randint(6, 40)
            r = m * z / 2
            ratio = r * math.sin(phi) ** 2 / m
            if abs(ratio - 1) < 0.03:
                continue
            motion = rack_motion(r)
            curve, normal = rack_flank(phi)
            (_, psi, p), = envelope(curve, normal, motion, [-m / math.cos(phi)], -2.0, 2.0)
            c = rack_clearance(phi, motion, p, psi - 0.3, psi + 0.3, m, 3000)
            if ratio >= 1:
                self.assertGreater(c, -1e-9 * r)
            else:
                self.assertLess(c, -1e-6 * m)
            seen[ratio >= 1] += 1


class TestShaperGeneration(unittest.TestCase):
    def test_shaper_cuts_the_same_involute_as_the_rack(self):
        rng = random.Random(6)
        checked = 0
        for _ in range(300):
            m, phi, z, r = random_rack_case(rng, undercut_free=False)
            rc = m * rng.randint(10, 40) / 2
            rb = r * math.cos(phi)
            theta0 = math.pi / 2 + inv(phi)
            curve, normal = shaper_flank(rc, phi)
            motion = shaper_motion(r, rc)
            t = math.tan(phi) + rng.uniform(-0.15, 0.15)
            expect = -(rc / r) * (t - math.tan(phi))
            pts = envelope(curve, normal, motion, [t], expect - 0.02, expect + 0.02, cells=4)
            self.assertEqual(len(pts), 1)
            _, psi, p = pts[0]
            self.assertAlmostEqual(psi, expect, delta=1e-11)
            # The contact is (t - tan(phi)) rc cos(phi) from the pitch point along the line of action.
            # Past the tangent point of the gear base circle, r sin(phi) away, the point is undercut.
            if rc * math.cos(phi) * (t - math.tan(phi)) <= 0.999 * r * math.sin(phi):
                rho, theta = polar(p)
                self.assertGreaterEqual(rho, rb)
                self.assertAlmostEqual(theta + inv(math.acos(rb / rho)), theta0, delta=1e-7)
                checked += 1
        self.assertGreater(checked, 200)

    def test_wide_window_shows_a_second_branch(self):
        phi = math.radians(20)
        curve, normal = shaper_flank(24.0, phi)
        pts = envelope(curve, normal, shaper_motion(40.0, 24.0), [math.tan(phi) - 0.2], -0.3, 0.3)
        self.assertEqual(len(pts), 2)
        rb = 40.0 * math.cos(phi)
        theta0 = math.pi / 2 + inv(phi)
        errs = sorted(abs(polar(p)[1] + inv(math.acos(rb / polar(p)[0])) - theta0) for _, _, p in pts)
        self.assertLess(errs[0], 1e-9)
        self.assertGreater(errs[1], 1e-2)


if __name__ == "__main__":
    unittest.main()
