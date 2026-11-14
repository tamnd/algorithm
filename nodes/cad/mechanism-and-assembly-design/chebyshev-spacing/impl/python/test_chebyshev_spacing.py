# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-spacing/. The authors are listed in prov/PFRWQN.jsonl.

import cmath
import math
import random
import unittest

from chebyshev_spacing import (
    Generator,
    chebyshev_bound,
    chebyshev_design,
    chebyshev_points,
    equal_points,
    link_lengths,
    node_polynomial,
    output_angle,
    solve3,
    wrap,
)


def cheb_t(n, t):
    """Oracle: T_n(t) by the three-term recurrence T_{k+1} = 2t T_k - T_{k-1}."""
    if n == 0:
        return 1.0
    prev, cur = 1.0, t
    for _ in range(n - 1):
        prev, cur = cur, 2.0 * t * cur - prev
    return cur


def roots_by_bisection(n, grid=20000):
    """Oracle: the zeros of T_n on [-1, 1], found by sign changes and bisection."""
    out = []
    ts = [-1.0 + 2.0 * i / grid for i in range(grid + 1)]
    for lo, hi in zip(ts, ts[1:]):
        flo, fhi = cheb_t(n, lo), cheb_t(n, hi)
        if flo == 0.0:
            out.append(lo)
            continue
        if flo * fhi < 0.0:
            for _ in range(80):
                mid = (lo + hi) / 2.0
                if cheb_t(n, lo) * cheb_t(n, mid) <= 0.0:
                    hi = mid
                else:
                    lo = mid
            out.append((lo + hi) / 2.0)
    return out


def output_by_circles(a, b, c, d, phi, near):
    """Oracle: psi from the intersection of circle(A, b) and circle(O4, c), the point nearest to `near`."""
    pa = a * cmath.exp(1j * phi)
    o4 = complex(d, 0.0)
    dist = abs(o4 - pa)
    x = (b * b - c * c + dist * dist) / (2.0 * dist)
    h2 = b * b - x * x
    if h2 < 0.0:
        return None
    e = (o4 - pa) / dist
    cands = [pa + e * complex(x, s * math.sqrt(h2)) for s in (1.0, -1.0)]
    psis = [cmath.phase(p - o4) for p in cands]
    return min(psis, key=lambda v: abs(wrap(v - near)))


class TestPoints(unittest.TestCase):
    def test_zeros_of_t_n(self):
        for n in range(1, 13):
            xs = chebyshev_points(-1.0, 1.0, n)
            for x in xs:
                self.assertLess(abs(cheb_t(n, x)), 1e-12)
            oracle = roots_by_bisection(n)
            self.assertEqual(len(oracle), n)
            for x, y in zip(xs, oracle):
                self.assertAlmostEqual(x, y, delta=1e-12)

    def test_mapping_is_affine(self):
        rng = random.Random(11)
        for _ in range(200):
            a = rng.uniform(-5, 5)
            b = a + rng.uniform(0.1, 10)
            n = rng.randint(1, 9)
            xs = chebyshev_points(a, b, n)
            ts = chebyshev_points(-1.0, 1.0, n)
            self.assertEqual(xs, sorted(xs))
            for x, t in zip(xs, ts):
                self.assertAlmostEqual(x, (a + b) / 2 + (b - a) / 2 * t, delta=1e-12 * (1 + abs(a) + abs(b)))
                self.assertTrue(a < x < b)
            for x, y in zip(xs, reversed(xs)):
                self.assertAlmostEqual(x + y, a + b, delta=1e-12 * (1 + abs(a) + abs(b)))

    def test_three_points_on_unit_interval(self):
        xs = chebyshev_points(0.0, 1.0, 3)
        r = math.sqrt(3) / 4
        for x, y in zip(xs, [0.5 - r, 0.5, 0.5 + r]):
            self.assertAlmostEqual(x, y, delta=1e-15)
        self.assertEqual(equal_points(0.0, 1.0, 3), [0.25, 0.5, 0.75])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            chebyshev_points(0.0, 1.0, 0)
        with self.assertRaises(ValueError):
            chebyshev_points(1.0, 1.0, 3)


class TestNodePolynomial(unittest.TestCase):
    def extremal_points(self, a, b, n):
        return [(a + b) / 2 + (b - a) / 2 * math.cos(k * math.pi / n) for k in range(n + 1)]

    def test_equioscillation_of_chebyshev_nodes(self):
        for n in range(1, 11):
            a, b = -0.5, 2.5
            xs = chebyshev_points(a, b, n)
            bound = chebyshev_bound(a, b, n)
            ext = self.extremal_points(a, b, n)
            for k, x in enumerate(ext):
                w = node_polynomial(xs, x)
                self.assertAlmostEqual(abs(w), bound, delta=1e-12 * bound)
                if k > 0:
                    prev = node_polynomial(xs, ext[k - 1])
                    self.assertLess(w * prev, 0.0)
            grid = max(abs(node_polynomial(xs, a + (b - a) * i / 4000)) for i in range(4001))
            self.assertLessEqual(grid, bound * (1 + 1e-12))

    def test_no_node_set_does_better(self):
        # For any n nodes, max |w| over the n + 1 extremal points is already at least the bound.
        rng = random.Random(2024)
        for _ in range(3000):
            n = rng.randint(1, 8)
            a = rng.uniform(-3, 3)
            b = a + rng.uniform(0.5, 4)
            nodes = sorted(rng.uniform(a, b) for _ in range(n))
            bound = chebyshev_bound(a, b, n)
            peak = max(abs(node_polynomial(nodes, x)) for x in self.extremal_points(a, b, n))
            self.assertGreaterEqual(peak, bound * (1 - 1e-12))

    def test_equal_spacing_is_worse(self):
        for n in range(2, 12):
            eq = equal_points(0.0, 1.0, n)
            peak = max(abs(node_polynomial(eq, i / 20000)) for i in range(20001))
            self.assertGreater(peak, chebyshev_bound(0.0, 1.0, n))


