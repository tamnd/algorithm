# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quiescence-search/. The authors are listed in prov/F29MJX.jsonl.

import random
import unittest

from quiescence_search import INF, MaterialGame, best_move, quiesce, search


class ExplicitGame:
    """A small hand-made tree. `kids[n]` lists (child, is_capture), and
    `static[n]` is the score for the side to move at n."""

    def __init__(self, kids, static):
        self.kids, self.static = kids, static

    def evaluate(self, n):
        return self.static[n]

    def moves(self, n):
        return [c for c, _ in self.kids.get(n, [])]

    def captures(self, n):
        return [c for c, cap in self.kids.get(n, []) if cap]


# The horizon example of the page. White moves at A. QxP wins a pawn (B), but
# the black rook then takes the queen (D). The quiet move leads to C.
HORIZON = ExplicitGame(
    kids={
        "A": [("B", True), ("C", False)],
        "B": [("D", True), ("E", False)],
        "C": [("F", False)],
        "D": [("G", False)],
        "E": [("H", False)],
        "F": [("I", False)],
    },
    static={"A": 0, "B": -1, "C": 0, "D": -8, "E": 1, "F": 0, "G": 8, "H": -1, "I": 0},
)


def negamax_full(g, n):
    """Reference: exact negamax value of the whole tree below n."""
    kids = g.moves(n)
    if not kids:
        return g.evaluate(n)
    return max(-negamax_full(g, c) for c in kids)


def capture_or_stop(g, n):
    """Reference: plain negamax of the game in which the side to move may
    capture or stop, and a stop is worth the static score."""
    return max([g.evaluate(n)] + [-capture_or_stop(g, c) for c in g.captures(n)])


def depth_then_quiesce(g, n, d):
    """Reference: plain negamax to depth d, then capture_or_stop at the frontier."""
    kids = g.moves(n)
    if not kids:
        return g.evaluate(n)
    if d == 0:
        return capture_or_stop(g, n)
    return max(-depth_then_quiesce(g, c, d - 1) for c in kids)


def nodes_to(g, depth):
    out, frontier = [()], [()]
    for _ in range(depth):
        frontier = [c for n in frontier for c in g.moves(n)]
        out.extend(frontier)
    return out


class TestQuiescence(unittest.TestCase):
    def test_horizon_example(self):
        g = HORIZON
        self.assertEqual(negamax_full(g, "A"), 0)
        self.assertEqual(-negamax_full(g, "B"), -8)
        # Depth 1 without quiescence takes the pawn and scores it +1.
        self.assertEqual(best_move("A", 1, g.evaluate, g.moves, g.captures, use_quiescence=False), ("B", 1))
        # Quiescence sees the recapture and picks the quiet move.
        self.assertEqual(best_move("A", 1, g.evaluate, g.moves, g.captures, use_quiescence=True), ("C", 0))
        self.assertEqual(quiesce("B", -INF, INF, g.evaluate, g.captures), 8)

    def test_equals_capture_or_stop_game(self):
        checked = 0
        for seed in range(40):
            g = MaterialGame(seed, b=3, height=6)
            for n in nodes_to(g, 3):
                self.assertEqual(quiesce(n, -INF, INF, g.evaluate, g.captures), capture_or_stop(g, n))
                checked += 1
        self.assertEqual(checked, 1600)

    def test_fail_soft_window(self):
        rng = random.Random(7)
        for seed in range(600):
            g = MaterialGame(1000 + seed, b=3, height=5)
            q = capture_or_stop(g, ())
            a = rng.randint(-12, 12)
            b = a + rng.randint(1, 10)
            r = quiesce((), a, b, g.evaluate, g.captures)
            if q <= a:
                self.assertLessEqual(r, a)
                self.assertGreaterEqual(r, q)
            elif q >= b:
                self.assertGreaterEqual(r, b)
                self.assertLessEqual(r, q)
            else:
                self.assertEqual(r, q)

    def test_search_with_quiescence(self):
        for seed in range(500):
            g = MaterialGame(5000 + seed, b=3, height=6)
            d = seed % 4
            self.assertEqual(search((), d, -INF, INF, g.evaluate, g.moves, g.captures), depth_then_quiesce(g, (), d))

    def test_full_depth_is_exact(self):
        # When the depth limit reaches the end of the tree, the search is exact.
        for seed in range(100):
            g = MaterialGame(9000 + seed, b=3, height=4)
            for flag in (True, False):
                self.assertEqual(search((), 4, -INF, INF, g.evaluate, g.moves, g.captures, flag), negamax_full(g, ()))

    def test_measured_error(self):
        # The page states these counts: 200 trees, seeds 20000 to 20199,
        # b = 3, height 6, depth 2. The error is |search value - exact value|.
        plain = quiet = plain_wrong = quiet_wrong = 0
        cp, cq = [0], [0]
        for seed in range(200):
            g = MaterialGame(20000 + seed, b=3, height=6)
            exact = negamax_full(g, ())
            a = search((), 2, -INF, INF, g.evaluate, g.moves, g.captures, False, cp)
            b = search((), 2, -INF, INF, g.evaluate, g.moves, g.captures, True, cq)
            plain, plain_wrong = plain + abs(a - exact), plain_wrong + (a != exact)
            quiet, quiet_wrong = quiet + abs(b - exact), quiet_wrong + (b != exact)
        self.assertEqual((plain, plain_wrong, cp[0]), (347, 164, 1938))
        self.assertEqual((quiet, quiet_wrong, cq[0]), (298, 150, 3774))

    def test_node_counter(self):
        g = MaterialGame(3, b=3, height=6)
        c = [0]
        quiesce((), -INF, INF, g.evaluate, g.captures, c)
        self.assertGreaterEqual(c[0], 1)


if __name__ == "__main__":
    unittest.main()
