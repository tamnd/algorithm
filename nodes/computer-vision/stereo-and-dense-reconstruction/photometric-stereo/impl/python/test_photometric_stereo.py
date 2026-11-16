# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/photometric-stereo/. The authors are listed in prov/QKJF6P.jsonl.

import math
import random
import unittest

from photometric_stereo import gradients, photometric_stereo, render, solve3


def unit(x, y, z):
    n = math.sqrt(x * x + y * y + z * z)
    return [x / n, y / n, z / n]


def sphere_cap(size, extent, rng):
    """Normals and albedo of the cap z = sqrt(1 - x^2 - y^2) seen from +z."""
    albedo, normals = [], []
    for v in range(size):
        y = -extent + 2.0 * extent * v / (size - 1)
        arow, nrow = [], []
        for u in range(size):
            x = -extent + 2.0 * extent * u / (size - 1)
            nrow.append([x, y, math.sqrt(1.0 - x * x - y * y)])
            arow.append(rng.uniform(0.3, 1.0))
        albedo.append(arow)
        normals.append(nrow)
    return albedo, normals


def mat_vec(M, x):
    return [sum(M[r][c] * x[c] for c in range(3)) for r in range(3)]


class PhotometricStereoTest(unittest.TestCase):
    def test_worked_example(self):
        lights = [[0.0, 0.0, 1.0], [0.6, 0.0, 0.8], [0.0, 0.6, 0.8]]
        images = [[[0.6]], [[0.84]], [[0.66]]]
        albedo, normals = photometric_stereo(images, lights)
        self.assertAlmostEqual(albedo[0][0], 0.9, places=12)
        for got, want in zip(normals[0][0], (2.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0)):
            self.assertAlmostEqual(got, want, places=12)
        p, q = gradients(normals[0][0])
        self.assertAlmostEqual(p, -1.0, places=12)
        self.assertAlmostEqual(q, -0.5, places=12)

    def test_exact_recovery_without_shadows(self):
        rng = random.Random(1)
        albedo, normals = sphere_cap(15, 0.6, rng)
        lights = [unit(0.0, 0.0, 1.0), unit(0.3, 0.1, 1.0), unit(-0.2, 0.3, 1.0),
                  unit(0.1, -0.35, 1.0), [0.4, 0.4, 1.5]]
        images = render(albedo, normals, lights)
        self.assertTrue(all(x > 0.0 for img in images for row in img for x in row))
        est_a, est_n = photometric_stereo(images, lights)
        for v in range(15):
            for u in range(15):
                self.assertAlmostEqual(est_a[v][u], albedo[v][u], places=9)
                for a, b in zip(est_n[v][u], normals[v][u]):
                    self.assertAlmostEqual(a, b, places=9)

    def test_three_lights_invert_the_light_matrix(self):
        rng = random.Random(2)
        lights = [unit(0.5, 0.0, 1.0), unit(-0.3, 0.4, 1.0), unit(0.0, -0.5, 1.0)]
        for _ in range(20):
            g = [rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(0.5, 1.0)]
            I = [sum(s[r] * g[r] for r in range(3)) for s in lights]
            if min(I) <= 0.0:
                continue
            albedo, normals = photometric_stereo([[[x]] for x in I], lights)
            got = [albedo[0][0] * c for c in normals[0][0]]
            want = solve3(lights, I)
            for a, b, c in zip(got, want, g):
                self.assertAlmostEqual(a, b, places=12)
                self.assertAlmostEqual(a, c, places=12)

    def test_shadowed_readings_are_dropped(self):
        rng = random.Random(3)
        albedo, normals = sphere_cap(13, 0.68, rng)
        lights = [unit(0.0, 0.0, 1.0), unit(1.2, 0.0, 1.0), unit(-1.2, 0.0, 1.0),
                  unit(0.0, 1.2, 1.0), unit(0.0, -1.2, 1.0)]
        images = render(albedo, normals, lights)
        shadowed = sum(1 for img in images for row in img for x in row if x == 0.0)
        self.assertGreater(shadowed, 0)
        est_a, est_n = photometric_stereo(images, lights, threshold=0.0)
        naive_a, _ = photometric_stereo(images, lights, threshold=-1.0)
        worst_naive = 0.0
        for v in range(13):
            for u in range(13):
                self.assertAlmostEqual(est_a[v][u], albedo[v][u], places=9)
                worst_naive = max(worst_naive, abs(naive_a[v][u] - albedo[v][u]))
        self.assertGreater(worst_naive, 0.01)

    def test_coplanar_lights_give_no_answer(self):
        lights = [unit(1.0, 0.0, 1.0), unit(-1.0, 0.0, 1.0), unit(0.0, 0.0, 1.0)]
        albedo, normals = photometric_stereo([[[0.5]], [[0.4]], [[0.7]]], lights)
        self.assertIsNone(albedo[0][0])
        self.assertIsNone(normals[0][0])

    def test_generalized_bas_relief_gives_the_same_images(self):
        rng = random.Random(4)
        albedo, normals = sphere_cap(9, 0.68, rng)
        lights = [unit(0.0, 0.0, 1.0), unit(0.9, 0.2, 1.0), unit(-0.7, 0.6, 1.0), unit(0.1, -0.9, 1.0)]
        mu, nu, lam = 0.4, -0.3, 1.7
        G = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [mu, nu, lam]]
        G_inv_T = [[1.0, 0.0, -mu / lam], [0.0, 1.0, -nu / lam], [0.0, 0.0, 1.0 / lam]]
        new_lights = [mat_vec(G, s) for s in lights]
        new_albedo, new_normals = [], []
        for arow, nrow in zip(albedo, normals):
            ar, nr = [], []
            for a, n in zip(arow, nrow):
                b = mat_vec(G_inv_T, [a * c for c in n])
                r = math.sqrt(sum(c * c for c in b))
                ar.append(r)
                nr.append([c / r for c in b])
            new_albedo.append(ar)
            new_normals.append(nr)
        first = render(albedo, normals, lights)
        second = render(new_albedo, new_normals, new_lights)
        for img_a, img_b in zip(first, second):
            for row_a, row_b in zip(img_a, img_b):
                for x, y in zip(row_a, row_b):
                    self.assertAlmostEqual(x, y, places=12)
        self.assertTrue(any(x == 0.0 for img in first for row in img for x in row))
        est_a, _ = photometric_stereo(second, new_lights)
        self.assertAlmostEqual(est_a[4][4], new_albedo[4][4], places=9)
        self.assertGreater(abs(new_albedo[4][4] - albedo[4][4]), 0.1)


if __name__ == "__main__":
    unittest.main()
