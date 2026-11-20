# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-iteration/. The authors are listed in prov/ZGYN85.jsonl.
import math
import random
import unittest

from source_iteration import (dd_sweep, error_bound, fourier_continuous, fourier_dd, fourier_sn,
                              gauss_legendre, source_iteration, sweep_all)


def weighted_norm(v, sigma_t, dx):
    return math.sqrt(sum(s * x * x * h for x, s, h in zip(v, sigma_t, dx)))


class TestInfiniteMedium(unittest.TestCase):
    def test_iterates_are_the_neumann_series(self):
        # reflecting faces, sigma_t = 1, c = 0.5, q = 1: phi_l = 1 + c + ... + c^(l-1)
        for l in range(1, 6):
            r = source_iteration(2, [1.0, 1.0], [0.5, 0.5], [1.0, 1.0], [1.0, 1.0],
                                 "reflect", "reflect", tol=0.0, max_iter=l)
            exact = (1.0 - 0.5 ** l) / 0.5
            for p in r["phi"]:
                self.assertAlmostEqual(p, exact, places=13)

    def test_error_falls_by_exactly_c(self):
        for c in (0.5, 0.9, 0.99):
            r = source_iteration(8, [1.0] * 10, [c] * 10, [1.0] * 10, [0.5] * 10,
                                 "reflect", "reflect", tol=0.0, max_iter=20)
            ch = r["changes"]
            for i in range(len(ch) - 1):
                self.assertAlmostEqual(ch[i + 1] / ch[i], c, places=7)

    def test_error_is_c_over_one_minus_c_times_the_last_change(self):
        for c in (0.5, 0.9, 0.99):
            r = source_iteration(2, [1.0] * 2, [c] * 2, [1.0] * 2, [1.0] * 2, "reflect", "reflect", tol=1e-8)
            exact = 1.0 / (1.0 - c)
            err = exact - r["phi"][0]
            self.assertAlmostEqual(err / r["changes"][-1], c / (1.0 - c), delta=1e-5 * c / (1.0 - c))
            self.assertAlmostEqual(error_bound(r["changes"][-1], c), err, delta=1e-5 * err)

    def test_iteration_count(self):
        # the change test stops at the first l with c^(l-1) (1 - c) / (1 - c^l) <= tol
        for c, expected in ((0.5, 27), (0.9, 154), (0.99, 1376)):
            r = source_iteration(2, [1.0] * 2, [c] * 2, [1.0] * 2, [1.0] * 2, "reflect", "reflect", tol=1e-8)
            self.assertEqual(r["iterations"], expected)


class TestFourier(unittest.TestCase):
    def test_continuous_factor(self):
        self.assertEqual(fourier_continuous(0.0, 0.9), 0.9)
        self.assertAlmostEqual(fourier_continuous(1.0, 1.0), math.pi / 4.0, places=15)
        for lam in (0.1, 1.0, 3.0, 30.0):
            self.assertLess(fourier_continuous(lam, 1.0), 1.0)
        mus, ws = gauss_legendre(64)
        for lam in (0.5, 2.0, 5.0):
            self.assertAlmostEqual(fourier_sn(lam, 0.8, mus, ws), fourier_continuous(lam, 0.8), places=6)

    def test_reflecting_slab_cosine_modes_are_eigenvectors(self):
        m, h, c = 40, 0.5, 0.9
        mus, ws = gauss_legendre(8)
        for k in (0, 1, 3, 10, 39):
            theta = math.pi * k / m
            e = [math.cos(theta * (j + 0.5)) for j in range(m)]
            r = source_iteration(8, [1.0] * m, [c] * m, [0.0] * m, [h] * m, "reflect", "reflect",
                                 tol=0.0, max_iter=1, phi0=e)
            omega = fourier_dd(theta, c, h, mus, ws)
            for j in range(m):
                self.assertAlmostEqual(r["phi"][j], omega * e[j], places=12)
            self.assertLessEqual(omega, c + 1e-15)

    def test_thin_cells_approach_the_sn_factor(self):
        mus, ws = gauss_legendre(8)
        lam = 1.5
        for tau in (0.1, 0.01):
            theta = 2.0 * math.atan(lam * tau / 2.0)
            self.assertAlmostEqual(fourier_dd(theta, 1.0, tau, mus, ws), fourier_sn(lam, 1.0, mus, ws), places=12)


