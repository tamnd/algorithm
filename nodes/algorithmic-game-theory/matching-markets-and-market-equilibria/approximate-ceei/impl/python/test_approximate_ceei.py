# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-ceei/. The authors are listed in prov/DWVSMG.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations, product
from math import sqrt

from approximate_ceei import approximate_ceei, budish_bound, clearing_error, demand, perturbed_budgets

ONE_SEAT = [[(0,)], [(0,)]]  # two agents who both want the single seat of good 0


class TestApproximateCEEI(unittest.TestCase):
    def test_equal_budgets_cannot_clear(self):
        # The example of the page: with equal budgets every price leaves an error of 1.
        alpha, p, bundles = approximate_ceei(ONE_SEAT, [1], [1, 1], Fraction(1, 10), Fraction(2))
        self.assertEqual(alpha, 1.0)
        for k in range(21):
            price = Fraction(k, 10)
            got = [demand(prefs, 1, [price]) for prefs in ONE_SEAT]
            self.assertEqual(abs(clearing_error(got, [1], [price])[0]), 1)

    def test_perturbed_budgets_clear(self):
        budgets = [1, Fraction(11, 10)]
        alpha, p, bundles = approximate_ceei(ONE_SEAT, [1], budgets, Fraction(1, 20), Fraction(2))
        self.assertEqual(alpha, 0.0)
        self.assertEqual(p, [Fraction(21, 20)])
        self.assertEqual(bundles, [(), (0,)])

    def test_three_students(self):
        # Good 0 has one seat, good 1 has three; everyone ranks {0, 1} > {0} > {1}.
        prefs = [[(0, 1), (0,), (1,)]] * 3
        alpha_equal = approximate_ceei(prefs, [1, 3], [1, 1, 1], Fraction(1, 8), Fraction(3, 2))[0]
        self.assertEqual(alpha_equal, 1.0)
        budgets = perturbed_budgets(3, Fraction(3, 10))
        alpha, p, bundles = approximate_ceei(prefs, [1, 3], budgets, Fraction(1, 40), Fraction(3, 2))
        self.assertEqual(alpha, 0.0)
        self.assertEqual(sorted(bundles), [(0, 1), (1,), (1,)])
        self.assertEqual(bundles[2], (0, 1))

    def test_grid_minimum(self):
        rng = random.Random(5)
        for _ in range(15):
            n, m = rng.randint(2, 3), rng.randint(1, 2)
            q = [rng.randint(1, 2) for _ in range(m)]
            bundles = [b for k in (1, 2) for b in combinations(range(m), k)]
            prefs = [rng.sample(bundles, len(bundles)) for _ in range(n)]
            budgets = perturbed_budgets(n, Fraction(1, 5))
            step, cap = Fraction(1, 4), Fraction(5, 2)
            alpha, p, got = approximate_ceei(prefs, q, budgets, step, cap)
            # the returned bundles are the agents' demands at the returned prices
            self.assertEqual(got, [demand(prefs[i], budgets[i], p) for i in range(n)])
            for i in range(n):
                self.assertLessEqual(sum(p[j] for j in got[i]), budgets[i])
            # no grid point does better
            grid = [step * k for k in range(11)]
            for r in product(grid, repeat=m):
                z = clearing_error([demand(prefs[i], budgets[i], r) for i in range(n)], q, r)
                self.assertGreaterEqual(sqrt(sum(v * v for v in z)), alpha - 1e-12)

    def test_budish_bound_values(self):
        self.assertEqual(budish_bound(1, 1), 0.5)
        self.assertEqual(budish_bound(2, 3), 1.5)
        self.assertEqual(budish_bound(1, 8), 2.0)


if __name__ == "__main__":
    unittest.main()
