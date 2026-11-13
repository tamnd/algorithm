# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pattern-database/. The authors are listed in prov/KA46D3.jsonl.

import heapq
import random
import unittest
from collections import deque

from pattern_database import (
    PatternDatabaseHeuristic,
    abstract,
    build_pdb,
    goal_board,
    lookup,
    puzzle_moves,
    table_size,
)


def bfs_from_goal(rows, cols):
    goal = goal_board(rows, cols)
    dist = {goal: 0}
    q = deque([goal])
    while q:
        u = q.popleft()
        for v, _ in puzzle_moves(u, rows, cols):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def manhattan(board, tiles, cols):
    goal_sq = {t: t - 1 for t in tiles}
    total = 0
    for i, v in enumerate(board):
        if v in goal_sq:
            j = goal_sq[v]
            total += abs(i // cols - j // cols) + abs(i % cols - j % cols)
    return total


def projected_dijkstra(boards, rows, cols, pattern, additive):
    """Brute force: project every real move into the abstract space, then run Dijkstra.

    The edge from the image of b to the image of b' costs 1 when the moved tile
    is in the pattern or all moves count, and 0 otherwise.
    """
    adj = {}
    for b in boards:
        u = abstract(b, pattern)
        for nb, tile in puzzle_moves(b, rows, cols):
            c = 1 if (tile in pattern or not additive) else 0
            adj.setdefault(u, set()).add((abstract(nb, pattern), c))
    src = abstract(goal_board(rows, cols), pattern)
    dist = {src: 0}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, c in adj.get(u, ()):
            if d + c < dist.get(v, d + c + 1):
                dist[v] = d + c
                heapq.heappush(pq, (d + c, v))
    return dist


class BuildMatchesBruteForce(unittest.TestCase):
    def test_2x3_all_patterns_of_two_tiles(self):
        boards = list(bfs_from_goal(2, 3))
        for pattern in ((1, 2), (1, 5), (3, 4), (2, 5)):
            for additive in (False, True):
                table = build_pdb(pattern, 2, 3, additive)
                brute = projected_dijkstra(boards, 2, 3, pattern, additive)
                self.assertEqual(table, brute, (pattern, additive))
                self.assertEqual(len(table), table_size(6, 2, with_blank=True))

    def test_3x3_pattern_of_three_tiles(self):
        boards = list(bfs_from_goal(3, 3))
        for additive in (False, True):
            table = build_pdb((2, 4, 7), 3, 3, additive)
            brute = projected_dijkstra(boards, 3, 3, (2, 4, 7), additive)
            self.assertEqual(table, brute)
            self.assertEqual(len(table), table_size(9, 3, with_blank=True))

    def test_blank_free_table_is_minimum_over_blank_squares(self):
        full = build_pdb((1, 2, 3, 4), 3, 3, additive=True)
        small = build_pdb((1, 2, 3, 4), 3, 3, additive=True, blank_free=True)
        self.assertEqual(len(small), table_size(9, 4, with_blank=False))
        for key, d in full.items():
            self.assertLessEqual(small[key[:-1]], d)


class EightPuzzleHeuristics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dist = bfs_from_goal(3, 3)
        a, b = (1, 2, 3, 4), (5, 6, 7, 8)
        cls.single = PatternDatabaseHeuristic(3, 3, [a], additive=False)
        cls.maximum = PatternDatabaseHeuristic(3, 3, [a, b], additive=False)
        cls.additive = PatternDatabaseHeuristic(3, 3, [a, b], additive=True)
        cls.blank_free = PatternDatabaseHeuristic(3, 3, [a, b], additive=True, blank_free=True)
        rng = random.Random(5)
        cls.sample = rng.sample(sorted(cls.dist), 12000)

    def test_admissible_on_every_state(self):
        for h in (self.single, self.maximum, self.additive, self.blank_free):
            for board, d in self.dist.items():
                self.assertLessEqual(h(board), d, board)
            self.assertEqual(h(goal_board(3, 3)), 0)

    def test_consistent_on_sampled_states(self):
        for h in (self.single, self.maximum, self.additive):
            for board in self.sample:
                hb = h(board)
                for nb, _ in puzzle_moves(board, 3, 3):
                    self.assertLessEqual(hb, 1 + h(nb))

    def test_blank_free_additive_table_is_not_consistent(self):
        bad = 0
        for board in self.sample:
            hb = self.blank_free(board)
            bad += sum(1 for nb, _ in puzzle_moves(board, 3, 3) if hb > 1 + self.blank_free(nb))
        self.assertGreater(bad, 0)

    def test_additive_dominates_manhattan(self):
        for board in self.sample:
            self.assertGreaterEqual(self.additive(board), manhattan(board, range(1, 9), 3))
            self.assertGreaterEqual(self.blank_free(board), manhattan(board, range(1, 9), 3))

    def test_page_example(self):
        board = (5, 1, 3, 4, 0, 2, 7, 8, 6)
        self.assertEqual(manhattan(board, range(1, 9), 3), 6)
        self.assertEqual(self.single(board), 12)
        self.assertEqual(self.additive(board), 8)
        self.assertEqual(self.dist[board], 12)
        self.assertEqual(lookup(self.single.tables[0], board, (1, 2, 3, 4)), 12)

    def test_table_values(self):
        self.assertEqual([max(t.values()) for t in self.maximum.tables], [28, 26])
        self.assertEqual([max(t.values()) for t in self.additive.tables], [15, 16])

    def test_overlapping_additive_patterns_rejected(self):
        with self.assertRaises(ValueError):
            PatternDatabaseHeuristic(2, 3, [(1, 2), (2, 3)], additive=True)

    def test_sizes(self):
        self.assertEqual(table_size(16, 7, False), 57657600)
        self.assertEqual(table_size(16, 8, False), 518918400)
        self.assertEqual(table_size(25, 6, False), 127512000)


if __name__ == "__main__":
    unittest.main()
