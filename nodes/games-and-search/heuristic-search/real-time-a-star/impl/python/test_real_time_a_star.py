# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-a-star/. The authors are listed in prov/YMQYKM.jsonl.

import heapq
import random
import unittest

from real_time_a_star import INF, real_time_a_star, walk_cost


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


def grid4(w, h, blocked):
    """4-connected grid of free cells, unit costs."""
    succ = {}
    for y in range(h):
        for x in range(w):
            if (x, y) in blocked:
                continue
            succ[(x, y)] = {}
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (x + dx, y + dy)
                if 0 <= nb[0] < w and 0 <= nb[1] < h and nb not in blocked:
                    succ[(x, y)][nb] = 1
    return succ


def component(succ, s):
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        for v in succ[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def random_maze(rng, w, h, density):
    """A grid whose free cells all reach the goal: keep the component of the goal."""
    goal = (w - 1, h - 1)
    blocked = {(x, y) for y in range(h) for x in range(w) if rng.random() < density} - {goal}
    succ = grid4(w, h, blocked)
    keep = component(succ, goal)
    succ = {u: {v: c for v, c in vs.items() if v in keep} for u, vs in succ.items() if u in keep}
    return succ, goal


def random_strong_digraph(rng, n):
    """A directed graph in which every state reaches the goal 0: a random cycle plus random arcs."""
    order = list(range(n))
    rng.shuffle(order)
    succ = {u: {} for u in range(n)}
    for i in range(n):
        succ[order[i]][order[(i + 1) % n]] = rng.randint(1, 9)
    for _ in range(rng.randint(0, 3 * n)):
        u, v = rng.sample(range(n), 2)
        succ[u][v] = rng.randint(1, 9)
    return succ


def manhattan_to(goal):
    return lambda s: abs(s[0] - goal[0]) + abs(s[1] - goal[1])


class Reaches(unittest.TestCase):
    def check(self, succ, start, goal, h0):
        walk, table = real_time_a_star(succ, start, goal, h0)
        self.assertEqual((walk[0], walk[-1]), (start, goal))
        for a, b in zip(walk, walk[1:]):
            self.assertIn(b, succ[a])
        self.assertNotIn(goal, table)
        self.assertGreaterEqual(walk_cost(succ, walk), dist_to(succ, goal)[start])
        return walk, table

    def test_grids_with_several_heuristics(self):
        rng = random.Random(60)
        for _ in range(40):
            succ, goal = random_maze(rng, 12, 12, 0.3)
            dist = dist_to(succ, goal)
            start = rng.choice(sorted(succ))
            for h0 in (lambda s: 0, manhattan_to(goal), dist.get, lambda s: 3 * manhattan_to(goal)(s)):
                self.check(succ, start, goal, h0)

    def test_random_digraphs(self):
        """Directed graphs, random costs, and finite heuristics that need not be admissible."""
        rng = random.Random(61)
        for _ in range(200):
            n = rng.randint(1, 15)
            succ = random_strong_digraph(rng, n) if n > 1 else {0: {}}
            noise = {u: rng.randint(0, 30) for u in succ}
            self.check(succ, rng.randrange(n), 0, noise.get)

    def test_perfect_heuristic_on_a_tree_path(self):
        """With h0 = the true distance and no ties, every move is on a shortest path."""
        succ = {0: {1: 1, 3: 5}, 1: {0: 1, 2: 1}, 2: {1: 1, 4: 1}, 3: {0: 5, 4: 1}, 4: {2: 1, 3: 1}}
        dist = dist_to(succ, 4)
        walk, table = self.check(succ, 0, 4, dist.get)
        self.assertEqual(walk, [0, 1, 2, 4])
        self.assertEqual(table, {0: 6, 1: 7, 2: 8})  # second-best values

    def test_page_example(self):
        """The corridor example of the page."""
        succ, start, goal, h0 = page_example()
        walk, table = self.check(succ, start, goal, h0)
        self.assertEqual(walk, PAGE_WALK)
        self.assertEqual(table, PAGE_TABLE)

    def test_rejects_bad_costs(self):
        with self.assertRaises(ValueError):
            real_time_a_star({0: {1: 0}, 1: {}}, 0, 1, lambda s: 0)
        with self.assertRaises(ValueError):
            real_time_a_star({0: {1: INF}, 1: {}}, 0, 1, lambda s: 0)


def page_example():
    """A 4-connected 5 by 3 grid with a wall: the agent first walks into the dead end."""
    blocked = {(3, 0), (3, 1)}
    succ = grid4(5, 3, blocked)
    goal = (4, 0)
    return succ, (0, 0), goal, manhattan_to(goal)


PAGE_WALK = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 1), (4, 0)]
PAGE_TABLE = {(0, 0): 6, (1, 0): 5, (2, 0): 6, (2, 1): 7, (1, 1): 6, (2, 2): 6, (3, 2): 7, (4, 2): 8, (4, 1): 9}


def experiment(seed, trials=50, w=20, h=20, density=0.25):
    """Mean cost of RTA* walks over the optimal cost on random mazes, Manhattan heuristic."""
    rng = random.Random(seed)
    total_rta, total_opt = 0, 0
    for _ in range(trials):
        succ, goal = random_maze(rng, w, h, density)
        start = rng.choice(sorted(succ))
        walk, _ = real_time_a_star(succ, start, goal, manhattan_to(goal))
        total_rta += walk_cost(succ, walk)
        total_opt += dist_to(succ, goal)[start]
    return total_rta, total_opt


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual(experiment(7), EXPECTED)


EXPECTED = (1750, 1026)

if __name__ == "__main__":
    unittest.main()
