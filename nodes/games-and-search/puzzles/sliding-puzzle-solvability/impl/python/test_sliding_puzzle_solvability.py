# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-puzzle-solvability/. The authors are listed in prov/9Q436M.jsonl.
import math
import random
import unittest
from itertools import permutations

from sliding_puzzle_solvability import (
    bfs_distances,
    grid_adjacency,
    inversions,
    is_bipartite,
    is_solvable,
    is_solvable_standard,
    permutation_parity,
    puzzle_group_order,
    reachable,
    standard_goal,
    theta_graph,
)


def random_walk(board, w, h, steps, rng):
    adj = grid_adjacency(w, h)
    b = list(board)
    for _ in range(steps):
        z = b.index(0)
        y = rng.choice(adj[z])
        b[z], b[y] = b[y], 0
    return tuple(b)


class TestExhaustive(unittest.TestCase):
    """The rule against breadth-first search over every arrangement."""

    def check_board(self, w, h, diameter):
        goal = standard_goal(w, h)
        dist = bfs_distances(goal, grid_adjacency(w, h))
        total = math.factorial(w * h)
        self.assertEqual(len(dist), total // 2)
        self.assertEqual(max(dist.values()), diameter)
        for p in permutations(range(w * h)):
            ok = is_solvable(p, w, h)
            self.assertEqual(p in dist, ok)
            self.assertEqual(is_solvable_standard(p, w), ok)

    def test_2x2(self):
        self.check_board(2, 2, 6)

    def test_3x2_and_2x3(self):
        self.check_board(3, 2, 21)
        self.check_board(2, 3, 21)

    def test_3x3(self):
        self.check_board(3, 3, 31)

    def test_4x2_count(self):
        dist = bfs_distances(standard_goal(4, 2), grid_adjacency(4, 2))
        self.assertEqual(len(dist), math.factorial(8) // 2)
        self.assertEqual(max(dist.values()), 36)
        for b in list(dist)[::97]:
            self.assertTrue(is_solvable(b, 4, 2))


class TestFourByFour(unittest.TestCase):
    def test_random_walks_stay_solvable(self):
        rng = random.Random(1)
        goal = standard_goal(4, 4)
        for _ in range(200):
            b = random_walk(goal, 4, 4, rng.randrange(0, 300), rng)
            self.assertTrue(is_solvable(b, 4, 4))
            self.assertTrue(is_solvable_standard(b, 4))

    def test_swap_of_two_tiles_is_unsolvable(self):
        rng = random.Random(2)
        goal = standard_goal(4, 4)
        for _ in range(200):
            b = list(random_walk(goal, 4, 4, rng.randrange(0, 300), rng))
            i, j = rng.sample([k for k in range(16) if b[k] != 0], 2)
            b[i], b[j] = b[j], b[i]
            self.assertFalse(is_solvable(tuple(b), 4, 4))
            self.assertFalse(is_solvable_standard(tuple(b), 4))

    def test_sam_loyd_14_15(self):
        b = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0)
        self.assertFalse(is_solvable(b, 4, 4))

    def test_random_boards_both_forms_agree(self):
        rng = random.Random(3)
        for w, h in [(4, 4), (5, 5), (4, 3), (6, 2), (5, 4)]:
            for _ in range(300):
                b = list(range(w * h))
                rng.shuffle(b)
                self.assertEqual(is_solvable(tuple(b), w, h), is_solvable_standard(tuple(b), w))

    def test_general_goal(self):
        rng = random.Random(4)
        start = standard_goal(4, 4)
        for _ in range(100):
            a = random_walk(start, 4, 4, rng.randrange(0, 200), rng)
            b = random_walk(start, 4, 4, rng.randrange(0, 200), rng)
            self.assertTrue(is_solvable(a, 4, 4, goal=b))


class TestParity(unittest.TestCase):
    def test_cycle_parity_matches_inversions(self):
        rng = random.Random(5)
        for n in range(0, 12):
            for _ in range(50):
                s = rng.sample(range(100), n)
                self.assertEqual(permutation_parity(s), inversions(s) % 2)

    def test_rejects_one_row(self):
        with self.assertRaises(ValueError):
            is_solvable((1, 2, 0), 3, 1)


class TestWilson(unittest.TestCase):
    """Wilson's theorem on small 2-connected graphs."""

    def test_theta_zero_gives_s5(self):
        adj = theta_graph(2, 3, 3)
        self.assertEqual(len(adj), 7)
        self.assertEqual(sum(len(a) for a in adj) // 2, 8)
        self.assertFalse(is_bipartite(adj))
        self.assertEqual(puzzle_group_order(adj), 120)

    def test_bipartite_gives_alternating_group(self):
        for t in [(2, 2, 4), (1, 3, 3), (2, 2, 2)]:
            adj = theta_graph(*t)
            self.assertTrue(is_bipartite(adj))
            self.assertEqual(puzzle_group_order(adj), math.factorial(len(adj) - 1) // 2)

    def test_other_nonbipartite_gives_symmetric_group(self):
        for t in [(1, 3, 4), (1, 2, 5), (1, 2, 2)]:
            adj = theta_graph(*t)
            self.assertFalse(is_bipartite(adj))
            self.assertEqual(puzzle_group_order(adj), math.factorial(len(adj) - 1))

    def test_cycle_only_rotates(self):
        for n in range(3, 8):
            adj = [[(v - 1) % n, (v + 1) % n] for v in range(n)]
            self.assertEqual(puzzle_group_order(adj), n - 1)
            start = tuple([0] + list(range(1, n)))
            self.assertEqual(len(reachable(start, adj)), n * (n - 1))


if __name__ == "__main__":
    unittest.main()
