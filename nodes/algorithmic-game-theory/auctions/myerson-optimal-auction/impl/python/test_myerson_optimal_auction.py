# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/myerson-optimal-auction/. The authors are listed in prov/VMDH3M.jsonl.

import math
import random
import unittest
from fractions import Fraction as F
from itertools import product

from myerson_optimal_auction import (
    Auction,
    expected_revenue,
    expected_virtual_surplus,
    ironed_virtual_values,
    myerson,
    myerson_regular,
    profiles,
    virtual_values,
)

IRREGULAR = [(2, F(1, 2)), (3, F(1, 6)), (5, F(1, 3))]


def random_dist(rng, k, denom=6):
    """A distribution on k distinct values in 1..9 with probabilities that are multiples of 1/denom."""
    values = sorted(rng.sample(range(1, 10), k))
    cuts = sorted(rng.sample(range(1, denom), k - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [denom])]
    return [(v, F(p, denom)) for v, p in zip(values, parts)]


def brute_force_optimum(d1, d2):
    """The best revenue of a deterministic monotone rule with threshold payments, for two bidders."""
    s1, s2 = [v for v, _ in d1], [v for v, _ in d2]
    denom = 1
    for _, p in d1 + d2:
        denom = denom * p.denominator // math.gcd(denom, p.denominator)
    w1 = [int(p * denom) for _, p in d1]
    w2 = [int(p * denom) for _, p in d2]
    cells = list(product(range(len(s1)), range(len(s2))))
    best = None
    for rule in product((0, 1, 2), repeat=len(cells)):
        x = dict(zip(cells, rule))
        ok = True
        for a, b in cells:
            # monotone: a winner keeps winning when it raises its own bid
            if x[(a, b)] == 1 and a + 1 < len(s1) and x[(a + 1, b)] != 1:
                ok = False
                break
            if x[(a, b)] == 2 and b + 1 < len(s2) and x[(a, b + 1)] != 2:
                ok = False
                break
        if not ok:
            continue
        rev = 0
        for a, b in cells:
            if x[(a, b)] == 1:
                t = min(k for k in range(len(s1)) if x[(k, b)] == 1)
                rev += w1[a] * w2[b] * s1[t]
            elif x[(a, b)] == 2:
                t = min(k for k in range(len(s2)) if x[(a, k)] == 2)
                rev += w1[a] * w2[b] * s2[t]
        if best is None or rev > best:
            best = rev
    return F(best, denom * denom)


class TestVirtualValues(unittest.TestCase):
    def test_irregular_example(self):
        self.assertEqual(virtual_values(IRREGULAR), [1, -1, 5])
        self.assertEqual(ironed_virtual_values(IRREGULAR), [F(1, 2), F(1, 2), 5])

    def test_regular_needs_no_ironing(self):
        d = [(1, F(1, 3)), (2, F(1, 3)), (3, F(1, 3))]
        self.assertEqual(virtual_values(d), [-1, F(1), 3])
        self.assertEqual(ironed_virtual_values(d), virtual_values(d))

    def test_ironed_values_are_monotone(self):
        rng = random.Random(1)
        for _ in range(200):
            d = random_dist(rng, rng.randint(1, 5), denom=12)
            phi = virtual_values(d)
            bar = ironed_virtual_values(d)
            self.assertTrue(all(a <= b for a, b in zip(bar, bar[1:])))
            self.assertEqual(sum(phi[k] * p for k, (_, p) in enumerate(d)),
                             sum(bar[k] * p for k, (_, p) in enumerate(d)))


class TestAuction(unittest.TestCase):
    def test_worked_example(self):
        a = Auction([IRREGULAR, IRREGULAR])
        self.assertEqual(a.run([2, 3]), (0, [2, 0]))
        self.assertEqual(a.run([3, 5]), (1, [0, 5]))
        self.assertEqual(a.run([5, 3]), (0, [2, 0]))
        self.assertEqual(a.run([5, 5]), (0, [5, 0]))
        self.assertEqual(expected_revenue([IRREGULAR, IRREGULAR]), 3)

    def test_one_bidder_posts_the_monopoly_price(self):
        d = [(1, F(1, 2)), (2, F(1, 4)), (5, F(1, 4))]
        self.assertEqual(myerson([d], [1]), (None, [0]))
        self.assertEqual(myerson([d], [5]), (0, [5]))
        self.assertEqual(expected_revenue([d]), F(5, 4))

    def test_truthful_and_individually_rational(self):
        rng = random.Random(2)
        for _ in range(25):
            n = rng.randint(1, 3)
            dists = [random_dist(rng, rng.randint(1, 4)) for _ in range(n)]
            a = Auction(dists)
            for bids, _ in profiles(dists):
                winner, pay = a.run(bids)
                for i in range(n):
                    u = (bids[i] if winner == i else 0) - pay[i]
                    self.assertGreaterEqual(u, 0)
                    for lie, _ in dists[i]:
                        other = list(bids)
                        other[i] = F(lie)
                        w2, p2 = a.run(other)
                        self.assertGreaterEqual(u, (bids[i] if w2 == i else 0) - p2[i])

    def test_revenue_equals_virtual_surplus(self):
        rng = random.Random(3)
        for _ in range(30):
            n = rng.randint(1, 3)
            dists = [random_dist(rng, rng.randint(1, 4)) for _ in range(n)]
            self.assertEqual(expected_revenue(dists), expected_virtual_surplus(dists))

    def test_optimal_against_all_monotone_rules(self):
        rng = random.Random(4)
        cases = [(IRREGULAR, IRREGULAR), (random_dist(rng, 3), random_dist(rng, 3))]
        for d1, d2 in cases:
            self.assertEqual(expected_revenue([d1, d2]), brute_force_optimum(d1, d2))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            myerson([[(1, F(1, 2))]], [1])
        with self.assertRaises(ValueError):
            myerson([IRREGULAR], [4])
        with self.assertRaises(ValueError):
            Auction([])


class TestRegularContinuous(unittest.TestCase):
    def setUp(self):
        self.phi = lambda v: 2 * v - 1
        self.inv = lambda y: (y + 1) / 2

    def test_uniform_outcomes(self):
        two = ([self.phi] * 2, [self.inv] * 2)
        self.assertEqual(myerson_regular([F(4, 5), F(3, 5)], *two), (0, [F(3, 5), 0]))
        self.assertEqual(myerson_regular([F(4, 5), F(3, 10)], *two), (0, [F(1, 2), 0]))
        self.assertEqual(myerson_regular([F(2, 5), F(3, 10)], *two), (None, [0, 0]))

    def test_uniform_revenue_by_monte_carlo(self):
        rng = random.Random(5)
        for n, exact in ((1, 1 / 4), (2, 5 / 12)):
            trials, total = 40000, 0.0
            for _ in range(trials):
                bids = [rng.random() for _ in range(n)]
                total += sum(myerson_regular(bids, [self.phi] * n, [self.inv] * n)[1])
            self.assertAlmostEqual(total / trials, exact, delta=0.01)


if __name__ == "__main__":
    unittest.main()
