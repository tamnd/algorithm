# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-ordering/. The authors are listed in prov/4VF43D.jsonl.

import random
import unittest
from fractions import Fraction

from move_ordering import INF, ordered_alpha_beta, shallow_search_score, static_score

# ---------------------------------------------------------------- trees as nested lists
# A leaf is a number, the value for the side to move there (negamax form).


def tree_moves(t):
    return [] if not isinstance(t, list) else list(enumerate(t))


def tree_eval(t):
    return 0 if isinstance(t, list) else t  # an inner node cut off by the depth counts as 0


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


def uniform_distinct(rng, b, d):
    vals = list(range(b**d))
    rng.shuffle(vals)
    it = iter(vals)

    def build(k):
        return next(it) if k == 0 else [build(k - 1) for _ in range(b)]

    return build(d)


# ---------------------------------------------------------------- tic-tac-toe

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


def ttt_score(b, mv, c):
    """Win first, then block a win of the opponent, then the center, the corners and the edges."""
    if winner(c):
        return 100
    other = "O" if to_move(b) == "X" else "X"
    if winner(b[:mv] + other + b[mv + 1 :]):
        return 50
    return {4: 4, 0: 3, 2: 3, 6: 3, 8: 3}.get(mv, 2)


# ---------------------------------------------------------------- an incremental game
# Each move adds w[m] + noise to the score of the side that makes it. The
# static value of a position is the score difference so far, for the side to
# move, so it is a good but not perfect guide to the value of the search.


def incremental_game(seed, b, d):
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


class TestMoveOrdering(unittest.TestCase):
    def test_value_does_not_depend_on_order(self):
        rng = random.Random(11)
        for trial in range(300):
            t = random_tree(rng, rng.randint(1, 5), trial % 2 == 1, trial % 3 != 0)
            want = negamax(t, 99, tree_moves, tree_eval)
            noise = random.Random(trial)
            scores = [
                None,
                static_score(tree_eval),
                shallow_search_score(1, tree_moves, tree_eval),
                shallow_search_score(99, tree_moves, tree_eval),
                lambda p, m, c: noise.random(),
            ]
            for sc in scores:
                self.assertEqual(ordered_alpha_beta(t, 99, -INF, INF, tree_moves, tree_eval, sc), want)

    def test_perfect_order_reaches_the_knuth_moore_count(self):
        rng = random.Random(4)
        for b in (2, 3, 4):
            for d in range(1, 6):
                t = uniform_distinct(rng, b, d)
                leaves = [0]
                perfect = shallow_search_score(d, tree_moves, tree_eval)
                ordered_alpha_beta(t, d, -INF, INF, tree_moves, tree_eval, perfect, leaves=leaves)
                self.assertEqual(leaves[0], b ** ((d + 1) // 2) + b ** (d // 2) - 1)

    def test_tictactoe_fewer_nodes_on_average(self):
        plain = ordered = 0
        for seed in range(10):
            order = list(range(9))
            random.Random(seed).shuffle(order)
            moves = ttt_moves_in(order)
            c0, c1 = [0], [0]
            self.assertEqual(ordered_alpha_beta("." * 9, 9, -INF, INF, moves, ttt_eval, None, c0), 0)
            self.assertEqual(ordered_alpha_beta("." * 9, 9, -INF, INF, moves, ttt_eval, ttt_score, c1), 0)
            plain += c0[0]
            ordered += c1[0]
        self.assertLessEqual(ordered, plain)
        self.assertEqual((plain, ordered), (194578, 20968))

    def test_incremental_game_fewer_nodes_on_average(self):
        plain = ordered = 0
        for seed in range(20):
            moves, ev = incremental_game(seed, 4, 6)
            root = ((), 0)
            want = negamax(root, 6, moves, ev)
            c0, c1 = [0], [0]
            self.assertEqual(ordered_alpha_beta(root, 6, -INF, INF, moves, ev, None, c0), want)
            self.assertEqual(ordered_alpha_beta(root, 6, -INF, INF, moves, ev, static_score(ev), c1), want)
            plain += c0[0]
            ordered += c1[0]
        self.assertLessEqual(ordered, plain)
        self.assertEqual((plain, ordered), (27496, 6932))


if __name__ == "__main__":
    unittest.main()
