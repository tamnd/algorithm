# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/householder-methods/. The authors are listed in prov/M9RH7W.jsonl.

import math
import random
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction

from householder_methods import householder, householder_step, poly_derivs

CUBIC = [1, 0, -2, -5]  # x^3 - 2x - 5, root 2.0945514815423265...
ROOT = 2.0945514815423265


class TestHouseholder(unittest.TestCase):
    def test_converges_for_each_order(self):
        for d in range(1, 7):
            r = householder(poly_derivs(CUBIC, d), 2.0, d)
            self.assertTrue(r.converged, (d, r.status))
            self.assertAlmostEqual(r.root, ROOT, delta=1e-15)
            self.assertEqual(r.evaluations, len(r.iterates) - 1 + (r.status == "exact"))

    def test_step_counts_fall_with_order(self):
        steps = [householder(poly_derivs(CUBIC, d), 2.0, d).iterations for d in range(1, 7)]
        self.assertEqual(steps, [5, 4, 3, 3, 3, 3])

    def test_d1_is_newton_and_d2_is_halley(self):
        f = lambda x: x ** 3 - 2 * x - 5
        df = lambda x: 3 * x * x - 2
        d2f = lambda x: 6 * x
        x = Fraction(2)
        n = householder(poly_derivs([Fraction(c) for c in CUBIC], 1), x, 1, tol=0, max_iter=2)
        h = householder(poly_derivs([Fraction(c) for c in CUBIC], 2), x, 2, tol=0, max_iter=2)
        xn, xh = x, x
        for k in range(2):
            xn = xn - f(xn) / df(xn)
            xh = xh - 2 * f(xh) * df(xh) / (2 * df(xh) ** 2 - f(xh) * d2f(xh))
            self.assertEqual(n.iterates[k + 1], xn)
            self.assertEqual(h.iterates[k + 1], xh)

    def test_observed_order_is_d_plus_1(self):
        with localcontext() as ctx:
            ctx.prec = 400
            cs = [Decimal(c) for c in CUBIC]
            nd = poly_derivs(cs, 1)
            r = Decimal(2)
            for _ in range(12):
                v = nd(r)
                r -= v[0] / v[1]
            for d in range(1, 6):
                res = householder(poly_derivs(cs, d), Decimal(2), d, tol=Decimal(10) ** -380, max_iter=3)
                e = [abs(x - r) for x in res.iterates[:4]]
                q = (e[3].ln() - e[2].ln()) / (e[2].ln() - e[1].ln())
                self.assertAlmostEqual(float(q), d + 1, delta=0.01)

    def test_error_constant(self):
        # e_{k+1} / e_k^(d+1) -> (-1)^d f'(x*) psi_d with psi = 1/phi, phi = f/(x - x*)
        with localcontext() as ctx:
            ctx.prec = 300
            cs = [Decimal(c) for c in CUBIC]
            nd = poly_derivs(cs, 1)
            r = Decimal(2)
            for _ in range(12):
                v = nd(r)
                r -= v[0] / v[1]
            p0, p1 = 3 * r * r - 2, 3 * r
            psi = [1 / p0]
            for n in range(1, 4):
                psi.append(-(p1 * psi[n - 1] + (psi[n - 2] if n >= 2 else 0)) / p0)
            for d in (1, 2, 3):
                res = householder(poly_derivs(cs, d), Decimal(2), d, tol=0, max_iter=6)
                e = [x - r for x in res.iterates]
                k = max(i for i in range(len(e) - 1) if abs(e[i + 1]) > Decimal(10) ** -250)
                ratio = e[k + 1] / e[k] ** (d + 1)
                self.assertAlmostEqual(float(ratio), float((-1) ** d * p0 * psi[d]), places=5)

    def test_multiple_root_rate(self):
        # (x - 1)^m (x + 2): rate (m - 1) / (m + d - 1)
        for m in (2, 3):
            cs = [1]
            for _ in range(m):
                cs = [a - b for a, b in zip(cs + [0], [0] + cs)]
            cs = [a + 2 * b for a, b in zip(cs + [0], [0] + cs)]
            with localcontext() as ctx:
                ctx.prec = 60
                for d in (1, 2, 3):
                    res = householder(poly_derivs([Decimal(c) for c in cs], d), Decimal(2), d, tol=0, max_iter=40)
                    e = [x - 1 for x in res.iterates]
                    self.assertAlmostEqual(float(e[-1] / e[-2]), (m - 1) / (m + d - 1), delta=1e-6)

    def test_pure_power_exact_ratio(self):
        for m in (2, 3, 4):
            for d in (1, 2, 3):
                res = householder(lambda x: [math.perm(m, j) * x ** (m - j) for j in range(d + 1)],
                                  Fraction(1), d, tol=0, max_iter=4)
                for a, b in zip(res.iterates, res.iterates[1:]):
                    self.assertEqual(b, a * Fraction(m - 1, m + d - 1))

    def test_root_at_start(self):
        r = householder(poly_derivs([1, 0, -4], 3), 2.0, 3)
        self.assertEqual((r.status, r.root, r.iterations, r.evaluations), ("exact", 2.0, 0, 1))

    def test_zero_derivative(self):
        derivs = poly_derivs([1, 0, -2], 3)
        self.assertEqual(householder(derivs, 0.0, 1).status, "zero-denominator")  # Newton divides by f'
        self.assertEqual(householder(derivs, 0.0, 2).status, "stalled")  # Halley's step is 0

    def test_no_real_root_hits_max_iter(self):
        r = householder(poly_derivs([1, 0, 1], 2), 0.5, 2, max_iter=50)
        self.assertEqual((r.status, r.iterations, r.evaluations), ("max-iter", 50, 50))

    def test_non_finite_raises(self):
        with self.assertRaises(ArithmeticError):
            householder(lambda x: [float("nan"), 1.0, 0.0], 1.0, 2)
        with self.assertRaises(ArithmeticError):
            householder(lambda x: [math.inf, 1.0, 0.0], 1.0, 2)
        with self.assertRaises(ValueError):
            householder(poly_derivs(CUBIC, 1), 2.0, 2)
        with self.assertRaises(ValueError):
            householder(poly_derivs(CUBIC, 1), 2.0, 0)

    def test_transcendental(self):
        # f = exp(x) - 2: all derivatives equal exp(x)
        for d in range(1, 6):
            r = householder(lambda x: [math.exp(x) - 2] + [math.exp(x)] * d, 0.0, d)
            self.assertTrue(r.converged)
            self.assertAlmostEqual(r.root, math.log(2), delta=1e-15)

    def test_step_helper(self):
        a0, b1, b2 = householder_step([2.0, 3.0, 4.0], 2)
        self.assertEqual((a0, b1, b2), (2.0, -3.0, 9.0 - 2.0 * 2.0))

    def test_random_cubics(self):
        rng = random.Random(20261107)
        for _ in range(600):
            roots = sorted(rng.uniform(-10, 10) for _ in range(3))
            if min(roots[1] - roots[0], roots[2] - roots[1]) < 0.5:
                continue
            a, b, c = roots
            cs = [1, -(a + b + c), a * b + b * c + a * c, -a * b * c]
            i = rng.randrange(3)
            gap = min(abs(roots[i] - roots[j]) for j in range(3) if j != i)
            x0 = roots[i] + rng.uniform(-0.1, 0.1) * gap
            d = rng.randint(1, 5)
            r = householder(poly_derivs(cs, d), x0, d, max_iter=60)
            self.assertTrue(r.converged, (roots, x0, d, r.status))
            self.assertAlmostEqual(r.root, roots[i], delta=1e-9 * (1 + abs(roots[i])))
            self.assertLessEqual(r.evaluations, 12)


if __name__ == "__main__":
    unittest.main()
