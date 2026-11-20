# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serial-dictatorship/. The authors are listed in prov/RKCZD9.jsonl.

import random
import unittest
from itertools import permutations

from agtprefs import all_rankings, all_profiles, random_profile
from serial_dictatorship import serial_dictatorship


def rank_of(lst, o):
    """Position of object o in the list, len(lst) for -1 (no object), None if unacceptable."""
    if o == -1:
        return len(lst)
    return lst.index(o) if o in lst else None


def all_matchings(prefs, m):
    """Every matching: each agent gets an acceptable object or -1, no object twice."""
    n = len(prefs)
    out = []

    def rec(i, used, cur):
        if i == n:
            out.append(tuple(cur))
            return
        cur.append(-1)
        rec(i + 1, used, cur)
        cur.pop()
        for o in prefs[i]:
            if o not in used:
                used.add(o)
                cur.append(o)
                rec(i + 1, used, cur)
                cur.pop()
                used.discard(o)

    rec(0, set(), [])
    return out


def dominates(prefs, a, b):
    """True if matching a is at least as good as b for all agents and better for one."""
    better = False
    for i, lst in enumerate(prefs):
        ra, rb = rank_of(lst, a[i]), rank_of(lst, b[i])
        if ra > rb:
            return False
        if ra < rb:
            better = True
    return better


def pareto_optimal_set(prefs, m):
    ms = all_matchings(prefs, m)
    return {a for a in ms if not any(dominates(prefs, b, a) for b in ms)}


def random_lists(rng, n, m):
    """Random incomplete strict lists: each agent ranks a random subset of the objects."""
    return [rng.sample(range(m), rng.randint(0, m)) for _ in range(n)]


BM = [[0, 1, 2, 3], [0, 1, 2, 3], [1, 0, 3, 2], [1, 0, 3, 2]]  # a > b > c > d and b > a > d > c


class TestSerialDictatorship(unittest.TestCase):
    def test_page_example(self):
        self.assertEqual(serial_dictatorship(BM), [0, 1, 3, 2])
        self.assertEqual(serial_dictatorship(BM, [0, 2, 1, 3]), [0, 2, 1, 3])
        self.assertEqual(serial_dictatorship(BM, [2, 3, 0, 1]), [2, 3, 1, 0])
        outcomes = {tuple(serial_dictatorship(BM, o)) for o in permutations(range(4))}
        self.assertEqual(len(outcomes), 12)
        self.assertEqual(outcomes, pareto_optimal_set(BM, 4))

    def test_edge_cases(self):
        self.assertEqual(serial_dictatorship([]), [])
        self.assertEqual(serial_dictatorship([[], [0]]), [-1, 0])
        self.assertEqual(serial_dictatorship([[0], [0], [0]], [2, 0, 1]), [-1, -1, 0])
        self.assertEqual(serial_dictatorship([[1, 0], [1]], m=3), [1, -1])
        self.assertEqual(serial_dictatorship([[1, 0], [1]], [1, 0], m=3), [0, 1])
        with self.assertRaises(ValueError):
            serial_dictatorship([[0, 0]])
        with self.assertRaises(ValueError):
            serial_dictatorship([[0], [1]], [0, 0])

    def test_pareto_optimal_and_every_po_matching_is_reached(self):
        rng = random.Random(11)
        for _ in range(300):
            n, m = rng.randint(1, 4), rng.randint(1, 4)
            prefs = random_lists(rng, n, m)
            po = pareto_optimal_set(prefs, m)
            reached = {tuple(serial_dictatorship(prefs, o, m)) for o in permutations(range(n))}
            self.assertEqual(reached, po)

    def test_strategyproof_exhaustive_three_agents(self):
        for P in all_profiles(3, 3):
            prefs = [list(r) for r in P]
            for order in ([0, 1, 2], [2, 0, 1]):
                truth = serial_dictatorship(prefs, order)
                for i in range(3):
                    for lie in all_rankings(3):
                        q = prefs[:i] + [list(lie)] + prefs[i + 1:]
                        got = serial_dictatorship(q, order)[i]
                        self.assertGreaterEqual(rank_of(prefs[i], got), rank_of(prefs[i], truth[i]))

    def test_strategyproof_random_four_agents_with_truncation(self):
        rng = random.Random(5)
        lies = [list(r[:k]) for r in all_rankings(4) for k in range(5)]
        for _ in range(200):
            prefs = [list(r) for r in random_profile(rng, 4, 4)]
            order = rng.sample(range(4), 4)
            truth = serial_dictatorship(prefs, order)
            i = rng.randrange(4)
            for lie in lies:
                q = prefs[:i] + [lie] + prefs[i + 1:]
                got = serial_dictatorship(q, order, 4)[i]
                self.assertGreaterEqual(rank_of(prefs[i], got), rank_of(prefs[i], truth[i]))

    def test_first_agent_gets_top_and_reads_bound(self):
        rng = random.Random(8)
        for _ in range(200):
            n, m = rng.randint(1, 6), rng.randint(1, 6)
            prefs = random_lists(rng, n, m)
            order = rng.sample(range(n), n)
            match = serial_dictatorship(prefs, order, m)
            taken = set()
            for i in order:
                free = [o for o in prefs[i] if o not in taken]
                self.assertEqual(match[i], free[0] if free else -1)
                if free:
                    taken.add(free[0])


if __name__ == "__main__":
    unittest.main()
