# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsdf-fusion/. The authors are listed in prov/AYN2F8.jsonl.

import math
import random
import unittest

from tsdf_fusion import Volume, batch_average, integrate, zero_crossings

I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def column(nz, z0, h):
    """A single column of voxels on the optical axis of a camera at the origin."""
    return Volume((1, 1, nz), (-h / 2.0, -h / 2.0, z0), h)


ONE_PIXEL = ([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], I3, [0.0, 0.0, 0.0])


def sphere_depth(cam, width, height, c, r, rng, sigma):
    K, _, t = cam
    C = [-t[0], -t[1], -t[2]]
    out = []
    for v in range(height):
        row = []
        for u in range(width):
            d = [(u - K[0][2]) / K[0][0], (v - K[1][2]) / K[1][1], 1.0]
            oc = [C[a] - c[a] for a in range(3)]
            A = sum(x * x for x in d)
            B = 2.0 * sum(d[a] * oc[a] for a in range(3))
            disc = B * B - 4.0 * A * (sum(x * x for x in oc) - r * r)
            if disc < 0.0:
                row.append(None)
            else:
                row.append((-B - math.sqrt(disc)) / (2.0 * A) + rng.gauss(0.0, sigma))
        out.append(row)
    return out


class TsdfFusionTest(unittest.TestCase):
    def test_worked_example(self):
        vol = column(4, 1.9625, 0.025)
        for z, w in ((2.00, 1.0), (2.03, 2.0), (1.98, 1.0)):
            integrate(vol, [[z]], ONE_PIXEL, 0.05, w)
        for got, want in zip(vol.D, (0.65, 0.2, -0.3, -0.6)):
            self.assertAlmostEqual(got, want, places=12)
        self.assertEqual(vol.W, [4.0, 4.0, 4.0, 3.0])
        (p,) = zero_crossings(vol)
        self.assertAlmostEqual(p[2], 2.01, places=12)

    def test_crossing_is_weighted_mean_of_readings(self):
        rng = random.Random(3)
        for _ in range(20):
            readings = [(2.0 + rng.uniform(-0.01, 0.01), rng.uniform(0.5, 2.0)) for _ in range(6)]
            vol = column(16, 1.8, 0.025)
            for z, w in readings:
                integrate(vol, [[z]], ONE_PIXEL, 0.1, w)
            mean, _ = batch_average(readings)
            crossings = zero_crossings(vol)
            self.assertEqual(len(crossings), 1)
            self.assertAlmostEqual(crossings[0][2], mean, places=10)

    def test_running_average_ignores_order(self):
        rng = random.Random(5)
        readings = [(2.0 + rng.uniform(-0.03, 0.03), rng.uniform(0.5, 2.0)) for _ in range(5)]
        a, b = column(12, 1.85, 0.025), column(12, 1.85, 0.025)
        for z, w in readings:
            integrate(a, [[z]], ONE_PIXEL, 0.05, w)
        for z, w in reversed(readings):
            integrate(b, [[z]], ONE_PIXEL, 0.05, w)
        for x, y in zip(a.D, b.D):
            self.assertAlmostEqual(x, y, places=12)
        for x, y in zip(a.W, b.W):
            self.assertAlmostEqual(x, y, places=12)

    def test_free_space_and_unseen(self):
        vol = column(20, 1.5, 0.05)
        integrate(vol, [[2.0]], ONE_PIXEL, 0.1)
        for k in range(20):
            z = 1.5 + 0.05 * (k + 0.5)
            if z < 1.9:
                self.assertEqual((vol.D[k], vol.W[k]), (1.0, 1.0))
            elif z > 2.1:
                self.assertEqual(vol.W[k], 0.0)
        integrate(vol, [[None]], ONE_PIXEL, 0.1)
        self.assertEqual(vol.W[0], 1.0)

    def test_fusion_reduces_noise_on_a_sphere(self):
        rng = random.Random(1)
        K = [[30.0, 0.0, 15.5], [0.0, 30.0, 15.5], [0.0, 0.0, 1.0]]
        offsets = [(0, 0), (0.4, 0), (-0.4, 0), (0, 0.4), (0, -0.4), (0.3, 0.3), (-0.3, 0.3), (0.3, -0.3)]
        cams = [(K, I3, [-ox, -oy, 0.0]) for ox, oy in offsets]
        c, r = (0.0, 0.0, 3.0), 1.0

        def mean_error(vol):
            e = [abs(math.dist(p, c) - r) for p in zero_crossings(vol)
                 if abs(p[0]) < 0.6 and abs(p[1]) < 0.6]
            self.assertGreater(len(e), 100)
            return sum(e) / len(e)

        single = Volume((24, 24, 14), (-1.2, -1.2, 1.6), 0.1)
        integrate(single, sphere_depth(cams[0], 32, 32, c, r, rng, 0.02), cams[0], 0.15)
        fused = Volume((24, 24, 14), (-1.2, -1.2, 1.6), 0.1)
        for cam in cams:
            integrate(fused, sphere_depth(cam, 32, 32, c, r, rng, 0.02), cam, 0.15)
        e1, e8 = mean_error(single), mean_error(fused)
        self.assertLess(e8, 0.6 * e1)
        self.assertLess(e8, 0.01)


if __name__ == "__main__":
    unittest.main()
