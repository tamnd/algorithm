# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treat-algorithm/. The authors are listed in prov/.

import random
import unittest
from itertools import product

from treat_algorithm import Treat, match

CONSTS = ["a", "b", "c"]
PREDS = [("p", 1), ("q", 2), ("r", 2)]
VARS = ["?x", "?y", "?z"]
ALL_WMES = [(name,) + args for name, arity in PREDS for args in product(CONSTS, repeat=arity)]


def naive_conflict_set(rules, memory):
    """Rematch every rule against the whole working memory."""
    out = set()
    for name, conditions in rules:
        def go(k, b, chosen):
            if k == len(conditions):
                out.add((name, tuple(chosen)))
                return
            for w in memory:
                b2 = match(conditions[k], w, b)
                if b2 is not None:
                    go(k + 1, b2, chosen + [w])
        go(0, {}, [])
    return out


def random_rules(rng):
    def condition():
        name, arity = rng.choice(PREDS)
        return (name,) + tuple(rng.choice(VARS + VARS + CONSTS) for _ in range(arity))

    return [("r" + str(r), [condition() for _ in range(rng.randint(1, 4))]) for r in range(rng.randint(1, 5))]


class TestTreat(unittest.TestCase):
    def test_page_example(self):
        rules = [
            ("R1", [("goal", "?g"), ("block", "?b", "red"), ("on", "?b", "?t")]),
            ("R2", [("goal", "?g"), ("block", "?b", "red"), ("clear", "?b")]),
        ]
        m = Treat(rules)
        self.assertEqual(len(m.alpha), 4)
        for w in [("goal", "g1"), ("block", "b1", "red"), ("block", "b2", "red"), ("block", "b3", "blue"), ("on", "b1", "table"), ("clear", "b2")]:
            m.insert(w)
        r2 = ("R2", (("goal", "g1"), ("block", "b2", "red"), ("clear", "b2")))
        self.assertEqual(m.conflict_set(), {("R1", (("goal", "g1"), ("block", "b1", "red"), ("on", "b1", "table"))), r2})
        before = m.partial_matches
        m.delete(("block", "b1", "red"))
        self.assertEqual(m.conflict_set(), {r2})
        self.assertEqual(m.partial_matches, before)  # a delete does no join

    def test_same_wme_in_two_conditions(self):
        m = Treat([("loop", [("q", "?x", "?y"), ("q", "?y", "?x")])])
        m.insert(("q", "a", "a"))
        self.assertEqual(m.conflict_set(), {("loop", (("q", "a", "a"), ("q", "a", "a")))})
        m.insert(("q", "a", "b"))
        m.insert(("q", "b", "a"))
        self.assertEqual(len(m.conflict_set()), 3)
        self.assertEqual(m.duplicates, 0)

    def test_random_against_naive(self):
        rng = random.Random(20261115)
        for _ in range(150):
            rules = random_rules(rng)
            m = Treat(rules)
            memory = set()
            for _ in range(40):
                w = rng.choice(ALL_WMES)
                if w in memory and rng.random() < 0.5:
                    memory.discard(w)
                    m.delete(w)
                else:
                    memory.add(w)
                    m.insert(w)
                self.assertEqual(m.conflict_set(), naive_conflict_set(rules, memory))
                self.assertEqual(m.duplicates, 0)
                for key, items in m.alpha.items():
                    self.assertEqual(items, {w for w in memory if match(key, w, {}) is not None})


if __name__ == "__main__":
    unittest.main()
