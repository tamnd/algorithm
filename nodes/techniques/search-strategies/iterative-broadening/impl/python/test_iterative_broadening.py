# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-broadening/. The authors are listed in prov/5WXKC7.jsonl.

import random
import unittest

from iterative_broadening import iterative_broadening


def uniform(b, d):
    return lambda s: [s + (i,) for i in range(b)] if len(s) < d else []


def all_nodes(start, successors):
    out, stack = [], [start]
    while stack:
        s = stack.pop()
        out.append(s)
        stack.extend(successors(s))
    return out


class TestPageExample(unittest.TestCase):
    goals = {(1, 0, 1), (1, 2, 2), (2, 1, 0)}

    def test_broadening(self):
        trace: list = []
        r = iterative_broadening((), uniform(3, 3), lambda s: s in self.goals, trace=trace)
        self.assertEqual(r, [(), (1,), (1, 0), (1, 0, 1)])
        self.assertEqual(len(trace), 12)

    def test_plain_dfs(self):
        trace: list = []
        r = iterative_broadening((), uniform(3, 3), lambda s: s in self.goals, first_cutoff=3, trace=trace)
        self.assertEqual(r, [(), (1,), (1, 0), (1, 0, 1)])
        self.assertEqual(len(trace), 18)

    def test_worst_case_table(self):
        def n(c, d):
            return sum(c**i for i in range(d + 1))

        rows = {(3, 3): 55, (4, 7): 25380, (6, 6): 82199, (10, 5): 249627}
        for (b, d), total in rows.items():
            self.assertEqual(sum(n(c, d) for c in range(2, b + 1)), total)
            self.assertLess(sum(c**d for c in range(2, b + 1)), (1 + b / (d + 1)) * b**d)

    def test_worst_case_run_count(self):
        b, d = 3, 3
        last = (2, 2, 2)
        trace: list = []
        r = iterative_broadening((), uniform(b, d), lambda s: s == last, trace=trace)
        self.assertEqual(r[-1], last)
        self.assertEqual(len(trace), 15 + 40)


class TestEdgeCases(unittest.TestCase):
    def test_start_is_goal(self):
        self.assertEqual(iterative_broadening(0, lambda s: [], lambda s: s == 0), [0])

    def test_no_goal(self):
        trace: list = []
        self.assertIsNone(iterative_broadening((), uniform(4, 2), lambda s: False, trace=trace))
        self.assertEqual(len(trace), 7 + 13 + 21)

    def test_bad_cutoff(self):
        with self.assertRaises(ValueError):
            iterative_broadening(0, lambda s: [], lambda s: False, first_cutoff=0)

    def test_leaf_root_no_goal(self):
        self.assertIsNone(iterative_broadening(0, lambda s: [], lambda s: False))


class TestRandom(unittest.TestCase):
    def test_random_trees(self):
        rng = random.Random(1992)
        for trial in range(600):
            kids: dict = {}

            def build(node, depth):
                k = rng.randint(0, 5) if depth < 4 else 0
                kids[node] = [node + (i,) for i in range(k)]
                for ch in kids[node]:
                    build(ch, depth + 1)

            build((), 0)
            nodes = all_nodes((), lambda s: kids[s])
            goals = {v for v in nodes if rng.random() < 0.05}
            r = iterative_broadening((), lambda s: kids[s], lambda s: s in goals)
            if not goals:
                self.assertIsNone(r, trial)
            else:
                self.assertIsNotNone(r, trial)
                self.assertEqual(r[0], ())
                self.assertIn(r[-1], goals)
                for a, b in zip(r, r[1:]):
                    self.assertIn(b, kids[a])


if __name__ == "__main__":
    unittest.main()
