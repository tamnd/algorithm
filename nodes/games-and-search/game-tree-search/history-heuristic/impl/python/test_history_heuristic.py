# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/history-heuristic/. The authors are listed in prov/XSFAN1.jsonl.

import random
import unittest
from fractions import Fraction

from history_heuristic import INF, HistoryTable, history_alpha_beta


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


class TestHistoryHeuristic(unittest.TestCase):
    def test_value_unchanged_on_random_trees(self):
        rng = random.Random(31)
        for trial in range(300):
            t = random_tree(rng, rng.randint(1, 6), trial % 2 == 1, trial % 3 != 0)
            want = negamax(t, 99, tree_moves, tree_eval)
            for bonus in (lambda d: 1 << d, lambda d: d * d):
                self.assertEqual(history_alpha_beta(t, 99, -INF, INF, tree_moves, tree_eval, HistoryTable(bonus)), want)
            # A table filled by an earlier search, and random windows.
            h = HistoryTable()
            history_alpha_beta(random_tree(rng, 4, False, True), 99, -INF, INF, tree_moves, tree_eval, h)
            a = Fraction(rng.randint(-20, 20), rng.randint(1, 3))
            b = a + Fraction(rng.randint(1, 20), rng.randint(1, 3))
            r = history_alpha_beta(t, 99, a, b, tree_moves, tree_eval, h)
            if r <= a:
                self.assertLessEqual(want, r)
            elif r >= b:
                self.assertGreaterEqual(want, r)
            else:
                self.assertEqual(r, want)

    def test_table_order_and_age(self):
        h = HistoryTable()
        h.reward("a", 1)
        h.reward("b", 3)
        h.reward("a", 2)
        self.assertEqual(h.score, {"a": 6, "b": 8})
        self.assertEqual([m for m, _ in h.order([("a", 0), ("c", 0), ("b", 0)])], ["b", "a", "c"])
        h.age()
        self.assertEqual(h.score, {"a": 3, "b": 4})

    def test_tictactoe_fewer_nodes_on_average(self):
        plain = hist = 0
        for seed in range(10):
            order = list(range(9))
            random.Random(seed).shuffle(order)
            moves = ttt_moves_in(order)
            c0, c1 = [0], [0]
            self.assertEqual(history_alpha_beta("." * 9, 9, -INF, INF, moves, ttt_eval, None, c0), 0)
            self.assertEqual(history_alpha_beta("." * 9, 9, -INF, INF, moves, ttt_eval, HistoryTable(), c1), 0)
            plain += c0[0]
            hist += c1[0]
        self.assertLessEqual(hist, plain)
        self.assertEqual((plain, hist), (194578, 106163))

    def test_incremental_game_fewer_nodes_on_average(self):
        plain = hist = 0
        for seed in range(20):
            moves, ev = incremental_game(seed, 4, 6)
            root = ((), 0)
            want = negamax(root, 6, moves, ev)
            c0, c1 = [0], [0]
            self.assertEqual(history_alpha_beta(root, 6, -INF, INF, moves, ev, None, c0), want)
            self.assertEqual(history_alpha_beta(root, 6, -INF, INF, moves, ev, HistoryTable(), c1), want)
            plain += c0[0]
            hist += c1[0]
        self.assertLessEqual(hist, plain)
        self.assertEqual((plain, hist), (27496, 12705))


if __name__ == "__main__":
    unittest.main()
