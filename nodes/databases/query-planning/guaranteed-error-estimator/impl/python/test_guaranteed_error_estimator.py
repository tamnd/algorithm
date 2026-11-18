# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guaranteed-error-estimator/. The authors are listed in prov/32XY8A.jsonl.

import itertools
import math
import unittest
from fractions import Fraction
from random import Random

from guaranteed_error_estimator import (
    draw_sample,
    estimate_distinct,
    frequency_profile,
    gee,
    gee_from_profile,
    lower_bound,
    ratio_error,
)


def exact_estimates(column, r):
    """GEE on every r-subset of the rows of the column."""
    n = len(column)
    return [gee([column[i] for i in s], n) for s in itertools.combinations(range(n), r)]


class TestGEE(unittest.TestCase):
    def test_page_example(self):
        sample = ["a", "a", "b", "e"]
        self.assertEqual(frequency_profile(sample), {1: 2, 2: 1})
        self.assertEqual(gee(sample, 16), 5.0)

    def test_page_example_all_samples(self):
        column = ["a"] * 8 + ["b"] * 4 + ["c", "d", "e", "f"]
        values = exact_estimates(column, 4)
        self.assertEqual(len(values), 1820)
        counts = {}
        for v in values:
            counts[v] = counts.get(v, 0) + 1
        self.assertEqual(counts, {1.0: 71, 2.0: 168, 3.0: 496, 5.0: 844, 8.0: 241})
        mean = sum(values) / len(values)
        self.assertAlmostEqual(mean, 8043 / 1820)
        self.assertGreaterEqual(mean, 6 / (1 + 2))

    def test_bounds_on_every_sample(self):
        rng = Random(7)
        for _ in range(40):
            n = rng.randint(2, 9)
            column = [rng.randrange(rng.randint(1, n)) for _ in range(n)]
            D = len(set(column))
            for r in range(1, n + 1):
                c = math.sqrt(n / r)
                values = []
                for s in itertools.combinations(range(n), r):
                    sample = [column[i] for i in s]
                    d = len(set(sample))
                    g = gee(sample, n)
                    self.assertLessEqual(d - 1e-9, g)
                    self.assertLessEqual(g, c * d + 1e-9)
                    self.assertLessEqual(g, c * D + 1e-9)
                    values.append(g)
                mean = sum(values) / len(values)
                self.assertGreaterEqual(mean, D / (1 + c) - 1e-9)

    def test_full_sample_is_exact(self):
        rng = Random(3)
        for _ in range(20):
            column = [rng.randrange(30) for _ in range(rng.randint(1, 60))]
            self.assertEqual(gee(column, len(column)), len(set(column)))

    def test_expected_estimate_monte_carlo(self):
        rng = Random(11)
        n, r = 3000, 100
        c = math.sqrt(n / r)
        columns = [
            [rng.randrange(300) for _ in range(n)],
            [int(1 / (1 - rng.random())) for _ in range(n)],
            list(range(n)),
            [0] * (n - 150) + list(range(1, 151)),
        ]
        for column in columns:
            D = len(set(column))
            runs = [estimate_distinct(column, r, rng) for _ in range(150)]
            mean = sum(runs) / len(runs)
            self.assertLessEqual(max(runs), c * D + 1e-9)
            # E[GEE] >= D / (1 + c); the sample mean is checked with a margin of 20 percent.
            self.assertGreaterEqual(mean, 0.8 * D / (1 + c))
            self.assertLessEqual(ratio_error(mean, D), 1 + c)

    def test_single_estimate_can_be_far_off(self):
        # n / r singletons in a column of one common value: with probability
        # about 1/e the sample misses every singleton and GEE returns 1.
        n, r = 400, 20
        k = n // r
        column = [0] * (n - k) + list(range(1, k + 1))
        miss = Fraction(math.comb(n - k, r), math.comb(n, r))
        self.assertGreater(miss, Fraction(1, 3))
        self.assertEqual(gee([0] * r, n), 1.0)
        self.assertEqual(ratio_error(1.0, k + 1), k + 1)
        self.assertGreater(k + 1, 4 * math.sqrt(n / r))
        rng = Random(5)
        hits = sum(1 for _ in range(600) if estimate_distinct(column, r, rng) == 1.0)
        self.assertLess(abs(hits / 600 - float(miss)), 0.07)

    def test_lower_bound_pair(self):
        # Input A has one value. Input B has k singletons as well. On samples
        # that see only the common value, every estimator must give one answer,
        # and that answer has ratio error at least sqrt(k + 1) on A or on B.
        for n, r, gamma in [(1000, 10, 0.5), (5000, 50, 0.3), (200, 20, 0.9)]:
            K = (n - r) / (2 * r) * math.log(1 / gamma)
            k = int(K)
            miss = Fraction(math.comb(n - k, r), math.comb(n, r))
            self.assertGreaterEqual(float(miss), gamma)
            self.assertGreater(math.sqrt(k + 1), lower_bound(n, r, gamma))
            g = gee([0] * r, n)
            worst = max(ratio_error(g, 1), ratio_error(g, k + 1))
            self.assertGreaterEqual(worst, math.sqrt(k + 1))

    def test_lower_bound_value(self):
        # One percent of the rows, gamma = 1/2: the ratio error is at least about 5.86.
        self.assertAlmostEqual(lower_bound(10000, 100, 0.5), 5.8575, places=3)
        with self.assertRaises(ValueError):
            lower_bound(100, 2, 0.1)

    def test_profile_checks(self):
        with self.assertRaises(ValueError):
            gee_from_profile({1: 3}, 10, 4)
        with self.assertRaises(ValueError):
            gee_from_profile({1: 3}, 2, 3)
        self.assertEqual(len(draw_sample(list(range(10)), 4, Random(1))), 4)


if __name__ == "__main__":
    unittest.main()
