# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cam-profile-synthesis/. The authors are listed in prov/59Q72X.jsonl.

import math
import random
import unittest
from fractions import Fraction as F

from cam_profile_synthesis import (
    TWO_PI,
    CamProgram,
    Segment,
    flat_faced_profile,
    flat_sample,
    poly345,
    poly4567,
    roller_profile,
    roller_sample,
    rot_minus,
)

SMOOTH = ["cycloidal", "poly345", "poly4567"]
ALL = SMOOTH + ["harmonic"]


def random_program(rng, laws, max_lift=15.0):
    """Rise, optional dwell, return, optional dwell, each motion at least about 50 degrees."""
    lift = rng.uniform(3.0, max_lift)
    parts = [("rise", rng.uniform(1.0, 2.0)), ("dwell", rng.uniform(0.0, 1.5)),
             ("return", rng.uniform(1.0, 2.0)), ("dwell", rng.uniform(0.0, 1.5))]
    parts = [p for p in parts if p[0] != "dwell" or p[1] > 0.3]
    total = sum(w for _, w in parts)
    segs = []
    for kind, w in parts:
        beta = TWO_PI * w / total
        if kind == "dwell":
            segs.append(Segment("dwell", beta, 0.0))
        else:
            segs.append(Segment(rng.choice(laws), beta, lift if kind == "rise" else -lift))
    # make the angles sum to 2 pi in floating point
    last = segs[-1]
    segs[-1] = Segment(last.law, TWO_PI - sum(g.beta for g in segs[:-1]), last.lift)
    return CamProgram(segs)


def poly_eval(c, x):
    return sum(ci * x ** i for i, ci in enumerate(c))


def poly_der(c):
    return [i * ci for i, ci in enumerate(c)][1:]


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def signed_circumradius(a, b, c):
    """Radius of the circle through three points, positive when they turn clockwise."""
    cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return -dist(a, b) * dist(b, c) * dist(a, c) / (2.0 * cross)


class TestLaws(unittest.TestCase):
    def test_polynomial_laws_exact(self):
        rng = random.Random(1)
        for law, coef in ((poly345, [0, 0, 0, 10, -15, 6]), (poly4567, [0, 0, 0, 0, 35, -84, 70, -20])):
            ders = [coef]
            for _ in range(3):
                ders.append(poly_der(ders[-1]))
            for _ in range(200):
                x = F(rng.randint(0, 1000), 1000)
                self.assertEqual(law(x), tuple(poly_eval(d, x) for d in ders))
        self.assertEqual(poly345(F(0)), (0, 0, 0, 60))
        self.assertEqual(poly345(F(1)), (1, 0, 0, 60))
        self.assertEqual(poly4567(F(0)), (0, 0, 0, 0))
        self.assertEqual(poly4567(F(1)), (1, 0, 0, 0))

    def test_derivatives_against_finite_differences(self):
        rng = random.Random(2)
        cases = 0
        while cases < 600:
            prog = random_program(rng, ALL)
            theta = rng.uniform(0, TWO_PI)
            ends = prog.starts + [TWO_PI]
            if min(abs(theta - e) for e in ends) < 1e-3:
                continue
            i = prog.segment_at(theta)
            g = prog.segments[i]
            h = 1e-5
            lo, mid, hi = prog.svaj(theta - h), prog.svaj(theta), prog.svaj(theta + h)
            for k in range(3):
                fd = (hi[k] - lo[k]) / (2 * h)
                scale = abs(g.lift) / g.beta ** (k + 1) + 1.0
                self.assertLess(abs(fd - mid[k + 1]), 1e-6 * scale, (g.law, k))
            fd2 = (hi[0] - 2 * mid[0] + lo[0]) / (h * h)
            self.assertLess(abs(fd2 - mid[2]), 1e-3 * (abs(g.lift) / g.beta ** 2 + 1.0))
            cases += 1

    def test_continuity_at_segment_ends(self):
        rng = random.Random(3)
        for _ in range(500):
            prog = random_program(rng, SMOOTH)
            m = len(prog.segments)
            for i in range(m):
                left = prog.eval_segment(i, 1.0)
                right = prog.eval_segment((i + 1) % m, 0.0)
                scale = 1 + sum(abs(g.lift) / g.beta ** 2 for g in prog.segments)
                for k in range(3):
                    self.assertLess(abs(left[k] - right[k]), 1e-9 * scale, (i, k))

    def test_harmonic_acceleration_jump_at_dwell(self):
        rng = random.Random(4)
        for _ in range(500):
            b1, b2, b3 = rng.uniform(0.5, 2.0), rng.uniform(0.3, 1.5), rng.uniform(0.5, 2.0)
            lift = rng.uniform(1, 20)
            prog = CamProgram([Segment("harmonic", b1, lift), Segment("dwell", b2, 0.0),
                               Segment("harmonic", b3, -lift), Segment("dwell", TWO_PI - b1 - b2 - b3, 0.0)])
            left, right = prog.eval_segment(0, 1.0), prog.eval_segment(1, 0.0)
            self.assertAlmostEqual(left[0], right[0], places=9)
            self.assertAlmostEqual(left[1], right[1], places=9)
            jump = right[2] - left[2]
            self.assertAlmostEqual(jump, math.pi ** 2 * lift / (2 * b1 * b1), places=7)
            start = prog.eval_segment(0, 0.0)
            self.assertAlmostEqual(start[2], math.pi ** 2 * lift / (2 * b1 * b1), places=7)

    def test_rejects_open_programs(self):
        with self.assertRaises(ValueError):
            CamProgram([Segment("cycloidal", math.pi, 10.0), Segment("dwell", math.pi, 0.0)])
        with self.assertRaises(ValueError):
            CamProgram([Segment("cycloidal", 1.0, 10.0), Segment("cycloidal", 1.0, -10.0)])


