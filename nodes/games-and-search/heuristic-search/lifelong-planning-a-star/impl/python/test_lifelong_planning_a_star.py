# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lifelong-planning-a-star/. The authors are listed in prov/X7W103.jsonl.

import heapq
import itertools
import random
import unittest
from collections import deque

from lifelong_planning_a_star import INF, LPAStar, lifelong_planning_a_star


def dijkstra(succ, s):
    dist = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, c in succ[u].items():
            if d + c < dist.get(v, INF):
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


def fresh_a_star(succ, s, t, h):
    """Expansions of A* from scratch, the goal counted, ties toward smaller g."""
    g = {s: 0}
    cnt = itertools.count()
    pq = [(h(s), 0, next(cnt), s)]
    closed = set()
    exp = 0
    while pq:
        _, gu, _, u = heapq.heappop(pq)
        if u in closed or gu != g[u]:
            continue
        exp += 1
        if u == t:
            return gu, exp
        closed.add(u)
        for v, c in succ[u].items():
            if c < INF and gu + c < g.get(v, INF):
                g[v] = gu + c
                heapq.heappush(pq, (g[v] + h(v), g[v], next(cnt), v))
    return INF, exp


def random_digraph(rng, n, p):
    succ = {u: {} for u in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < p:
                succ[u][v] = rng.randint(1, 9)
    return succ


def hop_heuristic(succ, goal):
    """Number of edges to the goal in the graph of all edges, and n where the goal cannot be reached.

    It is consistent when every cost is at least 1: an edge from a vertex that reaches the goal
    to a vertex that does not goes to the value n, which is larger than every hop count.
    """
    pred = {u: [] for u in succ}
    for u, vs in succ.items():
        for v in vs:
            pred[v].append(u)
    d = {goal: 0}
    q = deque([goal])
    while q:
        u = q.popleft()
        for p in pred[u]:
            if p not in d:
                d[p] = d[u] + 1
                q.append(p)
    n = len(succ)
    for u, vs in succ.items():
        for v in vs:
            assert d.get(u, n) <= 1 + d.get(v, n)
    return lambda s: d.get(s, n)


def grid(w, h, blocked):
    succ = {}
    for y in range(h):
        for x in range(w):
            succ[(x, y)] = {}
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (x + dx, y + dy)
                if 0 <= nb[0] < w and 0 <= nb[1] < h:
                    succ[(x, y)][nb] = INF if ((x, y) in blocked or nb in blocked) else 1
    return succ


class Checks(unittest.TestCase):
    def check_call(self, lpa, g_old, first):
        dist = dijkstra(lpa.succ, lpa.start)
        gs = lambda s: dist.get(s, INF)
        cost = lpa.g[lpa.goal]
        self.assertEqual(cost, gs(lpa.goal))
        path = lpa.path()
        if cost < INF:
            self.assertEqual(path[0], lpa.start)
            self.assertEqual(path[-1], lpa.goal)
            self.assertEqual(sum(lpa.succ[a][b] for a, b in zip(path, path[1:])), cost)
        else:
            self.assertIsNone(path)
        goal_key = (gs(lpa.goal), gs(lpa.goal))
        log = lpa.calls[-1]
        kinds = {}
        for s, kind, _ in log:
            self.assertNotIn(kind, kinds.setdefault(s, set()), "a vertex expanded twice in the same way")
            kinds[s].add(kind)
            # Theorem 10: a vertex whose g was already its start distance is not expanded.
            self.assertNotEqual(g_old[s], gs(s))
            # Theorem 11.
            star = (gs(s) + lpa.h(s), gs(s))
            old = (g_old[s] + lpa.h(s), g_old[s])
            self.assertTrue(star <= goal_key or old <= goal_key)
        for s, kind, key in log:
            if kind == "over":  # Theorem 6 and Theorem 8
                self.assertEqual(key, (gs(s) + lpa.h(s), gs(s)))
                self.assertLessEqual(key, goal_key)
        keys = [k for _, _, k in log]
        self.assertEqual(keys, sorted(keys))  # Theorem 1
        if first:  # every vertex with a smaller key than the goal is expanded
            expanded = {s for s, _, _ in log}
            for s in lpa.succ:
                if gs(s) < INF and (gs(s) + lpa.h(s), gs(s)) < goal_key:
                    self.assertIn(s, expanded)

    def run_rounds(self, succ, start, goal, h, rng, rounds, changes, costs):
        lpa = LPAStar(succ, start, goal, h)
        g_old = dict(lpa.g)
        lpa.compute_shortest_path()
        self.check_call(lpa, g_old, first=True)
        edges = [(u, v) for u, vs in succ.items() for v in vs]
        for _ in range(rounds):
            for _ in range(changes):
                u, v = rng.choice(edges)
                lpa.set_cost(u, v, rng.choice(costs))
            g_old = dict(lpa.g)
            lpa.compute_shortest_path()
            self.check_call(lpa, g_old, first=False)
        return lpa


class RandomGraphs(Checks):
    def test_against_dijkstra_with_heuristic(self):
        rng = random.Random(20)
        for _ in range(25):
            succ = random_digraph(rng, 30, 0.12)
            goal = 29
            h = hop_heuristic(succ, goal)
            self.run_rounds(succ, 0, goal, h, rng, 15, 4, [1, 2, 3, 5, 8, 9, INF])

    def test_against_dijkstra_without_heuristic(self):
        rng = random.Random(21)
        for _ in range(15):
            succ = random_digraph(rng, 25, 0.15)
            self.run_rounds(succ, 0, 24, lambda s: 0, rng, 15, 3, [1, 4, 7, INF])

    def test_rejects_bad_costs(self):
        with self.assertRaises(ValueError):
            LPAStar({0: {1: 0}, 1: {}}, 0, 1, lambda s: 0)
        lpa = LPAStar({0: {1: 1}, 1: {}}, 0, 1, lambda s: 0)
        with self.assertRaises(ValueError):
            lpa.set_cost(0, 1, -2)


class Grids(Checks):
    def test_grid_changes(self):
        rng = random.Random(30)
        for _ in range(4):
            w = h = 14
            start, goal = (0, 0), (w - 1, h - 1)
            blocked = {(x, y) for y in range(h) for x in range(w) if rng.random() < 0.25} - {start, goal}
            succ = grid(w, h, blocked)
            man = lambda c, goal=goal: abs(c[0] - goal[0]) + abs(c[1] - goal[1])
            lpa = LPAStar(succ, start, goal, man)
            lpa.compute_shortest_path()
            self.check_call(lpa, {s: INF for s in succ}, first=True)
            cells = [c for c in succ if c not in (start, goal)]
            for _ in range(20):
                for _ in range(3):
                    cell = rng.choice(cells)
                    blocked ^= {cell}
                    for nb in succ[cell]:
                        c = INF if (cell in blocked or nb in blocked) else 1
                        lpa.set_cost(cell, nb, c)
                        lpa.set_cost(nb, cell, c)
                g_old = dict(lpa.g)
                lpa.compute_shortest_path()
                self.check_call(lpa, g_old, first=False)

    def test_page_example(self):
        edges = {("S", "A"): 1, ("S", "B"): 2, ("A", "C"): 1, ("B", "C"): 2, ("C", "G"): 2, ("B", "D"): 3, ("D", "G"): 2, ("A", "D"): 4}
        succ = {v: {} for e in edges for v in e}
        for (u, v), c in edges.items():
            succ[u][v] = c
        hv = {"S": 3, "A": 2, "B": 2, "C": 2, "D": 2, "G": 0}
        lpa = LPAStar(succ, "S", "G", hv.get)
        self.assertEqual(lpa.compute_shortest_path(), 4)
        self.assertEqual([s for s, _, _ in lpa.calls[-1]], ["S", "A", "B", "C", "G"])
        self.assertEqual(lpa.path(), ["S", "A", "C", "G"])
        lpa.set_cost("A", "C", 5)
        self.assertEqual(lpa.compute_shortest_path(), 6)
        self.assertEqual([(s, k) for s, k, _ in lpa.calls[-1]], [("C", "under"), ("G", "under"), ("C", "over"), ("G", "over")])
        self.assertEqual(lpa.path(), ["S", "B", "C", "G"])
        self.assertEqual(fresh_a_star(lpa.succ, "S", "G", hv.get), (6, 5))
        runs = list(lifelong_planning_a_star(succ, "S", "G", hv.get, [[("A", "C", 5)], [("C", "G", INF)]]))
        self.assertEqual(runs, [(4, ["S", "A", "C", "G"], 5), (6, ["S", "B", "C", "G"], 4), (7, ["S", "A", "D", "G"], 3)])

    def test_measured_experiment(self):
        """The 40 by 40 experiment of the page: counts, not a guarantee."""
        results = []
        for seed in (1, 2, 3):
            rng = random.Random(seed)
            w = h = 40
            cells = [(x, y) for y in range(h) for x in range(w)]
            start, goal = (0, 0), (w - 1, h - 1)
            blocked = {c for c in cells if rng.random() < 0.25 and c not in (start, goal)}
            succ = grid(w, h, blocked)
            man = lambda c, goal=goal: abs(c[0] - goal[0]) + abs(c[1] - goal[1])
            lpa = LPAStar(succ, start, goal, man)
            lpa.compute_shortest_path()
            first = (lpa.expansions, fresh_a_star(lpa.succ, start, goal, man)[1])
            inc = scratch = worse = 0
            for _ in range(30):
                for _ in range(5):
                    cell = rng.choice([q for q in cells if q not in (start, goal)])
                    blocked ^= {cell}
                    for nb in succ[cell]:
                        c = INF if (cell in blocked or nb in blocked) else 1
                        if lpa.succ[cell][nb] != c:
                            lpa.set_cost(cell, nb, c)
                        if lpa.succ[nb][cell] != c:
                            lpa.set_cost(nb, cell, c)
                cost = lpa.compute_shortest_path()
                ca, ea = fresh_a_star(lpa.succ, start, goal, man)
                self.assertEqual(cost, ca)
                inc += lpa.expansions
                scratch += ea
                worse += lpa.expansions > ea
            results.append((first, inc, scratch, worse))
        self.assertEqual(results, [((660, 660), 316, 16436, 0), ((419, 419), 1432, 11171, 1), ((796, 796), 400, 20504, 0)])


if __name__ == "__main__":
    unittest.main()
