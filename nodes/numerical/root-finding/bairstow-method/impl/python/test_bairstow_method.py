# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bairstow-method/. The authors are listed in prov/J2HSDJ.jsonl.

import math
import random
import unittest

from bairstow_method import bairstow_roots, divide, find_factor, quadratic_roots


def from_roots(rs):
    p = [1 + 0j]
    for r in rs:
        p = [x - r * y for x, y in zip(p + [0], [0] + p)]
    return [x.real for x in p]


def match_error(found, expected):
    left = list(found)
    err = 0.0
    for r in expected:
        j = min(range(len(left)), key=lambda i: abs(left[i] - r))
        err = max(err, abs(left[j] - r))
        left.pop(j)
    return err


QUARTIC = [1, 0, 3, 6, 10]  # (x^2 + 2x + 2)(x^2 - 2x + 5)


class TestBairstow(unittest.TestCase):
    def test_division_identity(self):
        a = [2.0, -3.0, 5.0, 7.0, -11.0, 13.0]
        u, v = 0.75, -1.5
        b = divide(a, u, v)
        n = len(a) - 1
        for x in (-2.0, -0.5, 0.0, 1.0, 3.0):
            p = sum(c * x ** (n - i) for i, c in enumerate(a))
            q = sum(c * x ** (n - 2 - i) for i, c in enumerate(b[:n - 1]))
            self.assertAlmostEqual(p, (x * x - u * x - v) * q + b[n - 1] * (x - u) + b[n], places=9)

    def test_example_quartic(self):
        r = find_factor(QUARTIC, -2.0, -10 / 3)
        self.assertIn(r.status, ("converged", "exact"))
        self.assertLess(abs(r.u + 2) + abs(r.v + 2), 1e-15)
        self.assertLessEqual(r.evaluations, 8)
        roots = bairstow_roots(QUARTIC)
        self.assertLess(match_error(roots.roots, [-1 + 1j, -1 - 1j, 1 + 2j, 1 - 2j]), 1e-14)

    def test_quadratic_convergence(self):
        u, v = -2.0, -10 / 3
        errs = []
        for _ in range(5):
            errs.append(abs(u + 2) + abs(v + 2))
            r = find_factor(QUARTIC, u, v, tol=0, max_iter=1)
            u, v = r.u, r.v
        # e_{k+1} / e_k^2 stays bounded and the observed order approaches 2
        for e0, e1, e2 in zip(errs, errs[1:], errs[2:]):
            if e2 > 1e-13:
                self.assertGreater(math.log(e2 / e1) / math.log(e1 / e0), 1.8)
        self.assertLess(errs[4], 1e-10)

    def test_double_root_factor_still_quadratic(self):
        # factor (x - 1)^2 is coprime to the quotient, so the Jacobian is nonsingular
        p = from_roots([1, 1, complex(-0.5, 0.75 ** 0.5), complex(-0.5, -0.75 ** 0.5), -3])
        u, v = 1.9, -0.9
        errs = []
        for _ in range(3):
            r = find_factor(p, u, v, tol=0, max_iter=1)
            u, v = r.u, r.v
            errs.append(abs(u - 2) + abs(v + 1))
        self.assertLess(errs[1], 10 * errs[0] ** 2)
        self.assertLess(errs[2], 1e-7)

    def test_exact_factor_at_start(self):
        r = find_factor(QUARTIC, -2.0, -2.0)
        self.assertEqual((r.status, r.iterations, r.evaluations), ("exact", 0, 1))
        self.assertEqual(r.quotient, [1.0, -2.0, 5.0])

    def test_root_at_zero(self):
        res = bairstow_roots([1, -6, 11, -6, 0])  # x (x - 1)(x - 2)(x - 3)
        self.assertLess(match_error(res.roots, [0, 1, 2, 3]), 1e-12)

    def test_singular_jacobian(self):
        # u = v = 0 on x^4 + 1: b = a, c = (1, 0, 0, 0) gives det = 0
        r = find_factor([1, 0, 0, 0, 1], 0.0, 0.0)
        self.assertEqual(r.status, "singular")
        res = bairstow_roots([1, 0, 0, 0, 1])
        self.assertEqual(res.status, "converged")
        self.assertGreaterEqual(res.restarts, 1)
        s = 0.5 ** 0.5
        self.assertLess(match_error(res.roots, [complex(s, s), complex(s, -s), complex(-s, s), complex(-s, -s)]), 1e-13)

    def test_max_iter_and_failure(self):
        r = find_factor([1, 0, 3, 6, 10], 40.0, 30.0, max_iter=2)
        self.assertEqual((r.status, r.iterations, r.evaluations), ("max-iter", 2, 3))
        res = bairstow_roots([1, 0, 3, 6, 10], max_iter=1, max_restarts=2)
        self.assertEqual(res.status, "failed")
        self.assertEqual(res.restarts, 3)

    def test_low_degree_and_bad_input(self):
        self.assertEqual(bairstow_roots([2, -4]).roots, [2 + 0j])
        self.assertLess(match_error(bairstow_roots([0, 1, 0, 1]).roots, [1j, -1j]), 1e-15)
        self.assertEqual(sorted(z.real for z in quadratic_roots(1e8, -1.0)), [1e-8, 1e8])
        with self.assertRaises(ValueError):
            bairstow_roots([1, float("nan"), 2])
        with self.assertRaises(ValueError):
            bairstow_roots([1, math.inf, 2])
        with self.assertRaises(ValueError):
            bairstow_roots([0, 0])
        with self.assertRaises(ValueError):
            find_factor([1, 2, 3], 0.0, 0.0)

    def test_wilkinson_10(self):
        res = bairstow_roots(from_roots(range(1, 11)))
        self.assertEqual(res.status, "converged")
        self.assertLess(match_error(res.roots, range(1, 11)), 1e-6)

    def test_random_polynomials(self):
        rng = random.Random(20261108)
        total = 0
        for _ in range(600):
            n = rng.randint(3, 8)
            rs = []
            while len(rs) < n:
                if n - len(rs) >= 2 and rng.random() < 0.5:
                    z = complex(rng.uniform(-3, 3), rng.uniform(0.3, 3))
                    cand = [z, z.conjugate()]
                else:
                    cand = [complex(rng.uniform(-3, 3), 0)]
                if all(abs(c - r) > 0.3 for c in cand for r in rs):
                    rs += cand
            res = bairstow_roots(from_roots(rs))
            self.assertEqual(res.status, "converged")
            self.assertEqual(len(res.roots), n)
            self.assertLess(match_error(res.roots, rs), 1e-9)
            total += res.evaluations
        self.assertLess(total / 600, 60)


if __name__ == "__main__":
    unittest.main()
