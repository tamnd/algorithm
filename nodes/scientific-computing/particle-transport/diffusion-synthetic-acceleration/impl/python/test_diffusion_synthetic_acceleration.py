# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-synthetic-acceleration/. The authors are listed in prov/XAVARJ.jsonl.
import math
import random
import unittest

from diffusion_synthetic_acceleration import (dsa, fourier_dsa, fourier_dsa_dd, fourier_dsa_inconsistent,
                                              gauss_legendre, spectral_radius_dsa)


def slab_rate(accel, h, c=0.99, m=100, iters=40):
    phi0 = [1.0 + 0.5 * math.sin(3.7 * j) for j in range(m)]
    r = dsa(8, [1.0] * m, [c] * m, [0.0] * m, [h] * m, accel=accel, tol=0.0, max_iter=iters, phi0=phi0)
    ch = r["changes"]
    return ch[-1] / ch[-2]


class TestFourier(unittest.TestCase):
    def test_continuous_spectral_radius(self):
        rho, lam = spectral_radius_dsa(1.0)
        self.assertAlmostEqual(rho, 0.2247, delta=1e-4)
        self.assertAlmostEqual(lam, 2.53, delta=0.02)
        rho, _ = spectral_radius_dsa(0.99)
        self.assertAlmostEqual(rho, 0.2214, delta=1e-4)
        self.assertEqual(fourier_dsa(0.0, 0.9), 0.0)

    def test_s2_dsa_is_exact(self):
        mus, ws = gauss_legendre(2)
        for lam in (0.1, 1.0, 3.0, 30.0):
            for c in (0.5, 0.99, 1.0):
                self.assertAlmostEqual(fourier_dsa(lam, c, mus, ws), 0.0, delta=1e-11)

    def test_cosine_modes_are_eigenvectors(self):
        mus, ws = gauss_legendre(8)
        m, h, c = 30, 0.7, 0.95
        for accel, factor in (("consistent", fourier_dsa_dd), ("inconsistent", fourier_dsa_inconsistent)):
            for k in (0, 1, 4, 15, 29):
                theta = math.pi * k / m
                e = [math.cos(theta * (j + 0.5)) for j in range(m)]
                r = dsa(8, [1.0] * m, [c] * m, [0.0] * m, [h] * m, "reflect", "reflect", accel,
                        tol=0.0, max_iter=1, phi0=e)
                omega = factor(theta, c, h, mus, ws)
                for j in range(m):
                    self.assertAlmostEqual(r["phi"][j], omega * e[j], places=12)

    def test_consistent_factor_is_bounded_for_all_cell_sizes(self):
        mus, ws = gauss_legendre(8)
        for tau in (0.01, 0.1, 1.0, 10.0, 100.0):
            worst = max(abs(fourier_dsa_dd(math.pi * k / 500, 0.999, tau, mus, ws)) for k in range(500))
            self.assertLess(worst, 0.2247)
        bad = max(abs(fourier_dsa_inconsistent(math.pi * k / 500, 0.99, 10.0, mus, ws)) for k in range(500))
        self.assertGreater(bad, 40.0)


class TestIteration(unittest.TestCase):
    def test_infinite_medium_in_one_step(self):
        r = dsa(8, [1.0] * 10, [0.9] * 10, [1.0] * 10, [1.0] * 10, "reflect", "reflect", tol=0.0, max_iter=1)
        for p in r["phi"]:
            self.assertAlmostEqual(p, 10.0, places=12)

    def test_s2_reflecting_slab_in_one_step(self):
        rng = random.Random(4)
        m = 25
        st = [rng.uniform(0.5, 5.0) for _ in range(m)]
        ss = [s * rng.uniform(0.8, 0.999) for s in st]
        q = [rng.uniform(0.0, 1.0) for _ in range(m)]
        dx = [rng.uniform(0.1, 2.0) for _ in range(m)]
        phi0 = [rng.uniform(0.0, 5.0) for _ in range(m)]
        exact = dsa(2, st, ss, q, dx, "reflect", "reflect", "none", tol=1e-15)["phi"]
        one = dsa(2, st, ss, q, dx, "reflect", "reflect", tol=0.0, max_iter=1, phi0=phi0)["phi"]
        for a, b in zip(one, exact):
            self.assertAlmostEqual(a, b, delta=1e-11 * b)
        # with S4, or with vacuum faces, one step is not exact
        four = dsa(4, st, ss, q, dx, "reflect", "reflect", tol=0.0, max_iter=1, phi0=phi0)["phi"]
        self.assertGreater(max(abs(a - b) / b for a, b in zip(four, exact)), 0.1)

    def test_measured_rates(self):
        for h in (0.1, 1.0, 10.0):
            self.assertLess(slab_rate("consistent", h), 0.22)
        self.assertLess(slab_rate("inconsistent", 0.1), 0.22)
        self.assertGreater(slab_rate("inconsistent", 1.0), 0.7)
        self.assertGreater(slab_rate("inconsistent", 10.0), 30.0)
        self.assertGreater(slab_rate("none", 10.0, iters=200), 0.985)

    def test_same_solution_far_fewer_iterations(self):
        m, length = 40, 10.0
        args = (8, [1.0] * m, [0.99] * m, [1.0] * m, [length / m] * m)
        si = dsa(*args, accel="none", tol=1e-8)
        ac = dsa(*args, accel="consistent", tol=1e-8)
        self.assertEqual(si["iterations"], 437)
        self.assertLessEqual(ac["iterations"], 12)
        ref = dsa(*args, accel="consistent", tol=1e-14)
        self.assertAlmostEqual(ac["leak_right"], ref["leak_right"], delta=1e-8)
        # source iteration stops much farther from the solution than its tolerance suggests
        self.assertGreater(abs(si["leak_right"] - ref["leak_right"]), 1e-7)
        absorbed = sum(0.01 * p * length / m for p in ref["phi"])
        self.assertAlmostEqual(absorbed + ref["leak_left"] + ref["leak_right"], length, places=9)

    def test_heterogeneous_slab(self):
        rng = random.Random(9)
        m = 60
        st = [rng.uniform(0.5, 20.0) for _ in range(m)]
        ss = [s * rng.uniform(0.9, 0.999) for s in st]
        q = [rng.uniform(0.0, 1.0) for _ in range(m)]
        dx = [rng.uniform(0.05, 2.0) for _ in range(m)]
        ac = dsa(8, st, ss, q, dx, "reflect", "vacuum", tol=1e-12)
        self.assertLess(ac["iterations"], 20)
        ic = dsa(8, st, ss, q, dx, "reflect", "vacuum", "inconsistent", tol=1e-12, max_iter=300)
        self.assertFalse(math.isfinite(ic["changes"][-1]))
        si = dsa(8, st, ss, q, dx, "reflect", "vacuum", "none", tol=1e-12, phi0=ac["phi"])
        self.assertLessEqual(si["iterations"], 3)
        absorbed = sum((a - b) * p * h for a, b, p, h in zip(st, ss, ac["phi"], dx))
        self.assertAlmostEqual(absorbed + ac["leak_right"], sum(x * h for x, h in zip(q, dx)), delta=1e-8)


if __name__ == "__main__":
    unittest.main()