class TestSlab(unittest.TestCase):
    def test_rate_approaches_c_in_a_thick_slab(self):
        rates = []
        for length in (1.0, 10.0, 100.0):
            m = int(length / 0.25)
            r = source_iteration(8, [1.0] * m, [0.99] * m, [0.0] * m, [0.25] * m, tol=0.0, max_iter=300,
                                 phi0=[1.0] * m)
            ch = r["changes"]
            rates.append(ch[-1] / ch[-2])
        self.assertLess(rates[0], 0.65)
        self.assertLess(rates[0], rates[1])
        self.assertLess(rates[1], rates[2])
        self.assertLess(rates[2], 0.99)
        self.assertGreater(rates[2], 0.985)

    def test_contraction_in_weighted_norm(self):
        rng = random.Random(7)
        m = 30
        st = [rng.uniform(0.5, 3.0) for _ in range(m)]
        ss = [s * rng.uniform(0.0, 0.95) for s in st]
        dx = [rng.uniform(0.05, 1.5) for _ in range(m)]
        c = max(b / a for a, b in zip(st, ss))
        exact = source_iteration(6, st, ss, [1.0] * m, dx, tol=1e-15)["phi"]
        for left, right in (("vacuum", "vacuum"), ("reflect", "vacuum"), ("vacuum", "reflect")):
            exact = source_iteration(6, st, ss, [1.0] * m, dx, left, right, tol=1e-15)["phi"]
            prev = None
            for l in range(1, 15):
                phi = source_iteration(6, st, ss, [1.0] * m, dx, left, right, tol=0.0, max_iter=l)["phi"]
                err = weighted_norm([a - b for a, b in zip(phi, exact)], st, dx)
                if prev is not None and prev > 1e-12:
                    self.assertLessEqual(err, c * prev * (1 + 1e-9))
                prev = err

    def test_balance(self):
        m, length = 40, 10.0
        r = source_iteration(8, [1.0] * m, [0.9] * m, [1.0] * m, [length / m] * m, tol=1e-13)
        absorbed = sum(0.1 * p * length / m for p in r["phi"])
        self.assertAlmostEqual(absorbed + r["leak_left"] + r["leak_right"], length, places=9)
        r = source_iteration(8, [1.0] * m, [0.9] * m, [1.0] * m, [length / m] * m, "reflect", "vacuum", tol=1e-13)
        absorbed = sum(0.1 * p * length / m for p in r["phi"])
        self.assertEqual(r["leak_left"], 0.0)
        self.assertAlmostEqual(absorbed + r["leak_right"], length, places=9)

    def test_pure_absorber_needs_one_sweep(self):
        m = 50
        r = source_iteration(4, [1.0] * m, [0.0] * m, [0.0] * m, [2.0 / m] * m, left=[1.0, 1.0], tol=1e-14)
        self.assertEqual(r["iterations"], 2)
        self.assertEqual(r["changes"][-1], 0.0)

    def test_reflection_matches_a_doubled_slab(self):
        # a slab with a reflecting right face equals the left half of a symmetric slab twice as wide
        m = 20
        st = [1.0 + 0.1 * j for j in range(m)]
        ss = [0.7 * s for s in st]
        q = [1.0 + 0.05 * j for j in range(m)]
        dx = [0.2] * m
        half = source_iteration(4, st, ss, q, dx, "vacuum", "reflect", tol=1e-14)["phi"]
        full = source_iteration(4, st + st[::-1], ss + ss[::-1], q + q[::-1], dx + dx, tol=1e-14)["phi"]
        for j in range(m):
            self.assertAlmostEqual(half[j], full[j], places=10)

    def test_incoming_data_order_on_the_right(self):
        mus, ws = gauss_legendre(4)
        m = 10
        st, dx = [1.0] * m, [0.1] * m
        src = [0.0] * m
        # incoming at x = L for the directions mu < 0 in the order of the rule: mus[0], mus[1]
        phi, leak_l, _ = sweep_all(mus, ws, st, src, dx, "vacuum", [2.0, 5.0])
        expect = 0.0
        for k, v in ((0, 2.0), (1, 5.0)):
            _, out = dd_sweep(mus[k], v, st, src, dx)
            expect += ws[k] * abs(mus[k]) * out
        self.assertAlmostEqual(leak_l, expect, places=14)


if __name__ == "__main__":
    unittest.main()
