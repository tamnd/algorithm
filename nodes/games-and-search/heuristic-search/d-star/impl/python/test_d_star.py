# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-star/. The authors are listed in prov/X5ZAVD.jsonl.

import heapq
import itertools
import random
import unittest

from d_star import CLOSED, INF, DStar, d_star

MOVES8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


def grid8(w, h, blocked):
    """8-connected grid, every move costs 1, corner cutting allowed, blocked cells cost inf."""
    succ = {}
    for y in range(h):
        for x in range(w):
            succ[(x, y)] = {}
            for dx, dy in MOVES8:
                nb = (x + dx, y + dy)
                if 0 <= nb[0] < w and 0 <= nb[1] < h:
                    succ[(x, y)][nb] = INF if ((x, y) in blocked or nb in blocked) else 1
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


def backward_dijkstra_count(succ, robot, goal):
    """Pops of Dijkstra from the goal until the robot is popped: the work of planning from scratch."""
    pred = {u: {} for u in succ}
    for u, vs in succ.items():
        for v, c in vs.items():
            pred[v][u] = c
    d, done, cnt, pops = {goal: 0}, set(), itertools.count(), 0
    pq = [(0, next(cnt), goal)]
    while pq:
        du, _, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        pops += 1
        if u == robot:
            break
        for p, c in pred[u].items():
            if du + c < d.get(p, INF):
                d[p] = du + c
                heapq.heappush(pq, (du + c, next(cnt), p))
    return pops


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
    def check_robot(self, d, robot):
        """h(robot) is the distance on the map, and the back pointers give a path of that cost."""
        dist = dist_to(d.succ, d.goal)
        self.assertEqual(d.h[robot], dist.get(robot, INF))
        if d.h[robot] < INF:
            p = d.path(robot)
            self.assertEqual(sum(d.succ[a][b] for a, b in zip(p, p[1:])), d.h[robot])


class Navigation(Checked):
    def run_robot(self, rng, w, h, density, radius):
        start, goal, blocked = random_world(rng, w, h, density)
        sense = make_sensor(blocked, radius)
        believed = grid8(w, h, set())
        for u, v, c in sense(start, believed):
            believed[u][v] = c
        d = DStar(believed, goal)
        robot = start
        d.plan_first(robot)
        self.check_robot(d, robot)
        walk = [robot]
        while robot != goal and d.h[robot] < INF:
            robot = d.b[robot]
            walk.append(robot)
            changes = sense(robot, d.succ)
            for u, v, c in changes:
                d.modify_cost(u, v, c)
            d.replan(robot)
            self.check_robot(d, robot)
        true_map = grid8(w, h, blocked)
        self.assertEqual(robot == goal, dist_to(true_map, goal).get(start, INF) < INF)
        for a, b in zip(walk, walk[1:]):
            self.assertLess(true_map[a][b], INF)  # the robot never enters a blocked cell
        return walk

    def test_unknown_terrain(self):
        rng = random.Random(50)
        for trial in range(15):
            self.run_robot(rng, 12, 12, 0.3, 1 + trial % 3)

    def test_driver_function(self):
        rng = random.Random(51)
        for _ in range(30):
            start, goal, blocked = random_world(rng, 10, 10, 0.35)
            walk, d = d_star(grid8(10, 10, set()), start, goal, make_sensor(blocked, 1))
            true_dist = dist_to(grid8(10, 10, blocked), goal)
            if start in true_dist:
                self.assertEqual((walk[0], walk[-1]), (start, goal))
                self.assertGreaterEqual(len(walk) - 1, true_dist[start])
            else:
                self.assertIsNone(walk)

    def test_first_plan_is_dijkstra(self):
        """The first phase only lowers: every closed state has its exact distance."""
        rng = random.Random(52)
        for _ in range(20):
            start, goal, blocked = random_world(rng, 15, 15, 0.25)
            succ = grid8(15, 15, blocked)
            d = DStar(succ, goal)
            d.plan_first(start)
            dist = dist_to(succ, goal)
            for s, tag in d.t.items():
                if tag == CLOSED:
                    self.assertEqual(d.h[s], dist.get(s, INF))
            self.check_robot(d, start)


