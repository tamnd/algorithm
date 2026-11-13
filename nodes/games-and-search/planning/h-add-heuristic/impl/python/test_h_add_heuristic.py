# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-add-heuristic/. The authors are listed in prov/FN069M.jsonl.

import heapq
import itertools
import random
import unittest

from h_add_heuristic import INF, best_supporter_plan, fact_costs_bellman_ford, fact_costs_dijkstra, h_add, make_action


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


def closure(state, acts):
    s = set(state)
    changed = True
    while changed:
        changed = False
        for a in acts:
            if a.pre <= s and not a.add <= s:
                s |= a.add
                changed = True
    return s


def h_plus(init, goal, acts):
    best = INF
    for r in range(len(acts) + 1):
        for sub in itertools.combinations(acts, r):
            c = sum(a.cost for a in sub)
            if c < best and goal <= closure(init, sub):
                best = c
    return best


def h_max(init, goal, acts):
    g = {p: 0 for p in init}
    changed = True
    while changed:
        changed = False
        for a in acts:
            if all(q in g for q in a.pre):
                v = a.cost + max((g[q] for q in a.pre), default=0)
                for p in a.add:
                    if v < g.get(p, INF):
                        g[p] = v
                        changed = True
    return max((g.get(p, INF) for p in goal), default=0)


def h_star(init, goal, acts):
    best = {init: 0}
    heap = [(0, 0, init)]
    tie = 0
    while heap:
        c, _, s = heapq.heappop(heap)
        if c > best[s]:
            continue
        if goal <= s:
            return c
        for a in acts:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if c + a.cost < best.get(t, INF):
                    best[t] = c + a.cost
                    tie += 1
                    heapq.heappush(heap, (c + a.cost, tie, t))
    return INF


def two_package_task():
    acts = [make_action("drive(A,B)", ["tA"], ["tB"], ["tA"]), make_action("drive(B,A)", ["tB"], ["tA"], ["tB"])]
    for p in ("p1", "p2"):
        for x in ("A", "B"):
            acts.append(make_action(f"load({p},{x})", ["t" + x, f"{p}@{x}"], [f"{p}@T"], [f"{p}@{x}"]))
            acts.append(make_action(f"unload({p},{x})", ["t" + x, f"{p}@T"], [f"{p}@{x}"], [f"{p}@T"]))
    return frozenset(["tA", "p1@A", "p2@A"]), frozenset(["p1@B", "p2@B"]), acts


class TestHAdd(unittest.TestCase):
    def test_dijkstra_equals_bellman_ford(self):
        rng = random.Random(1997)
        for _ in range(500):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 10))
            self.assertEqual(fact_costs_dijkstra(init, acts)[0], fact_costs_bellman_ford(init, acts))

    def test_order_of_bounds(self):
        rng = random.Random(2001)
        finite = above = 0
        for _ in range(300):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 8))
            ha, hp, hm = h_add(init, goal, acts), h_plus(init, goal, acts), h_max(init, goal, acts)
            self.assertLessEqual(hm, ha)
            self.assertLessEqual(hp, ha)
            self.assertEqual(ha == INF, hp == INF)
            plan = best_supporter_plan(init, goal, acts)
            self.assertEqual(plan is None, ha == INF)
            if plan is not None:
                finite += 1
                s = set(init)
                for a in plan:
                    self.assertTrue(a.pre <= s)
                    s |= a.add
                self.assertTrue(goal <= s)
                cost = sum(a.cost for a in plan)
                self.assertLessEqual(hp, cost)
                self.assertLessEqual(cost, ha)
                above += ha > h_star(init, goal, acts)
        self.assertGreater(finite, 100)
        self.assertGreater(above, 0)

    def test_overcounting_shared_work(self):
        both = make_action("both", [], ["g1", "g2"], [])
        self.assertEqual(h_add(frozenset(), frozenset(["g1", "g2"]), [both]), 2)
        self.assertEqual(h_star(frozenset(), frozenset(["g1", "g2"]), [both]), 1)

    def test_two_package_example(self):
        init, goal, acts = two_package_task()
        g = fact_costs_dijkstra(init, acts)[0]
        self.assertEqual(g, {"tA": 0, "p1@A": 0, "p2@A": 0, "tB": 1, "p1@T": 1, "p2@T": 1, "p1@B": 3, "p2@B": 3})
        self.assertEqual(h_add(init, goal, acts), 6)
        self.assertEqual(h_add(init, goal, acts, "bellman-ford"), 6)
        self.assertEqual(h_plus(init, goal, acts), 5)
        self.assertEqual(h_star(init, goal, acts), 5)
        plan = best_supporter_plan(init, goal, acts)
        self.assertEqual(sorted(a.name for a in plan), ["drive(A,B)", "load(p1,A)", "load(p2,A)", "unload(p1,B)", "unload(p2,B)"])


if __name__ == "__main__":
    unittest.main()
