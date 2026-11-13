# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-star-lite/. The authors are listed in prov/TCGXBA.jsonl.

import heapq
import itertools
import random
import unittest

from d_star_lite import INF, DStarLite, d_star_lite

MOVES8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def grid8(w, h, blocked, cost=None):
    """8-connected grid, every move costs 1 (or cost[(cell, nb)]), corner cutting allowed."""
    succ = {}
    for y in range(h):
        for x in range(w):
            succ[(x, y)] = {}
            for dx, dy in MOVES8:
                nb = (x + dx, y + dy)
                if 0 <= nb[0] < w and 0 <= nb[1] < h:
                    c = 1 if cost is None else cost[((x, y), nb)]
                    succ[(x, y)][nb] = INF if ((x, y) in blocked or nb in blocked) else c
    return succ


def dist_to(succ, goal):
    """Distances to goal by Dijkstra on the reversed graph."""
    pred = {u: {} for u in succ}
    for u, vs in succ.items():
        for v, c in vs.items():
            pred[v][u] = c
    d = {goal: 0}
    pq = [(0, goal)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue
        for p, c in pred[u].items():
            if du + c < d.get(p, INF):
                d[p] = du + c
                heapq.heappush(pq, (du + c, p))
    return d


def backward_a_star(succ, start, goal, h):
    """A* from the goal to the robot on the reversed graph, ties toward smaller g, the last pop counted."""
    pred = {u: {} for u in succ}
    for u, vs in succ.items():
        for v, c in vs.items():
            pred[v][u] = c
    g = {goal: 0}
    cnt = itertools.count()
    pq = [(h(start, goal), 0, next(cnt), goal)]
    closed = set()
    exp = 0
    while pq:
        _, gu, _, u = heapq.heappop(pq)
        if u in closed or gu != g[u]:
            continue
        exp += 1
        if u == start:
            return gu, exp
        closed.add(u)
        for p, c in pred[u].items():
            if c < INF and gu + c < g.get(p, INF):
                g[p] = gu + c
                heapq.heappush(pq, (g[p] + h(start, p), g[p], next(cnt), p))
    return INF, exp


def make_sensor(true_blocked, radius):
    def sense(robot, succ):
        changes = []
        for x in range(robot[0] - radius, robot[0] + radius + 1):
            for y in range(robot[1] - radius, robot[1] + radius + 1):
                cell = (x, y)
                if cell in true_blocked and cell in succ:
                    for nb in succ[cell]:
                        if succ[cell][nb] != INF:
                            changes.append((cell, nb, INF))
                        if succ[nb][cell] != INF:
                            changes.append((nb, cell, INF))
        return changes

    return sense


def random_world(rng, w, h, density):
    start, goal = (0, 0), (w - 1, h - 1)
    blocked = {(x, y) for y in range(h) for x in range(w) if rng.random() < density} - {start, goal}
    return start, goal, blocked


class Checked(unittest.TestCase):
    def check_call(self, d):
        dist = dist_to(d.succ, d.goal)
        gs = lambda s: dist.get(s, INF)
        self.assertEqual(d.g[d.start], gs(d.start))
        seen = set()
        for s, kind, key in d.calls[-1]:
            self.assertNotIn((s, kind), seen)  # at most once each way per call
            seen.add((s, kind))
            if kind == "over":
                self.assertEqual(key, (gs(s) + d.h(d.start, s) + d.km, gs(s)))
        if d.g[d.start] < INF:  # the greedy walk on g follows a shortest path of the map
            s, total = d.start, 0
            while s != d.goal:
                nxt = min(d.succ[s], key=lambda t: d.succ[s][t] + d.g[t])
                total += d.succ[s][nxt]
                self.assertEqual(d.g[nxt], gs(nxt))
                s = nxt
            self.assertEqual(total, gs(d.start))


class Navigation(Checked):
    def run_robot(self, rng, w, h, density, radius):
        start, goal, blocked = random_world(rng, w, h, density)
        sense = make_sensor(blocked, radius)
        believed = grid8(w, h, set())
        for u, v, c in sense(start, believed):
            believed[u][v] = c
        d = DStarLite(believed, start, goal, chebyshev)
        d.compute_shortest_path()
        self.check_call(d)
        s_last = start
        walk = [start]
        while d.start != goal and d.g[d.start] < INF:
            d.start = d.next_vertex()
            walk.append(d.start)
            changes = sense(d.start, d.succ)
            if changes:
                d.km += chebyshev(s_last, d.start)
                s_last = d.start
                for u, v, c in changes:
                    d.set_cost(u, v, c)
                d.compute_shortest_path()
                self.check_call(d)
        true_map = grid8(w, h, blocked)
        reachable = dist_to(true_map, goal).get(start, INF) < INF
        self.assertEqual(d.start == goal, reachable)
        for a, b in zip(walk, walk[1:]):
            self.assertLess(true_map[a][b], INF)  # the robot never enters a blocked cell
        return walk, d

    def test_unknown_terrain(self):
        rng = random.Random(40)
        for trial in range(30):
            self.run_robot(rng, 12, 12, 0.3, 1 + trial % 3)

    def test_driver_function(self):
        rng = random.Random(41)
        for _ in range(30):
            start, goal, blocked = random_world(rng, 10, 10, 0.35)
            walk, d = d_star_lite(grid8(10, 10, set()), start, goal, chebyshev, make_sensor(blocked, 1))
            true_dist = dist_to(grid8(10, 10, blocked), goal)
            if start in true_dist:
                self.assertEqual(walk[0], start)
                self.assertEqual(walk[-1], goal)
                self.assertGreaterEqual(len(walk) - 1, true_dist[start])
            else:
                self.assertIsNone(walk)

    def test_first_call_is_backward_a_star(self):
        rng = random.Random(42)
        for _ in range(20):
            start, goal, blocked = random_world(rng, 15, 15, 0.25)
            succ = grid8(15, 15, blocked)
            d = DStarLite(succ, start, goal, chebyshev)
            cost = d.compute_shortest_path()
            self.assertEqual((cost, len(d.calls[-1])), backward_a_star(succ, start, goal, chebyshev))


class CostChanges(Checked):
    def test_weighted_grid_moving_robot(self):
        """Costs go up and down, blocked edges appear and vanish, and the robot moves."""
        rng = random.Random(43)
        for _ in range(8):
            w = h = 10
            cost = {}
            for y in range(h):
                for x in range(w):
                    for dx, dy in MOVES8:
                        cost[((x, y), (x + dx, y + dy))] = rng.randint(1, 3)
            succ = grid8(w, h, set(), cost)
            d = DStarLite(succ, (0, 0), (w - 1, h - 1), chebyshev)
            d.compute_shortest_path()
            self.check_call(d)
            s_last = d.start
            edges = [(u, v) for u, vs in succ.items() for v in vs]
            steps = 0
            while d.start != d.goal and d.g[d.start] < INF and steps < 60:
                steps += 1
                d.start = d.next_vertex()
                if rng.random() < 0.6:
                    d.km += chebyshev(s_last, d.start)
                    s_last = d.start
                    for _ in range(rng.randint(1, 6)):
                        u, v = rng.choice(edges)
                        d.set_cost(u, v, rng.choice([1, 2, 3, 5, INF]))
                    d.compute_shortest_path()
                    self.check_call(d)

    def test_rejects_bad_costs(self):
        with self.assertRaises(ValueError):
            DStarLite({0: {1: 0}, 1: {}}, 0, 1, lambda a, b: 0)


def experiment(seed, w=50, h=50, density=0.3, radius=1):
    """D* Lite against A* from scratch at the same replanning points."""
    rng = random.Random(seed)
    start, goal, blocked = random_world(rng, w, h, density)
    sense = make_sensor(blocked, radius)
    believed = grid8(w, h, set())
    for u, v, c in sense(start, believed):
        believed[u][v] = c
    d = DStarLite(believed, start, goal, chebyshev)
    d.compute_shortest_path()
    first = len(d.calls[-1])
    s_last, moves, a_total, lite_total = start, 0, 0, 0
    while d.start != goal and d.g[d.start] < INF:
        d.start = d.next_vertex()
        moves += 1
        changes = sense(d.start, d.succ)
        if changes:
            d.km += chebyshev(s_last, d.start)
            s_last = d.start
            for u, v, c in changes:
                d.set_cost(u, v, c)
            d.compute_shortest_path()
            lite_total += len(d.calls[-1])
            a_total += backward_a_star(d.succ, d.start, goal, chebyshev)[1]
    return first, len(d.calls) - 1, lite_total, a_total, moves, d.start == goal


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual([experiment(s) for s in (1, 2, 3)], EXPECTED)


EXPECTED = [(50, 46, 233, 2352, 63, True), (50, 47, 332, 3067, 65, True), (50, 50, 249, 2635, 66, True)]

if __name__ == "__main__":
    unittest.main()
