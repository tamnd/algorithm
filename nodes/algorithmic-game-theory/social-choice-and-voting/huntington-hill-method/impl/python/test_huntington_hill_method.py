# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huntington-hill-method/. The authors are listed in prov/Y00758.jsonl.

import random
import unittest
from fractions import Fraction

from huntington_hill_method import huntington_hill_method


def compositions_at_least_one(h, n):
    """Yield every list of n integers >= 1 with sum h."""
    if n == 1:
        if h >= 1:
            yield [h]
        return
    for x in range(1, h - n + 2):
        for rest in compositions_at_least_one(h - x, n - 1):
            yield [x] + rest


def by_scan(pops, h):
    """A second implementation: a linear scan for each seat, on the squared priorities."""
    a = [1] * len(pops)
    for _ in range(h - len(pops)):
        best = max(range(len(pops)), key=lambda i: (Fraction(pops[i] ** 2, a[i] * (a[i] + 1)), -i))
        a[best] += 1
    return a


def gap(pops, a):
    """Return (low, high) on squared priorities: the largest p^2 / (a (a + 1)) and the smallest p^2 / ((a - 1) a).

    a is a Huntington-Hill apportionment exactly when low <= high; it is the only one when low < high.
    """
    low = max(Fraction(p * p, x * (x + 1)) for p, x in zip(pops, a))
    high = min((Fraction(p * p, (x - 1) * x) for p, x in zip(pops, a) if x >= 2), default=None)
    return low, high


def is_hh(pops, a):
    low, high = gap(pops, a)
    return high is None or low <= high


def tie_free(pops, a):
    low, high = gap(pops, a)
    return high is None or low < high


def round_geometric(x2):
    """Round x >= 0 given by its square x2: the a >= 1 with (a - 1) a <= x2 < a (a + 1)."""
    a = 1
    while a * (a + 1) <= x2:
        a += 1
    return a


def quotas(pops, h):
    return [Fraction(h * p, sum(pops)) for p in pops]


def floor(x):
    return x.numerator // x.denominator


class TestCheckValues(unittest.TestCase):
    V = [100000, 80000, 30000, 20000]

    def test_eight_seats(self):
        self.assertEqual(huntington_hill_method(self.V, 8), [3, 3, 1, 1])

    def test_four_seats(self):
        self.assertEqual(huntington_hill_method(self.V, 4), [1, 1, 1, 1])

    def test_lower_quota_violation(self):
        p, h = [18, 7, 2, 1], 8
        a = huntington_hill_method(p, h)
        self.assertEqual(a, [4, 2, 1, 1])
        self.assertEqual(quotas(p, h)[0], Fraction(36, 7))
        self.assertTrue(tie_free(p, a))

    def test_errors(self):
        with self.assertRaises(ValueError):
            huntington_hill_method([5, 3, 2], 2)
        with self.assertRaises(ValueError):
            huntington_hill_method([0, 0], 3)
        with self.assertRaises(ValueError):
            huntington_hill_method([4, -1], 3)


class TestProperties(unittest.TestCase):
    def test_against_scan_and_divisor_form(self):
        rng = random.Random(51)
        for _ in range(1500):
            n = rng.randint(1, 7)
            p = [rng.randint(0, 500) for _ in range(n)]
            if sum(p) == 0:
                continue
            h = rng.randint(n, n + 30)
            a = huntington_hill_method(p, h)
            self.assertEqual(sum(a), h)
            self.assertEqual(a, by_scan(p, h))
            self.assertTrue(is_hh(p, a))
            low, high = gap(p, a)
            if high is not None and low < high:
                m2 = (low + high) / 2
                self.assertEqual([round_geometric(Fraction(x * x) / m2) for x in p], a)

    def test_brute_force(self):
        rng = random.Random(52)
        for _ in range(250):
            n = rng.randint(1, 4)
            p = [rng.randint(1, 60) for _ in range(n)]
            h = rng.randint(n, n + 8)
            a = huntington_hill_method(p, h)
            hh = [b for b in compositions_at_least_one(h, n) if is_hh(p, b)]
            self.assertIn(a, hh)
            if tie_free(p, a):
                self.assertEqual(hh, [a])

    def test_no_transfer_lowers_the_relative_difference(self):
        rng = random.Random(53)
        for _ in range(400):
            n = rng.randint(2, 5)
            p = [rng.randint(1, 200) for _ in range(n)]
            h = rng.randint(n, n + 20)
            a = huntington_hill_method(p, h)
            for i in range(n):
                for j in range(n):
                    if i == j or a[i] < 2:
                        continue
                    r = [Fraction(a[i], p[i]), Fraction(a[j], p[j])]
                    s = [Fraction(a[i] - 1, p[i]), Fraction(a[j] + 1, p[j])]
                    self.assertGreaterEqual(max(s) / min(s), max(r) / min(r))

    def test_house_and_population_monotone(self):
        rng = random.Random(54)
        for _ in range(600):
            n = rng.randint(2, 5)
            p = [rng.randint(1, 100) for _ in range(n)]
            h = rng.randint(n, n + 15)
            a = huntington_hill_method(p, h)
            b = huntington_hill_method(p, h + 1)
            self.assertTrue(all(y >= x for x, y in zip(a, b)))
            p2 = [max(1, v + rng.randint(-30, 30)) for v in p]
            a2 = huntington_hill_method(p2, h)
            if not (tie_free(p, a) and tie_free(p2, a2)):
                continue
            for i in range(n):
                for j in range(n):
                    if i != j and p2[i] >= p[i] and p2[j] <= p[j]:
                        self.assertFalse(a2[i] < a[i] and a2[j] > a[j])


if __name__ == "__main__":
    unittest.main()
