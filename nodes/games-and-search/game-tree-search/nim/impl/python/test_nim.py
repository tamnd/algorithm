# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nim/. The authors are listed in prov/02YCWR.jsonl.

import random
import unittest
from itertools import product

from nim import (
    brute_force_first_player_wins,
    first_player_wins,
    lasker_grundy_rule,
    lasker_grundy_table,
    misere_first_player_wins,
    moore_brute_first_player_wins,
    moore_first_player_wins,
    nim_sum,
    winning_moves,
    wythoff_brute_losses,
    wythoff_pairs,
)


def all_positions(max_heaps=4, max_size=7):
    for k in range(1, max_heaps + 1):
        yield from product(range(max_size + 1), repeat=k)


class TestNormalPlay(unittest.TestCase):
    def test_xor_rule_matches_search(self):
        count = losses = 0
        for h in all_positions():
            count += 1
            losses += not first_player_wins(h)
            self.assertEqual(first_player_wins(h), brute_force_first_player_wins(h), h)
        self.assertEqual(count, 4680)
        self.assertEqual(losses, 585)

    def test_winning_moves_reach_zero(self):
        for h in all_positions():
            ws = winning_moves(h)
            if nim_sum(h) == 0:
                self.assertEqual(ws, [])
                continue
            self.assertTrue(ws)
            self.assertEqual(len(ws) % 2, 1)
            for i, b in ws:
                self.assertLess(b, h[i])
                after = list(h)
                after[i] = b
                self.assertEqual(nim_sum(after), 0)
                self.assertFalse(brute_force_first_player_wins(after))

    def test_examples(self):
        self.assertEqual(nim_sum((3, 4, 5)), 2)
        self.assertEqual(winning_moves((3, 4, 5)), [(0, 1)])
        self.assertEqual(nim_sum((1, 2, 3)), 0)
        self.assertEqual(winning_moves((3, 5, 7)), [(0, 2), (1, 4), (2, 6)])

    def test_large_random_heaps(self):
        rng = random.Random(7)
        for _ in range(2000):
            h = [rng.randrange(1 << 40) for _ in range(rng.randint(1, 9))]
            for i, b in winning_moves(h):
                after = list(h)
                after[i] = b
                self.assertEqual(nim_sum(after), 0)


class TestVariants(unittest.TestCase):
    def test_misere_rule(self):
        for h in all_positions(4, 6):
            self.assertEqual(
                misere_first_player_wins(h),
                brute_force_first_player_wins(h, misere=True),
                h,
            )

    def test_moore(self):
        for k in (1, 2, 3):
            for h in all_positions(4, 4):
                self.assertEqual(moore_first_player_wins(h, k), moore_brute_first_player_wins(h, k), (h, k))

    def test_lasker(self):
        g = lasker_grundy_table(120)
        for h in range(121):
            self.assertEqual(g[h], lasker_grundy_rule(h))

    def test_wythoff(self):
        self.assertEqual(wythoff_brute_losses(60), sorted(wythoff_pairs(60)))
        self.assertEqual(wythoff_pairs(20), [(0, 0), (1, 2), (3, 5), (4, 7), (6, 10), (8, 13), (9, 15), (11, 18), (12, 20)])


if __name__ == "__main__":
    unittest.main()
