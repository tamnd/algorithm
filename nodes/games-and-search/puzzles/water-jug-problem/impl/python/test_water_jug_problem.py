# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/water-jug-problem/. The authors are listed in prov/DYGENX.jsonl.
import unittest
from math import gcd

from water_jug_problem import (
    bfs,
    measurable,
    pour_only_bfs,
    shortest_plan,
    strategy_steps,
    two_jug_moves,
)


def replay(a, b, plan):
    s = (0, 0)
    for name in plan:
        s = dict(two_jug_moves(s, a, b))[name]
    return s


class TestGcdRule(unittest.TestCase):
    def test_rule_against_bfs(self):
        for a in range(1, 21):
            for b in range(1, 21):
                dist, _ = bfs(a, b)
                for c in range(0, max(a, b) + 3):
                    found = any(c in s for s in dist)
                    self.assertEqual(found, measurable(a, b, c), (a, b, c))

    def test_reachable_states(self):
        for a in range(1, 21):
            for b in range(1, 21):
                g = gcd(a, b)
                dist, _ = bfs(a, b)
                boundary = {
                    (x, y)
                    for x in range(0, a + 1, g)
                    for y in range(0, b + 1, g)
                    if x in (0, a) or y in (0, b)
                }
                self.assertEqual(set(dist), boundary)
                self.assertEqual(len(dist), 2 * (a + b) // g)
                totals = {x + y for x, y in dist}
                self.assertEqual(totals, set(range(0, a + b + 1, g)))


class TestShortest(unittest.TestCase):
    def test_die_hard(self):
        plan = shortest_plan(3, 5, 4)
        self.assertEqual(len(plan), 6)
        self.assertIn(4, replay(3, 5, plan))

    def test_unmeasurable(self):
        self.assertIsNone(shortest_plan(4, 6, 3))
        self.assertIsNone(shortest_plan(3, 5, 6))

    def test_plans_replay(self):
        for a, b in ((3, 5), (4, 9), (6, 10), (7, 11)):
            dist, _ = bfs(a, b)
            for c in range(1, max(a, b) + 1):
                plan = shortest_plan(a, b, c)
                if plan is None:
                    continue
                self.assertIn(c, replay(a, b, plan))
                self.assertEqual(len(plan), min(dist[s] for s in dist if c in s))

    def test_strategies_are_shortest(self):
        for a in range(1, 21):
            for b in range(1, 21):
                dist, _ = bfs(a, b)
                for c in range(0, max(a, b) + 1):
                    goals = [dist[s] for s in dist if c in s]
                    if goals:
                        self.assertEqual(strategy_steps(a, b, c), min(goals), (a, b, c))
                    else:
                        self.assertIsNone(strategy_steps(a, b, c))


class TestThreeJugs(unittest.TestCase):
    def test_bachet_8_5_3(self):
        dist = pour_only_bfs((8, 5, 3), (8, 0, 0))
        self.assertEqual(dist[(4, 4, 0)], 7)
        self.assertEqual(len(dist), 16)
        self.assertTrue(all(sum(s) == 8 for s in dist))


if __name__ == "__main__":
    unittest.main()
