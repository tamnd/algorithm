# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-ordinates-method/. The authors are listed in prov/S57PHM.jsonl.
import math
import unittest

from discrete_ordinates_method import discrete_ordinates, gauss_legendre, sweep, sweep_cell


def e3(x, k=20000):
    """E_3(x) = integral over mu in (0, 1] of mu e^(-x/mu), by the midpoint rule."""
    s = 0.0
    for i in range(k):
        m = (i + 0.5) / k
        s += m * math.exp(-x / m)
    return s / k


class TestGaussLegendre(unittest.TestCase):
    def test_weights_sum_to_two_and_rule_is_symmetric(self):
        for n in (2, 4, 8, 16):
            x, w = gauss_legendre(n)
            self.assertAlmostEqual(sum(w), 2.0, places=13)
            for i in range(n):
                self.assertAlmostEqual(x[i], -x[n - 1 - i], places=14)
                self.assertAlmostEqual(w[i], w[n - 1 - i], places=14)

    def test_exact_to_degree_2n_minus_1(self):
        for n in (2, 4, 8):
            x, w = gauss_legendre(n)
            for d in range(0, 2 * n, 2):
                got = sum(wi * xi ** d for xi, wi in zip(x, w))
                self.assertAlmostEqual(got, 2.0 / (d + 1), places=12)

    def test_known_nodes(self):
        x, w = gauss_legendre(2)
        self.assertAlmostEqual(x[1], 1.0 / math.sqrt(3.0), places=14)
        x, w = gauss_legendre(4)
        self.assertAlmostEqual(x[3], 0.8611363115940526, places=13)
        self.assertAlmostEqual(w[3], 0.3478548451374538, places=13)


class TestHandTrace(unittest.TestCase):
    def test_first_sweep_and_first_iterate(self):
        cells, out = sweep(1.0 / math.sqrt(3.0), 0.0, [1.0, 1.0], [0.5, 0.5], [1.0, 1.0])
        self.assertAlmostEqual(cells[0], 0.2320508075688773, places=12)
        self.assertAlmostEqual(cells[1], 0.4807621135331595, places=12)
        self.assertAlmostEqual(out, 0.4974226119285644, places=12)
        r = discrete_ordinates(2, [1.0, 1.0], [0.5, 0.5], [1.0, 1.0], [1.0, 1.0], tol=0.0, max_iter=1)
        self.assertAlmostEqual(r["phi"][0], 0.7128129211020369, places=12)
        self.assertAlmostEqual(r["phi"][1], 0.7128129211020369, places=12)

    def test_balance(self):
        r = discrete_ordinates(2, [1.0, 1.0], [0.5, 0.5], [1.0, 1.0], [1.0, 1.0], tol=1e-14)
        absorbed = sum(0.5 * p * 1.0 for p in r["phi"])
        self.assertAlmostEqual(absorbed + r["leak_left"] + r["leak_right"], 2.0, places=11)
        self.assertAlmostEqual(r["leak_left"], r["leak_right"], places=12)


class TestPureAbsorber(unittest.TestCase):
    def test_single_direction_is_second_order(self):
        mu = 1.0 / math.sqrt(3.0)
        exact = math.exp(-2.0 / mu)
        errs = []
        for m in (8, 16, 32):
            _, out = sweep(mu, 1.0, [1.0] * m, [0.0] * m, [2.0 / m] * m)
            errs.append(abs(out - exact))
        for a, b in zip(errs, errs[1:]):
            self.assertAlmostEqual(math.log2(a / b), 2.0, delta=0.05)

    def test_normal_beam_transmission(self):
        # one direction with mu = 1 is not in the rule, so sweep it directly
        m = 400
        _, out = sweep(1.0, 1.0, [1.0] * m, [0.0] * m, [2.0 / m] * m)
        self.assertAlmostEqual(out, math.exp(-2.0), delta=2e-6)
        self.assertAlmostEqual(math.exp(-2.0), 0.135335, places=6)

    def test_isotropic_incidence_converges_in_angle(self):
        exact = 2.0 * e3(2.0)
        m = 200
        errs = []
        for n in (2, 4, 8, 16):
            x, w = gauss_legendre(n)
            r = discrete_ordinates(n, [1.0] * m, [0.0] * m, [0.0] * m, [2.0 / m] * m, left=[1.0] * (n // 2))
            jin = sum(w[k] * x[k] for k in range(n) if x[k] > 0)
            errs.append(abs(r["leak_right"] / jin - exact))
        for a, b in zip(errs, errs[1:]):
            self.assertLess(b, a)
        self.assertLess(errs[-1], 3e-4)


class TestScattering(unittest.TestCase):
    def test_infinite_medium(self):
        # reflecting faces: phi = q / sigma_a = 1 / 0.5 = 2
        r = discrete_ordinates(8, [1.0] * 10, [0.5] * 10, [1.0] * 10, [0.5] * 10,
                               left="reflect", right="reflect", tol=1e-13)
        for p in r["phi"]:
            self.assertAlmostEqual(p, 2.0, places=11)

    def test_balance_with_strong_scattering(self):
        m, length = 40, 10.0
        r = discrete_ordinates(8, [1.0] * m, [0.9] * m, [1.0] * m, [length / m] * m, tol=1e-13)
        absorbed = sum(0.1 * p * length / m for p in r["phi"])
        self.assertAlmostEqual(absorbed + r["leak_left"] + r["leak_right"], length, places=9)

    def test_leakage_is_second_order_in_space(self):
        length = 10.0
        leaks = []
        for m in (20, 40, 80):
            r = discrete_ordinates(8, [1.0] * m, [0.9] * m, [1.0] * m, [length / m] * m, tol=1e-13)
            leaks.append(r["leak_left"])
        p = math.log2((leaks[0] - leaks[1]) / (leaks[1] - leaks[2]))
        self.assertAlmostEqual(p, 2.0, delta=0.2)


class TestNegativeFlux(unittest.TestCase):
    def test_thick_cell_gives_negative_outgoing_flux(self):
        c, out = sweep_cell(0.1, 1.0, 1.0, 0.0, 1.0)
        self.assertAlmostEqual(c, 0.2 / 1.2, places=14)
        self.assertAlmostEqual(out, -0.8 / 1.2, places=14)
        self.assertLess(out, 0.0)


if __name__ == "__main__":
    unittest.main()
