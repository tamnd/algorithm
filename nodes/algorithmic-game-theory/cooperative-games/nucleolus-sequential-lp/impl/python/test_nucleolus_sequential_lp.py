# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nucleolus-sequential-lp/. The authors are listed in prov/F1V2JQ.jsonl.
"""Tests for nucleolus_sequential_lp: check values, a grid brute force, Kohlberg's criterion."""

import itertools
import random
import unittest
from fractions import Fraction as F

from agtlp import lp_max
from nucleolus_sequential_lp import (
    excess,
    excess_vector,
    members,
    nucleolus,
    nucleolus_trace,
)


def bankruptcy_game(c, E):
    n = len(c)
    v = [0] * (1 << n)
    for S in range(1, 1 << n):
        rest = sum(c[i] for i in range(n) if not S >> i & 1)
        v[S] = max(0, E - rest)
    return v


def random_game(rng, n, top):
    v = [0] + [rng.randint(0, top) for _ in range((1 << n) - 1)]
    for i in range(n):
        v[1 << i] = rng.randint(0, 1)
    full = (1 << n) - 1
    v[full] = max(v[full], sum(v[1 << i] for i in range(n)))  # the imputation set is nonempty
    return v


def grid_imputations(v, n, D):
    """All imputations x with x_i - v({i}) a multiple of 1/D."""
    full = (1 << n) - 1
    base = [F(v[1 << i]) for i in range(n)]
    slack = (F(v[full]) - sum(base)) * D
    if slack.denominator != 1 or slack < 0:
        return
    slack = int(slack)
    for ks in itertools.product(range(slack + 1), repeat=n - 1):
        last = slack - sum(ks)
        if last < 0:
            continue
        ks = list(ks) + [last]
        yield [base[i] + F(ks[i], D) for i in range(n)]


def balanced(collection, n):
    """True if the coalitions have positive weights with sum of w_S 1_S = 1_N."""
    m = len(collection)
    # Variables: w_S for S in the collection, then s. Maximize s with s <= w_S and s <= 1.
    c = [F(0)] * m + [F(1)]
    A_ub, b_ub = [], []
    for k in range(m):
        row = [F(0)] * (m + 1)
        row[k], row[m] = F(-1), F(1)
        A_ub.append(row)
        b_ub.append(F(0))
    A_ub.append([F(0)] * m + [F(1)])
    b_ub.append(F(1))
    A_eq = [[F(1) if S >> i & 1 else F(0) for S in collection] + [F(0)] for i in range(n)]
    b_eq = [F(1)] * n
    status, _, value, _ = lp_max(c, A_ub, b_ub, A_eq, b_eq)
    return status == "optimal" and value > 0


def kohlberg(v, x):
    """Kohlberg's criterion for the prenucleolus: every upper level set of excesses is balanced."""
    n = len(x)
    full = (1 << n) - 1
    coalitions = range(1, full)
    for level in {excess(v, S, x) for S in coalitions}:
        top = [S for S in coalitions if excess(v, S, x) >= level]
        if not balanced(top, n):
            return False
    return True


def in_core(v, x):
    n = len(x)
    full = (1 << n) - 1
    return sum(x) == v[full] and all(excess(v, S, x) <= 0 for S in range(1, full))


