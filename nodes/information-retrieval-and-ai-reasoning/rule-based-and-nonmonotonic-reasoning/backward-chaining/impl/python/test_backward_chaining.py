# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-chaining/. The authors are listed in prov/.

import random
import unittest
from itertools import combinations

from backward_chaining import BackwardChainer, backward_chain


def least_model_brute(rules):
    """The smallest set of atoms that is closed under every rule, by brute force over all subsets."""
    base = sorted({h for h, _ in rules} | {b for _, body in rules for b in body})
    assert len(base) <= 12
    for k in range(len(base) + 1):
        for subset in combinations(base, k):
            s = set(subset)
            if all(h in s for h, body in rules if all(b in s for b in body)):
                return s
    raise AssertionError("the full base is always closed")


def random_rules(rng, n_atoms, n_rules):
    rules = []
    for _ in range(n_rules):
        head = rng.randrange(n_atoms)
        body = tuple(rng.choice(range(n_atoms)) for _ in range(rng.choice([0, 1, 1, 2, 2, 3])))
        rules.append((head, body))
    return rules


def complete_graph(n):
    """a_i <- a_j for every i != j, and no facts: nothing is provable."""
    return [(i, (j,)) for i in range(n) for j in range(n) if i != j]


class TestBackwardChaining(unittest.TestCase):
    def test_page_example(self):
        rules = [("g", ("d",)), ("d", ("d",)), ("g", ("a", "b")), ("a", ("g",)), ("a", ("c",)), ("b", ("a",)), ("c", ())]
        bc = BackwardChainer(rules)
        self.assertTrue(bc.prove("g"))
        self.assertEqual(
            bc.trace,
            [
                ("loop", "d"),
                ("failed", "d"),
                ("loop", "g"),
                ("proved", "c"),
                ("proved", "a"),
                ("memo true", "a"),
                ("proved", "b"),
                ("proved", "g"),
            ],
        )
        self.assertEqual(bc.failed, {"d"})
        self.assertFalse(bc.prove("d"))

    def test_conditional_failure_is_not_stored(self):
        # From the goal g, q fails because its only route goes back to g, which is on the stack.
        # Later q is asked again from the top and must succeed through g.
        rules = [("g", ("q",)), ("g", ("s",)), ("q", ("g",)), ("s", ())]
        bc = BackwardChainer(rules)
        self.assertTrue(bc.prove("g"))
        self.assertNotIn("q", bc.failed)
        self.assertTrue(bc.prove("q"))

    def test_random_against_least_model(self):
        rng = random.Random(20261115)
        for _ in range(600):
            n = rng.randint(1, 9)
            rules = random_rules(rng, n, rng.randint(0, 14))
            m = least_model_brute(rules)
            shared = BackwardChainer(rules)
            for a in range(n):
                self.assertEqual(backward_chain(rules, a), a in m)
                self.assertEqual(shared.prove(a), a in m)
                self.assertTrue(shared.proved <= m)
                self.assertFalse(shared.failed & m)
                self.assertEqual(shared.depth, {})

    def test_complete_graph_is_exponential(self):
        counts = []
        for n in range(2, 8):
            bc = BackwardChainer(complete_graph(n))
            self.assertFalse(bc.prove(0))
            counts.append(bc.calls)
        self.assertEqual(counts, [3, 11, 49, 261, 1631, 11743])
        for n, c in zip(range(2, 8), counts):
            f = 1
            for i in range(2, n):
                f *= i
            self.assertGreaterEqual(c, f)


if __name__ == "__main__":
    unittest.main()
