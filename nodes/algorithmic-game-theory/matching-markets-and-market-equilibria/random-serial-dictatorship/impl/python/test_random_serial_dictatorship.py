# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-serial-dictatorship/. The authors are listed in prov/K05SWB.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import permutations

from agtprefs import all_profiles, random_profile
from random_serial_dictatorship import random_serial_dictatorship, rsd_lottery, rsd_probabilities


def rank_of(lst, o):
    """Position of object o in the list; len(lst) for -1 (no object)."""
    return len(lst) if o == -1 else lst.index(o)


def all_matchings(prefs):
    """Every matching: each agent gets an acceptable object or -1, no object twice."""
    out = []

    def rec(i, used, cur):
        if i == len(prefs):
            out.append(tuple(cur))
            return
        for o in [-1] + [o for o in prefs[i] if o not in used]:
            rec(i + 1, used | ({o} if o >= 0 else set()), cur + [o])

    rec(0, frozenset(), [])
    return out


def dominates(prefs, a, b):
    """True if matching a is at least as good as b for all agents and better for one."""
    ra = [rank_of(lst, a[i]) for i, lst in enumerate(prefs)]
    rb = [rank_of(lst, b[i]) for i, lst in enumerate(prefs)]
    return all(x <= y for x, y in zip(ra, rb)) and ra != rb


def pareto_optimal_set(prefs):
    ms = all_matchings(prefs)
    return {a for a in ms if not any(dominates(prefs, b, a) for b in ms)}


def sd_weakly_better(true_list, p, q):
    """True if row p gives at least as much probability as row q to each top set of the true list."""
    sp = sq = Fraction(0)
    for o in true_list:
        sp += p[o]
        sq += q[o]
        if sp < sq:
            return False
    return True


def ttc(prefs, endowment):
    """Top trading cycles with complete lists; agent i owns object endowment[i]."""
    owner = {o: i for i, o in enumerate(endowment)}
    left = set(range(len(prefs)))
    match = [-1] * len(prefs)
    while left:
        point = {i: owner[next(o for o in prefs[i] if owner[o] in left)] for i in left}
        i = next(iter(left))
        seen = []
        while i not in seen:
            seen.append(i)
            i = point[i]
        cycle = seen[seen.index(i):]
        for j in cycle:
            match[j] = endowment[point[j]]
        left -= set(cycle)
    return tuple(match)


def ordered_subsets(m):
    """Every strict list over a subset of 0, ..., m - 1: all possible reports."""
    out = []
    for k in range(m + 1):
        for s in permutations(range(m), k):
            out.append(list(s))
    return out


BM = [[0, 1, 2, 3], [0, 1, 2, 3], [1, 0, 3, 2], [1, 0, 3, 2]]  # a > b > c > d and b > a > d > c


class TestRandomSerialDictatorship(unittest.TestCase):
    def test_page_example(self):
        F = Fraction
        P = rsd_probabilities(BM)
        self.assertEqual(P[0], [F(5, 12), F(1, 12), F(5, 12), F(1, 12)])
        self.assertEqual(P[1], P[0])
        self.assertEqual(P[2], [F(1, 12), F(5, 12), F(1, 12), F(5, 12)])
        self.assertEqual(P[3], P[2])
        lottery = rsd_lottery(BM)
        self.assertEqual(len(lottery), 12)
        self.assertEqual(lottery[(0, 2, 1, 3)], F(1, 6))
        self.assertEqual(lottery[(0, 1, 2, 3)], F(1, 24))
        # Probabilistic serial gives a, c half and half to agents 1 and 2, and b, d to 3 and 4.
        # Its rows dominate the RSD rows for every agent, strictly for all, so RSD is not
        # ordinally efficient here.
        half = F(1, 2)
        Q = [[half, 0, half, 0], [half, 0, half, 0], [0, half, 0, half], [0, half, 0, half]]
        for i in range(4):
            self.assertTrue(sd_weakly_better(BM[i], Q[i], P[i]))
            self.assertNotEqual(Q[i], P[i])

    def test_edge_cases(self):
        rng = random.Random(1)
        self.assertEqual(random_serial_dictatorship([], rng), [])
        self.assertEqual(rsd_probabilities([[0]]), [[Fraction(1)]])
        self.assertEqual(rsd_probabilities([[], [0]]), [[Fraction(0)], [Fraction(1)]])
        three = rsd_probabilities([[0], [0], [0]])
        self.assertEqual([row[0] for row in three], [Fraction(1, 3)] * 3)
        with self.assertRaises(ValueError):
            rsd_probabilities([[0, 0]])
        with self.assertRaises(ValueError):
            random_serial_dictatorship([[2]], rng, m=2)

    def test_ex_post_efficient(self):
        rng = random.Random(7)
        for _ in range(150):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            prefs = [rng.sample(range(m), rng.randint(0, m)) for _ in range(n)]
            lottery = rsd_lottery(prefs, m)
            self.assertEqual(sum(lottery.values()), 1)
            # every order gives a Pareto optimal matching, and every Pareto optimal
            # matching has positive probability
            self.assertEqual(set(lottery), pareto_optimal_set(prefs))

    def test_equal_treatment_and_bistochastic(self):
        rng = random.Random(11)
        for _ in range(100):
            n = rng.randint(2, 5)
            kinds = [rng.sample(range(n), n) for _ in range(2)]
            prefs = [kinds[rng.randint(0, 1)] for _ in range(n)]
            P = rsd_probabilities(prefs, n)
            for i in range(n):
                self.assertEqual(sum(P[i]), 1)
                for j in range(n):
                    if prefs[i] == prefs[j]:
                        self.assertEqual(P[i], P[j])
            for o in range(n):
                self.assertEqual(sum(P[i][o] for i in range(n)), 1)

    def test_strategyproof_exhaustive(self):
        reports = ordered_subsets(3)
        for profile in all_profiles(3, 3):
            prefs = [list(r) for r in profile]
            P = rsd_probabilities(prefs, 3)
            for i in range(3):
                for lie in reports:
                    Q = rsd_probabilities(prefs[:i] + [lie] + prefs[i + 1:], 3)
                    self.assertTrue(sd_weakly_better(prefs[i], P[i], Q[i]), (prefs, i, lie))

    def test_core_from_random_endowments(self):
        # Abdulkadiroglu and Sonmez (1998): TTC from a uniform random endowment gives the
        # same lottery over matchings as random serial dictatorship.
        rng = random.Random(5)
        for n in (2, 3, 4):
            for _ in range(15):
                prefs = [list(r) for r in random_profile(rng, n, n)]
                core = {}
                for e in permutations(range(n)):
                    mu = ttc(prefs, e)
                    core[mu] = core.get(mu, 0) + Fraction(1, len(list(permutations(range(n)))))
                self.assertEqual(core, rsd_lottery(prefs, n))

    def test_sampler(self):
        rng = random.Random(2024)
        draws = 12000
        count = [[0] * 4 for _ in range(4)]
        po = pareto_optimal_set(BM)
        for _ in range(draws):
            mu = random_serial_dictatorship(BM, rng)
            self.assertIn(tuple(mu), po)
            for i, o in enumerate(mu):
                count[i][o] += 1
        P = rsd_probabilities(BM)
        for i in range(4):
            for o in range(4):
                self.assertLess(abs(count[i][o] / draws - float(P[i][o])), 0.02)


if __name__ == "__main__":
    unittest.main()
