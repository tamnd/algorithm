# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hsp-planner/. The authors are listed in prov/WZK9NT.jsonl.

import random
import unittest
from collections import deque

from hsp_planner import INF, HAdd, hsp1, hsp2, is_plan, make_action, successor


def bfs_length(init, goal, acts):
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        if goal <= s:
            return dist[s]
        for a in acts:
            if a.pre <= s:
                t = successor(s, a)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


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


def blocks_world(blocks, towers_from, towers_to):
    H = ("handempty",)
    acts = []
    for x in blocks:
        acts.append(make_action(f"pickup({x})", [("clear", x), ("ontable", x), H], [("holding", x)], [("clear", x), ("ontable", x), H]))
        acts.append(make_action(f"putdown({x})", [("holding", x)], [("ontable", x), ("clear", x), H], [("holding", x)]))
        for y in blocks:
            if x != y:
                acts.append(make_action(f"stack({x},{y})", [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), H], [("holding", x), ("clear", y)]))
                acts.append(make_action(f"unstack({x},{y})", [("on", x, y), ("clear", x), H], [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), H]))

    def state(towers):
        s = {H}
        for t in towers:                       # each tower is listed bottom first
            s.add(("ontable", t[0]))
            s.add(("clear", t[-1]))
            for below, above in zip(t, t[1:]):
                s.add(("on", above, below))
        return frozenset(s)

    goal = frozenset(f for f in state(towers_to) if f[0] == "on")
    return state(towers_from), goal, acts


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


def hanoi_task(n):
    disks = list(range(1, n + 1))
    places = disks + ["P1", "P2", "P3"]
    acts = []
    for d in disks:
        for x in places:
            for y in places:
                if x == y or d == x or d == y:
                    continue
                if (isinstance(x, int) and x <= d) or (isinstance(y, int) and y <= d):
                    continue
                acts.append(make_action(f"move({d},{x},{y})", [("on", d, x), ("clear", d), ("clear", y)],
                                        [("on", d, y), ("clear", x)], [("on", d, x), ("clear", y)]))
    init = {("on", n, "P1"), ("clear", 1), ("clear", "P2"), ("clear", "P3")}
    goal = {("on", n, "P3")}
    for d in range(1, n):
        init.add(("on", d, d + 1))
        goal.add(("on", d, d + 1))
    return frozenset(init), frozenset(goal), acts


def structured_tasks():
    tasks = [
        blocks_world("ABC", ["AC", "B"], ["CBA"]),          # Sussman: C on A, goal A on B on C
        blocks_world("ABC", ["ABC"], ["CBA"]),
        blocks_world("ABCD", ["AB", "CD"], ["DCBA"]),
        logistics_task(2),
        logistics_task(3),
    ]
    tasks += [hanoi_task(n) for n in range(1, 5)]
    return tasks


class TestHSP(unittest.TestCase):
    def test_hsp2_finds_valid_plans_on_every_solvable_task(self):
        rng = random.Random(1998)
        tasks = structured_tasks() + [random_task(rng, rng.randint(4, 8), rng.randint(3, 8)) for _ in range(300)]
        solvable = 0
        for init, goal, acts in tasks:
            ref = bfs_length(init, goal, acts)
            for w in (1, 5):
                plan, _ = hsp2(init, goal, acts, weight=w)
                self.assertEqual(plan is None, ref is None)
                if plan is not None:
                    self.assertTrue(is_plan(init, goal, plan))
                    self.assertGreaterEqual(len(plan), ref)
            solvable += ref is not None
        self.assertGreater(solvable, 100)

    def test_hanoi_lengths(self):
        for n in range(1, 5):
            init, goal, acts = hanoi_task(n)
            plan, _ = hsp2(init, goal, acts)
            self.assertTrue(is_plan(init, goal, plan))
            self.assertGreaterEqual(len(plan), 2 ** n - 1)

    def test_weight_trades_quality_for_effort(self):
        init, goal, acts = logistics_task(3)
        p1, s1 = hsp2(init, goal, acts, weight=1)
        p5, s5 = hsp2(init, goal, acts, weight=5)
        self.assertTrue(is_plan(init, goal, p1) and is_plan(init, goal, p5))
        self.assertLessEqual(s5.expanded, s1.expanded)

    def test_hsp1_plans_are_valid(self):
        rng = random.Random(42)
        found = 0
        tasks = structured_tasks() + [random_task(rng, rng.randint(4, 8), rng.randint(3, 8)) for _ in range(200)]
        for k, (init, goal, acts) in enumerate(tasks):
            plan = hsp1(init, goal, acts, seed=k)
            if plan is not None:
                self.assertTrue(is_plan(init, goal, plan))
                found += 1
            if bfs_length(init, goal, acts) is None:
                self.assertIsNone(plan)
        self.assertGreater(found, 80)

    def test_hill_climbing_is_trapped_by_the_sussman_anomaly(self):
        init, goal, acts = structured_tasks()[0]
        h = HAdd(goal, acts)
        self.assertEqual(h(init), 5)
        self.assertEqual(sorted(h(successor(init, a)) for a in acts if a.pre <= init), [7, 7])
        for seed in range(5):
            self.assertIsNone(hsp1(init, goal, acts, seed=seed))
        plan, stats = hsp2(init, goal, acts)
        self.assertEqual([a.name for a in plan], ["unstack(C,A)", "putdown(C)", "pickup(B)", "stack(B,C)", "pickup(A)", "stack(A,B)"])
        self.assertEqual(stats.expanded, 10)

    def test_relaxed_dead_ends_are_pruned(self):
        use1 = make_action("use1", ["key"], ["g1"], ["key"])
        use2 = make_action("use2", ["key"], ["g2"], ["key"])
        init, goal = frozenset(["key"]), frozenset(["g1", "g2"])
        h = HAdd(goal, [use1, use2])
        self.assertEqual(h(init), 2)
        self.assertEqual(h(frozenset(["g1"])), INF)
        plan, stats = hsp2(init, goal, [use1, use2])
        self.assertIsNone(plan)
        self.assertEqual(stats.expanded, 1)


if __name__ == "__main__":
    unittest.main()
