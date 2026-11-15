# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/assumption-based-truth-maintenance/. The authors are listed in prov/.

import random
import unittest
from itertools import combinations

from assumption_based_truth_maintenance import ATMS, FALSE


def closure(env, justs):
    """Every node that follows from the assumptions of env by the Horn justifications."""
    known = set(env)
    changed = True
    while changed:
        changed = False
        for x, ants in justs:
            if x not in known and all(a in known for a in ants):
                known.add(x)
                changed = True
    return known


def brute_force(assumptions, nodes, justs):
    """Labels and nogoods from every environment: the minimal consistent environments that derive each node."""
    envs = [frozenset(c) for k in range(len(assumptions) + 1) for c in combinations(sorted(assumptions), k)]
    closed = {e: closure(e, justs) for e in envs}
    bad = [e for e in envs if FALSE in closed[e]]
    nogoods = {e for e in bad if not any(o < e for o in bad)}
    labels = {}
    for x in nodes:
        good = [e for e in envs if FALSE not in closed[e] and x in closed[e]]
        labels[x] = {e for e in good if not any(o < e for o in good)}
    return labels, nogoods, envs, closed


class TestATMS(unittest.TestCase):
    def check_properties(self, atms, assumptions, nodes, justs):
        labels, nogoods, envs, closed = brute_force(assumptions, nodes, justs)
        self.assertEqual(set(atms.nogoods), nogoods)
        for x in nodes:
            label = atms.label[x]
            self.assertEqual(len(label), len(set(label)))
            for e in label:
                self.assertIn(x, closed[e])  # sound
                self.assertNotIn(FALSE, closed[e])  # consistent
                self.assertFalse(any(o < e for o in label))  # minimal
            for e in envs:  # complete
                if FALSE not in closed[e] and x in closed[e]:
                    self.assertTrue(any(o <= e for o in label))
            self.assertEqual(set(label), labels[x])

    def test_page_example(self):
        t = ATMS()
        for a in "ABC":
            t.add_assumption(a)
        t.justify("x", ["A", "B"])
        t.justify("y", ["B"])
        t.justify("y", ["C"])
        self.assertEqual(set(t.label["y"]), {frozenset("B"), frozenset("C")})
        t.justify("z", ["x", "y"])
        self.assertEqual(set(t.label["z"]), {frozenset("AB")})
        t.justify("z", ["y"])
        self.assertEqual(set(t.label["z"]), {frozenset("B"), frozenset("C")})
        t.justify(FALSE, ["A", "B"])
        self.assertEqual(t.nogoods, [frozenset("AB")])
        self.assertEqual(t.label["x"], [])
        self.assertEqual(set(t.label["z"]), {frozenset("B"), frozenset("C")})
        self.assertTrue(t.holds("z", frozenset("BC")))
        self.assertFalse(t.holds("z", frozenset("AB")))

    def test_random_against_brute_force(self):
        rng = random.Random(20261115)
        with_nogoods = 0
        for _ in range(150):
            assumptions = ["A" + str(i) for i in range(rng.randint(1, 6))]
            derived = ["n" + str(i) for i in range(rng.randint(1, 4))]
            nodes = assumptions + derived
            t = ATMS()
            for a in assumptions:
                t.add_assumption(a)
            for x in derived:
                t.add_node(x)
            justs = []
            for _ in range(rng.randint(1, 10)):
                x = FALSE if rng.random() < 0.15 else rng.choice(derived + assumptions[:1])
                ants = tuple(rng.sample(nodes, rng.randint(0 if x != FALSE else 1, min(3, len(nodes)))))
                justs.append((x, ants))
                t.justify(x, ants)
                self.check_properties(t, assumptions, nodes, justs)
            with_nogoods += bool(t.nogoods)
        self.assertGreater(with_nogoods, 30)  # the random cases do reach contradictions

    def test_exponential_label(self):
        for n in range(1, 8):
            t = ATMS()
            xs = []
            for i in range(n):
                t.add_assumption("A" + str(i))
                t.add_assumption("B" + str(i))
                t.justify("x" + str(i), ["A" + str(i)])
                t.justify("x" + str(i), ["B" + str(i)])
                xs.append("x" + str(i))
            t.justify("g", xs)
            self.assertEqual(len(t.label["g"]), 2**n)
            self.assertTrue(all(len(e) == n for e in t.label["g"]))


if __name__ == "__main__":
    unittest.main()
