# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bernoulli-method/. The authors are listed in prov/QQR2VY.jsonl.

import math
import random
import unittest

from bernoulli_method import bernoulli, bernoulli_pair, power_sums


def from_roots(rs):
    p = [1.0]
    for r in rs:
        p = [x - r * y for x, y in zip(p + [0.0], [0.0] + p)]
    return p


CUBIC = [1, -6, 11, -6]  # (x - 1)(x - 2)(x - 3)


class TestBernoulli(unittest.TestCase):
    def test_power_sums(self):
        self.assertEqual(power_sums(CUBIC, 8), [1.0 + 2 ** k + 3 ** k for k in range(8)])
        self.assertEqual(power_sums([2, 0, -8], 5), [2.0, 0.0, 8.0, 0.0, 32.0])

    def test_example_ratios_and_rate(self):
        r = bernoulli(CUBIC)
        self.assertEqual(r.status, "converged")
        self.assertAlmostEqual(r.root, 3.0, delta=1e-11)
        # ratio k is s_(j+1) / s_j with j = n + k - 2; its error is (-2 - 2^j) / (1 + 2^j + 3^j)
        for k, rho in enumerate(r.ratios[:20], start=1):
            j = 3 + k - 2
            self.assertAlmostEqual(rho - 3, (-2 - 2 ** j) / (1 + 2 ** j + 3 ** j), delta=1e-12)
        e = [abs(x - 3) for x in r.ratios]
        self.assertAlmostEqual(e[30] / e[29], 2 / 3, delta=1e-4)
        self.assertLessEqual(r.iterations, 70)

    def test_negative_and_double_dominant(self):
        self.assertAlmostEqual(bernoulli([1, 4, 1, -6]).root, -3.0, delta=1e-10)
        self.assertAlmostEqual(bernoulli([1, -7, 15, -9]).root, 3.0, delta=1e-10)  # (x - 3)^2 (x - 1)
        r = bernoulli([1, -4, 4])  # (x - 2)^2: y_k = 2 * 2^k, exact at once
        self.assertEqual((r.status, r.root, r.iterations), ("converged", 2.0, 2))

    def test_degree_one_and_zero_roots(self):
        self.assertEqual(bernoulli([1, -3]).root, 3.0)
        r = bernoulli([1, 0, 0, 0])
        self.assertEqual((r.status, r.root), ("converged", 0.0))
        self.assertAlmostEqual(bernoulli([1, -5, 6, 0]).root, 3.0, delta=1e-10)  # root at 0 too

    def test_tie_hits_max_iter(self):
        r = bernoulli([1, 0, -1], max_iter=500)  # roots +1 and -1 have the same modulus
        self.assertEqual((r.status, r.iterations), ("max-iter", 500))
        r = bernoulli([1, 0, 4, 0], max_iter=300)  # dominant pair +-2i
        self.assertEqual(r.status, "max-iter")

    def test_complex_pair(self):
        S, P, k, status = bernoulli_pair([1, 0, 3, 6, 10])  # dominant pair 1 +- 2i
        self.assertEqual(status, "converged")
        self.assertAlmostEqual(S, 2.0, delta=1e-9)
        self.assertAlmostEqual(P, 5.0, delta=1e-9)
        S, P, k, status = bernoulli_pair([1, 1, 1])
        self.assertEqual((status, S, P), ("converged", -1.0, 1.0))

    def test_no_overflow(self):
        r = bernoulli(from_roots([2.0, 1.999]), tol=0.0, max_iter=5000)
        self.assertEqual(r.status, "max-iter")
        self.assertTrue(math.isfinite(r.root))
        self.assertAlmostEqual(r.root, 2.0, delta=1e-3)
        self.assertAlmostEqual(bernoulli([1.0, -(1e100 + 1), 1e100]).root / 1e100, 1.0, delta=1e-12)

    def test_bad_input(self):
        for bad in ([1, float("nan")], [1, math.inf, 2], [0, 0], [5]):
            with self.assertRaises(ValueError):
                bernoulli(bad)
        with self.assertRaises(ValueError):
            bernoulli_pair([1, 2])

    def test_random_real_roots(self):
        rng = random.Random(20261108)
        for _ in range(600):
            n = rng.randint(2, 7)
            r1 = rng.choice([-1, 1]) * rng.uniform(1, 10)
            rest = [rng.uniform(-0.8, 0.8) * abs(r1) for _ in range(n - 1)]
            lam = max(abs(x) for x in rest) / abs(r1)
            res = bernoulli(from_roots([r1] + rest), tol=1e-13)
            self.assertEqual(res.status, "converged")
            # error is about diff * lam / (1 - lam) <= 4 * diff
            self.assertLess(abs(res.root - r1), 1e-10 * (1 + abs(r1)))
            self.assertLessEqual(res.iterations, int(40 / -math.log(lam)) + 20)


if __name__ == "__main__":
    unittest.main()
