# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taubin-fitting/. The authors are listed in prov/4TBMTK.jsonl.

import random
import unittest
from fractions import Fraction as F
from math import cos, pi, sin, sqrt

from re1lin import nullspace
from taubin_fitting import (circle_basis, conic_basis, first_order_distance, monomials, taubin_fit)


# ---- independent helpers, written out by hand for conics ----


def conic_row(p):
    x, y = p
    return [x * x, x * y, y * y, x, y, 1]


def conic_grad_rows(p):
    x, y = p
    return [(2 * x, 0), (y, x), (0, 2 * y), (1, 0), (0, 1), (0, 0)]


def taubin_cost(a, pts):
    """sum f^2 / sum |grad f|^2 for the conic with coefficients a."""
    num = sum(sum(c * v for c, v in zip(a, conic_row(p))) ** 2 for p in pts)
    den = 0.0
    for p in pts:
        g = conic_grad_rows(p)
        gx = sum(c * r[0] for c, r in zip(a, g))
        gy = sum(c * r[1] for c, r in zip(a, g))
        den += gx * gx + gy * gy
    return float(num) / float(den)


def same_up_to_sign(a, b, tol):
    nb = sqrt(sum(float(v) ** 2 for v in b))
    bu = [float(v) / nb for v in b]
    d1 = max(abs(x - y) for x, y in zip(a, bu))
    d2 = max(abs(x + y) for x, y in zip(a, bu))
    return min(d1, d2) <= tol


def circle_of(a):
    A, B, C, D = a
    cx, cy = -B / (2 * A), -C / (2 * A)
    return cx, cy, sqrt(cx * cx + cy * cy - D / A)


def rational_unit_circle(s):
    s = F(s)
    return (1 - s * s) / (1 + s * s), 2 * s / (1 + s * s)


def rational_unit_hyperbola(s):
    s = F(s)
    return (s + 1 / s) / 2, (s - 1 / s) / 2


def affine_conic(B, h, signs):
    """Coefficients of sum_k signs[k] * (B_k . p + h_k)^2 - 1 on x^2, xy, y^2, x, y, 1."""
    a = [F(0)] * 6
    for k in range(2):
        b0, b1, hk, sg = B[k][0], B[k][1], h[k], signs[k]
        a[0] += sg * b0 * b0
        a[1] += sg * 2 * b0 * b1
        a[2] += sg * b1 * b1
        a[3] += sg * 2 * b0 * hk
        a[4] += sg * 2 * b1 * hk
        a[5] += sg * hk * hk
    a[5] -= 1
    return a


class TestWorkedExample(unittest.TestCase):
    def test_ellipse_of_the_page(self):
        pts = [(F(2), F(0)), (F(8, 5), F(3, 5)), (F(6, 5), F(4, 5)), (F(0), F(1)), (F(-6, 5), F(4, 5)),
               (F(6, 5), F(-4, 5))]
        truth = [1, 0, 4, 0, 0, -4]
        # exact: the design matrix has the one-dimensional null space spanned by the true conic
        ns = nullspace([conic_row(p) for p in pts])
        self.assertEqual(len(ns), 1)
        self.assertEqual([v / ns[0][0] for v in ns[0]], truth)
        a, lam = taubin_fit(pts, conic_basis())
        self.assertTrue(same_up_to_sign(a, truth, 1e-10))
        self.assertLess(lam, 1e-12)

    def test_monomials(self):
        self.assertEqual(len(monomials(2, 2)), 6)
        self.assertEqual(len(monomials(3, 2)), 10)
        self.assertEqual(len(monomials(3, 4)), 35)
        self.assertEqual(monomials(2, 2)[-1], {(0, 0): 1})
        self.assertEqual(monomials(2, 2)[0], {(2, 0): 1})


