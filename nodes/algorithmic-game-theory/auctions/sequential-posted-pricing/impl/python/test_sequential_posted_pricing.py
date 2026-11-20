# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-posted-pricing/. The authors are listed in prov/MES401.jsonl.

import random
import unittest
from fractions import Fraction as F
from itertools import product

from sequential_posted_pricing import (
    NO_OFFER,
    draw_prices,
    expected_revenue,
    hull_vertices,
    plan,
    run,
    sale_probability,
    sequential_posted_pricing,
)

IRREGULAR = [(2, F(1, 2)), (3, F(1, 6)), (5, F(1, 3))]
UNIFORM3 = [(1, F(1, 3)), (2, F(1, 3)), (3, F(1, 3))]


def random_dist(rng, k, denom=6):
    values = sorted(rng.sample(range(1, 10), k))
    cuts = sorted(rng.sample(range(1, denom), k - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [denom])]
    return [(v, F(p, denom)) for v, p in zip(values, parts)]


def ironed(dist):
    """Ironed virtual value of each support value: the hull slope over its quantile interval."""
    h = hull_vertices(dist)
    out = {}
    for v, _ in dist:
        q = sale_probability(dist, F(v))
        j = next(j for j in range(1, len(h)) if h[j - 1][0] < q <= h[j][0])
        out[F(v)] = (h[j][1] - h[j - 1][1]) / (h[j][0] - h[j - 1][0])
    return out


def optimal_revenue(dists):
    """Myerson's optimal revenue E[max(0, max_i ironed phi_i(v_i))], by enumeration."""
    bars = [ironed(d) for d in dists]
    total = F(0)
    for combo in product(*dists):
        p = F(1)
        for _, f in combo:
            p *= f
        total += p * max([F(0)] + [bars[i][F(v)] for i, (v, _) in enumerate(combo)])
    return total


class TestPlan(unittest.TestCase):
    def test_hull(self):
        self.assertEqual(hull_vertices(IRREGULAR), [(0, 0, NO_OFFER), (F(1, 3), F(5, 3), 5), (1, 2, 2)])

    def test_worked_example(self):
        value, lotteries = plan([IRREGULAR, IRREGULAR])
        self.assertEqual(value, F(7, 2))
        self.assertEqual(lotteries, [[(5, F(1, 2)), (2, F(1, 2))], [(5, 1)]])
        self.assertEqual(expected_revenue([IRREGULAR, IRREGULAR], lotteries), F(26, 9))
        self.assertEqual(optimal_revenue([IRREGULAR, IRREGULAR]), 3)

    def test_bound_is_tight_for_equal_prices(self):
        dists = [UNIFORM3] * 3
        value, lotteries = plan(dists)
        self.assertEqual(value, 3)
        self.assertEqual(lotteries, [[(3, 1)]] * 3)
        self.assertEqual(expected_revenue(dists, lotteries), F(19, 9))
        self.assertEqual(F(19, 9) / value, 1 - F(2, 3) ** 3)

    def test_lotteries_match_the_relaxation(self):
        rng = random.Random(1)
        for _ in range(60):
            dists = [random_dist(rng, rng.randint(1, 4)) for _ in range(rng.randint(1, 4))]
            value, lotteries = plan(dists)
            q_total, rev_total = F(0), F(0)
            for d, lot in zip(dists, lotteries):
                self.assertEqual(sum(p for _, p in lot), 1)
                for price, p in lot:
                    a = sale_probability(d, price)
                    q_total += p * a
                    rev_total += p * a * (price if price is not NO_OFFER else 0)
            self.assertLessEqual(q_total, 1)
            self.assertEqual(rev_total, value)

    def test_revenue_bounds(self):
        rng = random.Random(2)
        for _ in range(60):
            n = rng.randint(1, 4)
            dists = [random_dist(rng, rng.randint(1, 3)) for _ in range(n)]
            value, lotteries = plan(dists)
            spm = expected_revenue(dists, lotteries)
            opt = optimal_revenue(dists)
            self.assertGreaterEqual(value, opt)
            self.assertGreaterEqual(opt, spm)
            self.assertGreaterEqual(spm, (1 - (1 - F(1, n)) ** n) * value)


class TestRun(unittest.TestCase):
    def test_decreasing_order(self):
        self.assertEqual(run([F(3), F(5), NO_OFFER], [4, 4, 9]), (0, 3))
        self.assertEqual(run([F(3), F(5), NO_OFFER], [4, 6, 9]), (1, 5))
        self.assertEqual(run([F(3), F(3)], [3, 3]), (0, 3))
        self.assertEqual(run([F(3), F(5)], [2, 4]), (None, 0))

    def test_monte_carlo_matches_exact(self):
        rng = random.Random(3)
        dists = [IRREGULAR, IRREGULAR, UNIFORM3]
        value, lotteries = plan(dists)
        exact = float(expected_revenue(dists, lotteries))
        trials, total = 20000, 0.0
        supports = [([v for v, _ in d], [float(p) for _, p in d]) for d in dists]
        for _ in range(trials):
            values = [rng.choices(s, w)[0] for s, w in supports]
            total += float(run(draw_prices(lotteries, rng), values)[1])
        self.assertAlmostEqual(total / trials, exact, delta=0.06)

    def test_one_shot_and_bad_input(self):
        buyer, price = sequential_posted_pricing([IRREGULAR], [5], random.Random(4))
        self.assertEqual((buyer, price), (0, 2))
        with self.assertRaises(ValueError):
            plan([[(1, F(1, 2))]])
        with self.assertRaises(ValueError):
            plan([[(1, F(1, 2)), (1, F(1, 2))]])


if __name__ == "__main__":
    unittest.main()