class TestFunctionGenerator(unittest.TestCase):
    def setUp(self):
        d = math.radians
        # y = e^x on [0, 1]; phi from 90 to 210 degrees; psi from 195 to 255 degrees.
        self.g = Generator(math.exp, 0.0, 1.0, d(90), d(120), d(195), d(60))

    def check_design(self, xs):
        g = self.g
        k = g.design(xs)
        self.assertIsNotNone(k)
        a, b, c, d = link_lengths(k)
        s = g.branch(k, xs)
        self.assertIsNotNone(s)
        for x in xs:
            phi, psi = g.phi(x), g.psi(x)
            self.assertLess(abs(wrap(output_angle(k, phi, s) - psi)), 1e-12)
            pa = a * cmath.exp(1j * phi)
            pb = d + c * cmath.exp(1j * psi)
            self.assertAlmostEqual(abs(pb - pa), b, delta=1e-12)
            self.assertAlmostEqual(k[0] * math.cos(psi) - k[1] * math.cos(phi) + k[2], math.cos(phi - psi), delta=1e-12)
        return k, (a, b, c, d), s

    def test_precision_points_are_met(self):
        for xs in (chebyshev_points(0.0, 1.0, 3), equal_points(0.0, 1.0, 3), [0.0, 0.5, 1.0]):
            self.check_design(xs)

    def test_half_angle_matches_circle_intersection(self):
        k, (a, b, c, d), s = self.check_design(chebyshev_points(0.0, 1.0, 3))
        errs = self.g.errors(k, s, 1000)
        self.assertIsNotNone(errs)
        for x, _ in errs[::7]:
            phi = self.g.phi(x)
            psi = output_angle(k, phi, s)
            other = output_by_circles(a, b, c, d, phi, psi)
            self.assertLess(abs(wrap(psi - other)), 1e-9)

    def test_structural_error_at_1000_points(self):
        g = self.g
        ec = g.max_error(chebyshev_points(0.0, 1.0, 3), 1000)
        ee = g.max_error(equal_points(0.0, 1.0, 3), 1000)
        self.assertAlmostEqual(math.degrees(ec), 0.1649, delta=5e-4)
        self.assertAlmostEqual(math.degrees(ee), 0.5210, delta=5e-4)
        self.assertLess(ec, ee)

    def test_not_minimax(self):
        # Three other precision points give a smaller largest error, so the spacing is not minimax.
        g = self.g
        ec = g.max_error(chebyshev_points(0.0, 1.0, 3), 1000)
        better = g.max_error([0.048, 0.3773, 0.9999], 1000)
        self.assertIsNotNone(better)
        self.assertLess(better, 0.7 * ec)
        # The Chebyshev error peaks are unequal: no equioscillation.
        k = g.design(chebyshev_points(0.0, 1.0, 3))
        errs = [v for _, v in g.errors(k, g.branch(k, chebyshev_points(0.0, 1.0, 3)), 1000)]
        self.assertGreater(abs(errs[0]), 2 * abs(errs[-1]))

    def test_template_matches_parts(self):
        out = chebyshev_design(self.g, 3, 1000)
        self.assertIsNotNone(out)
        xs, k, lengths, e = out
        self.assertEqual(xs, chebyshev_points(0.0, 1.0, 3))
        self.assertEqual(k, self.g.design(xs))
        self.assertEqual(e, self.g.max_error(xs, 1000))
        for got, want in zip(lengths, (1.6216, 2.1233, 1.6390, 1.0)):
            self.assertAlmostEqual(got, want, delta=5e-5)
        with self.assertRaises(ValueError):
            chebyshev_design(self.g, 4)

    def test_template_reports_failure(self):
        # Ranges for which the three pairs are not on one branch or do not assemble.
        rng = random.Random(7)
        failures = 0
        for _ in range(200):
            g = Generator(math.exp, 0.0, 1.0, rng.uniform(0, 6.3), rng.uniform(0.5, 2.5), rng.uniform(0, 6.3), rng.uniform(0.5, 2.5))
            out = chebyshev_design(g, 3, 200)
            if out is None:
                failures += 1
                continue
            xs, k, lengths, e = out
            s = g.branch(k, xs)
            for x in xs:
                self.assertLess(abs(wrap(output_angle(k, g.phi(x), s) - g.psi(x))), 1e-9)
        self.assertGreater(failures, 0)

    def test_singular_system(self):
        self.assertIsNone(self.g.design([0.3, 0.3, 0.7]))
        self.assertIsNone(solve3([[1, 2, 3], [2, 4, 6], [0, 1, 1]], [1, 2, 3]))

    def test_solver_against_known_solution(self):
        rng = random.Random(5)
        for _ in range(500):
            m = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
            x = [rng.uniform(-2, 2) for _ in range(3)]
            r = [sum(m[i][j] * x[j] for j in range(3)) for i in range(3)]
            y = solve3(m, r)
            if y is None:
                continue
            res = max(abs(sum(m[i][j] * y[j] for j in range(3)) - r[i]) for i in range(3))
            self.assertLess(res, 1e-10)


if __name__ == "__main__":
    unittest.main()
