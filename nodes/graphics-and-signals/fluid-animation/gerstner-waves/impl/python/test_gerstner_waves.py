# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gerstner-waves/. The authors are listed in prov/4CGSP7.jsonl.
import math
import random
import unittest

import gerstner_waves as gw


def euler_residuals(a, b, t, amp, k, w, g=gw.G, h=1e-4):
    """The two Lagrangian momentum equations, by central differences.

    Returns (x_tt x_a + (z_tt + g) z_a, x_tt x_b + (z_tt + g) z_b), which equal -p_a / rho and -p_b / rho.
    """
    def pos(aa, bb, tt):
        return gw.particle(aa, bb, tt, amp, k, g, w=w)

    xp, zp = pos(a, b, t + h)
    x0, z0 = pos(a, b, t)
    xm, zm = pos(a, b, t - h)
    xtt, ztt = (xp - 2 * x0 + xm) / h ** 2, (zp - 2 * z0 + zm) / h ** 2
    xa = (pos(a + h, b, t)[0] - pos(a - h, b, t)[0]) / (2 * h)
    za = (pos(a + h, b, t)[1] - pos(a - h, b, t)[1]) / (2 * h)
    xb = (pos(a, b + h, t)[0] - pos(a, b - h, t)[0]) / (2 * h)
    zb = (pos(a, b + h, t)[1] - pos(a, b - h, t)[1]) / (2 * h)
    return xtt * xa + (ztt + g) * za, xtt * xb + (ztt + g) * zb


class TestDispersion(unittest.TestCase):
    def test_deep_water_check_values(self):
        k, w, period, speed = gw.deep_water(10.0, 9.81)
        self.assertAlmostEqual(k, 0.628319, places=6)
        self.assertAlmostEqual(w, 2.482701, places=6)
        self.assertAlmostEqual(period, 2.530786, places=6)
        self.assertAlmostEqual(speed, 3.951342, places=6)
        self.assertAlmostEqual(gw.phase_speed(k), speed, places=12)

    def test_shallow_limit(self):
        k = 2 * math.pi / 2000.0
        self.assertAlmostEqual(gw.phase_speed(k, depth=1.0), 3.13209, places=4)
        self.assertAlmostEqual(math.sqrt(9.81 * 1.0), 3.13209, places=5)
        self.assertLess(gw.phase_speed(0.628319, depth=1.0), gw.phase_speed(0.628319))


