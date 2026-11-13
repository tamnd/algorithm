# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delete-relaxation/. The authors are listed in prov/JJ5Q8N.jsonl.

import itertools
import random
import unittest

from delete_relaxation import (
    INF, h_plus, make_action, optimal_cost, relax, relaxed_closure, relaxed_solvable,
    set_cover_task, two_package_task,
)


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        rest = [f for f in facts if f not in add]
        delete = rng.sample(rest, rng.randint(0, min(2, len(rest))))
        acts.append(make_action(f"a{i}", pre, add, delete, rng.randint(0, 3)))
    init = frozenset(f for f in facts if rng.random() < 0.3)
    goal = frozenset(rng.sample(facts, rng.randint(1, 3)))
    return init, goal, acts


def h_plus_by_subsets(init, goal, acts):
    """Reference: the cheapest set of actions whose relaxed closure contains the goal.
    A set works exactly when some order of it is a relaxed plan."""
    best = INF
    for r in range(len(acts) + 1):
        for sub in itertools.combinations(acts, r):
            c = sum(a.cost for a in sub)
            if c < best and goal <= relaxed_closure(init, sub):
                best = c
    return best


def sussman():
    H = ("handempty",)
    acts = []
    blocks = ["A", "B", "C"]
    for x in blocks:
        acts.append(make_action(f"pickup({x})", [("clear", x), ("ontable", x), H], [("holding", x)], [("clear", x), ("ontable", x), H]))
        acts.append(make_action(f"putdown({x})", [("holding", x)], [("ontable", x), ("clear", x), H], [("holding", x)]))
        for y in blocks:
            if x != y:
                acts.append(make_action(f"stack({x},{y})", [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), H], [("holding", x), ("clear", y)]))
                acts.append(make_action(f"unstack({x},{y})", [("on", x, y), ("clear", x), H], [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), H]))
    init = frozenset([("on", "C", "A"), ("clear", "C"), ("ontable", "A"), ("ontable", "B"), ("clear", "B"), H])
    goal = frozenset([("on", "A", "B"), ("on", "B", "C")])
    return init, goal, acts


class TestDeleteRelaxation(unittest.TestCase):
    def test_h_plus_is_exact_and_admissible(self):
        rng = random.Random(2001)
        finite = 0
        for _ in range(300):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 8))
            hp, plan = h_plus(init, goal, acts)
            self.assertEqual(hp, h_plus_by_subsets(init, goal, acts))
            self.assertLessEqual(hp, optimal_cost(init, goal, acts))
            self.assertEqual(hp < INF, relaxed_solvable(init, goal, acts))
            if plan is not None:
                finite += 1
                s = set(init)
                for a in plan:
                    self.assertTrue(a.pre <= s)
                    s |= a.add
                self.assertTrue(goal <= s)
                self.assertEqual(sum(a.cost for a in plan), hp)
        self.assertGreater(finite, 100)

    def test_relaxed_unsolvable_implies_unsolvable(self):
        rng = random.Random(3)
        for _ in range(300):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 8))
            if not relaxed_solvable(init, goal, acts):
                self.assertEqual(optimal_cost(init, goal, acts), INF)

    def test_a_task_with_a_relaxed_plan_and_no_plan(self):
        use1 = make_action("use1", ["key"], ["g1"], ["key"])
        use2 = make_action("use2", ["key"], ["g2"], ["key"])
        init, goal = frozenset(["key"]), frozenset(["g1", "g2"])
        self.assertEqual(h_plus(init, goal, [use1, use2])[0], 2)
        self.assertEqual(optimal_cost(init, goal, [use1, use2]), INF)

    def test_worked_examples(self):
        init, goal, acts = two_package_task()
        self.assertEqual(h_plus(init, goal, acts)[0], 5)
        self.assertEqual(optimal_cost(init, goal, acts), 5)
        init, goal, acts = sussman()
        hp, plan = h_plus(init, goal, acts)
        self.assertEqual(hp, 5)
        self.assertEqual(optimal_cost(init, goal, acts), 6)
        self.assertEqual(sorted(a.name for a in plan), ["pickup(A)", "pickup(B)", "stack(A,B)", "stack(B,C)", "unstack(C,A)"])

    def test_set_cover_reduction(self):
        rng = random.Random(11)
        for _ in range(60):
            n = rng.randint(3, 7)
            universe = list(range(n))
            sets = [rng.sample(universe, rng.randint(1, 3)) for _ in range(rng.randint(2, 6))]
            init, goal, acts = set_cover_task(universe, sets)
            best = INF
            for r in range(len(sets) + 1):
                for sub in itertools.combinations(sets, r):
                    if set(universe) <= set().union(*map(set, sub)):
                        best = min(best, r)
            self.assertEqual(h_plus(init, goal, acts)[0], best)

    def test_relax_drops_only_deletes(self):
        init, goal, acts = sussman()
        for a, r in zip(acts, relax(acts)):
            self.assertEqual((a.pre, a.add, a.cost), (r.pre, r.add, r.cost))
            self.assertEqual(r.delete, frozenset())


if __name__ == "__main__":
    unittest.main()
