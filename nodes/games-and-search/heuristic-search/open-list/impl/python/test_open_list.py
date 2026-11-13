# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-list/. The authors are listed in prov/B9C3HD.jsonl.

import random
import unittest

from open_list import SLACK, OpenList


class Model:
    """A plain dict with a linear scan: the reference for OpenList."""

    def __init__(self):
        self.d = {}  # state -> (g, f, stamp)
        self.t = 0

    def push(self, n, g, f):
        if n in self.d and self.d[n][0] <= g:
            return False
        self.d[n] = (g, f, self.t)
        self.t += 1
        return True

    def pop_min(self):
        if not self.d:
            return None
        n = min(self.d, key=lambda s: (self.d[s][1], -self.d[s][0], self.d[s][2]))
        g, f, _ = self.d.pop(n)
        return n, g, f

    def remove(self, n):
        self.d.pop(n, None)


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        q = OpenList()
        self.assertTrue(q.push("A", 2, 6))
        self.assertTrue(q.push("B", 3, 7))
        self.assertTrue(q.push("F", 1, 8))
        self.assertEqual(q.pop_min(), ("A", 2, 6))
        self.assertTrue(q.push("C", 6, 8))
        self.assertTrue(q.push("D", 5, 7))
        self.assertEqual(q.pop_min(), ("D", 5, 7))  # tie at f = 7: larger g
        self.assertTrue(q.push("G", 8, 8))
        self.assertEqual(q.pop_min(), ("B", 3, 7))
        self.assertTrue(q.push("C", 5, 7))  # lower C from 6/8 to 5/7
        self.assertFalse(q.push("C", 5, 7))  # not cheaper: ignored
        self.assertEqual(len(q), 3)
        self.assertEqual(len(q.heap), 4)  # one stale entry of C
        self.assertEqual(q.pop_min(), ("C", 5, 7))
        self.assertTrue(q.push("G", 7, 7))
        self.assertEqual(q.pop_min(), ("G", 7, 7))
        self.assertEqual(q.pop_min(), ("F", 1, 8))
        self.assertIsNone(q.pop_min())
        q.check_invariant()

    def test_fifo_on_full_ties(self):
        q = OpenList()
        for s in "xyz":
            q.push(s, 4, 9)
        self.assertEqual([q.pop_min()[0] for _ in range(3)], ["x", "y", "z"])

    def test_remove_and_contains(self):
        q = OpenList()
        q.push(1, 0, 0)
        q.push(2, 1, 1)
        q.remove(1)
        q.remove(5)  # absent: no effect
        self.assertNotIn(1, q)
        self.assertIn(2, q)
        self.assertEqual(q.g(2), 1)
        self.assertEqual(q.pop_min(), (2, 1, 1))
        self.assertIsNone(q.pop_min())


class TestRandom(unittest.TestCase):
    def test_against_model(self):
        rng = random.Random(1234)
        for trial in range(600):
            q, m = OpenList(), Model()
            states = rng.randint(1, 12)
            for _ in range(rng.randint(0, 80)):
                r = rng.random()
                if r < 0.55:
                    n = rng.randrange(states)
                    g = rng.randint(0, 20)
                    f = g + rng.randint(0, 6)
                    self.assertEqual(q.push(n, g, f), m.push(n, g, f))
                elif r < 0.9:
                    self.assertEqual(q.pop_min(), m.pop_min())
                else:
                    n = rng.randrange(states)
                    q.remove(n)
                    m.remove(n)
                self.assertEqual(len(q), len(m.d))
                for n in range(states):
                    self.assertEqual(n in q, n in m.d)
                q.check_invariant()
            while m.d:
                self.assertEqual(q.pop_min(), m.pop_min())
            self.assertIsNone(q.pop_min())

    def test_many_decreases_keep_space_linear(self):
        q = OpenList()
        for g in range(1000, 0, -1):
            q.push("s", g, g)
            self.assertLessEqual(len(q.heap), 2 * len(q) + SLACK)
        self.assertEqual(q.pop_min(), ("s", 1, 1))
        self.assertEqual(len(q), 0)

    def test_heap_sort_order(self):
        rng = random.Random(77)
        for _ in range(100):
            items = [(i, rng.randint(0, 9), rng.randint(0, 9)) for i in range(rng.randint(0, 40))]
            q = OpenList()
            for n, g, f in items:
                q.push(n, g, f)
            out = []
            while len(q):
                out.append(q.pop_min())
            want = sorted(items, key=lambda x: (x[2], -x[1], x[0]))
            self.assertEqual(out, want)


if __name__ == "__main__":
    unittest.main()
