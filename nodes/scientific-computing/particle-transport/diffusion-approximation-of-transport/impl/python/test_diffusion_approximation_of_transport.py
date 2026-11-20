# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-approximation-of-transport/. The authors are listed in prov/P2WTRA.jsonl.
import math
import random
import unittest

from diffusion_approximation_of_transport import (MILNE, bare_slab_k, diffusion_coefficient,
                                                  diffusion_decay_constant, k_eigenvalue,
                                                  slab_leakage_marshak, solve_fixed_source,
                                                  transport_decay_constant)

D = 1.0 / 3.0


class TestModel(unittest.TestCase):
    def test_diffusion_coefficient(self):
        self.assertAlmostEqual(diffusion_coefficient(1.0), 1.0 / 3.0, places=15)
        # linearly anisotropic scattering lowers the transport cross section
        self.assertAlmostEqual(diffusion_coefficient(1.0, 0.9, 0.5), 1.0 / (3.0 * 0.55), places=15)

    def test_bare_slab_check_value(self):
        self.assertAlmostEqual(bare_slab_k(0.12, 0.1, D, 20.0), 1.108804, places=6)
        self.assertAlmostEqual(bare_slab_k(0.12, 0.1, D, 20.0 + 2.0 * MILNE), 1.119719, places=6)
        self.assertAlmostEqual(bare_slab_k(0.12, 0.1, D, 1e9), 1.2, places=9)

    def test_decay_constants(self):
        for c in (0.5, 0.9, 0.99, 0.999):
            kt = transport_decay_constant(c)
            self.assertAlmostEqual(c * math.atanh(kt) / kt, 1.0, places=12)
            kd = diffusion_decay_constant(c)
            self.assertGreater(kd, kt)
        self.assertAlmostEqual(transport_decay_constant(0.5), 0.957504, places=6)
        self.assertAlmostEqual(diffusion_decay_constant(0.9) / transport_decay_constant(0.9), 1.042428, places=6)
        self.assertLess(diffusion_decay_constant(0.999) / transport_decay_constant(0.999), 1.0005)


class TestSolver(unittest.TestCase):
    def test_infinite_medium(self):
        phi, ll, lr = solve_fixed_source([D] * 10, [0.1] * 10, [1.0] * 10, [1.0] * 10, "reflect", "reflect")
        for p in phi:
            self.assertAlmostEqual(p, 10.0, places=12)
        self.assertEqual((ll, lr), (0.0, 0.0))

    def test_balance_on_a_random_slab(self):
        rng = random.Random(2)
        m = 60
        d = [rng.uniform(0.1, 2.0) for _ in range(m)]
        sa = [rng.uniform(0.01, 1.0) for _ in range(m)]
        q = [rng.uniform(0.0, 3.0) for _ in range(m)]
        dx = [rng.uniform(0.05, 1.0) for _ in range(m)]
        for left, right in (("marshak", "zero"), ("reflect", 0.71), ("zero", "reflect")):
            phi, ll, lr = solve_fixed_source(d, sa, q, dx, left, right)
            absorbed = sum(s * p * h for s, p, h in zip(sa, phi, dx))
            source = sum(s * h for s, h in zip(q, dx))
            self.assertAlmostEqual(absorbed + ll + lr, source, delta=1e-11 * source)
            self.assertGreater(min(phi), 0.0)

    def test_fixed_source_leakage_is_second_order(self):
        exact = slab_leakage_marshak(1.0, 0.1, D, 10.0)
        errs = []
        for m in (25, 50, 100, 200):
            _, ll, lr = solve_fixed_source([D] * m, [0.1] * m, [1.0] * m, [10.0 / m] * m)
            self.assertAlmostEqual(ll, lr, places=12)
            errs.append(abs(lr - exact))
        for a, b in zip(errs, errs[1:]):
            self.assertAlmostEqual(a / b, 4.0, delta=0.1)
        self.assertAlmostEqual(exact, 1.329219, places=6)

    def test_bare_slab_k_is_second_order(self):
        exact = bare_slab_k(0.12, 0.1, D, 20.0)
        errs = []
        for m in (20, 40, 80):
            k, phi, _ = k_eigenvalue([D] * m, [0.1] * m, [0.12] * m, [20.0 / m] * m)
            errs.append(k - exact)
            self.assertAlmostEqual(phi[m // 2 - 1], phi[m // 2], places=9)
        self.assertAlmostEqual(errs[0], 1.731e-4, delta=1e-7)
        for a, b in zip(errs, errs[1:]):
            self.assertAlmostEqual(a / b, 4.0, delta=0.05)

    def test_extrapolated_faces(self):
        m = 80
        km, _, _ = k_eigenvalue([D] * m, [0.1] * m, [0.12] * m, [20.0 / m] * m, "marshak", "marshak")
        self.assertAlmostEqual(km, bare_slab_k(0.12, 0.1, D, 20.0 + 4.0 * D), delta=5e-5)
        kl, _, _ = k_eigenvalue([D] * m, [0.1] * m, [0.12] * m, [20.0 / m] * m, MILNE, MILNE)
        self.assertAlmostEqual(kl, bare_slab_k(0.12, 0.1, D, 20.0 + 2.0 * MILNE), delta=5e-5)
        self.assertLess(km, kl)


if __name__ == "__main__":
    unittest.main()
