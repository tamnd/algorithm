# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-stewart-algorithm/. The authors are listed in prov/NSH7PT.jsonl.
import unittest
from math import comb

from frame_stewart_algorithm import (
    apply_moves,
    best_split,
    frame_stewart_moves,
    frame_stewart_number,
    hanoi_distances,
    optimal_by_search,
)


def triangular_formula(n):
    """S(n, 4) as a sum: the j-th increment is 2^(t-1) where T(t-1) < j <= T(t)."""
    total, j, t = 0, 0, 1
    while j < n:
        for _ in range(t):
            if j == n:
                break
            j += 1
            total += 1 << (t - 1)
        t += 1
    return total


def increments_formula(n, p):
    """S(n, p) built from increments: 2^t appears comb(t + p - 3, p - 3) times."""
    total, j, t = 0, 0, 0
    while j < n:
        for _ in range(comb(t + p - 3, p - 3)):
            if j == n:
                break
            j += 1
            total += 1 << t
        t += 1
    return total


class TestNumbers(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual([frame_stewart_number(n, 4) for n in range(11)], [0, 1, 3, 5, 9, 13, 17, 25, 33, 41, 49])
        self.assertEqual([frame_stewart_number(n, 5) for n in range(11)], [0, 1, 3, 5, 7, 11, 15, 19, 23, 27, 31])
        self.assertEqual(frame_stewart_number(64, 4), 18433)

    def test_three_pegs(self):
        for n in range(20):
            self.assertEqual(frame_stewart_number(n, 3), 2 ** n - 1)

    def test_closed_forms(self):
        for n in range(60):
            self.assertEqual(frame_stewart_number(n, 4), triangular_formula(n))
        for p in (4, 5, 6, 7):
            for n in range(40):
                self.assertEqual(frame_stewart_number(n, p), increments_formula(n, p))

    def test_rejects_two_pegs(self):
        with self.assertRaises(ValueError):
            frame_stewart_number(3, 2)


class TestMoves(unittest.TestCase):
    def test_moves_are_legal_and_counted(self):
        for p in (3, 4, 5, 6):
            for n in range(0, 13):
                moves = frame_stewart_moves(n, p)
                self.assertEqual(len(moves), frame_stewart_number(n, p))
                pegs = apply_moves(n, p, moves)
                self.assertEqual(pegs[p - 1], list(range(n, 0, -1)))

    def test_other_source_and_target(self):
        moves = frame_stewart_moves(7, 4, src=2, dst=1)
        pegs = apply_moves(7, 4, moves, src=2)
        self.assertEqual(pegs[1], list(range(7, 0, -1)))

    def test_illegal_move_detected(self):
        with self.assertRaises(ValueError):
            apply_moves(2, 3, [(2, 0, 1)])

    def test_split(self):
        self.assertEqual([best_split(n, 4) for n in range(2, 11)], [1, 1, 1, 2, 3, 3, 4, 5, 6])

    def test_best_splits_four_pegs(self):
        for n in range(3, 80):
            vals = {n - k: 2 * frame_stewart_number(k, 4) + frame_stewart_number(n - k, 3) for k in range(1, n)}
            best = min(vals.values())
            ts = sorted(t for t, v in vals.items() if v == best)
            t = 1
            while (t + 1) * (t + 2) // 2 <= n:
                t += 1
            if t * (t + 1) // 2 == n:
                self.assertEqual(ts, [t])
            else:
                self.assertEqual(ts, [t, t + 1])
            nearest = int((2 * n) ** 0.5 + 0.5)
            self.assertIn(nearest, ts)


class TestAgainstSearch(unittest.TestCase):
    """Breadth-first search over all p^n states gives the true optimum."""

    def test_three_pegs_bfs(self):
        for n in range(1, 8):
            self.assertEqual(optimal_by_search(n, 3), 2 ** n - 1)

    def test_four_pegs_bfs(self):
        for n in range(1, 8):
            self.assertEqual(optimal_by_search(n, 4), frame_stewart_number(n, 4))

    def test_five_pegs_bfs(self):
        for n in range(1, 6):
            self.assertEqual(optimal_by_search(n, 5), frame_stewart_number(n, 5))

    def test_state_count(self):
        self.assertEqual(len(hanoi_distances(5, 4)), 4 ** 5)


if __name__ == "__main__":
    unittest.main()
