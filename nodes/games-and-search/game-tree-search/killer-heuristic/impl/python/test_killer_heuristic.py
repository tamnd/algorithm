# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/killer-heuristic/. The authors are listed in prov/V7ZSNV.jsonl.

import random
import unittest
from fractions import Fraction

from killer_heuristic import INF, KillerTable, killer_alpha_beta


def tree_moves(t):
    return [] if not isinstance(t, list) else list(enumerate(t))


def tree_eval(t):
    return 0 if isinstance(t, list) else t


def negamax(pos, depth, moves, evaluate):
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    return max(-negamax(c, depth - 1, moves, evaluate) for _, c in kids)


def random_tree(rng, depth, frac, irregular):
    if depth == 0 or (irregular and rng.random() < 0.2):
        v = rng.randint(-20, 20)
        return Fraction(v, rng.randint(1, 6)) if frac else v
    b = rng.randint(1, 4) if irregular else 3
    return [random_tree(rng, depth - 1, frac, irregular) for _ in range(b)]


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def to_move(b):
    return "X" if b.count("X") == b.count("O") else "O"


def ttt_moves_in(order):
    rank = {sq: r for r, sq in enumerate(order)}

    def moves(b):
        if winner(b) or "." not in b:
            return []
        p = to_move(b)
        return sorted(((i, b[:i] + p + b[i + 1 :]) for i in range(9) if b[i] == "."), key=lambda mc: rank[mc[0]])

    return moves


def ttt_eval(b):
    w = winner(b)
    return 0 if w is None else (1 if w == to_move(b) else -1)


def incremental_game(seed, b, d):
    """Each move m adds w[m] plus noise to the score of the mover, so good moves are good everywhere."""
    rng = random.Random(seed)
    w = [rng.randint(-5, 5) for _ in range(b)]

    def moves(pos):
        path, s = pos
        if len(path) == d:
            return []
        out = []
        for m in range(b):
            q = path + (m,)
            gain = w[m] + random.Random(f"{seed}:{q}").randint(-4, 4)
            out.append((m, (q, -(s + gain))))
        return out

    return moves, (lambda pos: pos[1])


class TestKillerHeuristic(unittest.TestCase):
    def test_value_unchanged_on_random_trees(self):
        rng = random.Random(21)
        for trial in range(300):
            t = random_tree(rng, rng.randint(1, 6), trial % 2 == 1, trial % 3 != 0)
            want = negamax(t, 99, tree_moves, tree_eval)
            for slots in (1, 2, 3):
                got = killer_alpha_beta(t, 99, -INF, INF, tree_moves, tree_eval, KillerTable(slots))
                self.assertEqual(got, want)
            # Random windows: the fail-soft bounds of alpha-beta still hold.
            a = Fraction(rng.randint(-20, 20), rng.randint(1, 3))
            b = a + Fraction(rng.randint(1, 20), rng.randint(1, 3))
            r = killer_alpha_beta(t, 99, a, b, tree_moves, tree_eval, KillerTable(2))
            if r <= a:
                self.assertLessEqual(want, r)
            elif r >= b:
                self.assertGreaterEqual(want, r)
            else:
                self.assertEqual(r, want)

    def test_table_keeps_recent_moves(self):
        k = KillerTable(2)
        for mv in ["a", "b", "a", "c", "c"]:
            k.record(5, mv)
        self.assertEqual(k.killers(5), ["c", "a"])
        self.assertEqual(k.order(5, [("b", 1), ("a", 2), ("c", 3)]), [("c", 3), ("a", 2), ("b", 1)])
        self.assertEqual(k.order(5, [("b", 1)]), [("b", 1)])  # a killer that is not legal here is skipped

    def test_only_quiet_moves_are_recorded(self):
        moves, ev = incremental_game(3, 4, 5)
        k = KillerTable(2)
        killer_alpha_beta(((), 0), 5, -INF, INF, moves, ev, k, is_quiet=lambda pos, mv: mv != 0)
        self.assertTrue(all(0 not in ks for ks in k.table.values()))

    def test_tictactoe_fewer_nodes_on_average(self):
        plain = killer = 0
        for seed in range(10):
            order = list(range(9))
            random.Random(seed).shuffle(order)
            moves = ttt_moves_in(order)
            c0, c1 = [0], [0]
            self.assertEqual(killer_alpha_beta("." * 9, 9, -INF, INF, moves, ttt_eval, None, count=c0), 0)
            self.assertEqual(killer_alpha_beta("." * 9, 9, -INF, INF, moves, ttt_eval, KillerTable(2), count=c1), 0)
            plain += c0[0]
            killer += c1[0]
        self.assertLessEqual(killer, plain)
        self.assertEqual((plain, killer), (194578, 75093))

    def test_incremental_game_fewer_nodes_on_average(self):
        plain = killer = 0
        for seed in range(20):
            moves, ev = incremental_game(seed, 4, 6)
            root = ((), 0)
            want = negamax(root, 6, moves, ev)
            c0, c1 = [0], [0]
            self.assertEqual(killer_alpha_beta(root, 6, -INF, INF, moves, ev, None, count=c0), want)
            self.assertEqual(killer_alpha_beta(root, 6, -INF, INF, moves, ev, KillerTable(2), count=c1), want)
            plain += c0[0]
            killer += c1[0]
        self.assertLessEqual(killer, plain)
        self.assertEqual((plain, killer), (27496, 16943))


if __name__ == "__main__":
    unittest.main()
