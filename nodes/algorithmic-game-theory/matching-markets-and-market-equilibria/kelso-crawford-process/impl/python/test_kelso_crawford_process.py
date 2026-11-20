# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kelso-crawford-process/. The authors are listed in prov/AYJGGA.jsonl.

import random
import unittest
from fractions import Fraction
from functools import lru_cache
from itertools import product

from kelso_crawford_process import NONE, allocation, bundles, kelso_crawford


def additive(w):
    return lambda S: sum(w[j] for j in S)


def unit_demand(w):
    return lambda S: max([0] + [w[j] for j in S])


def oxs(w):
    """An assignment valuation: the bidder has len(w) slots, slot s gives w[s][j] for item j,
    and v(S) is the best value of placing items of S in distinct slots. It has gross substitutes."""

    @lru_cache(maxsize=None)
    def v(S):
        items = sorted(S)

        def best(k, free):
            if k == len(items):
                return 0
            out = best(k + 1, free)  # item items[k] stays unused
            for s in free:
                out = max(out, w[s][items[k]] + best(k + 1, free - {s}))
            return out

        return best(0, frozenset(range(len(w))))

    return v


def welfare(values, owner):
    return sum(values[i](S) for i, S in enumerate(allocation(owner, len(values))))


def best_welfare(values, m):
    n = len(values)
    return max(welfare(values, list(o)) for o in product(range(-1, n), repeat=m))


def random_oxs(rng, m, hi):
    k = rng.randint(1, 3)
    return oxs(tuple(tuple(rng.randint(0, hi) for _ in range(m)) for _ in range(k)))


class TestKelsoCrawford(unittest.TestCase):
    def test_page_example(self):
        values = [additive([2, 1]), unit_demand([2, 2])]
        trace = []
        prices, owner = kelso_crawford(values, 2, Fraction(1, 3), trace)
        third = Fraction(1, 3)
        self.assertEqual(
            trace,
            [
                (0, [0, 1], [third, third]),
                (1, [0], [2 * third, third]),
                (0, [0], [1, third]),
                (1, [1], [1, 2 * third]),
            ],
        )
        self.assertEqual(prices, [1, 2 * third])
        self.assertEqual(owner, [0, 1])
        self.assertEqual(welfare(values, owner), 4)

    def test_single_item_is_english_auction(self):
        delta = Fraction(1, 2)
        prices, owner = kelso_crawford([additive([5]), additive([3])], 1, delta)
        self.assertEqual(owner, [0])
        self.assertTrue(3 - delta <= prices[0] <= 3 + delta)

    def test_optimal_with_small_step(self):
        rng = random.Random(1)
        for _ in range(120):
            n, m = rng.randint(1, 3), rng.randint(1, 4)
            values = [random_oxs(rng, m, 5) for _ in range(n)]
            _, owner = kelso_crawford(values, m)
            self.assertEqual(welfare(values, owner), best_welfare(values, m))

    def test_approximate_equilibrium(self):
        # Each bidder's bundle is within delta per extra item of her best bundle at the prices.
        rng = random.Random(2)
        for _ in range(120):
            n, m = rng.randint(1, 3), rng.randint(1, 4)
            values = [random_oxs(rng, m, 5) for _ in range(n)]
            delta = Fraction(1, rng.randint(1, 4))
            prices, owner = kelso_crawford(values, m, delta)
            held = allocation(owner, n)
            for i in range(n):
                u = values[i](held[i]) - sum(prices[j] for j in held[i])
                for T in bundles(m):
                    uT = values[i](T) - sum(prices[j] for j in T)
                    self.assertGreaterEqual(u, uT - delta * len(T - held[i]))
            for j in range(m):
                if owner[j] == NONE:
                    self.assertEqual(prices[j], 0)
            self.assertGreaterEqual(welfare(values, owner), best_welfare(values, m) - m * delta)

    def test_bid_bound(self):
        rng = random.Random(3)
        for _ in range(100):
            n, m = rng.randint(1, 3), rng.randint(1, 4)
            hi = 6
            values = [random_oxs(rng, m, hi) for _ in range(n)]
            delta = Fraction(1, m + 1)
            trace = []
            prices, _ = kelso_crawford(values, m, delta, trace)
            self.assertTrue(all(p <= hi + delta for p in prices))
            self.assertLessEqual(len(trace) * delta, m * (hi + delta))
            for k in range(1, len(trace)):
                self.assertTrue(all(a <= b for a, b in zip(trace[k - 1][2], trace[k][2])))

    def test_additive_bidders_get_their_items_cheaply(self):
        # With additive values every item is a separate English auction.
        rng = random.Random(4)
        for _ in range(60):
            n, m = rng.randint(2, 3), rng.randint(1, 3)
            w = [[rng.randint(0, 6) for _ in range(m)] for _ in range(n)]
            delta = Fraction(1, 4)
            prices, owner = kelso_crawford([additive(r) for r in w], m, delta)
            for j in range(m):
                col = sorted((w[i][j] for i in range(n)), reverse=True)
                if owner[j] != NONE:
                    self.assertEqual(w[owner[j]][j], col[0])
                    self.assertTrue(col[1] - delta <= prices[j] <= col[1] + delta)

    def test_complements_break_the_process(self):
        both = lambda S: 3 if len(S) == 2 else 0
        with self.assertRaises(ValueError):
            kelso_crawford([both, unit_demand([0, 3])], 2, Fraction(1, 3))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            kelso_crawford([additive([1])], 1, 0)
        with self.assertRaises(ValueError):
            kelso_crawford([additive([1])], -1)


if __name__ == "__main__":
    unittest.main()
