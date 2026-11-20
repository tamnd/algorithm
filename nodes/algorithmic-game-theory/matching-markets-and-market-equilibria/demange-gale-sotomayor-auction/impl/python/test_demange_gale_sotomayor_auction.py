# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/demange-gale-sotomayor-auction/. The authors are listed in prov/RZZ6FP.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import permutations, product

from demange_gale_sotomayor_auction import NONE, demand, dgs_auction

# The example of the page: 3 bidders, 3 items.
EXAMPLE = [[4, 6, 2], [5, 6, 1], [3, 7, 4]]


def assignments(n, m):
    """Every assignment of at most one item per bidder, each item to at most one bidder."""
    options = list(range(m)) + [NONE]
    for a in product(options, repeat=n):
        used = [j for j in a if j != NONE]
        if len(used) == len(set(used)):
            yield a


def welfare(values, a, skip=None):
    return sum(values[i][j] for i, j in enumerate(a) if j != NONE and i != skip)


def best_welfare(values, skip=None):
    n, m = len(values), len(values[0])
    return max(welfare(values, a, skip) for a in assignments(n, m) if skip is None or a[skip] == NONE)


def is_walrasian(values, prices, a):
    """Every bidder gets an option in her demand set and every unsold item has price 0."""
    n, m = len(values), len(prices)
    if any(a[i] not in demand(values, prices, i) for i in range(n)):
        return False
    sold = {j for j in a if j != NONE}
    return all(prices[j] == 0 for j in range(m) if j not in sold)


def walrasian_exists(values, prices):
    n, m = len(values), len(prices)
    return any(is_walrasian(values, prices, a) for a in assignments(n, m))


def random_values(rng, n, m, hi):
    return [[rng.randint(0, hi) for _ in range(m)] for _ in range(n)]


class TestDGS(unittest.TestCase):
    def test_single_item_check_value(self):
        prices, a = dgs_auction([[10], [7], [3]])
        self.assertEqual(prices, [7])
        self.assertEqual(a, [0, NONE, NONE])

    def test_page_example(self):
        trace = []
        prices, a = dgs_auction(EXAMPLE, trace)
        self.assertEqual(prices, [1, 3, 0])
        self.assertEqual(a, [1, 0, 2])
        self.assertTrue(is_walrasian(EXAMPLE, prices, a))
        self.assertEqual(
            trace,
            [([0, 0, 0], frozenset({1})), ([0, 1, 0], frozenset({1})), ([0, 2, 0], frozenset({0, 1}))],
        )

    def test_walrasian_and_efficient(self):
        rng = random.Random(1)
        for _ in range(300):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            values = random_values(rng, n, m, 9)
            prices, a = dgs_auction(values)
            self.assertTrue(is_walrasian(values, prices, a))
            self.assertEqual(welfare(values, a), best_welfare(values))
            self.assertTrue(all(p == int(p) and p >= 0 for p in prices))

    def test_prices_are_vcg_payments(self):
        # Leonard 1983: the minimum Walrasian prices are the VCG payments.
        rng = random.Random(2)
        for _ in range(250):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            values = random_values(rng, n, m, 9)
            prices, a = dgs_auction(values)
            total = best_welfare(values)
            for i, j in enumerate(a):
                if j != NONE:
                    vcg = best_welfare(values, skip=i) - (total - values[i][j])
                    self.assertEqual(prices[j], vcg)

    def test_prices_are_minimal(self):
        rng = random.Random(3)
        for _ in range(60):
            n, m = rng.randint(1, 3), rng.randint(1, 3)
            values = random_values(rng, n, m, 6)
            prices, _ = dgs_auction(values)
            for q in product(*[range(int(p) + 1) for p in prices]):
                q = [Fraction(x) for x in q]
                if q != prices:
                    self.assertFalse(walrasian_exists(values, q))

    def test_ties_and_zero_values(self):
        rng = random.Random(4)
        for _ in range(200):
            n, m = rng.randint(1, 5), rng.randint(1, 3)
            values = random_values(rng, n, m, 2)
            prices, a = dgs_auction(values)
            self.assertTrue(is_walrasian(values, prices, a))

    def test_identical_bidders(self):
        prices, a = dgs_auction([[5, 3], [5, 3], [5, 3]])
        # With three equal bidders and two items, the third bidder must be indifferent.
        self.assertEqual(prices, [5, 3])
        self.assertTrue(is_walrasian([[5, 3]] * 3, prices, a))

    def test_round_bound(self):
        rng = random.Random(5)
        for _ in range(100):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            values = random_values(rng, n, m, 9)
            trace = []
            prices, _ = dgs_auction(values, trace)
            # Each round raises at least one price by 1, so there are at most sum(prices) rounds.
            self.assertLessEqual(len(trace), sum(prices))
            for _, S in trace:
                self.assertGreater(len(S), 0)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            dgs_auction([[1, 2], [3]])
        with self.assertRaises(ValueError):
            dgs_auction([[-1]])


if __name__ == "__main__":
    unittest.main()
