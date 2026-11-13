# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retrograde-analysis/. The authors are listed in prov/CADFGP.jsonl.

import random
import unittest
from collections import Counter

from retrograde_analysis import KRK4, GraphGame, forward_solve, retrograde


def random_graph(rng, v):
    succ = {}
    for p in range(v):
        k = rng.choice([0, 1, 1, 2, 2, 3])
        succ[p] = [rng.randrange(v) for _ in range(k)]
    draws = [p for p in range(v) if not succ[p] and rng.random() < 0.3]
    return GraphGame(succ, draws)


def path_search(g, p, path):
    """Reference: a plain game-tree search in which a position that repeats
    on the current path scores 0 (a draw by repetition). Exponential; tiny
    graphs only."""
    if g.lost(p):
        return -1
    ms = g.moves(p)
    if not ms:
        return 0
    best = -1
    path.add(p)
    for c in ms:
        v = 0 if c in path else -path_search(g, c, path)
        best = max(best, v)
        if best == 1:
            break
    path.discard(p)
    return best


class TestRetrogradeAnalysis(unittest.TestCase):
    def test_random_graphs_with_cycles(self):
        rng = random.Random(5)
        cyclic = 0
        for _ in range(400):
            g = random_graph(rng, rng.randint(1, 14))
            self.assertEqual(retrograde(g), forward_solve(g))
            cyclic += any(p in g.moves(p) or any(p in g.moves(q) for q in g.moves(p)) for p in g.positions())
        self.assertGreater(cyclic, 200)

    def test_draw_by_repetition_on_tiny_graphs(self):
        rng = random.Random(6)
        for _ in range(300):
            g = random_graph(rng, rng.randint(1, 8))
            val, _ = retrograde(g)
            for p in g.positions():
                self.assertEqual(val[p], path_search(g, p, set()))

    def test_unmoves_inverts_moves(self):
        g = KRK4()
        ps = g.positions()
        s = set(ps)
        for p in ps:
            for q in g.moves(p):
                if q is not None:
                    self.assertIn(q, s)
                    self.assertIn(p, g.unmoves(q))
        for q in ps:
            for p in g.unmoves(q):
                self.assertIn(p, s)
                self.assertIn(q, g.moves(p))

    def test_krk4_equals_forward_solve(self):
        g = KRK4()
        val, dist = retrograde(g)
        self.assertEqual((val, dist), forward_solve(g))
        ps = g.positions()
        self.assertEqual(len(ps), 3496)
        white = [p for p in ps if p[3] == 0]
        black = [p for p in ps if p[3] == 1]
        self.assertEqual(len(white), 1312)
        self.assertTrue(all(val[p] == 1 for p in white))
        self.assertEqual(Counter(val[p] for p in black), {-1: 1572, 0: 612})
        self.assertEqual(sum(1 for p in ps if g.lost(p)), 40)
        self.assertEqual(max(dist[p] for p in white), 13)
        self.assertEqual(max(dist[p] for p in black if val[p] == -1), 14)
        self.assertEqual(sorted(Counter(dist[p] for p in white).items()),
                         [(1, 120), (3, 404), (5, 316), (7, 236), (9, 168), (11, 56), (13, 12)])
        # The longest mate of the page: White Ka1, Rd2, Black Kc3, White to move.
        # Squares are numbered 4 * (rank - 1) + file, with a = 0, so a1 = 0, d2 = 7, c3 = 10.
        p = (0, 7, 10, 0)
        self.assertEqual((val[p], dist[p]), (1, 13))
        self.assertEqual(sum(1 for q in white if dist[q] == 13), 12)
        # Follow the table: the winner takes a shortest mate, the loser a longest one.
        line = [p]
        while dist[p] > 0:
            kids = [c for c in g.moves(p) if c is not None]
            if val[p] == 1:
                p = min((c for c in kids if val[c] == -1), key=lambda c: (dist[c], c))
            else:
                p = max(kids, key=lambda c: (dist[c], c))
            line.append(p)
        self.assertEqual(len(line), 14)
        self.assertEqual(line[1], (0, 3, 10, 1))  # 1. Rd1
        self.assertEqual(line[-1], (9, 3, 11, 1))  # Kb3, Rd1, Kd3: mate
        self.assertTrue(g.lost(line[-1]))

    def test_distances_are_exact(self):
        # The winner has a move to a loss one ply shorter and none shorter;
        # every move of the loser goes to a win of at most d - 1, and one to d - 1.
        g = KRK4()
        val, dist = retrograde(g)
        for p in g.positions():
            kids = [c for c in g.moves(p) if c is not None]
            if val[p] == 1:
                self.assertEqual(min(dist[c] for c in kids if val[c] == -1), dist[p] - 1)
            elif val[p] == -1 and dist[p] > 0:
                self.assertEqual(len(kids), len(g.moves(p)))
                self.assertTrue(all(val[c] == 1 for c in kids))
                self.assertEqual(max(dist[c] for c in kids), dist[p] - 1)
            elif val[p] == 0:
                self.assertFalse(any(val[c] == -1 for c in kids))


if __name__ == "__main__":
    unittest.main()
