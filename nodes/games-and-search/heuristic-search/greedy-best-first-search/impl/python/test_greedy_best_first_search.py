# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-best-first-search/. The authors are listed in prov/TT8WY1.jsonl.

import heapq
import random
import unittest

from greedy_best_first_search import greedy_best_first_search

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


def random_digraph(rng, n, p, cmax):
    adj = {u: [] for u in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < p:
                adj[u].append((v, rng.randint(1, cmax)))
    return adj


def check_path(test, adj, path, s, t, cost):
    test.assertEqual((path[0], path[-1]), (s, t))
    total = 0
    for u, v in zip(path, path[1:]):
        cs = [c for w, c in adj[u] if w == v]
        test.assertTrue(cs, f"{u} -> {v} is not an edge")
        total += min(cs)
    test.assertEqual(total, cost)


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


# The loop example: S-A, S-B, B-C, C-D, D-G with unit costs. A is a dead end.
LOOP = {"S": [("A", 1), ("B", 1)], "A": [("S", 1)], "B": [("S", 1), ("C", 1)],
        "C": [("B", 1), ("D", 1)], "D": [("C", 1), ("G", 1)], "G": [("D", 1)]}
LOOP_H = {"S": 2, "A": 1, "B": 3, "C": 2, "D": 1, "G": 0}


class TestPageExample(unittest.TestCase):
    def test_trace(self):
        adj = page_graph()
        r = greedy_best_first_search("S", lambda u: adj[u], lambda u: u == "G", manhattan)
        self.assertEqual(r.path, ["S", "A", "C", "G"])
        self.assertEqual(r.cost, 8)
        self.assertEqual(r.expanded, ["S", "A", "C"])
        self.assertEqual(dijkstra(adj, "S")["G"], 7)

    def test_loop_heuristic_is_consistent(self):
        dist = dijkstra(LOOP, "G")
        for u in LOOP:
            self.assertLessEqual(LOOP_H[u], dist[u])
            for v, c in LOOP[u]:
                self.assertLessEqual(LOOP_H[u], c + LOOP_H[v])

    def test_tree_search_loops(self):
        r = greedy_best_first_search("S", lambda u: LOOP[u], lambda u: u == "G", LOOP_H.get,
                                     tree=True, max_expansions=1000)
        self.assertTrue(r.stopped)
        self.assertEqual(r.expanded[:6], ["S", "A", "S", "A", "S", "A"])
        self.assertEqual(set(r.expanded), {"S", "A"})

    def test_graph_search_does_not_loop(self):
        r = greedy_best_first_search("S", lambda u: LOOP[u], lambda u: u == "G", LOOP_H.get)
        self.assertEqual(r.path, ["S", "B", "C", "D", "G"])
        self.assertEqual(r.expanded, ["S", "A", "B", "C", "D"])

    def test_start_is_goal_and_unreachable(self):
        r = greedy_best_first_search("G", lambda u: LOOP[u], lambda u: u == "G", LOOP_H.get)
        self.assertEqual((r.path, r.cost), (["G"], 0))
        adj = {0: [(1, 1)], 1: [], 2: []}
        r = greedy_best_first_search(0, lambda u: adj[u], lambda u: u == 2, lambda u: 0)
        self.assertIsNone(r.path)
        self.assertEqual(r.expanded, [0, 1])


class TestRandom(unittest.TestCase):
    def run_case(self, adj, s, t, h):
        r = greedy_best_first_search(s, lambda u: adj[u], lambda u: u == t, h)
        dist = dijkstra(adj, s)
        if t in dist:
            self.assertIsNotNone(r.path)  # complete on finite graphs
            check_path(self, adj, r.path, s, t, r.cost)
            self.assertGreaterEqual(r.cost, dist[t])
            self.assertEqual(len(r.expanded), len(set(r.expanded)))
        else:
            self.assertIsNone(r.path)
            self.assertEqual(set(r.expanded), set(dist))  # it saw every reachable state
        return r, dist.get(t)

    def test_grids_manhattan(self):
        rng = random.Random(11)
        worse = 0
        for _ in range(300):
            adj = random_grid(rng, rng.randint(1, 10), rng.randint(1, 10), 0.3, 5)
            if not adj:
                continue
            cells = sorted(adj)
            s, t = rng.choice(cells), rng.choice(cells)
            r, best = self.run_case(adj, s, t, lambda u: abs(u[0] - t[0]) + abs(u[1] - t[1]))
            if r.path is not None and r.cost > best:
                worse += 1
        self.assertGreater(worse, 0)  # greedy search is not optimal

    def test_digraphs_any_heuristic(self):
        rng = random.Random(5)
        for _ in range(300):
            n = rng.randint(2, 20)
            adj = random_digraph(rng, n, rng.uniform(0.05, 0.4), 9)
            hv = [rng.randint(0, 30) for _ in range(n)]
            self.run_case(adj, rng.randrange(n), rng.randrange(n), lambda u: hv[u])


if __name__ == "__main__":
    unittest.main()
