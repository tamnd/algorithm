# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/method-of-characteristics-transport/. The authors are listed in prov/J4S5CW.jsonl.
import math
import random
import unittest

from method_of_characteristics_transport import (expint, lay_tracks, moc_solve, polar_quadrature, segment,
                                                 slab_absorber_flux)


def strip_error(n_azim, n_polar, spacing):
    width, height, nx, ny = 2.0, 20.0, 10, 5
    n = nx * ny
    r = moc_solve(width, height, nx, ny, [1.0] * n, [0.0] * n, [1.0] * n, n_azim, n_polar, spacing, tol=1e-12)
    exact = [slab_absorber_flux(1.0, 1.0, width, i * width / nx, (i + 1) * width / nx) for i in range(nx)]
    return max(abs(r["phi"][i + 2 * nx] - exact[i]) for i in range(nx)), r["iterations"]


class TestPieces(unittest.TestCase):
    def test_segment_is_exact(self):
        for psi_in, qs, tau in ((0.0, 1.0, 1.25), (2.0, 0.5, 0.3), (1.0, 1.0, 7.0), (0.3, 0.0, 1e-12)):
            out, avg = segment(psi_in, qs, tau)
            self.assertAlmostEqual(out, qs + (psi_in - qs) * math.exp(-tau), places=12)
            k = 20000
            mean = sum(qs + (psi_in - qs) * math.exp(-tau * (i + 0.5) / k) for i in range(k)) / k
            self.assertAlmostEqual(avg, mean, places=8)
        out, avg = segment(0.0, 1.0, 1.25)
        self.assertAlmostEqual(out, 0.7134952, places=7)
        self.assertAlmostEqual(avg, 0.4292038, places=7)

    def test_exponential_integrals(self):
        self.assertAlmostEqual(expint(1, 1.0), 0.219383934395520, places=13)
        self.assertAlmostEqual(expint(2, 1.0), 0.148495506775922, places=13)
        self.assertAlmostEqual(expint(1, 0.1), 1.822923958419390, places=12)
        self.assertAlmostEqual(expint(3, 0.0), 0.5, places=15)

    def test_polar_weights(self):
        for n in (1, 2, 3, 5):
            mus, ws = polar_quadrature(n)
            self.assertAlmostEqual(sum(ws), 2.0, places=13)
            if n > 1:
                # exact for mu^2 on (0, 1), counted on both hemispheres
                self.assertAlmostEqual(sum(w * mu * mu for mu, w in zip(mus, ws)), 2.0 / 3.0, places=12)

    def test_tracks_cover_cells(self):
        tracks = lay_tracks(4.0, 4.0, 8, 8, 8, 0.05)
        for a in range(8):
            areas = [0.0] * 64
            for b, delta, segs in tracks:
                if b == a:
                    for k, length in segs:
                        areas[k] += delta * length
            self.assertLess(max(abs(x - 0.25) for x in areas) / 0.25, 5e-3)
            self.assertAlmostEqual(sum(areas), 16.0, delta=2e-3)


class TestSolve(unittest.TestCase):
    def test_tall_strip_matches_slab_formula(self):
        coarse, it = strip_error(8, 3, 0.05)
        self.assertEqual(it, 2)
        fine, _ = strip_error(32, 5, 0.02)
        self.assertLess(coarse, 1.5e-2)
        self.assertLess(fine, 2.5e-3)
        self.assertLess(fine, coarse / 4.0)

    def test_balance_heterogeneous(self):
        rng = random.Random(5)
        nx = ny = 8
        st = [rng.uniform(0.5, 3.0) for _ in range(nx * ny)]
        ss = [s * rng.uniform(0.0, 0.8) for s in st]
        q = [rng.uniform(0.0, 1.0) for _ in range(nx * ny)]
        r = moc_solve(4.0, 4.0, nx, ny, st, ss, q, 8, 3, 0.05, tol=1e-12)
        area = 0.25
        absorbed = sum((a - b) * f * area for a, b, f in zip(st, ss, r["phi"]))
        self.assertAlmostEqual(absorbed + r["leakage"], sum(v * area for v in q), delta=1e-9)
        self.assertTrue(all(v > 0.0 for v in r["phi"]))

    def test_symmetry(self):
        nx = ny = 8
        r = moc_solve(4.0, 4.0, nx, ny, [1.0] * 64, [0.7] * 64, [1.0] * 64, 8, 3, 0.05, tol=1e-12)
        p = r["phi"]
        for i in range(nx):
            for j in range(ny):
                self.assertAlmostEqual(p[i + nx * j], p[nx - 1 - i + nx * j], places=12)
                self.assertAlmostEqual(p[i + nx * j], p[i + nx * (ny - 1 - j)], places=12)
                self.assertAlmostEqual(p[i + nx * j], p[j + nx * i], places=12)
        self.assertGreater(p[3 + 8 * 3], p[0])


if __name__ == "__main__":
    unittest.main()
