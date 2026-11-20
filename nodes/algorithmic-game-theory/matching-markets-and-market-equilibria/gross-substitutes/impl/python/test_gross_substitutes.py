# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gross-substitutes/. The authors are listed in prov/9N457B.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import product

from gross_substitutes import bundles, check_by_prices, check_local, demand

GRID = [0, 1, 2, 3]  # integer prices up to one more than every marginal value of the small tests


def table(m, vals):
    """A valuation given by its values on the nonempty bundles, in the order of bundles(m)."""
    d = dict(zip(bundles(m)[1:], vals))
    d[frozenset()] = 0
    return lambda S: d[frozenset(S)]


def is_monotone(v, m):
    B = bundles(m)
    return all(v(S) <= v(T) for S in B for T in B if S <= T)


def rank_sum_example():
    """The sum of matroid ranks v = r_a + 2 r_b + 3 r_c on goods a, b, c (0, 1, 2) from the
    survey of Paes Leme (2017). Here r_i(S) is 0 on the empty set, 1 on a single good and on
    the pair without i, and 2 otherwise."""

    def r(i, S):
        if not S:
            return 0
        if len(S) == 1 or S == frozenset({0, 1, 2}) - {i}:
            return 1
        return 2

    return lambda S: r(0, S) + 2 * r(1, S) + 3 * r(2, S)


class TestGrossSubstitutes(unittest.TestCase):
    def test_both_checks_agree_on_small_valuations(self):
        rng = random.Random(1)
        monotone = []
        for vals in product(range(3), repeat=7):
            v = table(3, vals)
            if is_monotone(v, 3):
                monotone.append(v)
        self.assertEqual(len(monotone), 148)
        sample = rng.sample(monotone, 40)
        for v in sample:
            self.assertEqual(check_by_prices(v, 3, GRID) is None, check_local(v, 3) is None)
        # Half-integer prices give the same answer on a few of them.
        for v in sample[:5]:
            half = [Fraction(k, 2) for k in range(7)]
            self.assertEqual(check_by_prices(v, 3, half) is None, check_local(v, 3) is None)

    def test_count_of_gs_valuations(self):
        count = 0
        for vals in product(range(3), repeat=7):
            v = table(3, vals)
            if is_monotone(v, 3) and check_local(v, 3) is None:
                count += 1
        self.assertEqual(count, 34)

    def test_known_classes_pass(self):
        rng = random.Random(2)
        for _ in range(60):
            m = rng.randint(1, 4)
            w = [rng.randint(0, 9) for _ in range(m)]
            k = rng.randint(1, m)
            additive = lambda S, w=w: sum(w[j] for j in S)
            unit = lambda S, w=w: max([0] + [w[j] for j in S])
            uniform_rank = lambda S, k=k: min(len(S), k)
            # Weighted rank of a uniform matroid: the best k items.
            best_k = lambda S, w=w, k=k: sum(sorted((w[j] for j in S), reverse=True)[:k])
            for v in (additive, unit, uniform_rank, best_k):
                self.assertIsNone(check_local(v, m))

    def test_complements_break_both(self):
        both = lambda S: 3 if len(S) == 2 else 0
        self.assertIsNotNone(check_local(both, 2))
        self.assertIsNotNone(check_by_prices(both, 2, [0, 1, 2, 3]))

    def test_rank_sum_example(self):
        v = rank_sum_example()
        self.assertEqual([v(S) for S in bundles(3)], [0, 6, 6, 6, 9, 10, 11, 12])
        p = (4, 5, 4)
        q = (4, 5, 13)
        dp = demand(v, p, 3)
        self.assertEqual(
            sorted(dp, key=sorted), sorted([frozenset({0}), frozenset({2}), frozenset({0, 2}), frozenset({1, 2})], key=sorted)
        )
        self.assertEqual(demand(v, q, 3), [frozenset({0})])
        self.assertIsNotNone(check_by_prices(v, 3, [0, 4, 5, 13]))
        self.assertIsNotNone(check_local(v, 3))

    def test_submodular_is_not_enough(self):
        # A budget-additive valuation: submodular, but not gross substitutes.
        v = lambda S: min(sum([2, 2, 3][j] for j in S), 4)
        B = bundles(3)
        for S in B:
            for T in B:
                self.assertLessEqual(v(S | T) + v(S & T), v(S) + v(T))
        self.assertIsNotNone(check_local(v, 3))
        self.assertIsNotNone(check_by_prices(v, 3, [0, 1, 2, 3, 4, 5]))


if __name__ == "__main__":
    unittest.main()