class TestRollerProfile(unittest.TestCase):
    def test_base_circle(self):
        prog = CamProgram([Segment("dwell", TWO_PI, 0.0)])
        for smp in roller_profile(prog, 30.0, 8.0, 5.0, 64):
            self.assertAlmostEqual(math.hypot(*smp.contact), 30.0, places=9)
            self.assertAlmostEqual(math.hypot(*smp.pitch), 38.0, places=9)

    def test_contact_at_roller_distance_from_pitch_curve(self):
        """Brute force: the nearest point of a dense pitch curve to each cam point is at distance rf."""
        rng = random.Random(5)
        used = 0
        for _ in range(6):
            prog = random_program(rng, SMOOTH)
            rb, rf, eps = rng.uniform(40, 60), rng.uniform(5, 12), rng.uniform(-8, 8)
            n = 180
            prof = roller_profile(prog, rb, rf, eps, n)
            if min(smp.rho for smp in prof) <= rf:
                continue
            dense = roller_profile(prog, rb, rf, eps, 4 * n)
            for smp in prof:
                self.assertAlmostEqual(dist(smp.contact, smp.pitch), rf, places=9)
                near = min(dist(smp.contact, d.pitch) for d in dense)
                self.assertAlmostEqual(near, rf, places=7)
            used += 1
        self.assertGreaterEqual(used, 4)

    def test_contact_is_on_pitch_normal(self):
        rng = random.Random(6)
        for _ in range(500):
            prog = random_program(rng, ALL)
            rb, rf, eps = rng.uniform(30, 60), rng.uniform(3, 12), rng.uniform(-8, 8)
            theta = rng.uniform(0, TWO_PI)
            if min(abs(theta - e) for e in prog.starts + [TWO_PI]) < 1e-4:
                continue
            a = roller_sample(prog, theta - 1e-6, rb, rf, eps)
            b = roller_sample(prog, theta + 1e-6, rb, rf, eps)
            c = roller_sample(prog, theta, rb, rf, eps)
            tangent = (b.pitch[0] - a.pitch[0], b.pitch[1] - a.pitch[1])
            radial = (c.contact[0] - c.pitch[0], c.contact[1] - c.pitch[1])
            cosang = (tangent[0] * radial[0] + tangent[1] * radial[1]) / (math.hypot(*tangent) * rf)
            self.assertLess(abs(cosang), 1e-5)
            # pressure angle: angle of the pitch tangent, turned back to the fixed frame, from the x axis
            back = rot_minus(-theta, tangent)
            self.assertLess(abs(math.atan2(back[1], back[0]) - c.pressure_angle), 1e-6)

    def test_radius_of_curvature_against_three_points(self):
        rng = random.Random(7)
        for _ in range(500):
            prog = random_program(rng, ALL)
            rb, rf, eps = rng.uniform(20, 60), rng.uniform(3, 12), rng.uniform(-8, 8)
            theta = rng.uniform(0, TWO_PI)
            if min(abs(theta - e) for e in prog.starts + [TWO_PI]) < 1e-2:
                continue
            d = 1e-4
            pts = [roller_sample(prog, theta + k * d, rb, rf, eps).pitch for k in (-1, 0, 1)]
            rho = roller_sample(prog, theta, rb, rf, eps).rho
            ref = signed_circumradius(*pts)
            self.assertLess(abs(1 / ref - 1 / rho), 1e-4 / abs(rho) + 1e-6)

    def test_undercut_flag_matches_interference(self):
        """A small cam with a large roller and a fast rise: flagged samples cut into the roller."""
        prog = CamProgram([Segment("cycloidal", math.radians(40), 20.0), Segment("dwell", math.radians(140), 0.0),
                           Segment("cycloidal", math.radians(40), -20.0), Segment("dwell", math.radians(140), 0.0)])
        rb, rf = 10.0, 9.0
        prof = roller_profile(prog, rb, rf, 0.0, 720)
        flagged = [smp for smp in prof if smp.undercut]
        self.assertTrue(flagged)
        worst = min(min(dist(smp.contact, d.pitch) for d in prof) for smp in flagged)
        self.assertLess(worst, rf - 1e-3)
        # a large base circle removes the undercut
        big = roller_profile(prog, 60.0, 9.0, 0.0, 720)
        self.assertFalse(any(smp.undercut for smp in big))


