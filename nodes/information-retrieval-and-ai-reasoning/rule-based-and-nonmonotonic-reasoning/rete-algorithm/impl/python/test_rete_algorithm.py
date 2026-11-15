# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rete-algorithm/. The authors are listed in prov/.

import random
import unittest
from itertools import product

from rete_algorithm import Rete, canonical, match

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

    rules = []
    first = [condition() for _ in range(2)]
    for r in range(rng.randint(1, 5)):
        conds = [rng.choice(first)] if rng.random() < 0.5 else []  # shared prefixes
        conds += [condition() for _ in range(rng.randint(1, 3))]
        rules.append(("r" + str(r), conds))
    return rules


class TestRete(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(canonical(("q", "?y", "?y")), ("q", "?0", "?0"))
        self.assertEqual(canonical(("q", "?x", "b")), canonical(("q", "?z", "b")))

    def test_page_example(self):
        rules = [
            ("R1", [("goal", "?g"), ("block", "?b", "red"), ("on", "?b", "?t")]),
            ("R2", [("goal", "?g"), ("block", "?b", "red"), ("clear", "?b")]),
        ]
        net = Rete(rules)
        self.assertEqual(len(net.alpha), 4)
        self.assertEqual(len(net.joins), 4)
        for w in [("goal", "g1"), ("block", "b1", "red"), ("block", "b2", "red"), ("block", "b3", "blue"), ("on", "b1", "table"), ("clear", "b2")]:
            net.insert(w)
        self.assertEqual(
            net.conflict_set(),
            {
                ("R1", (("goal", "g1"), ("block", "b1", "red"), ("on", "b1", "table"))),
                ("R2", (("goal", "g1"), ("block", "b2", "red"), ("clear", "b2"))),
            },
        )
        self.assertEqual(net.token_count(), 5)
        net.delete(("block", "b1", "red"))
        self.assertEqual(net.conflict_set(), {("R2", (("goal", "g1"), ("block", "b2", "red"), ("clear", "b2")))})
        self.assertEqual(net.token_count(), 3)

    def test_same_wme_in_two_conditions(self):
        rules = [("loop", [("q", "?x", "?y"), ("q", "?y", "?x")])]
        net = Rete(rules)
        net.insert(("q", "a", "a"))
        self.assertEqual(net.conflict_set(), {("loop", (("q", "a", "a"), ("q", "a", "a")))})
        self.assertEqual(net.duplicates, 0)
        net.delete(("q", "a", "a"))
        self.assertEqual(net.conflict_set(), set())
        self.assertEqual(net.token_count(), 0)

    def test_random_against_naive(self):
        rng = random.Random(20261115)
        for _ in range(150):
            rules = random_rules(rng)
            net = Rete(rules)
            memory = set()
            for _ in range(40):
                w = rng.choice(ALL_WMES)
                if w in memory and rng.random() < 0.5:
                    memory.discard(w)
                    net.delete(w)
                else:
                    memory.add(w)
                    net.insert(w)
                self.assertEqual(net.memory, memory)
                self.assertEqual(net.conflict_set(), naive_conflict_set(rules, memory))
                self.assertEqual(net.duplicates, 0)
            for w in list(memory):
                net.delete(w)
            self.assertEqual(net.conflict_set(), set())
            self.assertEqual(net.token_count(), 0)
            self.assertTrue(all(not am.items for am in net.alpha.values()))


if __name__ == "__main__":
    unittest.main()
