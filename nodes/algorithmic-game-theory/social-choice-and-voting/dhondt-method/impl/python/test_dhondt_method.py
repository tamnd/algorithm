# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dhondt-method/. The authors are listed in prov/0Y9DP6.jsonl.

import random
import unittest
from fractions import Fraction

from dhondt_method import dhondt_method


def compositions(h, n):
    """Yield every list of n nonnegative integers with sum h."""
    if n == 1:
        yield [h]
        return
    for x in range(h + 1):
        for rest in compositions(h - x, n - 1):
            yield [x] + rest


def by_scan(votes, h):
    """A second implementation: a linear scan for each seat, with Fraction quotients."""
    a = [0] * len(votes)
    for _ in range(h):
        best = max(range(len(votes)), key=lambda i: (Fraction(votes[i], a[i] + 1), -i))
        a[best] += 1
    return a


def gap(votes, a):
    """Return (low, high): the largest votes / (seats + 1) and the smallest votes / seats.

    a is a D'Hondt apportionment exactly when low <= high; it is the only one when low < high.
    """
    low = max(Fraction(v, x + 1) for v, x in zip(votes, a))
    high = min((Fraction(v, x) for v, x in zip(votes, a) if x > 0), default=None)
    return low, high


def is_jefferson(votes, a):
    low, high = gap(votes, a)
    return high is None or low <= high


def quotas(votes, h):
    return [Fraction(h * v, sum(votes)) for v in votes]


def floor(x):
    return x.numerator // x.denominator


class TestCheckValues(unittest.TestCase):
    V = [100000, 80000, 30000, 20000]

    def test_eight_seats(self):
        self.assertEqual(dhondt_method(self.V, 8), [4, 3, 1, 0])

    def test_sequence(self):
        got = [dhondt_method(self.V, h) for h in range(1, 8)]
        self.assertEqual(got, [[1, 0, 0, 0], [1, 1, 0, 0], [2, 1, 0, 0], [2, 2, 0, 0], [3, 2, 0, 0], [3, 2, 1, 0], [3, 3, 1, 0]])

    def test_three_way_tie(self):
        a = dhondt_method(self.V, 8)
        tied = [Fraction(v, x + 1) for v, x in zip(self.V, a)]
        self.assertEqual(tied.count(Fraction(20000)), 3)
        self.assertEqual(dhondt_method(self.V, 9), [5, 3, 1, 0])

    def test_upper_quota_violation(self):
        p, h = [8, 2, 1, 1], 7
        self.assertEqual(dhondt_method(p, h), [6, 1, 0, 0])
        self.assertEqual(quotas(p, h)[0], Fraction(14, 3))
        low, high = gap(p, [6, 1, 0, 0])
        self.assertLess(low, high)

    def test_errors(self):
        for p, h in (([0, 0], 3), ([1, -1, 2], 2), ([1, 2], -1)):
            with self.assertRaises(ValueError):
                dhondt_method(p, h)


class TestProperties(unittest.TestCase):
    def test_against_scan_and_divisor_form(self):
        rng = random.Random(31)
        for _ in range(1500):
            n = rng.randint(1, 7)
            p = [rng.randint(0, 500) for _ in range(n)]
            if sum(p) == 0:
                continue
            h = rng.randint(0, 30)
            a = dhondt_method(p, h)
            self.assertEqual(sum(a), h)
            self.assertEqual(a, by_scan(p, h))
            self.assertTrue(is_jefferson(p, a))
            low, high = gap(p, a)
            if high is not None and low < high and low > 0:
                lam = (low + high) / 2
                self.assertEqual([floor(Fraction(v) / lam) for v in p], a)
            for x, q in zip(a, quotas(p, h)):
                self.assertGreaterEqual(x, floor(q))

    def test_brute_force(self):
        rng = random.Random(32)
        for _ in range(250):
            n = rng.randint(1, 4)
            p = [rng.randint(1, 60) for _ in range(n)]
            h = rng.randint(0, 9)
            a = dhondt_method(p, h)
            divisor = [b for b in compositions(h, n) if is_jefferson(p, b)]
            self.assertIn(a, divisor)
            low, high = gap(p, a)
            if high is None or low < high:
                self.assertEqual(divisor, [a])
            cost = lambda b: sum(Fraction(x * (x + 1), v) for x, v in zip(b, p))
            self.assertEqual(cost(a), min(cost(b) for b in compositions(h, n)))

    def test_house_and_population_monotone(self):
        rng = random.Random(33)
        for _ in range(600):
            n = rng.randint(2, 5)
            p = [rng.randint(1, 100) for _ in range(n)]
            h = rng.randint(1, 15)
            a = dhondt_method(p, h)
            b = dhondt_method(p, h + 1)
            self.assertTrue(all(y >= x for x, y in zip(a, b)))
            p2 = [max(1, v + rng.randint(-30, 30)) for v in p]
            a2 = dhondt_method(p2, h)
            l1, h1 = gap(p, a)
            l2, h2 = gap(p2, a2)
            if (h1 is not None and l1 == h1) or (h2 is not None and l2 == h2):
                continue
            for i in range(n):
                for j in range(n):
                    if i != j and p2[i] >= p[i] and p2[j] <= p[j]:
                        self.assertFalse(a2[i] < a[i] and a2[j] > a[j])


if __name__ == "__main__":
    unittest.main()
