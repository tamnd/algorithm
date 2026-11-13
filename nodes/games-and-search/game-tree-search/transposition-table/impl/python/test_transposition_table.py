# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transposition-table/. The authors are listed in prov/25X300.jsonl.

import random
import unittest
from fractions import Fraction

from transposition_table import EXACT, INF, LOWER, TranspositionTable, search

# The game graph of the page, in minimax form. C is reached from P and from Q.
PAGE = {"R": ["Y", "T3"], "Y": ["P", "Q"], "P": ["T5", "C"], "Q": ["C", "T2"], "C": ["T4", "T1"]}
PAGE_LEAVES = {"T3": 3, "T5": 5, "T2": 2, "T4": 4, "T1": 1}  # values for MAX
PAGE_MAX = {"R", "P", "Q", "T4", "T1"}  # MAX to move here


def page_moves(p):
    return [(c, c) for c in PAGE.get(p, [])]


def page_eval(p):
    return PAGE_LEAVES[p] if p in PAGE_MAX else -PAGE_LEAVES[p]


PAGE_KEYS = {n: random.Random(n).getrandbits(64) for n in list(PAGE) + list(PAGE_LEAVES)}


def negamax(pos, depth, moves, evaluate):
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    return max(-negamax(c, depth - 1, moves, evaluate) for _, c in kids)


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
_ZRNG = random.Random(2026)
ZOBRIST = [[_ZRNG.getrandbits(64) for _ in range(2)] for i in range(9)]


def ttt_winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def ttt_to_move(b):
    return "X" if b.count("X") == b.count("O") else "O"


def ttt_moves(b):
    if ttt_winner(b) or "." not in b:
        return []
    p = ttt_to_move(b)
    return [(i, b[:i] + p + b[i + 1 :]) for i in range(9) if b[i] == "."]


def ttt_eval(b):
    w = ttt_winner(b)
    return 0 if w is None else (1 if w == ttt_to_move(b) else -1)


def ttt_key(b):
    k = 0
    for i, c in enumerate(b):
        if c != ".":
            k ^= ZOBRIST[i][c == "O"]
    return k


def plain_alpha_beta(b, alpha, beta, count):
    count[0] += 1
    kids = ttt_moves(b)
    if not kids:
        return ttt_eval(b)
    m = -INF
    for _, c in kids:
        t = -plain_alpha_beta(c, -beta, -max(m, alpha), count)
        m = max(m, t)
        if m >= beta:
            break
    return m


def nim_moves(h):
    return [((i, k), h[:i] + (h[i] - k,) + h[i + 1 :]) for i in range(len(h)) for k in range(1, h[i] + 1)]


def nim_eval(h):
    return -1  # no move left: the side to move has lost


def layered_game(rng, layers, width, frac):
    """A random game graph whose positions sit in layers; every move goes one layer down.

    Many positions have several parents, so the search meets transpositions,
    and every path to a position has the same length.
    """
    succ = {}
    for l in range(layers - 1):
        for i in range(width):
            kids = rng.sample(range(width), rng.randint(1, min(3, width)))
            succ[(l, i)] = [(l + 1, j) for j in kids]
    val = {}
    for l in range(layers):
        for i in range(width):
            v = rng.randint(-9, 9)
            val[(l, i)] = Fraction(v, rng.randint(1, 4)) if frac else v
    keys = {p: rng.getrandbits(64) for p in val}
    return (lambda p: [(c, c) for c in succ.get(p, [])]), val.__getitem__, keys.__getitem__


