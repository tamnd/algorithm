# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anytime-repairing-a-star/. The authors are listed in prov/PYDPRD.jsonl.

import heapq
import random
import unittest
from fractions import Fraction

from anytime_repairing_a_star import ara_star

SCHEDULE = (5, 3, 2, Fraction(3, 2), Fraction(5, 4), 1)

# ---------------------------------------------------------------- oracles and generators


def dijkstra(adj, src):
    """Independent oracle: exact distances from src on a nonnegative graph."""
    dist = {src: 0}
    pq = [(0, src)]
    done = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for v, c in adj[u]:
            if v not in dist or d + c < dist[v]:
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


def random_grid(rng, w, hgt, wall, cmax):
    """4-connected grid with walls; entering a cell costs 1 to cmax."""
    cells = [(x, y) for x in range(w) for y in range(hgt) if rng.random() >= wall]
    cost = {v: rng.randint(1, cmax) for v in cells}
    adj = {v: [] for v in cells}
    for x, y in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            m = (x + dx, y + dy)
            if m in cost:
                adj[(x, y)].append((m, cost[m]))
    return adj


def path_cost(test, adj, path):
    total = 0
    for u, v in zip(path, path[1:]):
        cs = [c for w, c in adj[u] if w == v]
        test.assertTrue(cs, f"{u} -> {v} is not an edge")
        total += min(cs)
    return total


# ---------------------------------------------------------------- the page example

POS = {"S": (0, 0), "A": (2, 0), "B": (0, 2), "C": (2, 2),
       "D": (4, 0), "E": (0, 4), "F": (-1, 0), "G": (4, 2)}
EDGES = [("S", "A", 2), ("S", "B", 3), ("A", "C", 4), ("A", "D", 3), ("B", "C", 2),
         ("B", "E", 2), ("C", "G", 2), ("D", "G", 3), ("S", "F", 1)]


def page_graph():
    adj = {v: [] for v in POS}
    for u, v, c in EDGES:
        adj[u].append((v, c))
        adj[v].append((u, c))
    for v in adj:
        adj[v].sort()
    return adj


def manhattan(u):
    return abs(POS[u][0] - 4) + abs(POS[u][1] - 2)


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        adj = page_graph()
        r = ara_star("S", "G", lambda u: adj[u], manhattan, (3, 2, Fraction(3, 2), 1))
        got = [(s.eps, s.bound, s.cost, "".join(s.path), s.expansions) for s in r.solutions]
        self.assertEqual(got, [
            (3, Fraction(8, 7), 8, "SADG", 3),
            (2, Fraction(8, 7), 8, "SADG", 0),
            (Fraction(3, 2), Fraction(8, 7), 8, "SADG", 0),
            (1, 1, 7, "SBCG", 2),
        ])
        self.assertEqual(r.expanded, ["S", "A", "D", "B", "C"])

    def test_bad_schedule(self):
        for sched in ((2, 3, 1), (2, 2, 1), (3, 2), ()):
            with self.assertRaises(ValueError):
                ara_star(0, 0, lambda u: [], lambda u: 0, sched)

    def test_start_is_goal_and_unreachable(self):
        r = ara_star(0, 0, lambda u: [(1, 1)], lambda u: 0)
        self.assertEqual((r.best.cost, r.best.path, r.best.bound), (0, [0], 1))
        adj = {0: [(1, 1)], 1: [], 2: []}
        r = ara_star(0, 2, lambda u: adj[u], lambda u: 0)
        self.assertEqual(r.solutions, [])
        self.assertIsNone(r.best)


class TestRandomGrids(unittest.TestCase):
    def test_bounds_and_monotone_costs(self):
        rng = random.Random(17)
        runs = reused = scratch = 0
        for _ in range(150):
            adj = random_grid(rng, rng.randint(2, 14), rng.randint(2, 14), 0.25, 5)
            if len(adj) < 2:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            h = lambda u, t=t: abs(u[0] - t[0]) + abs(u[1] - t[1])  # noqa: E731
            dist = dijkstra(adj, s)
            r = ara_star(s, t, lambda u: adj[u], h, SCHEDULE)
            if t not in dist:
                self.assertEqual(r.solutions, [])
                continue
            best = dist[t]
            runs += 1
            prev = None
            start = 0
            for sol in r.solutions:
                self.assertEqual((sol.path[0], sol.path[-1]), (s, t))
                pc = path_cost(self, adj, sol.path)
                self.assertGreaterEqual(pc, best)
                self.assertLessEqual(pc, sol.cost)
                self.assertLessEqual(sol.cost, sol.bound * best)  # the reported bound holds
                self.assertLessEqual(sol.bound, sol.eps)
                self.assertGreaterEqual(sol.bound, 1)
                if prev is not None:
                    self.assertLessEqual(sol.cost, prev)  # costs never go up
                prev = sol.cost
                part = r.expanded[start:start + sol.expansions]
                self.assertEqual(len(part), len(set(part)))  # once per call
                start += sol.expansions
            self.assertEqual(start, len(r.expanded))
            last = r.solutions[-1]
            self.assertEqual(last.bound, 1)
            self.assertEqual(last.cost, best)
            # the same weights, each searched from scratch
            for sol in r.solutions:
                one = ara_star(s, t, lambda u: adj[u], h, (sol.eps, 1) if sol.eps > 1 else (1,))
                scratch += one.solutions[0].expansions
            reused += len(r.expanded)
        self.assertGreater(runs, 100)
        self.assertLess(reused, scratch)  # reuse saves expansions on these grids


if __name__ == "__main__":
    unittest.main()