class TestNoiseFree(unittest.TestCase):
    def test_random_ellipses_and_hyperbolas_exact(self):
        rng = random.Random(7)
        for trial in range(40):
            while True:
                B = [[F(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(2)] for _ in range(2)]
                if B[0][0] * B[1][1] - B[0][1] * B[1][0] != 0:
                    break
            h = [F(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(2)]
            hyper = trial % 2 == 1
            signs = (1, -1) if hyper else (1, 1)
            truth = affine_conic(B, h, signs)
            det = B[0][0] * B[1][1] - B[0][1] * B[1][0]
            inv = [[B[1][1] / det, -B[0][1] / det], [-B[1][0] / det, B[0][0] / det]]
            params = rng.sample([F(n, d) for n in range(-9, 10) for d in (1, 2, 3, 5) if n != 0], 7)
            pts = []
            for s in params:
                q = rational_unit_hyperbola(s) if hyper else rational_unit_circle(s)
                q = (q[0] - h[0], q[1] - h[1])          # p = B^-1 (q - h)
                pts.append((inv[0][0] * q[0] + inv[0][1] * q[1], inv[1][0] * q[0] + inv[1][1] * q[1]))
            # exact: every point is on the true conic, and the points fix it
            for p in pts:
                self.assertEqual(sum(c * v for c, v in zip(truth, conic_row(p))), 0)
            self.assertEqual(len(nullspace([conic_row(p) for p in pts])), 1)
            a, lam = taubin_fit(pts, conic_basis())
            self.assertTrue(same_up_to_sign(a, truth, 1e-7), (trial, a, truth))
            self.assertLess(lam, 1e-9)

    def test_five_points_fix_a_conic(self):
        pts = [(F(x), F(y)) for x, y in [(2, 0), (F(6, 5), F(4, 5)), (0, 1), (F(-6, 5), F(4, 5)), (-2, 0)]]
        a, lam = taubin_fit(pts, conic_basis())
        self.assertTrue(same_up_to_sign(a, [1, 0, 4, 0, 0, -4], 1e-9))

    def test_circle_on_a_short_arc(self):
        units = [(F(4, 5), F(3, 5)), (F(12, 13), F(5, 13)), (F(15, 17), F(8, 17)), (F(24, 25), F(7, 25)), (1, 0)]
        pts = [(3 + 5 * c, -2 + 5 * s) for c, s in units]
        cx, cy, r = circle_of(taubin_fit(pts, circle_basis())[0])
        self.assertAlmostEqual(cx, 3, places=8)
        self.assertAlmostEqual(cy, -2, places=8)
        self.assertAlmostEqual(r, 5, places=8)

    def test_sphere(self):
        units = [(1, 2, 2), (2, 3, 6), (2, 6, 9), (1, 4, 8), (4, 4, 7), (6, 6, 7), (-1, 2, -2)]
        pts = []
        for u in units:
            n = sqrt(sum(v * v for v in u))
            pts.append(tuple(c + 2 * F(v) / int(round(n)) for c, v in zip((1, -1, 3), u)))
        a, lam = taubin_fit(pts, circle_basis(3))
        A = a[0]
        c = [-a[k] / (2 * A) for k in (1, 2, 3)]
        r = sqrt(sum(v * v for v in c) - a[4] / A)
        for got, want in zip(c, (1, -1, 3)):
            self.assertAlmostEqual(got, want, places=8)
        self.assertAlmostEqual(r, 2, places=8)

    def test_family_without_constant(self):
        # lines through the origin, a x + b y = 0: no constant, the elimination step is skipped
        basis = [{(1, 0): 1}, {(0, 1): 1}]
        pts = [(4, 3), (8, 6), (-4, -3), (F(2), F(3, 2))]
        a, lam = taubin_fit(pts, basis)
        self.assertTrue(same_up_to_sign(a, [3, -4], 1e-12))


class TestEdgeCases(unittest.TestCase):
    def test_collinear_points_are_rejected_for_conics(self):
        pts = [(i, 2 * i + 1) for i in range(6)]
        with self.assertRaises(ValueError):
            taubin_fit(pts, conic_basis())

    def test_two_constants_are_rejected(self):
        with self.assertRaises(ValueError):
            taubin_fit([(0, 0), (1, 0), (0, 1)], [{(1, 0): 1}, {(0, 0): 1}, {(0, 0): 2}])

    def test_constant_not_last_is_rejected(self):
        with self.assertRaises(ValueError):
            taubin_fit([(0, 0), (1, 0), (0, 1)], [{(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}])


class TestFirstOrderDistance(unittest.TestCase):
    def test_circle_closed_form(self):
        basis = circle_basis()
        a = [1, 0, 0, -1]
        for d in (0.1, 0.01, 0.001, -0.01):
            got = first_order_distance(a, basis, (1 + d, 0.0))
            self.assertAlmostEqual(got - abs(d), -d * d / (2 * (1 + d)) * (1 if d > 0 else -1), places=12)
            self.assertLessEqual(abs(got - abs(d)), d * d)

    def test_ellipse_against_brute_force_distance(self):
        # f = x^2 / 4 + y^2 - 1: Hessian bound K = 2, gradient on the curve at least g = 1, bound 6 delta^2
        basis = conic_basis()
        a = [0.25, 0, 1, 0, 0, -1]
        rng = random.Random(11)

        def dist(p):
            best = min(range(4000), key=lambda k: (p[0] - 2 * cos(2 * pi * k / 4000)) ** 2
                       + (p[1] - sin(2 * pi * k / 4000)) ** 2)
            lo, hi = 2 * pi * (best - 1) / 4000, 2 * pi * (best + 1) / 4000
            for _ in range(80):
                m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
                f1 = (p[0] - 2 * cos(m1)) ** 2 + (p[1] - sin(m1)) ** 2
                f2 = (p[0] - 2 * cos(m2)) ** 2 + (p[1] - sin(m2)) ** 2
                if f1 < f2:
                    hi = m2
                else:
                    lo = m1
            t = (lo + hi) / 2
            return sqrt((p[0] - 2 * cos(t)) ** 2 + (p[1] - sin(t)) ** 2)

        for _ in range(60):
            t = rng.uniform(0, 2 * pi)
            nx, ny = cos(t) / 2, 2 * sin(t) / 2       # gradient direction at (2 cos t, sin t)
            nn = sqrt(nx * nx + ny * ny)
            s = rng.uniform(-0.05, 0.05)
            p = (2 * cos(t) + s * nx / nn, sin(t) + s * ny / nn)
            delta = dist(p)
            self.assertLessEqual(abs(first_order_distance(a, basis, p) - delta), 6 * delta * delta + 1e-12)


class TestRandomizedNoisy(unittest.TestCase):
    def test_global_minimum_against_other_coefficients(self):
        rng = random.Random(2026)
        for trial in range(25):
            pts = []
            a0, b0 = rng.uniform(1, 3), rng.uniform(0.5, 1.5)
            for i in range(25):
                t = rng.uniform(0, 1.5 * pi)
                pts.append((a0 * cos(t) + rng.gauss(0, 0.05), b0 * sin(t) + rng.gauss(0, 0.05)))
            a, lam = taubin_fit(pts, conic_basis())
            q = taubin_cost(a, pts)
            self.assertAlmostEqual(q, lam, delta=1e-9 * max(1.0, lam))
            self.assertLessEqual(q, taubin_cost([1 / a0 ** 2, 0, 1 / b0 ** 2, 0, 0, -1], pts) + 1e-12)
            for _ in range(200):
                other = [v + rng.gauss(0, 0.05) for v in a]
                self.assertLessEqual(q, taubin_cost(other, pts) + 1e-12)
                other = [rng.gauss(0, 1) for _ in a]
                self.assertLessEqual(q, taubin_cost(other, pts) + 1e-12)

    def test_generalized_eigen_equation(self):
        rng = random.Random(5)
        pts = [(rng.uniform(-2, 2), rng.uniform(-1, 1)) for _ in range(30)]
        a, lam = taubin_fit(pts, conic_basis())
        M = [[0.0] * 6 for _ in range(6)]
        N = [[0.0] * 6 for _ in range(6)]
        for p in pts:
            u = conic_row(p)
            g = conic_grad_rows(p)
            for j in range(6):
                for k in range(6):
                    M[j][k] += u[j] * u[k]
                    N[j][k] += g[j][0] * g[k][0] + g[j][1] * g[k][1]
        for j in range(6):
            lhs = sum(M[j][k] * a[k] for k in range(6))
            rhs = lam * sum(N[j][k] * a[k] for k in range(6))
            self.assertAlmostEqual(lhs, rhs, delta=1e-8 * max(1.0, max(abs(v) for v in M[j])))

    def test_invariance_under_similarity(self):
        rng = random.Random(3)
        for _ in range(20):
            pts = []
            for i in range(15):
                t = rng.uniform(0, pi / 2)
                pts.append((1 + 2 * cos(t) + rng.gauss(0, 0.03), -1 + 2 * sin(t) + rng.gauss(0, 0.03)))
            cx, cy, r = circle_of(taubin_fit(pts, circle_basis())[0])
            th, s, tx, ty = rng.uniform(0, 2 * pi), rng.uniform(0.2, 5), rng.uniform(-9, 9), rng.uniform(-9, 9)

            def T(p):
                return (s * (cos(th) * p[0] - sin(th) * p[1]) + tx, s * (sin(th) * p[0] + cos(th) * p[1]) + ty)

            dx, dy, dr = circle_of(taubin_fit([T(p) for p in pts], circle_basis())[0])
            ex, ey = T((cx, cy))
            self.assertAlmostEqual(dx, ex, delta=1e-7 * s)
            self.assertAlmostEqual(dy, ey, delta=1e-7 * s)
            self.assertAlmostEqual(dr, s * r, delta=1e-7 * s)


if __name__ == "__main__":
    unittest.main()
