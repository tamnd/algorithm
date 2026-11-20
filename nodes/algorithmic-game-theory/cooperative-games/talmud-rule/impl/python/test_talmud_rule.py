# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/talmud-rule/. The authors are listed in prov/J1054R.jsonl.
"""Tests for talmud_rule: the Mishna values, consistency, duality and the nucleolus."""

import itertools
import random
import unittest
from fractions import Fraction as F

from talmud_rule import cea, cel, contested_garment, talmud


def cea_by_breakpoints(claims, amount):
    """A second CEA: try each number k of fully paid claimants and solve for lam."""
    claims = [F(c) for c in claims]
    n = len(claims)
    s = sorted(claims)
    for k in range(n):
        lam = (F(amount) - sum(s[:k])) / (n - k)
        low = s[k - 1] if k else F(0)
        if low <= lam <= s[k]:
            return [min(c, lam) for c in claims]
    return list(claims)


def talmud_by_formula(claims, estate):
    """The Talmud rule written as CEA or CEL on the half claims."""
    claims = [F(c) for c in claims]
    half = [c / 2 for c in claims]
    total = sum(claims)
    if estate <= total / 2:
        return cea_by_breakpoints(half, estate)
    extra = cel(half, F(estate) - total / 2)
    return [h + e for h, e in zip(half, extra)]


def bankruptcy_game(claims, estate):
    n = len(claims)
    v = [F(0)] * (1 << n)
    for S in range(1, 1 << n):
        rest = sum(claims[i] for i in range(n) if not S >> i & 1)
        v[S] = max(F(0), F(estate) - rest)
    return v


def theta(v, x):
    n = len(x)
    full = (1 << n) - 1
    ex = []
    for S in range(1, full):
        ex.append(v[S] - sum(x[i] for i in range(n) if S >> i & 1))
    return sorted(ex, reverse=True)


def grid_nucleolus(claims, estate, D):
    """The lexicographic minimum of the sorted excesses over the imputations on a 1/D grid.
    In a bankruptcy game v({i}) = max(0, E - sum of the other claims)."""
    n = len(claims)
    v = bankruptcy_game(claims, estate)
    base = [v[1 << i] for i in range(n)]
    slack = int((F(estate) - sum(base)) * D)
    best = None
    for ks in itertools.product(range(slack + 1), repeat=n - 1):
        last = slack - sum(ks)
        if last < 0:
            continue
        x = [base[i] + F(k, D) for i, k in enumerate(list(ks) + [last])]
        key = theta(v, x)
        if best is None or key < best[0]:
            best = (key, x)
    return best[1]


def random_problem(rng, n, top):
    claims = [rng.randint(0, top) for _ in range(n)]
    if sum(claims) == 0:
        claims[0] = 1
    estate = F(rng.randint(0, 4 * sum(claims)), 4)
    return claims, estate


class CheckValues(unittest.TestCase):
    def test_mishna_table(self):
        claims = [100, 200, 300]
        self.assertEqual(talmud(claims, 100), [F(100, 3)] * 3)
        self.assertEqual(talmud(claims, 200), [50, 75, 75])
        self.assertEqual(talmud(claims, 300), [50, 100, 150])

    def test_contested_garment(self):
        self.assertEqual(contested_garment(1, F(1, 2), 1), [F(3, 4), F(1, 4)])
        self.assertEqual(talmud([1, F(1, 2)], 1), [F(3, 4), F(1, 4)])

    def test_cea_cel(self):
        self.assertEqual(cea([100, 200, 300], 200), [F(200, 3)] * 3)
        self.assertEqual(cea([100, 200, 300], 400), [100, 150, 150])
        self.assertEqual(cel([100, 200, 300], 300), [0, 100, 200])
        self.assertEqual(cel([100, 200, 300], 450), [50, 150, 250])

    def test_edges(self):
        self.assertEqual(talmud([5], 3), [3])
        self.assertEqual(talmud([4, 6], 0), [0, 0])
        self.assertEqual(talmud([4, 6], 10), [4, 6])
        self.assertEqual(talmud([4, 6], 5), [2, 3])
        self.assertEqual(talmud([0, 6], 4), [0, 4])
        self.assertEqual(talmud([3, 3, 3], 4), [F(4, 3)] * 3)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            talmud([1, 2], 4)
        with self.assertRaises(ValueError):
            talmud([1, -2], 0)
        with self.assertRaises(ValueError):
            talmud([1, 2], -1)


class Properties(unittest.TestCase):
    def setUp(self):
        rng = random.Random(2024)
        self.cases = [random_problem(rng, rng.randint(1, 6), 20) for _ in range(300)]

    def test_feasible(self):
        for c, E in self.cases:
            x = talmud(c, E)
            self.assertEqual(sum(x), E)
            self.assertTrue(all(0 <= xi <= ci for xi, ci in zip(x, c)))

    def test_second_implementation(self):
        for c, E in self.cases:
            self.assertEqual(talmud(c, E), talmud_by_formula(c, E))
            self.assertEqual(cea(c, min(E, sum(c))), cea_by_breakpoints(c, min(E, sum(c))))

    def test_self_dual(self):
        for c, E in self.cases:
            x = talmud(c, E)
            y = talmud(c, sum(c) - E)
            self.assertEqual(y, [ci - xi for ci, xi in zip(c, x)])

    def test_order_preserving(self):
        for c, E in self.cases:
            x = talmud(c, E)
            for i, j in itertools.combinations(range(len(c)), 2):
                if c[i] <= c[j]:
                    self.assertLessEqual(x[i], x[j])
                    self.assertLessEqual(c[i] - x[i], c[j] - x[j])

    def test_half_claims(self):
        for c, E in self.cases:
            x = talmud(c, E)
            half = sum(c) / F(2)
            for xi, ci in zip(x, c):
                if E <= half:
                    self.assertLessEqual(xi, F(ci, 2))
                else:
                    self.assertGreaterEqual(xi, F(ci, 2))

    def test_contested_garment_consistent(self):
        for c, E in self.cases:
            x = talmud(c, E)
            for i, j in itertools.combinations(range(len(c)), 2):
                self.assertEqual([x[i], x[j]], contested_garment(c[i], c[j], x[i] + x[j]))

    def test_estate_monotone(self):
        rng = random.Random(5)
        for _ in range(40):
            c = [rng.randint(0, 15) for _ in range(rng.randint(1, 5))]
            prev = None
            for k in range(4 * sum(c) + 1):
                x = talmud(c, F(k, 4))
                if prev is not None:
                    self.assertTrue(all(a <= b for a, b in zip(prev, x)))
                prev = x


class Nucleolus(unittest.TestCase):
    def test_grid_nucleolus(self):
        rng = random.Random(77)
        cases = [([100, 200, 300], 100), ([100, 200, 300], 200), ([100, 200, 300], 300)]
        scaled = [([c // 50 for c in cl], E // 50) for cl, E in cases]
        for _ in range(12):
            n = rng.randint(2, 3)
            c = [rng.randint(0, 5) for _ in range(n)]
            if sum(c) == 0:
                continue
            scaled.append((c, rng.randint(0, sum(c))))
        for c, E in scaled:
            self.assertEqual(grid_nucleolus(c, E, 6), talmud(c, E), (c, E))


if __name__ == "__main__":
    unittest.main()
