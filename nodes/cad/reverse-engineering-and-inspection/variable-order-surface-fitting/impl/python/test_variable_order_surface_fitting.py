# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-order-surface-fitting/. The authors are listed in prov/710BVP.jsonl.

import random
import unittest
from fractions import Fraction

from re1lin import solve
from variable_order_surface_fitting import (curvatures, fit_polynomial, grow_region, hk_map, monomials,
                                            variable_order_segmentation)

N = 24
H2 = 2.0 / (N - 1)          # pixel spacing for the domain [0, 2] x [0, 2]

QUADRANT_POLYS = [
    (1, lambda x, y: 0.3 * x - 0.2 * y + 0.1),
    (2, lambda x, y: x * x + y * y + 0.5 * x * y + 3),
    (3, lambda x, y: x * x + y * y + 0.4 * x ** 3 - 0.2 * x * y * y + 6),
    (4, lambda x, y: x * x + y * y + 0.3 * x ** 4 + 0.2 * x * x * y * y - 0.1 * y ** 3 + 9),
]


def quadrant(i, j, n=N):
    return (1 if j >= n // 2 else 0) + (2 if i >= n // 2 else 0)


def quadrant_image(h, noise=0.0, rng=None):
    return [[QUADRANT_POLYS[quadrant(i, j)][1](j * h, i * h) + (rng.gauss(0, noise) if noise else 0.0)
             for j in range(N)] for i in range(N)]


def random_poly(rng, d):
    """x^2 + y^2 plus small random terms of total degree <= d, with a nonzero term of degree d."""
    coef = {m: rng.uniform(-0.05, 0.05) for m in monomials(d)}
    coef[(d, 0)] = rng.choice((-1, 1)) * rng.uniform(0.03, 0.05)
    if d >= 2:
        coef[(2, 0)] += 1.0
        coef[(0, 2)] += 1.0

    def g(x, y):
        return sum(c * x ** a * y ** b for (a, b), c in coef.items())
    return g


class TestWorkedExample(unittest.TestCase):
    def test_four_quadrants_get_their_true_orders(self):
        h = 1.0 / (N - 1)
        Z = quadrant_image(h)
        regions = variable_order_segmentation(Z, h, tol=1e-9, band=1e-7)
        self.assertEqual(len(regions), 4)
        found = {}
        for R, f, d in regions:
            quads = {quadrant(i, j) for i, j in R}
            self.assertEqual(len(quads), 1)
            q = quads.pop()
            self.assertEqual(len(R), 144)                       # the whole quadrant
            found[q] = d
            self.assertLess(max(abs(f(j * h, i * h) - Z[i][j]) for i, j in R), 1e-10)
        self.assertEqual(found, {0: 1, 1: 2, 2: 3, 3: 4})


class TestStopsAtTrueOrder(unittest.TestCase):
    def test_random_polynomial_patches(self):
        rng = random.Random(7)
        exact = trials = 0
        for d in (1, 2, 3, 4):
            for _ in range(5):
                g = random_poly(rng, d)
                Z = [[g(j * H2, i * H2) for j in range(N)] for i in range(N)]
                regions = variable_order_segmentation(Z, H2, tol=1e-9, band=1e-7)
                trials += 1
                self.assertEqual(len(regions), 1)
                R, f, order = regions[0]
                self.assertEqual(order, d)
                self.assertEqual(len(R), N * N)
                self.assertLess(max(abs(f(j * H2, i * H2) - Z[i][j]) for i, j in R), 1e-10)
                exact += 1
        self.assertEqual(exact, trials)                          # proved: every trial is exact

    def test_lower_orders_leave_a_positive_error_on_the_seed(self):
        rng = random.Random(8)
        for d in (2, 3, 4):
            g = random_poly(rng, d)
            seed = [(j * H2, i * H2, g(j * H2, i * H2)) for i in range(5) for j in range(5)]
            for lower in range(1, d):
                self.assertGreater(fit_polynomial(seed, lower)[1], 1e-7)
            self.assertLess(fit_polynomial(seed, d)[1], 1e-12)


class TestFitAgainstExactOracle(unittest.TestCase):
    def test_least_squares_matches_exact_normal_equations(self):
        rng = random.Random(9)
        for d in (1, 2, 3, 4):
            pts = [(Fraction(rng.randint(-20, 20), 10), Fraction(rng.randint(-20, 20), 10),
                    Fraction(rng.randint(-100, 100), 50)) for _ in range(30)]
            mons = monomials(d)
            rows = [[x ** a * y ** b for a, b in mons] for x, y, _ in pts]
            A = [[sum(r[i] * r[j] for r in rows) for j in range(len(mons))] for i in range(len(mons))]
            c = solve(A, [sum(r[i] * p[2] for r, p in zip(rows, pts)) for i in range(len(mons))])
            if c is None:
                continue
            f, _ = fit_polynomial([tuple(map(float, p)) for p in pts], d)
            for x, y, _ in pts:
                exact = sum(ci * x ** a * y ** b for ci, (a, b) in zip(c, mons))
                self.assertAlmostEqual(f(float(x), float(y)), float(exact), places=8)


class TestHKMap(unittest.TestCase):
    def test_surface_types_of_quadrics(self):
        h = 0.1
        cases = [(lambda x, y: x * x + y * y, "pit"), (lambda x, y: -x * x - y * y, "peak"),
                 (lambda x, y: x * x, "valley"), (lambda x, y: -y * y, "ridge"),
                 (lambda x, y: 0.2 * x - y, "flat"), (lambda x, y: x * y, "minimal"),
                 (lambda x, y: x * x - 0.5 * y * y, "saddle valley"), (lambda x, y: 0.5 * x * x - y * y, "saddle ridge")]
        for g, name in cases:
            Z = [[g((j - 5) * h, (i - 5) * h) for j in range(11)] for i in range(11)]
            self.assertEqual(hk_map(Z, h, 1e-9, 1e-9)[5][5], name, name)

    def test_curvature_formulas(self):
        # the sphere z = sqrt(1 - x^2 - y^2) at its top: H = -1, K = 1 with the upward normal
        H, K = curvatures(0.0, 0.0, -1.0, 0.0, -1.0)
        self.assertEqual((H, K), (-1.0, 1.0))
        # the cylinder z = x^2 / 2 at x = 1: curvature 1 / (1 + 1)^(3/2), mean curvature half of it
        H, K = curvatures(1.0, 0.0, 1.0, 0.0, 0.0)
        self.assertAlmostEqual(H, 0.5 / 2 ** 1.5, places=15)
        self.assertEqual(K, 0.0)


class TestEdgeCases(unittest.TestCase):
    def test_constant_image_is_one_planar_region(self):
        Z = [[2.5] * 12 for _ in range(12)]
        regions = variable_order_segmentation(Z, 0.1, 1e-9, 1e-7)
        self.assertEqual([(len(R), d) for R, _, d in regions], [(144, 1)])

    def test_too_small_for_a_seed(self):
        self.assertEqual(variable_order_segmentation([[0.0] * 6 for _ in range(6)], 0.1, 1e-9, 1e-7), [])

    def test_sphere_needs_more_than_a_quartic(self):
        # a sphere cap is no polynomial: every seed fails at order 4 and is rejected
        Z = [[(9 - (j * H2 - 1) ** 2 - (i * H2 - 1) ** 2) ** 0.5 for j in range(N)] for i in range(N)]
        self.assertEqual(variable_order_segmentation(Z, H2, 1e-9, 1e-7), [])

    def test_a_quintic_in_x_is_a_quartic_on_five_columns(self):
        # x^5 agrees with a quartic in x on 5 distinct x values, so thin strips are accepted
        Z = [[(j * H2) ** 5 + (i * H2) ** 2 + (j * H2) ** 2 for j in range(N)] for i in range(N)]
        regions = variable_order_segmentation(Z, H2, 1e-9, 1e-7)
        self.assertTrue(regions)
        for R, _, d in regions:
            self.assertEqual(d, 4)
            self.assertLessEqual(len({j for _, j in R}), 5)

    def test_region_never_enters_used_pixels(self):
        h = 1.0 / (N - 1)
        Z = [[0.0] * N for _ in range(N)]
        used = {(i, j) for i in range(N) for j in range(N) if j >= 12}
        seed = {(i, j) for i in range(5) for j in range(5)}
        R, f, d = grow_region(Z, h, seed, used, 1e-9, 1e-7)
        self.assertEqual(len(R), N * 12)
        self.assertFalse(R & used)
        self.assertEqual(d, 1)


class TestNoisy(unittest.TestCase):
    def test_measured_purity_and_coverage(self):
        # measured, not proved: with noise the regions stay inside one quadrant
        rng = random.Random(5)
        for sigma in (1e-4, 1e-3):
            Z = quadrant_image(H2, sigma, rng)
            regions = variable_order_segmentation(Z, H2, 2 * sigma, 6 * sigma, eps_h=0.1, eps_k=0.1)
            covered = 0
            for R, _, _ in regions:
                self.assertEqual(len({quadrant(i, j) for i, j in R}), 1)
                covered += len(R)
            self.assertGreaterEqual(covered / (N * N), 0.8)
            self.assertEqual(sorted(d for _, _, d in regions)[:2], [1, 2])


if __name__ == "__main__":
    unittest.main()
