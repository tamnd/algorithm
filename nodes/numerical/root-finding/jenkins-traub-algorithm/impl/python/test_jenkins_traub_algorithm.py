# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jenkins-traub-algorithm/. The authors are listed in prov/W75WVA.jsonl.

import math
import random
import unittest

from jenkins_traub_algorithm import _bound, _divide, jenkins_traub, jt_step, lower_bound


def poly(rs):
    c = [1 + 0j]
    for r in rs:
        c = c + [0j]
        for i in range(len(c) - 1, 0, -1):
            c[i] -= r * c[i - 1]
    return c


def match(test, got, want, tol):
    got = list(got)
    test.assertEqual(len(got), len(want))
    for w in want:
        j = min(range(len(got)), key=lambda i: abs(got[i] - w))
        test.assertLess(abs(got[j] - w), tol)
        got.pop(j)


class TestJenkinsTraub(unittest.TestCase):
    def test_cubic_and_counts(self):
        r = jenkins_traub(poly([1, 2, 3]))
        self.assertEqual(r.status, "done")
        match(self, r.roots, [1, 2, 3], 1e-13)
        self.assertEqual((r.evals, r.steps), (49, 21))

    def test_complex_roots_of_real_polynomial(self):
        match(self, jenkins_traub([1, 0, 1]).roots, [1j, -1j], 1e-15)
        match(self, jenkins_traub(poly([1 + 2j, 1 - 2j, -3, 0.5j])).roots,
              [1 + 2j, 1 - 2j, -3, 0.5j], 1e-12)

    def test_zero_roots_and_low_degree(self):
        r = jenkins_traub([1, -1, 0, 0])
        match(self, r.roots, [0, 0, 1], 1e-15)
        self.assertEqual(jenkins_traub([3, -6]).roots, [2])
        self.assertEqual(jenkins_traub([5]).roots, [])

    def test_double_root(self):
        r = jenkins_traub(poly([1, 1, -2]))
        self.assertEqual(r.status, "done")
        match(self, r.roots, [1, 1, -2], 1e-7)

    def test_wilkinson_10(self):
        r = jenkins_traub(poly(range(1, 11)))
        match(self, r.roots, list(range(1, 11)), 1e-8)

    def test_stage2_linear_rate(self):
        # fixed shift s: t converges to the root closest to s with ratio
        # |a1 - s| / |a2 - s| where a2 is the second closest root
        roots = [1, 2.5, -3]
        p, s = poly(roots), 0.6 + 0.4j
        H = [(3 - k) * p[k] / 3 for k in range(3)]
        errs = []
        for _ in range(25):
            H, t, _ = jt_step(p, H, s)
            errs.append(abs(t - 1))
        ratio = abs(1 - s) / abs(2.5 - s)
        for k in range(15, 24):
            self.assertAlmostEqual(errs[k + 1] / errs[k], ratio, delta=0.02)

    def test_stage3_observed_order(self):
        roots = [1, 2, 3, 4 + 1j, -2]
        r = jenkins_traub(poly(roots))
        orders = []
        for path in r.trace:
            z = min(roots, key=lambda w: abs(w - path[-1]))
            e = [abs(x - z) for x in path]
            for k in range(1, len(e) - 1):
                if e[k + 1] > 1e-11:
                    orders.append(math.log(e[k + 1] / e[k]) / math.log(e[k] / e[k - 1]))
        self.assertTrue(orders)
        self.assertGreater(min(orders), 2.0)

    def test_shift_at_exact_root(self):
        p = poly([1, 2, 3])
        H, t, ps = jt_step(p, [1, 0, 0], 2 + 0j)
        self.assertEqual(ps, 0)
        self.assertEqual(t, 2)
        match(self, [-H[1] / 2 + d for d in (1, -1)], [1, 3], 1e-15)  # H = (z-1)(z-3)

    def test_lower_bound(self):
        p = poly([2, -3, 4j])
        b = lower_bound(p)
        self.assertLessEqual(b, 2)
        self.assertGreater(b, 0.5)

    def test_max_steps_and_bad_input(self):
        r = jenkins_traub(poly([1, 2, 3, 4, 5]), max_steps=3)
        self.assertEqual(r.status, "max-iter")
        self.assertLessEqual(len(r.roots), 4)
        for bad in ([0, 1, 2], [], [1, float("nan")], [1, math.inf, 2]):
            with self.assertRaises(ValueError):
                jenkins_traub(bad)

    def test_random_polynomials(self):
        rng = random.Random(5)
        for _ in range(500):
            n = rng.randint(2, 10)
            while True:
                rs = [complex(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(n)]
                if min(abs(x - y) for i, x in enumerate(rs) for y in rs[:i]) > 0.1:
                    break
            c = poly(rs)
            r = jenkins_traub(c)
            self.assertEqual(r.status, "done")
            match(self, r.roots, rs, 1e-9)
            for z in r.roots:  # small backward error for the original polynomial
                self.assertLess(abs(_divide(c, z)[1]), 1e-12 * _bound(c, z))


if __name__ == "__main__":
    unittest.main()
