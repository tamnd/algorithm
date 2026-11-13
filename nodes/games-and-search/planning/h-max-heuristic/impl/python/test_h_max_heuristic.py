# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-max-heuristic/. The authors are listed in prov/7HHW76.jsonl.

import heapq
import itertools
import random
import unittest

from h_max_heuristic import INF, fact_costs_bellman_ford, fact_costs_dijkstra, h_max, make_action


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
    """Brute force: the cheapest action set whose relaxed closure contains the goal."""
    best = INF
    for r in range(len(acts) + 1):
        for sub in itertools.combinations(acts, r):
            c = sum(a.cost for a in sub)
            if c < best and goal <= closure(init, sub):
                best = c
    return best


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


class TestHMax(unittest.TestCase):
    def test_dijkstra_equals_bellman_ford(self):
        rng = random.Random(1977)
        for _ in range(500):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 10))
            self.assertEqual(fact_costs_dijkstra(init, acts), fact_costs_bellman_ford(init, acts))

    def test_h_max_le_h_plus_le_h_star(self):
        rng = random.Random(2000)
        finite = strict = 0
        for _ in range(300):
            init, goal, acts = random_task(rng, rng.randint(4, 8), rng.randint(3, 8))
            hm, hp, hs = h_max(init, goal, acts), h_plus(init, goal, acts), h_star(init, goal, acts)
            self.assertLessEqual(hm, hp)
            self.assertLessEqual(hp, hs)
            self.assertEqual(hm == INF, hp == INF)          # same dead ends as the relaxation
            if hp < INF:
                finite += 1
                strict += hm < hp
        self.assertGreater(finite, 100)
        self.assertGreater(strict, 5)

    def test_h_max_is_zero_exactly_on_goal_states(self):
        rng = random.Random(4)
        for _ in range(200):
            init, goal, acts = random_task(rng, 6, 6)
            acts = [a._replace(cost=a.cost + 1) for a in acts]   # positive costs
            self.assertEqual(h_max(init, goal, acts) == 0, goal <= init)

    def test_independent_goals(self):
        for n in range(1, 8):
            acts = [make_action(f"get{i}", [], [f"g{i}"], []) for i in range(n)]
            goal = frozenset(f"g{i}" for i in range(n))
            self.assertEqual(h_max(frozenset(), goal, acts), 1)
            self.assertEqual(h_star(frozenset(), goal, acts), n)

    def test_two_package_example(self):
        init, goal, acts = two_package_task()
        g = fact_costs_dijkstra(init, acts)
        self.assertEqual(g, {"tA": 0, "p1@A": 0, "p2@A": 0, "tB": 1, "p1@T": 1, "p2@T": 1, "p1@B": 2, "p2@B": 2})
        self.assertEqual(h_max(init, goal, acts), 2)
        self.assertEqual(h_max(init, goal, acts, "bellman-ford"), 2)
        self.assertEqual(h_plus(init, goal, acts), 5)


if __name__ == "__main__":
    unittest.main()
