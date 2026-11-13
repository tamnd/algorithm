# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-state-space-search/. The authors are listed in prov/3Y3JQ2.jsonl.

import random
import unittest
from collections import deque

from backward_state_space_search import (
    all_subgoals, backward_search, is_plan, make_action, regress, relevant,
)


def reachable(init, acts):
    """Reference: breadth first search over all reachable states."""
    init = frozenset(init)
    dist = {init: 0}
    q = deque([init])
    while q:
        s = q.popleft()
        for a in acts:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    q.append(t)
    return dist


def bfs_optimum(init, goal, acts):
    ds = [d for s, d in reachable(init, acts).items() if goal <= s]
    return min(ds) if ds else None


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


def delivery_task():
    acts = [
        make_action("drive(A,B)", ["tA"], ["tB"], ["tA"]),
        make_action("drive(B,A)", ["tB"], ["tA"], ["tB"]),
        make_action("load(A)", ["tA", "pA"], ["pT"], ["pA"]),
        make_action("load(B)", ["tB", "pB"], ["pT"], ["pB"]),
        make_action("unload(A)", ["tA", "pT"], ["pA"], ["pT"]),
        make_action("unload(B)", ["tB", "pT"], ["pB"], ["pT"]),
    ]
    return frozenset(["tA", "pA"]), frozenset(["pB"]), acts


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


def blocks_world_state(stacks):
    facts = {("handempty",)}
    for st in stacks:
        facts.add(("ontable", st[0]))
        for below, above in zip(st, st[1:]):
            facts.add(("on", above, below))
        facts.add(("clear", st[-1]))
    return frozenset(facts)


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
                if x == y or x == d or y == d:
                    continue
                if (x in disks and x <= d) or (y in disks and y <= d):
                    continue
                acts.append(make_action(f"move({d},{x},{y})", [("on", d, x), ("clear", d), ("clear", y)],
                                        [("on", d, y), ("clear", x)], [("on", d, x), ("clear", y)]))
    init = {("on", d, d + 1) for d in disks[:-1]} | {("on", n, "P1"), ("clear", 1), ("clear", "P2"), ("clear", "P3")}
    goal = {("on", d, d + 1) for d in disks[:-1]} | {("on", n, "P3")}
    return frozenset(init), frozenset(goal), acts


def all_tasks():
    rng = random.Random(7)
    tasks = [delivery_task(), logistics_task(1)]
    # Regression is slow on the blocks world (see the page), so one 3-block task is enough here.
    fr, to = [["A", "C"], ["B"]], [["C", "B", "A"]]
    tasks.append((blocks_world_state(fr), blocks_world_state(to) - {("handempty",)}, blocks_world_actions(["A", "B", "C"])))
    for n in range(1, 3):
        tasks.append(hanoi_task(n))
    for _ in range(300):
        tasks.append(random_task(rng, rng.randint(4, 8), rng.randint(3, 8)))
    return tasks


class TestBackwardSearch(unittest.TestCase):
    def test_existence_validity_and_optimal_length(self):
        solvable = 0
        for init, goal, acts in all_tasks():
            opt = bfs_optimum(init, goal, acts)
            for strategy in ("bfs", "dfs"):
                plan, _ = backward_search(init, goal, acts, strategy)
                self.assertEqual(plan is None, opt is None)
                if plan is not None:
                    self.assertTrue(is_plan(init, goal, plan))
                    if strategy == "bfs":
                        self.assertEqual(len(plan), opt)
            solvable += opt is not None
        self.assertGreater(solvable, 100)

    def test_every_step_is_relevant(self):
        for init, goal, acts in all_tasks():
            plan, _ = backward_search(init, goal, acts)
            if plan is None:
                continue
            g = frozenset(goal)
            for a in reversed(plan):
                self.assertTrue(relevant(g, a))
                g = regress(g, a)
            self.assertTrue(g <= init)

    def test_delivery_trace(self):
        init, goal, acts = delivery_task()
        trace = []
        plan, st = backward_search(init, goal, acts, trace=trace)
        self.assertEqual([a.name for a in plan], ["load(A)", "drive(A,B)", "unload(B)"])
        self.assertEqual(trace, [frozenset(["pB"]), frozenset(["tB", "pT"]), frozenset(["tA", "pT"]),
                                 frozenset(["tA", "tB", "pA"]), frozenset(["tB", "pB"])])
        self.assertEqual(st.expanded, 5)
        states = list(reachable(init, acts))
        unreachable = [g for g in all_subgoals(goal, acts) if not any(g <= s for s in states)]
        self.assertEqual(len(unreachable), 3)
        self.assertTrue(all({"tA", "tB"} <= g for g in unreachable))

    def test_regression_reaches_unreachable_subgoals(self):
        init = blocks_world_state([["A"], ["B"], ["C"]])
        acts = blocks_world_actions(["A", "B", "C"])
        goal = frozenset([("on", "A", "B"), ("on", "B", "C")])
        states = list(reachable(init, acts))
        g1 = regress(goal, next(a for a in acts if a.name == "stack(A,B)"))
        a2 = next(a for a in acts if a.name == "stack(B,C)")
        self.assertTrue(relevant(g1, a2))
        g2 = regress(g1, a2)
        self.assertEqual(g2, frozenset([("holding", "A"), ("holding", "B"), ("clear", "C")]))
        self.assertFalse(any(g2 <= s for s in states))
        subs = all_subgoals(goal, acts)
        dead = [g for g in subs if not any(g <= s for s in states)]
        self.assertGreater(len(dead), 0)


if __name__ == "__main__":
    unittest.main()
