# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sainte-lague-method/. The authors are listed in prov/YHWSF5.jsonl.

import random
import unittest
from fractions import Fraction

from sainte_lague_method import sainte_lague_method


def compositions(h, n):
    """Yield every list of n nonnegative integers with sum h."""
    if n == 1:
        yield [h]
        return
    for x in range(h + 1):
        for rest in compositions(h - x, n - 1):
            yield [x] + rest


def by_scan(votes, h):
    """A second implementation: a linear scan for each seat, dividing by a + 1/2."""
    a = [0] * len(votes)
    for _ in range(h):
        best = max(range(len(votes)), key=lambda i: (Fraction(votes[i]) / (a[i] + Fraction(1, 2)), -i))
        a[best] += 1
    return a


def gap(votes, a):
    """Return (low, high): the largest votes / (2 seats + 1) and the smallest votes / (2 seats - 1).

    a is a Sainte-Lague apportionment exactly when low <= high; it is the only one when low < high.
    """
    low = max(Fraction(v, 2 * x + 1) for v, x in zip(votes, a))
    high = min((Fraction(v, 2 * x - 1) for v, x in zip(votes, a) if x > 0), default=None)
    return low, high


def is_webster(votes, a):
    low, high = gap(votes, a)
    return high is None or low <= high


def tie_free(votes, a):
    low, high = gap(votes, a)
    return high is None or low < high


def quotas(votes, h):
    return [Fraction(h * v, sum(votes)) for v in votes]


def floor(x):
    return x.numerator // x.denominator


def within_quota(votes, h, a):
    return all(floor(q) <= x <= -floor(-q) for x, q in zip(a, quotas(votes, h)))


class TestCheckValues(unittest.TestCase):
    V = [100000, 80000, 30000, 20000]

    def test_eight_seats(self):
        self.assertEqual(sainte_lague_method(self.V, 8), [3, 3, 1, 1])

    def test_four_seats(self):
        self.assertEqual(sainte_lague_method(self.V, 4), [2, 1, 1, 0])

    def test_lower_quota_violation(self):
        p, h = [26, 5, 3, 1], 19
        a = sainte_lague_method(p, h)
        self.assertEqual(a, [13, 3, 2, 1])
        self.assertEqual(quotas(p, h)[0], Fraction(494, 35))
        self.assertTrue(tie_free(p, a))

    def test_errors(self):
        for p, h in (([0, 0], 3), ([1, -1, 2], 2), ([1, 2], -1)):
            with self.assertRaises(ValueError):
                sainte_lague_method(p, h)


class TestProperties(unittest.TestCase):
    def test_against_scan_and_divisor_form(self):
        rng = random.Random(41)
        for _ in range(1500):
            n = rng.randint(1, 7)
            p = [rng.randint(0, 500) for _ in range(n)]
            if sum(p) == 0:
                continue
            h = rng.randint(0, 30)
            a = sainte_lague_method(p, h)
            self.assertEqual(sum(a), h)
            self.assertEqual(a, by_scan(p, h))
            self.assertTrue(is_webster(p, a))
            low, high = gap(p, a)
            if high is not None and low < high and low > 0:
                lam = low + high
                self.assertEqual([floor(Fraction(v) / lam + Fraction(1, 2)) for v in p], a)

    def test_least_squares_by_brute_force(self):
        rng = random.Random(42)
        for _ in range(250):
            n = rng.randint(1, 4)
            p = [rng.randint(1, 60) for _ in range(n)]
            h = rng.randint(0, 9)
            a = sainte_lague_method(p, h)
            webster = [b for b in compositions(h, n) if is_webster(p, b)]
            self.assertIn(a, webster)
            if tie_free(p, a):
                self.assertEqual(webster, [a])
            cost = lambda b: sum(Fraction(x * x, v) for x, v in zip(b, p))
            self.assertEqual(cost(a), min(cost(b) for b in compositions(h, n)))

    def test_three_parties_stay_within_quota(self):
        rng = random.Random(43)
        for _ in range(3000):
            p = [rng.randint(1, 300) for _ in range(3)]
            h = rng.randint(1, 40)
            a = sainte_lague_method(p, h)
            if tie_free(p, a):
                self.assertTrue(within_quota(p, h, a))

    def test_house_and_population_monotone(self):
        rng = random.Random(44)
        for _ in range(600):
            n = rng.randint(2, 5)
            p = [rng.randint(1, 100) for _ in range(n)]
            h = rng.randint(1, 15)
            a = sainte_lague_method(p, h)
            b = sainte_lague_method(p, h + 1)
            self.assertTrue(all(y >= x for x, y in zip(a, b)))
            p2 = [max(1, v + rng.randint(-30, 30)) for v in p]
            a2 = sainte_lague_method(p2, h)
            if not (tie_free(p, a) and tie_free(p2, a2)):
                continue
            for i in range(n):
                for j in range(n):
                    if i != j and p2[i] >= p[i] and p2[j] <= p[j]:
                        self.assertFalse(a2[i] < a[i] and a2[j] > a[j])


if __name__ == "__main__":
    unittest.main()
