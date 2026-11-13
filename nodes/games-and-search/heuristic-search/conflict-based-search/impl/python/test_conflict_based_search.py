# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-based-search/. The authors are listed in prov/DBEXMS.jsonl.

import heapq
import random
import unittest

from conflict_based_search import Grid, at, conflict_based_search, cost, low_level


def joint_optimum(rows, starts, goals):
    """The least sum of costs by Dijkstra over the joint states, or None if there is no solution.

    A state is the cells of all agents and, for each agent, whether it has stopped for good at its goal.
    Stopping is free; each step costs 1 for each agent that has not stopped.
    """
    grid = Grid(rows)
    k = len(starts)
    begin = (tuple(starts), (False,) * k)
    best = {begin: 0}
    heap = [(0, begin)]
    while heap:
        d, state = heapq.heappop(heap)
        if d > best[state]:
            continue
        cells, done = state
        if all(done):
            return d
        nexts = []
        for i in range(k):
            if not done[i] and cells[i] == goals[i]:
                nexts.append((0, (cells, done[:i] + (True,) + done[i + 1 :])))
        choices = [[cells[i]] if done[i] else [cells[i], *grid.neighbours(cells[i])] for i in range(k)]

        def extend(i, chosen):
            if i == k:
                for a in range(k):
                    for b in range(a + 1, k):
                        if chosen[a] == cells[b] and chosen[b] == cells[a] and chosen[a] != cells[a]:
                            return
                nexts.append((sum(not x for x in done), (tuple(chosen), done)))
                return
            for c in choices[i]:
                if c not in chosen:
                    extend(i + 1, chosen + [c])

        extend(0, [])
        for w, nxt in nexts:
            if d + w < best.get(nxt, float("inf")):
                best[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))
    return None


def space_time_optimum(grid, start, goal, constraints):
    """The least cost of one agent under constraints, by breadth-first search over (cell, time) up to a safe horizon."""
    last = max((c[-1] for c in constraints), default=0)
    horizon = last + grid.w * grid.h + 2
    goal_block = max((c[1] for c in constraints if len(c) == 2 and c[0] == goal), default=-1)
    if (start, 0) in constraints:
        return None
    layer = {start}
    for t in range(horizon + 1):
        if goal in layer and t > goal_block:
            return t
        nxt = set()
        for v in layer:
            for w in (v, *grid.neighbours(v)):
                if (w, t + 1) not in constraints and (v, w, t + 1) not in constraints:
                    nxt.add(w)
        layer = nxt
    return None


def random_instance(rng, w, h, k, density):
    rows = ["".join("#" if rng.random() < density else "." for _ in range(w)) for _ in range(h)]
    cells = [(x, y) for y in range(h) for x in range(w) if rows[y][x] == "."]
    if len(cells) < k:
        return None
    return rows, rng.sample(cells, k), rng.sample(cells, k)


