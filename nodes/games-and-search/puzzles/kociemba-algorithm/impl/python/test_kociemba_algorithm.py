# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kociemba-algorithm/. The authors are listed in prov/42Y3XQ.jsonl.
import random
import unittest

from kociemba_algorithm import (
    ALL_MOVES,
    MOVES,
    PHASE2_MOVES,
    SOLVED,
    apply,
    in_g1,
    inverse,
    multiply,
    phase1_sequences,
    phase2,
    solve,
    tables,
)


def ball(start, radius):
    dist = {start: 0}
    frontier = [start]
    for d in range(1, radius + 1):
        nxt = []
        for c in frontier:
            for m in ALL_MOVES:
                n = multiply(c, MOVES[m])
                if n not in dist:
                    dist[n] = d
                    nxt.append(n)
        frontier = nxt
    return dist


def optimal_distance(cube, solved_ball, radius):
    best = -1
    for x, i in ball(cube, radius).items():
        j = solved_ball.get(x)
        if j is not None and (best < 0 or i + j < best):
            best = i + j
    return best


class TestTables(unittest.TestCase):
    def test_sizes(self):
        t = tables()
        self.assertEqual((len(t.tw), len(t.fl), len(t.sl)), (2187, 2048, 495))
        self.assertEqual((len(t.cp), len(t.ep), len(t.sp)), (40320, 40320, 24))
        self.assertEqual(2187 * 2048 * 495, 2217093120)
        self.assertEqual(40320 * 40320 * 24 // 2, 19508428800)
        for table in (t.p_sl_tw, t.p_sl_fl, t.p_cp_sp, t.p_ep_sp):
            self.assertNotIn(255, table)

    def test_g1_is_closed(self):
        rnd = random.Random(1)
        for _ in range(100):
            c = apply(SOLVED, [rnd.choice(PHASE2_MOVES) for _ in range(30)])
            self.assertTrue(in_g1(c))
        self.assertFalse(in_g1(MOVES["R"]))
        self.assertFalse(in_g1(MOVES["F"]))


class TestSolve(unittest.TestCase):
    def test_first_solution(self):
        rnd = random.Random(2)
        t = tables()
        for _ in range(6):
            c = apply(SOLVED, [rnd.choice(ALL_MOVES) for _ in range(30)])
            sol = solve(c)
            self.assertEqual(apply(c, sol), SOLVED)
            self.assertLessEqual(len(sol), 30)
            d1 = next(d for d in range(13) if any(True for _ in phase1_sequences(t, c, d)))
            p = next(phase1_sequences(t, c, d1))
            self.assertTrue(in_g1(apply(c, p)))
            q = phase2(t, apply(c, p), 18)
            self.assertIsNotNone(q)
            self.assertEqual(apply(c, p + q), SOLVED)

    def test_superflip(self):
        sf = (tuple(range(8)), (0,) * 8, tuple(range(12)), (1,) * 12)
        sol = solve(sf)
        self.assertEqual(apply(sf, sol), SOLVED)
        self.assertEqual(optimal_distance(sf, ball(SOLVED, 4), 4), -1)
        self.assertGreater(len(sol), 8)

    def test_run_to_the_end_is_optimal(self):
        rnd = random.Random(3)
        half = ball(SOLVED, 4)
        for length in range(0, 9):
            seq = [rnd.choice(ALL_MOVES) for _ in range(length)]
            c = apply(SOLVED, seq)
            best = solve(c, first_only=False)
            self.assertEqual(apply(c, best), SOLVED)
            self.assertEqual(len(best), optimal_distance(c, half, 4))
            self.assertLessEqual(len(best), len(solve(c)))

    def test_inverse_scramble(self):
        seq = "R U R' U' F2 D L' B".split()
        c = apply(SOLVED, seq)
        self.assertEqual(apply(c, inverse(seq)), SOLVED)
        self.assertEqual(len(solve(c, first_only=False)), optimal_distance(c, ball(SOLVED, 4), 4))


if __name__ == "__main__":
    unittest.main()
