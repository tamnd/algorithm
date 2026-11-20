# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-serial/. The authors are listed in prov/VY2D6A.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import permutations

from agtlp import lp_max
from agtprefs import all_profiles, random_profile
from probabilistic_serial import probabilistic_serial

F = Fraction


def cumulative(lst, row):
    """Partial sums of row along the list lst: the chance of one of the k best objects."""
    out, s = [], Fraction(0)
    for o in lst:
        s += row[o]
        out.append(s)
    return out


def sd_weakly_better(lst, p, q):
    return all(x >= y for x, y in zip(cumulative(lst, p), cumulative(lst, q)))


def ordinally_efficient(prefs, P, m):
    """True if no sub-bistochastic Q on the acceptable pairs stochastically dominates P.

    LP: maximize the sum over agents i and k of the chance under Q of the k best objects
    of i, subject to row and column sums at most 1 and each such chance at least the one
    under P. P is feasible, and P is dominated exactly when the optimum is larger than the
    value of P.
    """
    n = len(prefs)
    pairs = [(i, o) for i in range(n) for o in prefs[i]]
    col = {p: k for k, p in enumerate(pairs)}
    c = [0] * len(pairs)
    A, b = [], []
    for i in range(n):
        lst = prefs[i]
        for pos, o in enumerate(lst):
            c[col[(i, o)]] += len(lst) - pos  # o counts in the top-k sets for k > pos
        cum = cumulative(lst, P[i])
        for k in range(len(lst)):
            row = [0] * len(pairs)
            for o in lst[: k + 1]:
                row[col[(i, o)]] = -1
            A.append(row)
            b.append(-cum[k])
        A.append([1 if p[0] == i else 0 for p in pairs])
        b.append(1)
    for o in range(m):
        A.append([1 if p[1] == o else 0 for p in pairs])
        b.append(1)
    status, x, value, dual = lp_max(c, A, b)
    assert status == "optimal"
    own = sum(sum(cumulative(prefs[i], P[i])) for i in range(n))
    return value == own


def ordered_subsets(m):
    return [list(s) for k in range(m + 1) for s in permutations(range(m), k)]


BM = [[0, 1, 2, 3], [0, 1, 2, 3], [1, 0, 3, 2], [1, 0, 3, 2]]  # a > b > c > d and b > a > d > c
RSD_BM = [[F(5, 12), F(1, 12), F(5, 12), F(1, 12)]] * 2 + [[F(1, 12), F(5, 12), F(1, 12), F(5, 12)]] * 2


class TestProbabilisticSerial(unittest.TestCase):
    def test_page_examples(self):
        half = F(1, 2)
        self.assertEqual(
            probabilistic_serial(BM),
            [[half, 0, half, 0], [half, 0, half, 0], [0, half, 0, half], [0, half, 0, half]],
        )
        P = probabilistic_serial([[0, 1, 2], [0, 2, 1], [1, 0, 2]])
        self.assertEqual(P, [[F(1, 2), F(1, 4), F(1, 4)], [F(1, 2), 0, F(1, 2)], [0, F(3, 4), F(1, 4)]])
        # the RSD matrix of the Bogomolnaia-Moulin example is not ordinally efficient
        self.assertTrue(ordinally_efficient(BM, probabilistic_serial(BM), 4))
        self.assertFalse(ordinally_efficient(BM, RSD_BM, 4))

    def test_manipulation_example(self):
        prefs = [[0, 1, 2], [0, 1, 2], [1, 2, 0]]
        truth = probabilistic_serial(prefs)[0]
        lie = probabilistic_serial([[1, 0, 2]] + prefs[1:])[0]
        self.assertEqual(truth, [F(1, 2), F(1, 6), F(1, 3)])
        self.assertEqual(lie, [F(1, 4), F(1, 2), F(1, 4)])
        u = [F(3), F(29, 10), F(0)]  # a utility that agrees with a > b > c
        self.assertGreater(sum(x * y for x, y in zip(u, lie)), sum(x * y for x, y in zip(u, truth)))
        self.assertFalse(sd_weakly_better(prefs[0], truth, lie))
        self.assertFalse(sd_weakly_better(prefs[0], lie, truth))

    def test_edge_cases(self):
        self.assertEqual(probabilistic_serial([]), [])
        self.assertEqual(probabilistic_serial([[]], m=2), [[0, 0]])
        self.assertEqual(probabilistic_serial([[1, 0]]), [[0, 1]])
        self.assertEqual(probabilistic_serial([[0], [0], [0]]), [[F(1, 3)]] * 3)
        # more objects than agents: eating stops at time 1
        self.assertEqual(probabilistic_serial([[0, 1], [0, 1]], m=3), [[F(1, 2), F(1, 2), 0]] * 2)
        with self.assertRaises(ValueError):
            probabilistic_serial([[0, 0]])

    def test_properties_random(self):
        rng = random.Random(3)
        for trial in range(60):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            if trial % 2:
                prefs = [rng.sample(range(m), rng.randint(0, m)) for _ in range(n)]
            else:
                m = n
                prefs = [list(r) for r in random_profile(rng, n, n)]
            P = probabilistic_serial(prefs, m)
            for i in range(n):
                self.assertTrue(all(P[i][o] == 0 for o in range(m) if o not in prefs[i]))
                self.assertLessEqual(sum(P[i]), 1)
                for j in range(n):  # envy-free in the sense of stochastic dominance
                    self.assertTrue(sd_weakly_better(prefs[i], P[i], P[j]))
            for o in range(m):
                self.assertLessEqual(sum(P[i][o] for i in range(n)), 1)
            if all(len(lst) == m for lst in prefs) and n == m:
                self.assertTrue(all(sum(row) == 1 for row in P))
                self.assertTrue(all(sum(P[i][o] for i in range(n)) == 1 for o in range(m)))
            self.assertTrue(ordinally_efficient(prefs, P, m))

    def test_weakly_strategyproof_exhaustive(self):
        # Bogomolnaia and Moulin: no report gives a row that stochastically dominates the
        # true row. Full strategyproofness fails, as the manipulation example shows.
        reports = ordered_subsets(3)
        gains = 0
        for profile in all_profiles(3, 3):
            prefs = [list(r) for r in profile]
            P = probabilistic_serial(prefs, 3)
            for i in range(3):
                for lie in reports:
                    Q = probabilistic_serial(prefs[:i] + [lie] + prefs[i + 1:], 3)
                    if sd_weakly_better(prefs[i], Q[i], P[i]):
                        self.assertEqual(cumulative(prefs[i], Q[i]), cumulative(prefs[i], P[i]))
                    if not sd_weakly_better(prefs[i], P[i], Q[i]):
                        gains += 1
        self.assertGreater(gains, 0)


if __name__ == "__main__":
    unittest.main()
