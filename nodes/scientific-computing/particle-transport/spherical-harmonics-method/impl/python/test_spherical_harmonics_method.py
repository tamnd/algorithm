# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spherical-harmonics-method/. The authors are listed in prov/HXR9T4.jsonl.
import math
import random
import unittest

from spherical_harmonics_method import (gauss_legendre, legendre_all, moment_matrix, pn_decay_constant,
                                        pn_slab, sn_slab)


def uniform(m, length, c=0.9):
    return [1.0] * m, [c] * m, [1.0] * m, [length / m] * m


class TestMoments(unittest.TestCase):
    def test_eigenvalues_are_gauss_nodes(self):
        for n in (1, 3, 5, 7, 9):
            a = moment_matrix(n)
            mus, _ = gauss_legendre(n + 1)
            for mu in mus:
                v = legendre_all(n, mu)
                av = [sum(a[l][c] * v[c] for c in range(n + 1)) for l in range(n + 1)]
                for l in range(n + 1):
                    self.assertAlmostEqual(av[l], mu * v[l], places=12)

    def test_decay_constants(self):
        for c in (0.5, 0.9, 0.99):
            self.assertAlmostEqual(pn_decay_constant(1, c), math.sqrt(3.0 * (1.0 - c)), places=12)
        values = [pn_decay_constant(n, 0.5) for n in (1, 3, 5, 7, 15)]
        for a, b in zip(values, values[1:]):
            self.assertGreater(a, b)
        self.assertAlmostEqual(values[-1], 0.957504, delta=3e-5)
        for n in (3, 7):
            k = pn_decay_constant(n, 0.5)
            mus, ws = gauss_legendre(n + 1)
            self.assertAlmostEqual(0.25 * sum(w / (1.0 - (k * mu) ** 2) for mu, w in zip(mus, ws)), 1.0, places=10)


class TestSlab(unittest.TestCase):
    def test_mark_equals_s_n_plus_1(self):
        for n in (1, 3, 5):
            st, ss, q, dx = uniform(40, 4.0)
            p = pn_slab(n, st, ss, q, dx, bc="mark")
            phi, _, leak = sn_slab(n + 1, st, ss, q, dx)
            for a, b in zip(p["phi"], phi):
                self.assertAlmostEqual(a, b, delta=1e-9)
            self.assertAlmostEqual(p["leak_right"], leak, delta=1e-9)
        p = pn_slab(3, st, ss, q, dx, "reflect", "vacuum", bc="mark")
        phi, _, leak = sn_slab(4, st, ss, q, dx, "reflect", "vacuum")
        for a, b in zip(p["phi"], phi):
            self.assertAlmostEqual(a, b, delta=1e-9)

    def test_mark_equals_s_n_plus_1_heterogeneous(self):
        rng = random.Random(3)
        m = 30
        st = [rng.uniform(0.5, 4.0) for _ in range(m)]
        ss = [s * rng.uniform(0.0, 0.9) for s in st]
        q = [rng.uniform(0.0, 2.0) for _ in range(m)]
        dx = [rng.uniform(0.05, 0.5) for _ in range(m)]
        p = pn_slab(5, st, ss, q, dx, bc="mark")
        phi, ll, lr = sn_slab(6, st, ss, q, dx)
        for a, b in zip(p["phi"], phi):
            self.assertAlmostEqual(a, b, delta=1e-9 * max(phi))
        self.assertAlmostEqual(p["leak_left"], ll, delta=1e-9)

    def test_p1_marshak_is_diffusion(self):
        st, ss, q, dx = uniform(200, 10.0)
        p = pn_slab(1, st, ss, q, dx)
        kappa, d, half = math.sqrt(0.3), 1.0 / 3.0, 5.0
        b = 1.0 / (2.0 * d * kappa * math.sinh(kappa * half) + math.cosh(kappa * half))
        self.assertAlmostEqual(p["leak_right"], 10.0 * (1.0 - b * math.cosh(kappa * half)) / 2.0, delta=1e-5)
        self.assertAlmostEqual(p["leak_right"], 1.329219, delta=1e-5)

    def test_balance(self):
        rng = random.Random(8)
        m = 50
        st = [rng.uniform(0.5, 4.0) for _ in range(m)]
        ss = [s * rng.uniform(0.5, 0.99) for s in st]
        q = [rng.uniform(0.0, 2.0) for _ in range(m)]
        dx = [rng.uniform(0.05, 0.5) for _ in range(m)]
        for bc in ("marshak", "mark"):
            p = pn_slab(7, st, ss, q, dx, "vacuum", "vacuum", bc)
            absorbed = sum((a - b) * f * h for a, b, f, h in zip(st, ss, p["phi"], dx))
            source = sum(a * h for a, h in zip(q, dx))
            self.assertAlmostEqual(absorbed + p["leak_left"] + p["leak_right"], source, delta=1e-10)

    def test_infinite_medium(self):
        p = pn_slab(5, [1.0] * 10, [0.9] * 10, [1.0] * 10, [1.0] * 10, "reflect", "reflect")
        for v in p["phi"]:
            self.assertAlmostEqual(v, 10.0, places=10)
        for mom in p["moments"]:
            for v in mom[1:]:
                self.assertAlmostEqual(v, 0.0, places=10)

    def test_convergence_in_n(self):
        st, ss, q, dx = uniform(200, 2.0)
        ref = 0.743626  # S16 with the same mesh
        errors = [abs(pn_slab(n, st, ss, q, dx)["leak_right"] - ref) for n in (1, 3, 5, 7)]
        for a, b in zip(errors, errors[1:]):
            self.assertGreater(a, b)
        self.assertLess(errors[-1], 5e-4)
        self.assertGreater(errors[0], 0.02)

    def test_even_n_rejected(self):
        with self.assertRaises(ValueError):
            pn_slab(2, [1.0], [0.5], [1.0], [1.0])


if __name__ == "__main__":
    unittest.main()
