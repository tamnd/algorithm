# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamilton-method/. The authors are listed in prov/S01MQ4.jsonl.

import random
import unittest
from fractions import Fraction

from hamilton_method import hamilton_method, quotas


def compositions(h, n):
    """Yield every list of n nonnegative integers with sum h."""
    if n == 1:
        yield [h]
        return
    for x in range(h + 1):
        for rest in compositions(h - x, n - 1):
            yield [x] + rest


def cost(a, q):
    return sum((x - y) ** 2 for x, y in zip(a, q))


def by_fractions(populations, h):
    """A second implementation with Fraction quotas and their fractional parts."""
    q = quotas(populations, h)
    a = [x.numerator // x.denominator for x in q]
    frac = [x - y for x, y in zip(q, a)]
    for i in sorted(range(len(q)), key=lambda i: (-frac[i], i))[: h - sum(a)]:
        a[i] += 1
    return a


class TestCheckValues(unittest.TestCase):
    def test_four_parties(self):
        self.assertEqual(hamilton_method([100000, 80000, 30000, 20000], 8), [3, 3, 1, 1])

    def test_alabama_paradox(self):
        self.assertEqual(hamilton_method([3, 3, 1], 3), [1, 1, 1])
        self.assertEqual(hamilton_method([3, 3, 1], 4), [2, 2, 0])

    def test_population_paradox(self):
        self.assertEqual(hamilton_method([5, 1, 3], 5), [3, 0, 2])
        self.assertEqual(hamilton_method([6, 1, 6], 5), [2, 1, 2])

    def test_new_states_paradox(self):
        self.assertEqual(hamilton_method([8, 1], 4), [4, 0])
        self.assertEqual(hamilton_method([8, 1, 3], 5), [3, 1, 1])

    def test_errors(self):
        for p, h in (([0, 0], 3), ([1, -1, 2], 2), ([1, 2], -1)):
            with self.assertRaises(ValueError):
                hamilton_method(p, h)


class TestProperties(unittest.TestCase):
    def test_sum_and_quota(self):
        rng = random.Random(21)
        for _ in range(3000):
            n = rng.randint(1, 8)
            p = [rng.randint(0, 1000) for _ in range(n)]
            if sum(p) == 0:
                continue
            h = rng.randint(0, 40)
            a = hamilton_method(p, h)
            self.assertEqual(sum(a), h)
            for x, q in zip(a, quotas(p, h)):
                self.assertTrue(q.numerator // q.denominator <= x <= -(-q.numerator // q.denominator))
            self.assertEqual(a, by_fractions(p, h))

    def test_least_squares_by_brute_force(self):
        rng = random.Random(22)
        for _ in range(250):
            n = rng.randint(1, 4)
            p = [rng.randint(1, 60) for _ in range(n)]
            h = rng.randint(0, 9)
            q = quotas(p, h)
            a = hamilton_method(p, h)
            best = min(cost(b, q) for b in compositions(h, n))
            self.assertEqual(cost(a, q), best)
            r = [x - x.numerator // x.denominator for x in q]
            if len(set(r)) == n:
                self.assertEqual([b for b in compositions(h, n) if cost(b, q) == best], [a])

    def test_alabama_paradox_is_common(self):
        found = 0
        for p in ([3, 3, 1], [5, 5, 2], [7, 6, 2]):
            for h in range(1, 20):
                a, b = hamilton_method(p, h), hamilton_method(p, h + 1)
                if any(y < x for x, y in zip(a, b)):
                    found += 1
        self.assertGreater(found, 0)

    def test_quota_sums(self):
        self.assertEqual(sum(quotas([100000, 80000, 30000, 20000], 8)), 8)
        self.assertEqual(quotas([3, 3, 1], 4), [Fraction(12, 7), Fraction(12, 7), Fraction(4, 7)])


if __name__ == "__main__":
    unittest.main()
