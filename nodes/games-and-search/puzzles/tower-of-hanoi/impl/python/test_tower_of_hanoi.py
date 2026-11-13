# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tower-of-hanoi/. The authors are listed in prov/BFC4VM.jsonl.
import random
import unittest

from tower_of_hanoi import (
    apply_moves,
    bfs,
    distance_to_tower,
    hanoi_moves,
    kth_move,
    neighbours,
    state_after,
    trailing_zeros,
)


class TestOptimalMoves(unittest.TestCase):
    def test_count_and_legality(self):
        for n in range(0, 15):
            moves = hanoi_moves(n)
            self.assertEqual(len(moves), 2 ** n - 1)
            pegs = apply_moves(n, moves)
            self.assertEqual(pegs[2], list(range(n, 0, -1)))

    def test_other_pegs(self):
        moves = hanoi_moves(6, src=1, dst=0)
        self.assertEqual(apply_moves(6, moves, src=1)[0], list(range(6, 0, -1)))

    def test_disc_is_ruler_sequence(self):
        for n in range(1, 12):
            for k, (disc, _, _) in enumerate(hanoi_moves(n), start=1):
                self.assertEqual(disc, trailing_zeros(k) + 1)

    def test_kth_move_matches(self):
        for n in range(1, 12):
            self.assertEqual([kth_move(n, k) for k in range(1, 2 ** n)], hanoi_moves(n))

    def test_kth_move_large(self):
        rng = random.Random(7)
        n = 64
        for _ in range(200):
            k = rng.randrange(1, 2 ** n)
            before = state_after(n, k - 1)
            after = state_after(n, k)
            disc, a, b = kth_move(n, k)
            self.assertEqual(before[disc - 1], a)
            self.assertEqual(after[disc - 1], b)
            self.assertEqual([i for i in range(n) if before[i] != after[i]], [disc - 1])

    def test_state_after(self):
        for n in range(1, 9):
            pegs = [0] * n
            self.assertEqual(state_after(n, 0), tuple(pegs))
            for k, (disc, _, b) in enumerate(hanoi_moves(n), start=1):
                pegs[disc - 1] = b
                self.assertEqual(state_after(n, k), tuple(pegs))

    def test_rejects_bad_k(self):
        with self.assertRaises(ValueError):
            kth_move(3, 8)


class TestAgainstSearch(unittest.TestCase):
    """Breadth-first search over all 3^n states."""

    def test_distance_and_uniqueness(self):
        for n in range(1, 9):
            dist, ways = bfs(n)
            goal = (2,) * n
            self.assertEqual(len(dist), 3 ** n)
            self.assertEqual(dist[goal], 2 ** n - 1)
            self.assertEqual(ways[goal], 1)
            self.assertEqual(max(dist.values()), 2 ** n - 1)

    def test_distance_to_tower(self):
        for n in range(1, 8):
            for t in range(3):
                dist, _ = bfs(n, src=t)
                for s, d in dist.items():
                    self.assertEqual(distance_to_tower(s, t), d)

    def test_graph_size(self):
        for n in range(1, 7):
            dist, _ = bfs(n)
            edges = sum(len(neighbours(s)) for s in dist) // 2
            self.assertEqual(edges, (3 ** (n + 1) - 3) // 2)

    def test_solution_follows_shortest_path(self):
        n = 7
        dist, _ = bfs(n)
        pegs = [0] * n
        for k, (disc, _, b) in enumerate(hanoi_moves(n), start=1):
            pegs[disc - 1] = b
            self.assertEqual(dist[tuple(pegs)], k)


if __name__ == "__main__":
    unittest.main()