class CheckValues(unittest.TestCase):
    def test_glove_game(self):
        # One left glove (player 0) and two right gloves; also the game [51; 50, 49, 1].
        v = [0, 0, 0, 1, 0, 1, 0, 1]
        self.assertEqual(nucleolus(v), [1, 0, 0])
        self.assertEqual(nucleolus(v, imputations=False), [1, 0, 0])

    def test_majority_game(self):
        v = [0, 0, 0, 1, 0, 1, 1, 1]
        x, rounds = nucleolus_trace(v)
        self.assertEqual(x, [F(1, 3)] * 3)
        self.assertEqual(len(rounds), 1)
        self.assertEqual(rounds[0][0], F(1, 3))

    def test_half_pairs(self):
        v = [0, 0, 0, F(1, 2), 0, F(1, 2), F(1, 2), 1]
        x, rounds = nucleolus_trace(v)
        self.assertEqual(x, [F(1, 3)] * 3)
        self.assertEqual(rounds[0][0], F(-1, 6))

    def test_talmud_values(self):
        claims = [100, 200, 300]
        expected = {
            100: [F(100, 3)] * 3,
            200: [50, 75, 75],
            300: [50, 100, 150],
        }
        for E, want in expected.items():
            self.assertEqual(nucleolus(bankruptcy_game(claims, E)), want)

    def test_bankruptcy_trace(self):
        x, rounds = nucleolus_trace(bankruptcy_game([100, 200, 300], 200))
        self.assertEqual(x, [50, 75, 75])
        self.assertEqual([r[0] for r in rounds], [-50, -75])
        self.assertEqual(rounds[0][1], [1, 6])

    def test_small_n(self):
        self.assertEqual(nucleolus([0, 5]), [5])
        self.assertEqual(nucleolus([0, 5, 7, 20]), [9, 11])
        self.assertEqual(nucleolus([0, 5, 7, 20], imputations=False), [9, 11])

    def test_imputation_bound_binds(self):
        v = [0, 0, 0, 2, 0, 3, 4, 2]
        self.assertEqual(nucleolus(v), [0, F(1, 2), F(3, 2)])
        self.assertEqual(nucleolus(v, imputations=False), [F(-1, 3), F(2, 3), F(5, 3)])

    def test_no_imputation(self):
        with self.assertRaises(ValueError):
            nucleolus([0, 2, 2, 3])
        # The prenucleolus exists all the same.
        self.assertEqual(nucleolus([0, 2, 2, 3], imputations=False), [F(3, 2), F(3, 2)])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            nucleolus([0, 1, 2])
        with self.assertRaises(ValueError):
            nucleolus([1, 1, 1, 1])


class BruteForce(unittest.TestCase):
    def check_against_grid(self, v, n, D):
        x = nucleolus(v)
        full = (1 << n) - 1
        self.assertEqual(sum(x), v[full])
        self.assertTrue(all(x[i] >= v[1 << i] for i in range(n)))
        theta = excess_vector(v, x)
        best = min(excess_vector(v, y) for y in grid_imputations(v, n, D))
        on_grid = all(((xi - v[1 << i]) * D).denominator == 1 for i, xi in enumerate(x))
        if on_grid:
            self.assertEqual(theta, best)
        else:
            self.assertLess(theta, best)

    def test_three_players(self):
        rng = random.Random(7)
        for _ in range(25):
            self.check_against_grid(random_game(rng, 3, 6), 3, 12)

    def test_four_players(self):
        rng = random.Random(11)
        for _ in range(5):
            self.check_against_grid(random_game(rng, 4, 4), 4, 6)


class Properties(unittest.TestCase):
    def test_kohlberg(self):
        rng = random.Random(3)
        for n in (3, 4):
            for _ in range(4):
                v = random_game(rng, n, 5)
                x = nucleolus(v, imputations=False)
                self.assertEqual(sum(x), v[(1 << n) - 1])
                self.assertTrue(kohlberg(v, x))

    def test_core_games(self):
        rng = random.Random(5)
        for found in range(4):
            n = 3 + found % 2
            # A convex game: v(S) = (sum of weights in S)^2, so the core is nonempty.
            w = [rng.randint(0, 3) for _ in range(n)]
            v = [sum(w[i] for i in members(S, n)) ** 2 for S in range(1 << n)]
            x = nucleolus(v)
            self.assertTrue(in_core(v, x))
            self.assertEqual(x, nucleolus(v, imputations=False))

    def test_covariance(self):
        rng = random.Random(9)
        for _ in range(5):
            v = random_game(rng, 3, 6)
            a, b = F(3, 2), [F(1), F(-2), F(5, 7)]
            w = [a * v[S] + sum(b[i] for i in members(S, 3)) for S in range(8)]
            x, y = nucleolus(v), nucleolus(w)
            self.assertEqual(y, [a * x[i] + b[i] for i in range(3)])

    def test_symmetry(self):
        rng = random.Random(13)
        for _ in range(5):
            v = random_game(rng, 3, 6)
            perm = [2, 0, 1]  # player i becomes player perm[i]

            def image(S):
                return sum(1 << perm[i] for i in members(S, 3))

            w = [0] * 8
            for S in range(8):
                w[image(S)] = v[S]
            x, y = nucleolus(v), nucleolus(w)
            self.assertEqual([y[perm[i]] for i in range(3)], x)

    def test_round_count(self):
        rng = random.Random(17)
        for n in (3, 4):
            for _ in range(3):
                v = random_game(rng, n, 5)
                _, rounds = nucleolus_trace(v, imputations=False)
                self.assertLessEqual(len(rounds), n - 1)
                levels = [r[0] for r in rounds]
                self.assertEqual(levels, sorted(levels, reverse=True))


if __name__ == "__main__":
    unittest.main()
