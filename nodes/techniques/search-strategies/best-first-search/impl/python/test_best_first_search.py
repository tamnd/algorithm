# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-first-search/. The authors are listed in prov/MQ3R69.jsonl.

import random
import unittest

from best_first_search import Node, best_first_search

EDGES = {
    "S": [("A", 1), ("G", 12)],
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 3)],
    "C": [("D", 1), ("G", 2)],
    "D": [("G", 3)],
    "G": [],
}
H_STAR = {"S": 4, "A": 3, "B": 6, "C": 2, "D": 3, "G": 0}
H_1 = {"S": 4, "A": 3, "B": 1, "C": 2, "D": 1, "G": 0}


def run(f, edges=EDGES, start="S", goal="G"):
    trace: list = []
    res = best_first_search(start, lambda s: edges[s], lambda s: s == goal, f, trace)
    return res, trace


def bellman_ford(n, edges, src):
    """Independent oracle: shortest distances from src."""
    inf = float("inf")
    dist = [inf] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u in range(n):
            if dist[u] < inf:
                for v, c in edges[u]:
                    if dist[u] + c < dist[v]:
                        dist[v] = dist[u] + c
    return dist


def reverse_dist(n, edges, goals):
    """Least cost from each state to a goal, as the oracle h*."""
    rev = [[] for _ in range(n)]
    for u in range(n):
        for v, c in edges[u]:
            rev[v].append((u, c))
    inf = float("inf")
    best = [inf] * n
    for g in goals:
        d = bellman_ford(n, rev, g)
        best = [min(a, b) for a, b in zip(best, d)]
    return best


class TestPageExample(unittest.TestCase):
    def test_uniform_cost(self):
        res, trace = run(lambda n: n.g)
        self.assertEqual(res, (["S", "A", "C", "G"], 4))
        self.assertEqual(trace, ["S", "A", "C", "D"])

    def test_depth(self):
        res, trace = run(lambda n: n.depth)
        self.assertEqual(res, (["S", "G"], 12))
        self.assertEqual(trace, ["S", "A"])

    def test_a_star_perfect(self):
        res, trace = run(lambda n: n.g + H_STAR[n.state])
        self.assertEqual(res, (["S", "A", "C", "G"], 4))
        self.assertEqual(trace, ["S", "A", "C"])

    def test_greedy(self):
        res, trace = run(lambda n: H_1[n.state])
        self.assertEqual(res, (["S", "G"], 12))
        self.assertEqual(trace, ["S"])

    def test_admissible_h1_is_optimal(self):
        res, _ = run(lambda n: n.g + H_1[n.state])
        self.assertEqual(res[1], 4)


class TestEdgeCases(unittest.TestCase):
    def test_start_is_goal(self):
        res, trace = run(lambda n: n.g, start="G")
        self.assertEqual(res, (["G"], 0))
        self.assertEqual(trace, [])

    def test_unreachable(self):
        edges = {"S": [("A", 1)], "A": [("S", 1)], "G": []}
        res, trace = run(lambda n: n.g, edges)
        self.assertIsNone(res)
        self.assertEqual(sorted(trace), ["A", "S"])

    def test_cycle_stops_for_any_f(self):
        edges = {"S": [("A", 0)], "A": [("S", 0), ("B", 1)], "B": [("A", 0)]}
        for f in (lambda n: n.g, lambda n: -n.depth, lambda n: 0):
            res, _ = run(f, edges)
            self.assertIsNone(res)

    def test_inconsistent_heuristic_reopens(self):
        edges = {"S": [("A", 1), ("B", 2)], "A": [("C", 3)], "B": [("C", 1)], "C": [("G", 3)], "G": []}
        h = {"S": 0, "A": 0, "B": 3, "C": 0, "G": 0}
        res, trace = run(lambda n: n.g + h[n.state], edges)
        self.assertEqual(res, (["S", "B", "C", "G"], 6))
        self.assertEqual(trace.count("C"), 2)

    def test_negative_cost(self):
        with self.assertRaises(ValueError):
            best_first_search(0, lambda s: [(1, -1)], lambda s: False, lambda n: n.g)

    def test_infinite_space_a_star(self):
        # states are integers, moves +1 cost 1 and *2 cost 1, goal 37
        res = best_first_search(1, lambda s: [(s + 1, 1), (2 * s, 1)], lambda s: s == 37, lambda n: n.g)
        self.assertEqual(res[1], 7)

    def test_node_fields(self):
        n = Node("x", None, 0, 0)
        self.assertEqual((n.state, n.g, n.depth), ("x", 0, 0))


class TestRandom(unittest.TestCase):
    def test_random_graphs_against_bellman_ford(self):
        rng = random.Random(20261104)
        for trial in range(600):
            n = rng.randint(1, 9)
            edges = [[] for _ in range(n)]
            for u in range(n):
                for v in range(n):
                    if rng.random() < 0.35:
                        edges[u].append((v, rng.randint(0, 6)))
            goals = {v for v in range(n) if rng.random() < 0.25}
            dist = bellman_ford(n, edges, 0)
            best = min((dist[g] for g in goals), default=float("inf"))
            hstar = reverse_dist(n, edges, goals)
            scale = [rng.random() for _ in range(n)]
            h = [0 if hstar[v] == float("inf") else int(scale[v] * hstar[v]) for v in range(n)]
            for name, f in (
                ("g", lambda nd: nd.g),
                ("g+h", lambda nd: nd.g + h[nd.state]),
                ("depth", lambda nd: nd.depth),
                ("h", lambda nd: h[nd.state]),
            ):
                res = best_first_search(0, lambda s: edges[s], lambda s: s in goals, f)
                if best == float("inf"):
                    self.assertIsNone(res, (trial, name))
                    continue
                self.assertIsNotNone(res, (trial, name))
                path, cost = res
                self.assertEqual(path[0], 0)
                self.assertIn(path[-1], goals)
                total = 0
                for a, b in zip(path, path[1:]):
                    total += min(c for v, c in edges[a] if v == b)
                self.assertLessEqual(total, cost)
                self.assertGreaterEqual(cost, best)
                if name in ("g", "g+h"):
                    self.assertEqual(cost, best, (trial, name))


if __name__ == "__main__":
    unittest.main()
