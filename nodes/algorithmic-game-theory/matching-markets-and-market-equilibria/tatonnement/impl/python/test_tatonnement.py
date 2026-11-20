# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tatonnement/. The authors are listed in prov/ZA6PKF.jsonl.

import random
import unittest

from tatonnement import (fisher_cobb_douglas, fisher_ces, fisher_linear, scarf, tatonnement,
                         tatonnement_additive)


class TestTatonnement(unittest.TestCase):
    def test_check_value(self):
        # Linear Fisher market of the page: while p_1 / p_2 stays in (1/2, 2), z_j = 1 / p_j - 1
        # and the step with factor 1/2 halves the distance to (1, 1).
        z = fisher_linear([[2, 1], [1, 2]], [1, 1])
        p = [0.8, 1.4]
        for t in range(1, 8):
            p, _, _ = tatonnement(z, p, 0.5, 1, 0.0)
            self.assertAlmostEqual(p[0], 1 - 0.2 / 2 ** t, delta=1e-12)
            self.assertAlmostEqual(p[1], 1 + 0.4 / 2 ** t, delta=1e-12)
        p, t, ok = tatonnement(z, [0.8, 1.4], 0.5, 200, 1e-9)
        self.assertTrue(ok)
        self.assertAlmostEqual(p[0], 1.0, delta=1e-8)
        self.assertAlmostEqual(p[1], 1.0, delta=1e-8)

    def test_linear_tie_has_no_demand_function(self):
        z = fisher_linear([[2, 1], [1, 2]], [1, 1])
        with self.assertRaises(ValueError):
            z([2.0, 1.0])

    def test_cobb_douglas_contracts(self):
        rng = random.Random(1)
        for _ in range(20):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            a = []
            for _ in range(n):
                w = [rng.random() for _ in range(m)]
                a.append([v / sum(w) for v in w])
            budgets = [rng.uniform(0.5, 3) for _ in range(n)]
            c = [sum(a[i][j] * budgets[i] for i in range(n)) for j in range(m)]
            z = fisher_cobb_douglas(a, budgets)
            step = rng.uniform(0.1, 0.9)
            p = [cj * rng.uniform(0.5, 3) for cj in c]
            for _ in range(10):
                q, _, _ = tatonnement(z, p, step, 1, 0.0)
                for j in range(m):
                    self.assertAlmostEqual(q[j] - c[j], (1 - step) * (p[j] - c[j]), delta=1e-9)
                p = q
            p, _, ok = tatonnement(z, p, step, 10000, 1e-10)
            self.assertTrue(ok)
            for j in range(m):
                self.assertAlmostEqual(p[j], c[j], delta=1e-8)

    def test_ces_markets_converge(self):
        rng = random.Random(2)
        for rho in [0.75, 0.5, 0.25, -1.0]:
            for _ in range(5):
                a = [[rng.uniform(0.1, 1) for _ in range(3)] for _ in range(3)]
                budgets = [rng.uniform(0.5, 2) for _ in range(3)]
                z = fisher_ces(a, budgets, rho)
                p, _, ok = tatonnement(z, [1.0, 1.0, 1.0], 0.2, 5000, 1e-9)
                self.assertTrue(ok)
                self.assertAlmostEqual(sum(p), sum(budgets), delta=1e-7)

    def test_large_step_can_fail(self):
        # With rho = 3/4 demand is elastic, and the step 1/2 overshoots on one of these markets.
        rng = random.Random(2)
        results = []
        for _ in range(5):
            a = [[rng.uniform(0.1, 1) for _ in range(3)] for _ in range(3)]
            budgets = [rng.uniform(0.5, 2) for _ in range(3)]
            z = fisher_ces(a, budgets, 0.75)
            results.append(tatonnement(z, [1.0, 1.0, 1.0], 0.5, 5000, 1e-9)[2])
        self.assertIn(False, results)

    def test_scarf_identities(self):
        rng = random.Random(3)
        for _ in range(100):
            p = [rng.uniform(0.1, 5) for _ in range(3)]
            z = scarf(p)
            self.assertAlmostEqual(sum(p[j] * z[j] for j in range(3)), 0.0, delta=1e-12)
            self.assertAlmostEqual(sum(z[j] / p[j] for j in range(3)), 0.0, delta=1e-9)
            z2 = scarf([7 * q for q in p])
            for j in range(3):
                self.assertAlmostEqual(z[j], z2[j], delta=1e-12)
        self.assertEqual(scarf([1.0, 1.0, 1.0]), [0.0, 0.0, 0.0])

    def test_scarf_does_not_converge(self):
        step = 0.1
        path = tatonnement_additive(scarf, [1.2, 1.0, 0.8], step, 1000)
        for t in range(1000):
            p, q = path[t], path[t + 1]
            z = scarf(p)
            norm_p = sum(v * v for v in p)
            norm_q = sum(v * v for v in q)
            # Walras' law makes the additive step move away from the origin.
            self.assertAlmostEqual(norm_q, norm_p + step * step * sum(v * v for v in z), delta=1e-9)
            self.assertGreater(norm_q, norm_p)
            self.assertGreater(max(abs(v) for v in z), 0.05)
        _, _, ok = tatonnement(scarf, [1.2, 1.0, 0.8], 0.1, 3000, 1e-3)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