class Solutions(unittest.TestCase):
    def check_valid(self, rows, starts, goals, paths):
        grid = Grid(rows)
        k = len(starts)
        for i, p in enumerate(paths):
            self.assertEqual((p[0], p[-1]), (starts[i], goals[i]))
            for u, v in zip(p, p[1:]):
                self.assertTrue(v == u or v in set(grid.neighbours(u)))
        horizon = max(len(p) for p in paths) + 1
        for t in range(horizon):
            for i in range(k):
                for j in range(i + 1, k):
                    self.assertNotEqual(at(paths[i], t), at(paths[j], t))  # no vertex conflict
                    if t > 0:
                        swap = at(paths[i], t - 1) == at(paths[j], t) and at(paths[j], t - 1) == at(paths[i], t)
                        self.assertFalse(swap and at(paths[i], t) != at(paths[i], t - 1))  # no edge conflict

    def test_against_joint_search(self):
        rng = random.Random(21)
        solved = unsolved = 0
        for _ in range(160):
            k = rng.choice((2, 2, 3))
            w, h = rng.choice(((3, 3), (4, 2), (4, 3), (5, 2), (3, 4))) if k == 3 else rng.choice(((3, 3), (4, 4), (5, 3), (2, 6)))
            inst = random_instance(rng, w, h, k, rng.choice((0.0, 0.15, 0.3)))
            if inst is None:
                continue
            rows, starts, goals = inst
            best = joint_optimum(rows, starts, goals)
            paths, total, _ = conflict_based_search(rows, starts, goals, max_nodes=None if best is not None else 300)
            if best is None:
                self.assertIsNone(paths)
                unsolved += 1
                continue
            solved += 1
            self.assertEqual(total, best)
            self.assertEqual(total, sum(map(cost, paths)))
            self.check_valid(rows, starts, goals, paths)
        self.assertGreater(solved, 100)
        self.assertGreater(unsolved, 0)

    def test_low_level_against_space_time_search(self):
        rng = random.Random(22)
        for _ in range(300):
            rows, starts, goals = random_instance(rng, 4, 4, 1, 0.2) or ([".."], [(0, 0)], [(1, 0)])
            grid = Grid(rows)
            free = [(x, y) for y in range(grid.h) for x in range(grid.w) if grid.free((x, y))]
            constraints = set()
            for _ in range(rng.randint(0, 8)):
                t = rng.randint(1, 8)
                u = rng.choice(free)
                if rng.random() < 0.5:
                    constraints.add((u, t))
                else:
                    nb = list(grid.neighbours(u))
                    if nb:
                        constraints.add((u, rng.choice(nb), t))
            path = low_level(grid, starts[0], goals[0], frozenset(constraints), grid.distances(goals[0]))
            want = space_time_optimum(grid, starts[0], goals[0], constraints)
            self.assertEqual(None if path is None else cost(path), want)
            if path is not None:
                for t in range(len(path) + 3):
                    self.assertNotIn((at(path, t), t), constraints)
                    if t > 0:
                        self.assertNotIn((at(path, t - 1), at(path, t), t), constraints)

    def test_page_example(self):
        paths, total, expanded = conflict_based_search(PAGE_ROWS, PAGE_STARTS, PAGE_GOALS)
        self.assertEqual((paths, total, expanded), (PAGE_PATHS, PAGE_TOTAL, PAGE_EXPANDED))
        self.assertEqual(joint_optimum(PAGE_ROWS, PAGE_STARTS, PAGE_GOALS), PAGE_TOTAL)

    def test_corridor_swap(self):
        rows = ["....", "#.##"]
        paths, total, _ = conflict_based_search(rows, [(0, 0), (3, 0)], [(3, 0), (0, 0)])
        self.assertEqual(total, joint_optimum(rows, [(0, 0), (3, 0)], [(3, 0), (0, 0)]))
        self.check_valid(rows, [(0, 0), (3, 0)], [(3, 0), (0, 0)], paths)
        self.assertEqual(conflict_based_search(["...."], [(0, 0), (3, 0)], [(3, 0), (0, 0)], max_nodes=200)[0], None)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            conflict_based_search(["..."], [(0, 0), (0, 0)], [(1, 0), (2, 0)])
        with self.assertRaises(ValueError):
            conflict_based_search(["#.."], [(0, 0)], [(1, 0)])


PAGE_ROWS = ["....", "#.##"]
PAGE_STARTS, PAGE_GOALS = [(0, 0), (3, 0)], [(3, 0), (0, 0)]
PAGE_PATHS = [[(0, 0), (1, 0), (1, 1), (1, 0), (2, 0), (3, 0)], [(3, 0), (2, 0), (1, 0), (0, 0)]]
PAGE_TOTAL, PAGE_EXPANDED = 8, 8


def experiment(seed, instances=30, k=6, size=8, density=0.1):
    """Totals over solved instances: the sum of costs, the sum of the shortest single-agent costs,
    the expanded tree nodes, the most for one instance, and the number of instances given up after 2000 nodes."""
    rng = random.Random(seed)
    total = lower = expanded = most = hit = 0
    done = 0
    while done < instances:
        rows, starts, goals = random_instance(rng, size, size, k, density)
        grid = Grid(rows)
        dists = [grid.distances(g) for g in goals]
        if any(s not in d for s, d in zip(starts, dists)):
            continue
        paths, c, e = conflict_based_search(rows, starts, goals, max_nodes=2000)
        if paths is None:
            hit += 1
            continue
        total += c
        lower += sum(d[s] for s, d in zip(starts, dists))
        expanded += e
        most = max(most, e)
        done += 1
    return total, lower, expanded, most, hit


class Measured(unittest.TestCase):
    def test_experiment_numbers(self):
        """The numbers of the page: measurements, not guarantees."""
        self.assertEqual(experiment(23), EXPECTED)


EXPECTED = (1019, 992, 1037, 826, 0)

if __name__ == "__main__":
    unittest.main()
