# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moulin-mechanism/. The authors are listed in prov/ZZQA5X.jsonl.
"""Tests for moulin_mechanism: the worked example, the unique maximal feasible set,
budget balance, the participation properties, and group strategyproofness by brute force."""

import itertools
import random
import unittest
from fractions import Fraction as F

from moulin_mechanism import (airport_shapley, coverage_cost, coverage_shapley, equal_split,
                              moulin)


def subsets(players):
    players = list(players)
    for r in range(len(players) + 1):
        for T in itertools.combinations(players, r):
            yield frozenset(T)


def maximal_feasible(players, bids, xi):
    """Brute force: the union of all sets T with bids[i] >= xi(i, T) for every i in T."""
    union = frozenset()
    feasible = []
    for T in subsets(players):
        if not T:
            continue
        sh = xi(T)
        if all(bids[i] >= sh[i] for i in T):
            feasible.append(T)
            union |= T
    return union, feasible


def is_cross_monotonic(players, xi):
    for T in subsets(players):
        if not T:
            continue
        tt = xi(T)
        for S in subsets(T):
            if S:
                ss = xi(S)
                if any(ss[i] < tt[i] for i in S):
                    return False
    return True


def utility(values, served, pay, i):
    return (values[i] if i in served else 0) - pay[i]


def gsp_violation(players, values, xi, grid, coalitions_misreports):
    """Return a profitable group deviation, or None."""
    served, pay = moulin(players, values, xi)
    for C, lies in coalitions_misreports:
        for lie in lies:
            bids = dict(values)
            bids.update(zip(C, lie))
            s2, p2 = moulin(players, bids, xi)
            gain = [utility(values, s2, p2, i) - utility(values, served, pay, i) for i in C]
            if all(g >= 0 for g in gain) and any(g > 0 for g in gain):
                return C, lie
    return None


def random_coverage(rng, n):
    elems = list(range(5))
    covers = {i: set(e for e in elems if rng.random() < 0.5) or {rng.choice(elems)} for i in range(n)}
    weights = {e: rng.randint(1, 6) for e in elems}
    return covers, weights


class TestMoulin(unittest.TestCase):
    def test_worked_example(self):
        xi = airport_shapley({1: 2, 2: 4, 3: 6})
        self.assertEqual(xi(frozenset({1, 2, 3})), {1: F(2, 3), 2: F(5, 3), 3: F(11, 3)})
        served, pay = moulin([1, 2, 3], {1: F(1), 2: F(3, 2), 3: F(5)}, xi)
        self.assertEqual(served, frozenset({1, 3}))
        self.assertEqual(pay, {1: 1, 2: 0, 3: 5})
        served, pay = moulin([1, 2, 3], {1: F(1), 2: F(2), 3: F(5)}, xi)
        self.assertEqual(served, frozenset({1, 2, 3}))
        self.assertEqual(pay[2], F(5, 3))

    def test_public_good(self):
        xi = equal_split(1)
        served, pay = moulin([1, 2, 3], {1: F(6, 10), 2: F(4, 10), 3: F(3, 10)}, xi)
        self.assertEqual(served, frozenset())
        self.assertEqual(set(pay.values()), {0})
        served, pay = moulin([1, 2, 3], {1: F(6, 10), 2: F(1, 2), 3: F(3, 10)}, xi)
        self.assertEqual(served, frozenset({1, 2}))
        self.assertEqual(pay, {1: F(1, 2), 2: F(1, 2), 3: 0})

    def test_edge_cases(self):
        self.assertEqual(moulin([], {}, equal_split(1)), (frozenset(), {}))
        served, pay = moulin([7], {7: F(1)}, equal_split(1))
        self.assertEqual((served, pay), (frozenset({7}), {7: 1}))
        served, _ = moulin([7], {7: F(99, 100)}, equal_split(1))
        self.assertEqual(served, frozenset())

    def test_maximal_set_and_budget_balance(self):
        rng = random.Random(11)
        for _ in range(500):
            n = rng.randint(1, 5)
            covers, weights = random_coverage(rng, n)
            xi = coverage_shapley(covers, weights)
            players = list(range(n))
            self.assertTrue(is_cross_monotonic(players, xi))
            bids = {i: F(rng.randint(0, 24), 4) for i in players}
            served, pay = moulin(players, bids, xi)
            union, feasible = maximal_feasible(players, bids, xi)
            self.assertEqual(served, union)
            if served:
                self.assertIn(served, feasible)
            self.assertEqual(sum(pay.values()), coverage_cost(covers, weights, served))
            for i in players:
                self.assertGreaterEqual(pay[i], 0)
                if i in served:
                    self.assertLessEqual(pay[i], bids[i])
                else:
                    self.assertEqual(pay[i], 0)
            big = max(xi(frozenset({i}))[i] for i in players)
            for i in players:
                b2 = dict(bids)
                b2[i] = big
                self.assertIn(i, moulin(players, b2, xi)[0])

    def test_group_strategyproof_exhaustive(self):
        players = [1, 2, 3]
        xi = airport_shapley({1: 2, 2: 4, 3: 6})
        grid = [F(0), F(2, 3), F(5, 3), F(4), F(6)]
        plan = []
        for r in (1, 2, 3):
            for C in itertools.combinations(players, r):
                plan.append((C, list(itertools.product(grid, repeat=r))))
        for vals in itertools.product(grid, repeat=3):
            values = dict(zip(players, vals))
            self.assertIsNone(gsp_violation(players, values, xi, grid, plan))

    def test_group_strategyproof_random(self):
        rng = random.Random(5)
        players = [0, 1, 2]
        grid = [F(k, 2) for k in range(9)]
        for _ in range(8):
            covers, weights = random_coverage(rng, 3)
            xi = coverage_shapley(covers, weights)
            plan = []
            for r in (1, 2, 3):
                for C in itertools.combinations(players, r):
                    lies = list(itertools.product(grid, repeat=r))
                    if r == 3:
                        lies = rng.sample(lies, 60)
                    plan.append((C, lies))
            for _ in range(4):
                values = {i: rng.choice(grid) for i in players}
                self.assertIsNone(gsp_violation(players, values, xi, grid, plan))

    def test_not_cross_monotonic_breaks_truthfulness(self):
        table = {
            frozenset({1}): {1: F(8)}, frozenset({2}): {2: F(9)}, frozenset({3}): {3: F(7)},
            frozenset({1, 2}): {1: F(8), 2: F(1)}, frozenset({1, 3}): {1: F(8), 3: F(7)},
            frozenset({2, 3}): {2: F(4), 3: F(7)}, frozenset({1, 2, 3}): {1: F(1), 2: F(4), 3: F(7)},
            frozenset(): {},
        }
        xi = table.__getitem__
        self.assertFalse(is_cross_monotonic([1, 2, 3], xi))
        values = {1: F(8), 2: F(2), 3: F(0)}
        served, pay = moulin([1, 2, 3], values, xi)
        self.assertEqual(served, frozenset({1}))
        lie = dict(values)
        lie[2] = F(4)
        served2, pay2 = moulin([1, 2, 3], lie, xi)
        self.assertEqual(served2, frozenset({1, 2}))
        self.assertEqual(utility(values, served2, pay2, 2), 1)
        self.assertEqual(utility(values, served, pay, 2), 0)


if __name__ == "__main__":
    unittest.main()
