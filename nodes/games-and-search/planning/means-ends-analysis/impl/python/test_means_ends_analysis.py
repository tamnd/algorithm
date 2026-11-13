# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/means-ends-analysis/. The authors are listed in prov/GDKDXZ.jsonl.

import random
import unittest

from means_ends_analysis import bfs_plan, difference_table, is_plan, make_action, means_ends, register_swap_task, small_swap_task


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        rest = [f for f in facts if f not in add]
        delete = rng.sample(rest, rng.randint(0, min(2, len(rest))))
        acts.append(make_action(f"a{i}", pre, add, delete))
    init = frozenset(f for f in facts if rng.random() < 0.4)
    goal = frozenset(rng.sample(facts, rng.randint(1, 3)))
    return init, goal, acts


def blocks_world_actions(blocks):
    acts = []
    for x in blocks:
        acts.append(make_action(f"pickup({x})", [("clear", x), ("ontable", x), ("handempty",)], [("holding", x)], [("clear", x), ("ontable", x), ("handempty",)]))
        acts.append(make_action(f"putdown({x})", [("holding", x)], [("ontable", x), ("clear", x), ("handempty",)], [("holding", x)]))
        for y in blocks:
            if x != y:
                acts.append(make_action(f"stack({x},{y})", [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), ("handempty",)], [("holding", x), ("clear", y)]))
                acts.append(make_action(f"unstack({x},{y})", [("on", x, y), ("clear", x), ("handempty",)], [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), ("handempty",)]))
    return acts


def logistics_task(n_packages, places=("A", "B", "C")):
    acts = []
    for x in places:
        for y in places:
            if x != y:
                acts.append(make_action(f"drive({x},{y})", [("truck", x)], [("truck", y)], [("truck", x)]))
    for p in range(n_packages):
        for x in places:
            acts.append(make_action(f"load(p{p},{x})", [("truck", x), ("at", p, x)], [("in", p)], [("at", p, x)]))
            acts.append(make_action(f"unload(p{p},{x})", [("truck", x), ("in", p)], [("at", p, x)], [("in", p)]))
    init = {("truck", places[0])} | {("at", p, places[p % len(places)]) for p in range(n_packages)}
    goal = {("at", p, places[(p + 1) % len(places)]) for p in range(n_packages)}
    return frozenset(init), frozenset(goal), acts


SUSSMAN_INIT = frozenset([("on", "C", "A"), ("clear", "C"), ("ontable", "A"), ("ontable", "B"), ("clear", "B"), ("handempty",)])
SUSSMAN_GOAL = frozenset([("on", "A", "B"), ("on", "B", "C")])


class TestMeansEndsAnalysis(unittest.TestCase):
    def test_plans_are_valid_and_never_claimed_for_unsolvable_tasks(self):
        rng = random.Random(5)
        solved = 0
        for _ in range(300):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 8))
            ref = bfs_plan(init, goal, acts)
            plan = means_ends(init, goal, acts, depth=6)
            if plan is not None:
                self.assertTrue(is_plan(init, goal, plan))
                solved += 1
            if ref is None:
                self.assertIsNone(plan)
        self.assertGreater(solved, 100)

    def test_solves_a_logistics_task(self):
        init, goal, acts = logistics_task(2)
        plan = means_ends(init, goal, acts, depth=4)
        self.assertTrue(is_plan(init, goal, plan))
        self.assertEqual(len(plan), len(bfs_plan(init, goal, acts)))

    def test_sussman_anomaly_is_solved_with_extra_actions(self):
        acts = blocks_world_actions(["A", "B", "C"])
        self.assertEqual(len(bfs_plan(SUSSMAN_INIT, SUSSMAN_GOAL, acts)), 6)
        for depth in range(1, 5):
            self.assertIsNone(means_ends(SUSSMAN_INIT, SUSSMAN_GOAL, acts, depth))
        plan = means_ends(SUSSMAN_INIT, SUSSMAN_GOAL, acts, 5)
        self.assertEqual([a.name for a in plan], [
            "unstack(C,A)", "putdown(C)", "pickup(A)", "stack(A,B)",      # on(A,B) first
            "unstack(A,B)", "putdown(A)", "pickup(B)", "stack(B,C)",      # undone for on(B,C)
            "pickup(A)", "stack(A,B)"])                                     # and done again
        lengths = []
        for depth in (5, 6, 8, 10):
            plan = means_ends(SUSSMAN_INIT, SUSSMAN_GOAL, acts, depth)
            self.assertTrue(is_plan(SUSSMAN_INIT, SUSSMAN_GOAL, plan))
            lengths.append(len(plan))
        self.assertEqual(lengths, [10, 12, 14, 16])

    def test_register_swap_fails_though_a_plan_exists(self):
        init, goal, acts = register_swap_task()
        ref = bfs_plan(init, goal, acts)
        self.assertEqual([a.name for a in ref], ["assign(R3,R1,a,c)", "assign(R1,R2,b,a)", "assign(R2,R3,a,b)"])
        for depth in range(1, 11):
            self.assertIsNone(means_ends(init, goal, acts, depth))

    def test_small_swap_fails_for_every_depth(self):
        init, goal, acts = small_swap_task()
        ref = bfs_plan(init, goal, acts)
        self.assertEqual(len(ref), 3)
        self.assertTrue(is_plan(init, goal, [acts[0], acts[2], acts[5]]))   # saveA, o1, o2'
        for depth in range(0, 13):
            self.assertIsNone(means_ends(init, goal, acts, depth))
        reorder = lambda diffs: sorted(diffs, key=repr, reverse=True)
        for depth in range(0, 13):
            self.assertIsNone(means_ends(init, goal, acts, depth, order=reorder))

    def test_backtracking_over_the_order_of_differences(self):
        a1 = make_action("A1", [], ["g1"], ["key"])
        a2 = make_action("A2", ["key"], ["g2"], [])
        init, goal = frozenset(["key"]), frozenset(["g1", "g2"])
        plan = means_ends(init, goal, [a1, a2], depth=3)
        self.assertEqual([a.name for a in plan], ["A2", "A1"])
        # with only the first difference tried, the method fails
        first_only = lambda diffs: sorted(diffs)[:1]
        self.assertIsNone(means_ends(init, goal, [a1, a2], depth=3, order=first_only))

    def test_difference_table(self):
        init, goal, acts = register_swap_task()
        table = difference_table(acts)
        self.assertEqual(len(table[("contains", "R1", "b")]), 4)


if __name__ == "__main__":
    unittest.main()