class TestOneWave(unittest.TestCase):
    def test_circular_orbits(self):
        rng = random.Random(1)
        k, amp = 0.628319, 0.6
        for _ in range(50):
            a, b, t = rng.uniform(-20, 20), rng.uniform(-5, 0), rng.uniform(0, 10)
            x, z = gw.particle(a, b, t, amp, k)
            self.assertAlmostEqual(math.hypot(x - a, z - b), amp * math.exp(k * b), places=12)
            u, v = gw.particle_velocity(a, b, t, amp, k)
            self.assertAlmostEqual(math.hypot(u, v), amp * math.exp(k * b) * gw.dispersion(k), places=12)

    def test_crest_moves_at_phase_speed(self):
        k, amp = 0.628319, 0.5
        _, _, _, speed = gw.deep_water(2 * math.pi / k)
        for t in (0.0, 1.0, 3.7):
            crest = gw.dispersion(k) * t / k
            x, z = gw.particle(crest, 0.0, t, amp, k)
            self.assertAlmostEqual(x, speed * t, places=9)
            self.assertAlmostEqual(z, amp, places=12)

    def test_exact_euler_solution(self):
        rng = random.Random(2)
        k, amp = 0.5, 1.2
        w = gw.dispersion(k)
        for _ in range(20):
            a, b, t = rng.uniform(-10, 10), rng.uniform(-3, 0), rng.uniform(0, 5)
            ra, rb = euler_residuals(a, b, t, amp, k, w)
            self.assertLess(abs(ra), 1e-5)
            s = k * amp * math.exp(k * b)
            self.assertAlmostEqual(rb, gw.G * (1 - s * s), places=4)
        ra, _ = euler_residuals(1.0, 0.0, 0.3, amp, k, 1.2 * w)
        self.assertGreater(abs(ra), 0.1)

    def test_volume_and_vorticity(self):
        rng = random.Random(3)
        k, amp, h = 0.7, 1.0, 1e-5
        for _ in range(20):
            a, b, t = rng.uniform(-5, 5), rng.uniform(-2, 0), rng.uniform(0, 5)
            p = lambda aa, bb: gw.particle(aa, bb, t, amp, k)
            xa = [(p(a + h, b)[i] - p(a - h, b)[i]) / (2 * h) for i in (0, 1)]
            xb = [(p(a, b + h)[i] - p(a, b - h)[i]) / (2 * h) for i in (0, 1)]
            jac = xa[0] * xb[1] - xb[0] * xa[1]
            self.assertAlmostEqual(jac, gw.jacobian(a, b, amp, k), places=7)
            vel = lambda aa, bb: gw.particle_velocity(aa, bb, t, amp, k)
            ua = [(vel(a + h, b)[i] - vel(a - h, b)[i]) / (2 * h) for i in (0, 1)]
            ub = [(vel(a, b + h)[i] - vel(a, b - h)[i]) / (2 * h) for i in (0, 1)]
            dv_dx = (ua[1] * xb[1] - ub[1] * xa[1]) / jac
            du_dz = (ub[0] * xa[0] - ua[0] * xb[0]) / jac
            self.assertAlmostEqual(dv_dx - du_dz, gw.vorticity(b, amp, k), places=5)
        self.assertGreater(gw.vorticity(0.0, amp, k), 0.0)

    def test_crest_shape_and_loops(self):
        k = 1.0
        n = 2000

        def surface_x(amp):
            return [gw.particle(2 * math.pi * i / n, 0.0, 0.0, amp, k)[0] for i in range(-n // 2, n // 2)]

        for ka, loops in ((0.5, False), (0.99, False), (1.2, True)):
            xs = surface_x(ka / k)
            self.assertEqual(any(x2 <= x1 for x1, x2 in zip(xs, xs[1:])), loops)
        self.assertAlmostEqual(gw.jacobian(0.0, 0.0, 1.0, 1.0), 0.0, places=15)

    def test_mean_level(self):
        for k, amp in ((0.628319, 0.5), (1.0, 0.8), (0.2, 3.0)):
            self.assertAlmostEqual(gw.mean_level(amp, k), -k * amp * amp / 2, places=12)


class TestSum(unittest.TestCase):
    def waves(self, rng, count, total):
        out = []
        weights = [rng.uniform(0.2, 1.0) for _ in range(count)]
        for wt in weights:
            wl = rng.uniform(2.0, 40.0)
            ang = rng.uniform(0, 2 * math.pi)
            k = 2 * math.pi / wl
            out.append((total * wt / sum(weights) / k, wl, (math.cos(ang), math.sin(ang)), rng.uniform(0, 6)))
        return out

    def test_jacobian_matches_differences(self):
        rng = random.Random(4)
        waves = self.waves(rng, 5, 0.8)
        h = 1e-5
        for _ in range(10):
            px, py, t = rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(0, 9)
            (j11, j12), (j21, j22) = gw.horizontal_jacobian(px, py, t, waves)
            f = lambda qx, qy: gw.surface_point(qx, qy, t, waves)
            self.assertAlmostEqual(j11, (f(px + h, py)[0] - f(px - h, py)[0]) / (2 * h), places=6)
            self.assertAlmostEqual(j21, (f(px + h, py)[1] - f(px - h, py)[1]) / (2 * h), places=6)
            self.assertAlmostEqual(j12, (f(px, py + h)[0] - f(px, py - h)[0]) / (2 * h), places=6)

    def test_no_loops_below_steepness_one(self):
        rng = random.Random(5)
        for trial in range(5):
            waves = self.waves(rng, 6, 0.9)
            s = gw.steepness(waves)
            self.assertAlmostEqual(s, 0.9, places=12)
            for _ in range(200):
                p = (rng.uniform(-50, 50), rng.uniform(-50, 50))
                q = (rng.uniform(-50, 50), rng.uniform(-50, 50))
                t = rng.uniform(0, 20)
                fp = gw.surface_point(p[0], p[1], t, waves)
                fq = gw.surface_point(q[0], q[1], t, waves)
                dot = (fp[0] - fq[0]) * (p[0] - q[0]) + (fp[1] - fq[1]) * (p[1] - q[1])
                d2 = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
                self.assertGreaterEqual(dot, (1 - s) * d2 - 1e-9)
                (j11, j12), (_, j22) = gw.horizontal_jacobian(p[0], p[1], t, waves)
                self.assertGreater(j11 * j22 - j12 * j12, 0.0)

    def test_one_wave_sum_equals_particle(self):
        k, amp = 0.628319, 0.4
        waves = [(amp, 2 * math.pi / k, (1.0, 0.0), 0.3)]
        for px in (-3.0, 0.0, 2.5):
            x, y, z = gw.surface_point(px, 7.0, 1.1, waves)
            xe, ze = gw.particle(px, 0.0, 1.1, amp, k, phase=0.3)
            self.assertAlmostEqual(x, xe, places=12)
            self.assertAlmostEqual(z, ze, places=12)
            self.assertEqual(y, 7.0)


if __name__ == "__main__":
    unittest.main()
