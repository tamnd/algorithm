# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-state-space-search/. The authors are listed in prov/3SHV74.jsonl.

import heapq
import random
import unittest

from forward_state_space_search import (
    blocks_world_actions, blocks_world_state, delivery_task, forward_search, is_plan,
    make_action, reachable,
)


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        rest = [f for f in facts if f not in add]
        delete = rng.sample(rest, rng.randint(0, min(2, len(rest))))
        acts.append(make_action(f"a{i}", pre, add, delete, rng.randint(1, 4)))
    init = frozenset(f for f in facts if rng.random() < 0.4)
    goal = frozenset(rng.sample(facts, rng.randint(1, 3)))
    return init, goal, acts


def logistics_task(n_packages, places=("A", "B", "C")):
    """One truck; package i starts at places[i % len] and must reach the next place."""
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
    pegs = ["P1", "P2", "P3"]
    places = disks + pegs
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


def bfs_optimum(init, goal, acts):
    dist = reachable(init, acts)
    ds = [d for s, d in dist.items() if goal <= s]
    return min(ds) if ds else None


def dijkstra_optimum(init, goal, acts):
    best = {init: 0}
    heap = [(0, 0, init)]
    tie = 0
    while heap:
        g, _, s = heapq.heappop(heap)
        if g > best[s]:
            continue
        if goal <= s:
            return g
        for a in acts:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in best or g + a.cost < best[t]:
                    best[t] = g + a.cost
                    tie += 1
                    heapq.heappush(heap, (g + a.cost, tie, t))
    return None


def all_tasks():
    rng = random.Random(20240611)
    tasks = [delivery_task(), logistics_task(2), logistics_task(3)]
    for stacks_from, stacks_to in [([["C", "A"], ["B"]], [["C", "B", "A"]]), ([["A", "B", "C"]], [["C", "B", "A"]]),
                                   ([["A", "B"], ["C", "D"]], [["D", "C", "B", "A"]])]:
        blocks = sorted({b for st in stacks_from for b in st})
        goal = blocks_world_state(stacks_to) - {("handempty",)}
        tasks.append((blocks_world_state(stacks_from), goal, blocks_world_actions(blocks)))
    for n in range(1, 5):
        tasks.append(hanoi_task(n))
    for _ in range(300):
        tasks.append(random_task(rng, rng.randint(4, 8), rng.randint(3, 8)))
    return tasks


class TestForwardSearch(unittest.TestCase):
    def test_plans_are_valid_and_existence_agrees_with_reachability(self):
        solvable = 0
        for init, goal, acts in all_tasks():
            opt = bfs_optimum(init, goal, acts)
            for strategy in ("bfs", "dfs", "ucs"):
                plan, _ = forward_search(init, goal, acts, strategy)
                self.assertEqual(plan is None, opt is None)
                if plan is not None:
                    self.assertTrue(is_plan(init, goal, plan))
            solvable += opt is not None
        self.assertGreater(solvable, 100)

    def test_bfs_is_step_optimal_and_ucs_is_cost_optimal(self):
        for init, goal, acts in all_tasks():
            opt = bfs_optimum(init, goal, acts)
            plan, _ = forward_search(init, goal, acts, "bfs")
            if opt is not None:
                self.assertEqual(len(plan), opt)
            plan, _ = forward_search(init, goal, acts, "ucs")
            c = dijkstra_optimum(init, goal, acts)
            if c is not None:
                self.assertEqual(sum(a.cost for a in plan), c)

    def test_dfs_can_return_a_longer_plan(self):
        longer = 0
        for init, goal, acts in all_tasks():
            p1, _ = forward_search(init, goal, acts, "bfs")
            p2, _ = forward_search(init, goal, acts, "dfs")
            if p1 is not None and len(p2) > len(p1):
                longer += 1
        self.assertGreater(longer, 0)

    def test_hanoi_needs_two_to_the_n_minus_one_moves(self):
        for n in range(1, 6):
            init, goal, acts = hanoi_task(n)
            plan, _ = forward_search(init, goal, acts, "bfs")
            self.assertEqual(len(plan), 2 ** n - 1)
            self.assertEqual(len(reachable(init, acts)), 3 ** n)

    def test_delivery_example(self):
        init, goal, acts = delivery_task()
        plan, st = forward_search(init, goal, acts, "bfs")
        self.assertEqual([a.name for a in plan], ["load(A)", "drive(A,B)", "unload(B)"])
        self.assertEqual(len(reachable(init, acts)), 6)
        self.assertEqual(st.expanded, 4)

    def test_unsolvable_task_explores_every_reachable_state(self):
        init, _, acts = delivery_task()
        plan, st = forward_search(init, frozenset(["pA", "pB"]), acts, "bfs")
        self.assertIsNone(plan)
        self.assertEqual(st.expanded, 6)


if __name__ == "__main__":
    unittest.main()