class TestTranspositionTable(unittest.TestCase):
    def test_page_example_flags_matter(self):
        self.assertEqual(negamax("R", 10, page_moves, page_eval), 3)
        tt = TranspositionTable(4)
        self.assertEqual(search("R", 10, -INF, INF, page_moves, page_eval, PAGE_KEYS.get, tt), 3)
        # Storing the cut-off result of C (at most 4 for MAX) as exact gives 4.
        bad = TranspositionTable(4)
        self.assertEqual(search("R", 10, -INF, INF, page_moves, page_eval, PAGE_KEYS.get, bad, use_flags=False), 4)
        self.assertEqual(bad.probe(PAGE_KEYS["C"]).value, -4)  # -4 for MIN is 4 for MAX
        # With the flags, C was first stored as a lower bound and later as its exact value.
        e = tt.probe(PAGE_KEYS["C"])
        self.assertEqual((e.flag, e.value), (EXACT, -1))

    def test_cut_result_is_stored_as_bound(self):
        tt = TranspositionTable(4)
        # Inside P, C gets the window (-inf, -5) for MIN and cuts after T4.
        # The result -4 says only that C is worth at least -4 to MIN.
        search("P", 10, -INF, INF, page_moves, page_eval, PAGE_KEYS.get, tt)
        e = tt.probe(PAGE_KEYS["C"])
        self.assertEqual((e.flag, e.value), (LOWER, -4))

    def test_tictactoe_equals_search_without_table(self):
        rng = random.Random(8)
        boards = ["." * 9]
        for _ in range(15):
            b = "." * 9
            for _ in range(rng.randint(1, 5)):
                kids = ttt_moves(b)
                if not kids:
                    break
                b = rng.choice(kids)[1]
            boards.append(b)
        for b in boards:
            want = negamax(b, 9, ttt_moves, ttt_eval)
            for k, policy in ((16, "depth"), (4, "depth"), (4, "always")):
                tt = TranspositionTable(k, policy)
                self.assertEqual(search(b, 9, -INF, INF, ttt_moves, ttt_eval, ttt_key, tt), want)

    def test_tictactoe_node_counts(self):
        c0 = [0]
        self.assertEqual(plain_alpha_beta("." * 9, -INF, INF, c0), 0)
        c1 = [0]
        tt = TranspositionTable(16)
        self.assertEqual(search("." * 9, 9, -INF, INF, ttt_moves, ttt_eval, ttt_key, tt, count=c1), 0)
        self.assertEqual(c0[0], 18297)
        self.assertEqual(c1[0], 4858)  # depends on the Zobrist seed through index collisions

    def test_nim_matches_bouton(self):
        for heaps in [(1, 2, 3), (2, 2, 1), (3, 1, 4), (1, 1, 1, 2), (2, 3, 4)]:
            tt = TranspositionTable(10)
            key = lambda h: hash(h) & ((1 << 64) - 1)  # tuples of ints hash the same in every run
            v = search(heaps, 99, -INF, INF, nim_moves, nim_eval, key, tt)
            x = 0
            for h in heaps:
                x ^= h
            self.assertEqual(v, 1 if x else -1)

    def test_random_game_graphs_depth_limited(self):
        rng = random.Random(55)
        wrong_without_flags = 0
        for trial in range(300):
            moves, ev, key = layered_game(rng, rng.randint(2, 7), rng.randint(2, 6), trial % 2 == 1)
            depth = rng.randint(1, 6)
            want = negamax((0, 0), depth, moves, ev)
            for k, policy in ((12, "depth"), (2, "depth"), (2, "always")):
                got = search((0, 0), depth, -INF, INF, moves, ev, key, TranspositionTable(k, policy))
                self.assertEqual(got, want)
            bad = search((0, 0), depth, -INF, INF, moves, ev, key, TranspositionTable(12), use_flags=False)
            wrong_without_flags += bad != want
            # Random windows: the fail-soft bounds hold with the table too.
            a = Fraction(rng.randint(-12, 12), rng.randint(1, 3))
            b = a + Fraction(rng.randint(1, 12), rng.randint(1, 3))
            r = search((0, 0), depth, a, b, moves, ev, key, TranspositionTable(12))
            if r <= a:
                self.assertLessEqual(want, r)
            elif r >= b:
                self.assertGreaterEqual(want, r)
            else:
                self.assertEqual(r, want)
        self.assertGreater(wrong_without_flags, 0)


if __name__ == "__main__":
    unittest.main()
