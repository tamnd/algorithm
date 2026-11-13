# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winning-losing-states/. The authors are listed in prov/RX8R4R.jsonl.

import random
import unittest
from functools import lru_cache

from winning_losing_states import DRAW, LOSS, WIN, label_positions, reachable, subtraction_moves


def recursive_label(n, s):
    """Direct recursive solve of a subtraction game: True when the mover wins."""

    @lru_cache(maxsize=None)
    def wins(m):
        return any(not wins(m - k) for k in s if k <= m)

    return wins(n)


def bounded_game_labels(graph):
    """Independent oracle for graphs with cycles: p is W if the mover can force
    a win within h plies, L if the mover loses within h plies whatever he does,
    for h = 2V + 1; otherwise D. In a finite graph a forced result, if any,
    comes within V moves, so this bound is enough."""
    v = len(graph)
    h = 2 * v + 1
    win = {p: False for p in graph}  # forced win within k plies
    lose = {p: not graph[p] for p in graph}  # forced loss within k plies
    for _ in range(h):
        win = {p: win[p] or any(lose[c] for c in graph[p]) for p in graph}
        lose = {p: lose[p] or (bool(graph[p]) and all(win[c] for c in graph[p])) for p in graph}
    return {p: WIN if win[p] else LOSS if lose[p] else DRAW for p in graph}


def random_graph(rng, n, max_out):
    return {p: [rng.randrange(n) for _ in range(rng.randint(0, max_out))] for p in range(n)}


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def ttt_winner(b):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def ttt_moves(b):
    if ttt_winner(b) or "." not in b:
        return []
    p = "X" if b.count("X") == b.count("O") else "O"
    return [b[:i] + p + b[i + 1 :] for i in range(9) if b[i] == "."]


def ttt_terminal(b):
    # The player to move at a finished board has lost if there is a line, else it is a draw.
    return LOSS if ttt_winner(b) else DRAW


@lru_cache(maxsize=None)
def ttt_negamax(b):
    kids = ttt_moves(b)
    if not kids:
        return -1 if ttt_winner(b) else 0
    return max(-ttt_negamax(c) for c in kids)


class TestSubtractionGames(unittest.TestCase):
    def test_take_1_2_3(self):
        n = 200
        lab = label_positions(range(n + 1), subtraction_moves((1, 2, 3)))
        for m in range(n + 1):
            self.assertEqual(lab[m] == LOSS, m % 4 == 0)
            self.assertEqual(lab[m] == WIN, recursive_label(m, (1, 2, 3)))
        self.assertNotIn(DRAW, lab.values())

    def test_take_1_3_4(self):
        n = 300
        lab = label_positions(range(n + 1), subtraction_moves((1, 3, 4)))
        for m in range(n + 1):
            self.assertEqual(lab[m] == LOSS, m % 7 in (0, 2))
            self.assertEqual(lab[m] == WIN, recursive_label(m, (1, 3, 4)))

    def test_random_subtraction_sets(self):
        rng = random.Random(2024)
        for _ in range(40):
            s = tuple(sorted(rng.sample(range(1, 9), rng.randint(1, 4))))
            lab = label_positions(range(120), subtraction_moves(s))
            for m in range(120):
                self.assertEqual(lab[m] == WIN, recursive_label(m, s), (s, m))


class TestTicTacToe(unittest.TestCase):
    def test_matches_recursive_negamax(self):
        positions = reachable("." * 9, ttt_moves)
        lab = label_positions(positions, ttt_moves, ttt_terminal)
        expected = {1: WIN, 0: DRAW, -1: LOSS}
        for b in positions:
            self.assertEqual(lab[b], expected[ttt_negamax(b)])
        self.assertEqual(lab["." * 9], DRAW)
        counts = {x: list(lab.values()).count(x) for x in (WIN, LOSS, DRAW)}
        self.assertEqual(sum(counts.values()), 5478)


class TestCyclicGraphs(unittest.TestCase):
    def test_random_graphs_against_bounded_game(self):
        rng = random.Random(77)
        for trial in range(300):
            n = rng.randint(1, 14)
            g = random_graph(rng, n, 3)
            lab = label_positions(g.keys(), lambda p: g[p])
            self.assertEqual(lab, bounded_game_labels(g), (trial, g))

    def test_page_example(self):
        g = {"t": [], "a": ["t", "b"], "b": ["a", "c"], "c": ["b", "d"], "d": ["c"], "e": ["a"], "f": ["e", "c"]}
        lab = label_positions(g.keys(), lambda p: g[p])
        self.assertEqual(lab, {"t": LOSS, "a": WIN, "e": LOSS, "f": WIN, "b": DRAW, "c": DRAW, "d": DRAW})
        self.assertEqual(lab, bounded_game_labels(g))

    def test_tictactoe_label_counts(self):
        positions = reachable("." * 9, ttt_moves)
        lab = label_positions(positions, ttt_moves, ttt_terminal)
        self.assertEqual(sorted(lab.values()).count(WIN), 2836)
        self.assertEqual(sorted(lab.values()).count(LOSS), 1574)
        self.assertEqual(sorted(lab.values()).count(DRAW), 1068)

    def test_two_cycle_is_a_draw(self):
        g = {"a": ["b"], "b": ["a"]}
        self.assertEqual(label_positions(g.keys(), lambda p: g[p]), {"a": DRAW, "b": DRAW})

    def test_escape_from_a_cycle(self):
        # From a the mover can go to the dead end t, where the opponent cannot move.
        g = {"a": ["b", "t"], "b": ["a"], "t": []}
        self.assertEqual(label_positions(g.keys(), lambda p: g[p]), {"a": WIN, "b": LOSS, "t": LOSS})

    def test_multi_edges_count_twice(self):
        # p has two moves, both to the same won position w: p loses only after both are seen.
        g = {"p": ["w", "w"], "w": ["t"], "t": []}
        self.assertEqual(label_positions(g.keys(), lambda x: g[x])["p"], LOSS)


if __name__ == "__main__":
    unittest.main()