class TestFlatFaced(unittest.TestCase):
    def test_eccentric_circle(self):
        e, rb = 7.0, 25.0
        prog = CamProgram([Segment("harmonic", math.pi, 2 * e), Segment("harmonic", math.pi, -2 * e)])
        for smp in flat_faced_profile(prog, rb, 360):
            self.assertAlmostEqual(dist(smp.contact, (0.0, -e)), rb + e, places=9)
            self.assertAlmostEqual(smp.rho, rb + e, places=9)

    def test_face_supports_cam(self):
        rng = random.Random(8)
        used = 0
        for _ in range(8):
            prog = random_program(rng, ALL)
            rb = rng.uniform(30, 60)
            prof = flat_faced_profile(prog, rb, 720)
            if min(smp.rho for smp in prof) <= 0:
                continue
            for smp in prof[::12]:
                e = rot_minus(smp.theta, (0.0, 1.0))
                h = rb + smp.s
                top = max(q.contact[0] * e[0] + q.contact[1] * e[1] for q in prof)
                self.assertAlmostEqual(smp.contact[0] * e[0] + smp.contact[1] * e[1], h, places=9)
                self.assertLessEqual(top, h + 1e-9)
            used += 1
        self.assertGreaterEqual(used, 5)

    def test_tangency_and_curvature(self):
        rng = random.Random(9)
        done = 0
        while done < 500:
            prog = random_program(rng, ALL)
            rb = rng.uniform(30, 60)
            theta = rng.uniform(0, TWO_PI)
            if min(abs(theta - e) for e in prog.starts + [TWO_PI]) < 1e-2:
                continue
            d = 1e-4
            pts = [flat_sample(prog, theta + k * d, rb).contact for k in (-1, 0, 1)]
            s, s1, s2, _ = prog.svaj(theta)
            e = rot_minus(theta, (0.0, 1.0))
            tang = (pts[2][0] - pts[0][0], pts[2][1] - pts[0][1])
            self.assertLess(abs(tang[0] * e[0] + tang[1] * e[1]), 1e-6 * (1 + math.hypot(*tang)))
            rho = flat_sample(prog, theta, rb).rho
            self.assertAlmostEqual(rho, rb + s + s2, places=9)
            if abs(rho) > 1.0:
                self.assertLess(abs(signed_circumradius(*pts) - rho), 1e-3 * abs(rho))
            done += 1


if __name__ == "__main__":
    unittest.main()