class PageExample(Checked):
    def test_five_by_three(self):
        succ = {}
        for y in range(3):
            for x in range(5):
                succ[(x, y)] = {}
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < 5 and 0 <= y + dy < 3:
                        succ[(x, y)][(x + dx, y + dy)] = 1
        d = DStar(succ, (4, 1))
        self.assertEqual(d.plan_first((0, 1)), 4)
        self.assertEqual(d.processed, 12)
        robot = d.b[(0, 1)]
        self.assertEqual(robot, (1, 1))
        for nb in list(succ[(2, 1)]):
            d.modify_cost((2, 1), nb, INF)
            d.modify_cost(nb, (2, 1), INF)
        self.assertEqual(d.replan(robot), 5)
        self.assertEqual(d.processed, 20)
        self.assertEqual(d.path(robot), [(1, 1), (1, 2), (2, 2), (3, 2), (3, 1), (4, 1)])
        self.check_robot(d, robot)


class CostChanges(Checked):
    def random_digraph(self, rng, n, p):
        succ = {u: {} for u in range(n)}
        for u in range(n):
            for v in range(n):
                if u != v and rng.random() < p:
                    succ[u][v] = rng.randint(1, 9)
        return succ

    def test_random_digraphs(self):
        """Costs go up and down, arcs are blocked and come back, and arcs are added."""
        rng = random.Random(53)
        for _ in range(60):
            n = rng.randint(2, 25)
            succ = self.random_digraph(rng, n, rng.choice([0.1, 0.2, 0.4]))
            goal = rng.randrange(n)
            d = DStar(succ, goal)
            robot = rng.randrange(n)
            d.plan_first(robot)
            self.check_robot(d, robot)
            for _ in range(15):
                for _ in range(rng.randint(1, 5)):
                    u, v = rng.sample(range(n), 2)
                    d.modify_cost(u, v, rng.choice([1, 2, 3, 5, 8, INF]))
                if rng.random() < 0.5 and d.h[robot] < INF and robot != goal:
                    robot = d.b[robot]  # the robot moves along its path
                d.replan(robot)
                self.check_robot(d, robot)

    def test_rejects_bad_costs(self):
        with self.assertRaises(ValueError):
            DStar({0: {1: 0}, 1: {}}, 1)
        d = DStar({0: {1: 1}, 1: {}}, 1)
        with self.assertRaises(ValueError):
            d.modify_cost(0, 1, -2)


def experiment(seed, w=50, h=50, density=0.3, radius=1):
    """D* against Dijkstra from scratch at the same replanning points."""
    rng = random.Random(seed)
    start, goal, blocked = random_world(rng, w, h, density)
    sense = make_sensor(blocked, radius)
    believed = grid8(w, h, set())
    for u, v, c in sense(start, believed):
        believed[u][v] = c
    d = DStar(believed, goal)
    robot = start
    d.plan_first(robot)
    first = d.processed
    replans, moves, scratch = 0, 0, 0
    while robot != goal and d.h[robot] < INF:
        robot = d.b[robot]
        moves += 1
        changes = sense(robot, d.succ)
        if changes:
            replans += 1
            for u, v, c in changes:
                d.modify_cost(u, v, c)
            d.replan(robot)
            scratch += backward_dijkstra_count(d.succ, robot, goal)
    return first, replans, d.processed - first, scratch, moves, robot == goal


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual([experiment(s) for s in (1, 2)], EXPECTED)


EXPECTED = [(2500, 46, 203, 34986, 58, True), (2500, 47, 246, 37743, 63, True)]

if __name__ == "__main__":
    unittest.main()
