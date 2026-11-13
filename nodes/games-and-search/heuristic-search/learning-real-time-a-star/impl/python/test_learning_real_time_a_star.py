# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-real-time-a-star/. The authors are listed in prov/D7J46M.jsonl.

import heapq
import random
import unittest

from learning_real_time_a_star import INF, LRTAStar


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
    goal = (w - 1, h - 1)
    blocked = {(x, y) for y in range(h) for x in range(w) if rng.random() < density} - {goal}
    succ = grid4(w, h, blocked)
    keep = component(succ, goal)
    return {u: {v: c for v, c in vs.items() if v in keep} for u, vs in succ.items() if u in keep}, goal


def random_strong_digraph(rng, n):
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


class Watched(dict):
    """The table H, checking each update: values stay at most the distance, and go up if asked."""

    def __init__(self, test, dist, h0, monotone):
        super().__init__()
        self.test, self.dist, self.h0, self.monotone = test, dist, h0, monotone

    def __setitem__(self, s, v):
        old = self.get(s, self.h0(s))
        self.test.assertLessEqual(v, self.dist[s])  # admissible
        if self.monotone:
            self.test.assertGreaterEqual(v, old)  # does not decrease
        super().__setitem__(s, v)


def is_consistent(succ, value, goal):
    return value(goal) == 0 and all(value(u) <= c + value(v) for u, vs in succ.items() for v, c in vs.items())


class Learning(unittest.TestCase):
    def run_trials(self, succ, goal, start, h0, consistent):
        dist = dist_to(succ, goal)
        agent = LRTAStar(succ, goal, h0)
        agent.H = Watched(self, dist, h0, monotone=consistent)
        phi0 = sum(dist[s] - h0(s) for s in succ)
        walk, _ = agent.trial(start)
        self.assertEqual((walk[0], walk[-1]), (start, goal))
        first = sum(succ[a][b] for a, b in zip(walk, walk[1:]))
        self.assertLessEqual(first, h0(start) + phi0)  # the bound of one trial
        costs = [first] + agent.trials(start, max_trials=10 * phi0 + 10)
        excess = [c - dist[start] for c in costs]
        self.assertTrue(all(e >= 0 for e in excess))
        self.assertLessEqual(sum(excess), phi0)  # the bound over all trials
        self.assertEqual(costs[-1], dist[start])  # the last trial changed nothing and is optimal
        if consistent:
            self.assertTrue(is_consistent(succ, agent.value, goal))
        return costs

    def test_mazes_with_consistent_heuristics(self):
        rng = random.Random(70)
        for _ in range(25):
            succ, goal = random_maze(rng, 10, 10, 0.3)
            start = rng.choice(sorted(succ))
            for h0 in (lambda s: 0, manhattan_to(goal)):
                self.run_trials(succ, goal, start, h0, consistent=True)

    def test_digraphs_with_inconsistent_admissible_heuristics(self):
        rng = random.Random(71)
        for _ in range(150):
            n = rng.randint(2, 14)
            succ = random_strong_digraph(rng, n)
            dist = dist_to(succ, 0)
            h = {s: rng.randint(0, dist[s]) for s in succ}
            h[0] = 0
            self.run_trials(succ, 0, rng.randrange(n), h.get, consistent=is_consistent(succ, h.get, 0))

    def test_inadmissible_heuristic_still_reaches_the_goal(self):
        rng = random.Random(72)
        for _ in range(100):
            n = rng.randint(2, 14)
            succ = random_strong_digraph(rng, n)
            noise = {s: rng.randint(0, 40) for s in succ}
            agent = LRTAStar(succ, 0, noise.get)
            walk, _ = agent.trial(rng.randrange(n))
            self.assertEqual(walk[-1], 0)

    def test_page_example(self):
        blocked = {(3, 0), (3, 1)}
        succ = grid4(5, 3, blocked)
        goal = (4, 0)
        agent = LRTAStar(succ, goal, manhattan_to(goal))
        walk, _ = agent.trial((0, 0))
        self.assertEqual(walk, PAGE_WALK)
        self.assertEqual(agent.trials((0, 0)), PAGE_COSTS)

    def test_rejects_bad_costs(self):
        with self.assertRaises(ValueError):
            LRTAStar({0: {1: 0}, 1: {}}, 1, lambda s: 0)


PAGE_WALK = [(0, 0), (1, 0), (2, 0), (1, 0), (2, 0), (2, 1), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 1), (4, 0)]
PAGE_COSTS = [10, 8, 8, 8]  # the trials after the first one; the last one changes no value


def experiment(seed, mazes=30, w=20, h=20, density=0.25):
    """First-trial cost, trials to convergence and total cost on random mazes, Manhattan heuristic."""
    rng = random.Random(seed)
    first, opt, trials, total = 0, 0, 0, 0
    for _ in range(mazes):
        succ, goal = random_maze(rng, w, h, density)
        start = rng.choice(sorted(succ))
        agent = LRTAStar(succ, goal, manhattan_to(goal))
        costs = agent.trials(start)
        first += costs[0]
        opt += dist_to(succ, goal)[start]
        trials += len(costs)
        total += sum(costs)
    return first, opt, trials, total


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual(experiment(7), EXPECTED)


EXPECTED = (1310, 592, 371, 13791)

if __name__ == "__main__":
    unittest.main()
