# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goal-regression/. The authors are listed in prov/X17W61.jsonl.

import itertools
import random
import unittest

from goal_regression import make_action, regress, regress_plan, relevant, run_plan, suffix_conditions


def subsets(facts):
    for r in range(len(facts) + 1):
        for c in itertools.combinations(facts, r):
            yield frozenset(c)


def random_action(rng, facts, name="a"):
    pre = rng.sample(facts, rng.randint(0, 3))
    add = rng.sample(facts, rng.randint(1, 3))
    rest = [f for f in facts if f not in add]
    delete = rng.sample(rest, rng.randint(0, min(3, len(rest))))
    return make_action(name, pre, add, delete)


class TestGoalRegression(unittest.TestCase):
    def test_regression_is_the_weakest_precondition(self):
        """For every state s: s contains regress(g, a) iff a applies in s and its result contains g."""
        rng = random.Random(1977)
        checked_relevant = 0
        for _ in range(400):
            nf = rng.randint(4, 8)
            facts = list(range(nf))
            a = random_action(rng, facts)
            g = frozenset(rng.sample(facts, rng.randint(1, 4)))
            r = regress(g, a)
            for s in subsets(facts):
                works = a.pre <= s and g <= ((s - a.delete) | a.add)
                self.assertEqual(works, r is not None and r <= s)
            checked_relevant += relevant(g, a)
        self.assertGreater(checked_relevant, 50)

    def test_plan_regression_is_exact(self):
        rng = random.Random(42)
        for _ in range(150):
            facts = list(range(rng.randint(4, 7)))
            plan = [random_action(rng, facts, f"a{i}") for i in range(rng.randint(1, 4))]
            g = frozenset(rng.sample(facts, rng.randint(1, 3)))
            r = regress_plan(g, plan)
            for s in subsets(facts):
                final = run_plan(s, plan)
                works = final is not None and g <= final
                self.assertEqual(works, r is not None and r <= s)

    def test_regressed_goal_can_be_unsatisfiable_in_reachable_states(self):
        stack_ab = make_action("stack(A,B)", [("holding", "A"), ("clear", "B")], [("on", "A", "B"), ("clear", "A"), ("handempty",)], [("holding", "A"), ("clear", "B")])
        stack_bc = make_action("stack(B,C)", [("holding", "B"), ("clear", "C")], [("on", "B", "C"), ("clear", "B"), ("handempty",)], [("holding", "B"), ("clear", "C")])
        g = frozenset([("on", "A", "B"), ("on", "B", "C")])
        g1 = regress(g, stack_ab)
        self.assertEqual(g1, frozenset([("holding", "A"), ("clear", "B"), ("on", "B", "C")]))
        self.assertTrue(relevant(g1, stack_bc))
        self.assertEqual(regress(g1, stack_bc), frozenset([("holding", "A"), ("holding", "B"), ("clear", "C")]))

    def test_suffix_conditions_of_the_sussman_plan(self):
        def act(name, pre, add, delete):
            return make_action(name, pre, add, delete)
        H = ("handempty",)
        plan = [
            act("unstack(C,A)", [("on", "C", "A"), ("clear", "C"), H], [("holding", "C"), ("clear", "A")], [("on", "C", "A"), ("clear", "C"), H]),
            act("putdown(C)", [("holding", "C")], [("ontable", "C"), ("clear", "C"), H], [("holding", "C")]),
            act("pickup(B)", [("clear", "B"), ("ontable", "B"), H], [("holding", "B")], [("clear", "B"), ("ontable", "B"), H]),
            act("stack(B,C)", [("holding", "B"), ("clear", "C")], [("on", "B", "C"), ("clear", "B"), H], [("holding", "B"), ("clear", "C")]),
            act("pickup(A)", [("clear", "A"), ("ontable", "A"), H], [("holding", "A")], [("clear", "A"), ("ontable", "A"), H]),
            act("stack(A,B)", [("holding", "A"), ("clear", "B")], [("on", "A", "B"), ("clear", "A"), H], [("holding", "A"), ("clear", "B")]),
        ]
        g = frozenset([("on", "A", "B"), ("on", "B", "C")])
        conds = suffix_conditions(g, plan)
        init = frozenset([("on", "C", "A"), ("clear", "C"), ("ontable", "A"), ("ontable", "B"), ("clear", "B"), H])
        self.assertTrue(conds[0] <= init)
        self.assertEqual(len(conds[0]), 6)
        self.assertEqual(conds[4], frozenset([("on", "B", "C"), ("clear", "B"), ("clear", "A"), ("ontable", "A"), H]))
        s = init
        for i, a in enumerate(plan):
            self.assertTrue(conds[i] <= s)
            s = (s - a.delete) | a.add
        self.assertTrue(g <= s)


if __name__ == "__main__":
    unittest.main()
