# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boston-mechanism/. The authors are listed in prov/GWGCR1.jsonl.

import random
import unittest
from itertools import permutations, product

from agtprefs import all_rankings, random_profile
from boston_mechanism import boston, first_choice_count

# The example of the page, with students and schools indexed from 0.
PREFS = [(1, 0, 2), (2, 1, 0), (2, 1, 0)]
PRIORITY = [(0, 2, 1), (2, 1, 0), (0, 1, 2)]
CAPACITY = [1, 1, 1]


def deferred_acceptance(prefs, priority, capacity):
    """Student-proposing deferred acceptance, the reference method."""
    n, m = len(prefs), len(capacity)
    rank = [{i: r for r, i in enumerate(priority[s])} for s in range(m)]
    nxt = [0] * n
    held = [[] for _ in range(m)]
    free = list(range(n))
    while free:
        i = free.pop()
        if nxt[i] >= len(prefs[i]):
            continue
        s = prefs[i][nxt[i]]
        nxt[i] += 1
        held[s].append(i)
        held[s].sort(key=lambda x: rank[s][x])
        if len(held[s]) > capacity[s]:
            free.append(held[s].pop())
    out = [None] * n
    for s in range(m):
        for i in held[s]:
            out[i] = s
    return out


def adjusted_priority(prefs, priority, m):
    """Rank students at school s first by the place of s on their list, then by priority."""
    n = len(prefs)
    out = []
    for s in range(m):
        def key(i, s=s):
            place = prefs[i].index(s) if s in prefs[i] else m
            return (place, priority[s].index(i))
        out.append(tuple(sorted(range(n), key=key)))
    return out


def all_assignments(prefs, capacity):
    """Every feasible assignment: each student gets a school on her list or None."""
    options = [list(lst) + [None] for lst in prefs]
    for a in product(*options):
        if all(sum(1 for x in a if x == s) <= capacity[s] for s in range(len(capacity))):
            yield list(a)


def place(prefs, i, s):
    return prefs[i].index(s) if s is not None else len(prefs[i])


def is_stable(prefs, priority, capacity, a):
    n = len(prefs)
    for i in range(n):
        for s in prefs[i][: place(prefs, i, a[i])]:
            holders = [j for j in range(n) if a[j] == s]
            if len(holders) < capacity[s]:
                return False
            if any(priority[s].index(i) < priority[s].index(j) for j in holders):
                return False
    return True


def random_instance(rng, n, m):
    prefs = [tuple(r[: rng.randint(1, m)]) for r in random_profile(rng, m, n)]
    priority = list(random_profile(rng, n, m))
    capacity = [rng.randint(0, 2) for _ in range(m)]
    return prefs, priority, capacity


class TestBoston(unittest.TestCase):
    def test_page_example(self):
        trace = []
        self.assertEqual(boston(PREFS, PRIORITY, CAPACITY, trace), [1, 2, 0])
        self.assertEqual(trace, [{1: [0], 2: [1]}, {}, {0: [2]}])
        self.assertEqual(deferred_acceptance(PREFS, PRIORITY, CAPACITY), [0, 2, 1])

    def test_manipulation_on_page(self):
        lie = [PREFS[0], PREFS[1], (1, 2, 0)]
        a = boston(lie, PRIORITY, CAPACITY)
        self.assertEqual(a, [0, 2, 1])
        self.assertLess(place(PREFS, 2, a[2]), place(PREFS, 2, 0))

    def test_justified_envy_on_page(self):
        self.assertFalse(is_stable(PREFS, PRIORITY, CAPACITY, boston(PREFS, PRIORITY, CAPACITY)))

    def test_feasible(self):
        rng = random.Random(1)
        for _ in range(300):
            prefs, priority, capacity = random_instance(rng, rng.randint(1, 6), rng.randint(1, 4))
            a = boston(prefs, priority, capacity)
            for i, s in enumerate(a):
                self.assertTrue(s is None or s in prefs[i])
            for s in range(len(capacity)):
                self.assertLessEqual(sum(1 for x in a if x == s), capacity[s])

    def test_equals_da_with_adjusted_priorities(self):
        rng = random.Random(2)
        for _ in range(400):
            n, m = rng.randint(1, 7), rng.randint(1, 4)
            prefs, priority, capacity = random_instance(rng, n, m)
            adj = adjusted_priority(prefs, priority, m)
            self.assertEqual(boston(prefs, priority, capacity), deferred_acceptance(prefs, adj, capacity))

    def test_pareto_efficient_and_most_first_choices(self):
        rng = random.Random(3)
        for _ in range(150):
            n, m = rng.randint(1, 4), rng.randint(1, 3)
            prefs, priority, capacity = random_instance(rng, n, m)
            a = boston(prefs, priority, capacity)
            best_first = 0
            for b in all_assignments(prefs, capacity):
                best_first = max(best_first, first_choice_count(prefs, b))
                weakly = all(place(prefs, i, b[i]) <= place(prefs, i, a[i]) for i in range(n))
                strictly = any(place(prefs, i, b[i]) < place(prefs, i, a[i]) for i in range(n))
                self.assertFalse(weakly and strictly)
            self.assertEqual(first_choice_count(prefs, a), best_first)

    def test_not_strategyproof_search(self):
        rng = random.Random(4)
        found = 0
        for _ in range(200):
            prefs = list(random_profile(rng, 3, 3))
            priority = list(random_profile(rng, 3, 3))
            a = boston(prefs, priority, [1, 1, 1])
            for i in range(3):
                for lie in all_rankings(3):
                    b = boston(prefs[:i] + [lie] + prefs[i + 1:], priority, [1, 1, 1])
                    if place(prefs, i, b[i]) < place(prefs, i, a[i]):
                        found += 1
        self.assertGreater(found, 0)

    def test_nash_outcomes_are_the_stable_matchings(self):
        # Ergin and Sonmez 2006: with complete information, the outcomes of the Nash
        # equilibria of the Boston game are the stable matchings under the true preferences.
        rng = random.Random(6)
        strategies = all_rankings(3)
        cap = [1, 1, 1]
        for _ in range(8):
            prefs = list(random_profile(rng, 3, 3))
            priority = list(random_profile(rng, 3, 3))
            stable = {tuple(p) for p in permutations(range(3)) if is_stable(prefs, priority, cap, list(p))}
            result = {prof: boston(list(prof), priority, cap) for prof in product(strategies, repeat=3)}
            nash = set()
            for prof, a in result.items():
                if all(
                    place(prefs, i, result[prof[:i] + (d,) + prof[i + 1:]][i]) >= place(prefs, i, a[i])
                    for i in range(3)
                    for d in strategies
                ):
                    nash.add(tuple(a))
            self.assertEqual(nash, stable)
            self.assertIn(tuple(deferred_acceptance(prefs, priority, cap)), nash)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            boston([(0, 0)], [(0,)], [1])
        with self.assertRaises(ValueError):
            boston([(0,)], [(0, 0)], [1])
        with self.assertRaises(ValueError):
            boston([(1,)], [(0,)], [1])


if __name__ == "__main__":
    unittest.main()
