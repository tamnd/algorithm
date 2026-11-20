# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-trading-cycles/. The authors are listed in prov/YD7XQN.jsonl.

import random
import unittest
from itertools import combinations, permutations

from agtprefs import all_profiles, random_profile
from top_trading_cycles import top_trading_cycles


def ttc_by_rounds(prefs):
    """Reference: the textbook rounds. All agents point at once, all cycles leave."""
    n = len(prefs)
    left = set(range(n))
    x = [-1] * n
    while left:
        point = {i: next(h for h in prefs[i] if h in left) for i in left}
        gone = set()
        for s in left:
            seen = []
            i = s
            while i not in seen and i not in gone:
                seen.append(i)
                i = point[i]
            if i in seen:  # a new cycle
                for k in seen[seen.index(i):]:
                    x[k] = point[k]
                    gone.add(k)
        left -= gone
    return x


def rank(prefs, i, h):
    return prefs[i].index(h)


def weakly_blocked(prefs, x):
    """Return a coalition S and a trade y of the houses of S that weakly blocks x, or None."""
    n = len(prefs)
    for k in range(1, n + 1):
        for S in combinations(range(n), k):
            for y in permutations(S):
                a = [rank(prefs, i, h) for i, h in zip(S, y)]
                b = [rank(prefs, i, x[i]) for i in S]
                if all(p <= q for p, q in zip(a, b)) and a != b:
                    return S, y
    return None


def strict_core(prefs):
    n = len(prefs)
    return [list(x) for x in permutations(range(n)) if weakly_blocked(prefs, list(x)) is None]


class TestTopTradingCycles(unittest.TestCase):
    def test_page_example(self):
        # agents 1..5 of the page are 0..4 here
        prefs = [[2, 1, 0, 3, 4], [0, 2, 1, 3, 4], [1, 0, 2, 3, 4], [0, 4, 3, 1, 2], [3, 0, 1, 2, 4]]
        self.assertEqual(top_trading_cycles(prefs), [2, 0, 1, 4, 3])
        self.assertEqual(strict_core(prefs), [[2, 0, 1, 4, 3]])

    def test_weak_core_is_larger(self):
        # Roth-Postlewaite page: (h2, h3, h1) is not strongly blocked but is weakly blocked.
        prefs = [[1, 0, 2], [0, 2, 1], [0, 1, 2]]
        self.assertEqual(top_trading_cycles(prefs), [1, 0, 2])
        self.assertEqual(strict_core(prefs), [[1, 0, 2]])
        self.assertIsNotNone(weakly_blocked(prefs, [1, 2, 0]))

    def test_edge_cases(self):
        self.assertEqual(top_trading_cycles([]), [])
        self.assertEqual(top_trading_cycles([[0]]), [0])
        self.assertEqual(top_trading_cycles([[0, 1], [0, 1]]), [0, 1])
        self.assertEqual(top_trading_cycles([[1, 0], [0, 1]]), [1, 0])
        self.assertEqual(top_trading_cycles([[1, 0], [1]]), [0, 1])  # a list may stop at the own house
        with self.assertRaises(ValueError):
            top_trading_cycles([[1], [0]])

    def test_unique_strict_core_exhaustive(self):
        for profile in all_profiles(3, 3):
            prefs = [list(r) for r in profile]
            self.assertEqual(strict_core(prefs), [top_trading_cycles(prefs)])

    def test_unique_strict_core_random(self):
        rng = random.Random(4)
        for _ in range(60):
            prefs = [list(r) for r in random_profile(rng, 4, 4)]
            self.assertEqual(strict_core(prefs), [top_trading_cycles(prefs)])

    def test_strategyproof_exhaustive(self):
        lies = [list(r) for r in permutations(range(3))]
        for profile in all_profiles(3, 3):
            prefs = [list(r) for r in profile]
            x = top_trading_cycles(prefs)
            for i in range(3):
                for lie in lies:
                    y = top_trading_cycles(prefs[:i] + [lie] + prefs[i + 1:])
                    self.assertLessEqual(rank(prefs, i, x[i]), rank(prefs, i, y[i]))

    def test_strategyproof_random(self):
        rng = random.Random(9)
        for _ in range(150):
            n = 5
            prefs = [list(r) for r in random_profile(rng, n, n)]
            x = top_trading_cycles(prefs)
            i = rng.randrange(n)
            for _ in range(10):
                lie = rng.sample(range(n), n)
                y = top_trading_cycles(prefs[:i] + [lie] + prefs[i + 1:])
                self.assertLessEqual(rank(prefs, i, x[i]), rank(prefs, i, y[i]))

    def test_against_rounds_and_start_order(self):
        rng = random.Random(1)
        for _ in range(100):
            n = rng.randint(1, 40)
            prefs = [rng.sample(range(n), n) for _ in range(n)]
            x = top_trading_cycles(prefs)
            self.assertEqual(x, ttc_by_rounds(prefs))
            self.assertEqual(sorted(x), list(range(n)))
            order = rng.sample(range(n), n)
            self.assertEqual(top_trading_cycles(prefs, order), x)
            # cutting each list after the own house changes nothing
            cut = [lst[: lst.index(i) + 1] for i, lst in enumerate(prefs)]
            self.assertEqual(top_trading_cycles(cut), x)
            # individually rational
            self.assertTrue(all(rank(prefs, i, x[i]) <= rank(prefs, i, i) for i in range(n)))


if __name__ == "__main__":
    unittest.main()
