# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/games-on-graphs/. The authors are listed in prov/9S85XA.jsonl.

import random
import unittest

from games_on_graphs import (
    DRAW,
    LOSS,
    WIN,
    attractor,
    random_graph,
    reachability_by_depth,
    solve_token_game,
    token_game_as_reachability,
    token_game_by_depth,
)


class TestTokenGame(unittest.TestCase):
    def test_example_graph(self):
        # the example on the page
        a, b, c, d, e, f = range(6)
        edges = [(a, b), (a, e), (b, c), (c, d), (e, a), (e, f), (f, e)]
        self.assertEqual(solve_token_game(6, edges), [WIN, LOSS, WIN, LOSS, DRAW, DRAW])
        self.assertEqual(token_game_by_depth(6, edges, 1), [DRAW, DRAW, DRAW, LOSS, DRAW, DRAW])
        self.assertEqual(token_game_by_depth(6, edges, 2), [DRAW, DRAW, WIN, LOSS, DRAW, DRAW])
        self.assertEqual(token_game_by_depth(6, edges, 3), [DRAW, LOSS, WIN, LOSS, DRAW, DRAW])
        self.assertEqual(token_game_by_depth(6, edges, 4), [WIN, LOSS, WIN, LOSS, DRAW, DRAW])
        # the edge f -> d turns the draws into a win and a loss
        self.assertEqual(solve_token_game(6, edges + [(f, d)]), [WIN, LOSS, WIN, LOSS, LOSS, WIN])
        # with owners: player 0 owns a, c, e; player 1 owns b, d, f; target {d}
        owner = [0, 1, 0, 1, 0, 1]
        self.assertEqual(attractor(6, edges, owner, {d}), {a, b, c, d, e, f})
        self.assertEqual(attractor(6, edges + [(b, e)], owner, {d}), {c, d})

    def test_random_graphs_against_depth_search(self):
        rng = random.Random(4242)
        seen = {WIN: 0, LOSS: 0, DRAW: 0}
        for _ in range(400):
            n = rng.randint(1, 12)
            edges = random_graph(rng, n, rng.choice([0.1, 0.2, 0.3]))
            label = solve_token_game(n, edges)
            self.assertEqual(label, token_game_by_depth(n, edges, n + 1))
            self.assertEqual(label, token_game_by_depth(n, edges, 3 * n + 5))
            for v in range(n):
                seen[label[v]] += 1
                outs = [w for u, w in edges if u == v]
                if label[v] == DRAW:
                    # a draw has no move to a loss and some move to a draw
                    self.assertFalse(any(label[w] == LOSS for w in outs))
                    self.assertTrue(any(label[w] == DRAW for w in outs))
        self.assertTrue(all(seen.values()))


class TestReachability(unittest.TestCase):
    def test_attractor_against_depth_search(self):
        rng = random.Random(99)
        for _ in range(400):
            n = rng.randint(1, 12)
            edges = random_graph(rng, n, rng.choice([0.1, 0.2, 0.35]))
            owner = [rng.randint(0, 1) for _ in range(n)]
            target = {v for v in range(n) if rng.random() < 0.2}
            got = attractor(n, edges, owner, target)
            self.assertEqual(got, reachability_by_depth(n, edges, owner, target, n + 1))

    def test_token_game_is_a_reachability_game(self):
        rng = random.Random(5)
        for _ in range(200):
            n = rng.randint(1, 10)
            edges = random_graph(rng, n, 0.25)
            label = solve_token_game(n, edges)
            big_n, big_edges, owner, target = token_game_as_reachability(n, edges)
            win0 = attractor(big_n, big_edges, owner, target, 0)
            big_edges_1 = big_edges
            target1 = {v for v in range(n) if not any(u == v for u, _ in edges)}
            win1 = attractor(big_n, big_edges_1, owner, target1, 1)
            for v in range(n):
                if label[v] == WIN:
                    self.assertIn(v, win0)
                elif label[v] == LOSS:
                    self.assertIn(v, win1)
                else:
                    self.assertNotIn(v, win0)
                    self.assertNotIn(v, win1)


if __name__ == "__main__":
    unittest.main()
