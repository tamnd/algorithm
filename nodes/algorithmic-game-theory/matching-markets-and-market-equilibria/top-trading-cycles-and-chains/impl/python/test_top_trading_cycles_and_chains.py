# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-trading-cycles-and-chains/. The authors are listed in prov/4BQP88.jsonl.

import random
import unittest
from itertools import permutations, product

from top_trading_cycles_and_chains import W, top_trading_cycles_and_chains as ttcc


def all_lists(i, n):
    """Every list of patient i up to its own kidney: the entries after it never matter."""
    others = [h for h in range(n) if h != i] + [W]
    out = []
    for k in range(len(others) + 1):
        for s in permutations(others, k):
            out.append(list(s) + [i])
    return out


def random_list(rng, i, n):
    others = [h for h in range(n) if h != i] + [W]
    k = rng.randint(0, len(others))
    return rng.sample(others, k) + [i]


def rank(lst, h):
    """Position of h in the list; anything after the own kidney is worse than the own kidney."""
    return lst.index(h) if h in lst else len(lst)


def dominated(prefs, x):
    """Brute force: return an outcome that all patients weakly prefer and one strictly, or None.

    An outcome gives each patient a kidney or W; a kidney goes to at most one patient, and W
    can go to many. Only items up to the own kidney can be at least as good as x.
    """
    n = len(prefs)
    options = [lst[: lst.index(i) + 1] for i, lst in enumerate(prefs)]
    b = [rank(prefs[i], x[i]) for i in range(n)]
    for y in product(*options):
        ks = [h for h in y if h != W]
        if len(ks) != len(set(ks)):
            continue
        a = [rank(prefs[i], y[i]) for i in range(n)]
        if all(p <= q for p, q in zip(a, b)) and a != b:
            return y
    return None


def ttc_reference(prefs):
    """Plain top trading cycles by rounds, for lists in which W is never reached."""
    n = len(prefs)
    left = set(range(n))
    x = [None] * n
    while left:
        point = {i: next(h for h in prefs[i] if h in left) for i in left}
        gone = set()
        for s in left:
            seen = []
            i = s
            while i not in seen and i not in gone:
                seen.append(i)
                i = point[i]
            if i in seen:
                for k in seen[seen.index(i):]:
                    x[k] = point[k]
                    gone.add(k)
        left -= gone
    return x


class TestTopTradingCyclesAndChains(unittest.TestCase):
    def test_page_example(self):
        # pairs 1..5 of the page are 0..4 here
        prefs = [[1, 0], [0, 1], [0, W, 2], [2, 3], [2, 3, W, 4]]
        self.assertEqual(ttcc(prefs, keep=True), ([1, 0, W, 2, 3], [4]))
        self.assertEqual(ttcc(prefs, keep=False), ([1, 0, W, 3, W], [2, 4]))

    def test_rule_d_is_not_efficient(self):
        prefs = [[0], [W, 1], [1, 2]]
        x, wl = ttcc(prefs, keep=False)
        self.assertEqual((x, wl), ([0, W, 2], [1]))
        self.assertEqual(dominated(prefs, x), (0, W, 1))
        x, wl = ttcc(prefs, keep=True)
        self.assertEqual((x, wl), ([0, W, 1], [2]))
        self.assertIsNone(dominated(prefs, x))

    def test_edge_cases(self):
        self.assertEqual(ttcc([]), ([], []))
        self.assertEqual(ttcc([[0]]), ([0], []))
        self.assertEqual(ttcc([[W, 0]]), ([W], [0]))
        self.assertEqual(ttcc([[W, 0]], keep=False), ([W], [0]))
        with self.assertRaises(ValueError):
            ttcc([[1], [0]])
        with self.assertRaises(ValueError):
            ttcc([[0], [1]], priority=[0, 0])

    def test_without_w_it_is_ttc(self):
        rng = random.Random(3)
        for _ in range(100):
            n = rng.randint(1, 30)
            prefs = [rng.sample(range(n), n) for _ in range(n)]
            for keep in (True, False):
                self.assertEqual(ttcc(prefs, keep=keep), (ttc_reference(prefs), []))

    def test_outcome_structure(self):
        rng = random.Random(5)
        for _ in range(300):
            n = rng.randint(1, 12)
            prefs = [random_list(rng, i, n) for i in range(n)]
            pri = rng.sample(range(n), n)
            for keep in (True, False):
                x, wl = ttcc(prefs, pri, keep)
                given = [h for h in x if h != W]
                # each kidney goes to exactly one patient or to the waiting list
                self.assertEqual(sorted(given + wl), list(range(n)))
                self.assertEqual(x.count(W), len(wl))
                # individually rational
                for i in range(n):
                    self.assertLessEqual(rank(prefs[i], x[i]), rank(prefs[i], i))

    def test_rule_e_efficient(self):
        rng = random.Random(11)
        for _ in range(250):
            n = rng.randint(2, 4)
            prefs = [random_list(rng, i, n) for i in range(n)]
            pri = rng.sample(range(n), n)
            x, _ = ttcc(prefs, pri, keep=True)
            self.assertIsNone(dominated(prefs, x), (prefs, pri))

    def test_strategyproof_three_pairs(self):
        # every false list of the patient against a sample of true profiles, for rules d and e
        rng = random.Random(7)
        n = 3
        lists = [all_lists(i, n) for i in range(n)]
        for _ in range(60):
            prefs = [rng.choice(lists[i]) for i in range(n)]
            for keep in (True, False):
                x, _ = ttcc(prefs, keep=keep)
                for i in range(n):
                    for lie in lists[i]:
                        y, _ = ttcc(prefs[:i] + [lie] + prefs[i + 1:], keep=keep)
                        self.assertLessEqual(rank(prefs[i], x[i]), rank(prefs[i], y[i]))

    def test_strategyproof_random(self):
        rng = random.Random(8)
        for _ in range(120):
            n = 6
            prefs = [random_list(rng, i, n) for i in range(n)]
            pri = rng.sample(range(n), n)
            i = rng.randrange(n)
            for keep in (True, False):
                x, _ = ttcc(prefs, pri, keep)
                for _ in range(8):
                    lie = random_list(rng, i, n)
                    y, _ = ttcc(prefs[:i] + [lie] + prefs[i + 1:], pri, keep)
                    self.assertLessEqual(rank(prefs[i], x[i]), rank(prefs[i], y[i]))


if __name__ == "__main__":
    unittest.main()
