# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boutons-theorem/. The authors are listed in prov/9301CP.jsonl.

import random
import unittest
from itertools import product

from boutons_theorem import label_by_search, misere_p, moves, nim_sum, normal_p, winning_moves


def positions(k, top):
    return product(range(top + 1), repeat=k)


class TestNormalPlay(unittest.TestCase):
    def test_theorem_up_to_four_heaps_of_seven(self):
        for k in range(1, 5):
            lose = label_by_search(k, 7)
            for p, is_loss in lose.items():
                self.assertEqual(is_loss, normal_p(p), p)

    def test_lemma_moves_leave_p(self):
        for k in range(1, 5):
            for p in positions(k, 7):
                if normal_p(p):
                    self.assertTrue(all(not normal_p(q) for q in moves(p)))

    def test_lemma_winning_moves_exactly_top_bit_heaps(self):
        for k in range(1, 5):
            for p in positions(k, 7):
                x = nim_sum(p)
                to_p = sorted((i, q[i]) for q in moves(p) if normal_p(q) for i in range(k) if q[i] != p[i])
                self.assertEqual(to_p, sorted(winning_moves(p)))
                if x:
                    t = x.bit_length() - 1
                    heaps_with_t = [i for i in range(k) if (p[i] >> t) & 1]
                    self.assertEqual([i for i, _ in winning_moves(p)], heaps_with_t)
                    self.assertEqual(len(heaps_with_t) % 2, 1)
                    for i, b in winning_moves(p):
                        q = list(p)
                        q[i] = b
                        self.assertEqual(nim_sum(q), 0)

    def test_random_large_heaps(self):
        rng = random.Random(1901)
        for _ in range(3000):
            p = [rng.randrange(1, 1 << 30) for _ in range(rng.randint(1, 8))]
            if nim_sum(p):
                self.assertTrue(winning_moves(p))
            else:
                self.assertEqual(winning_moves(p), [])


class TestMisere(unittest.TestCase):
    def test_theorem(self):
        for k in range(1, 5):
            lose = label_by_search(k, 6, misere=True)
            for p, is_loss in lose.items():
                self.assertEqual(is_loss, misere_p(p), p)

    def test_counterexamples_to_xor_rule(self):
        self.assertTrue(normal_p((1, 1)))
        self.assertFalse(misere_p((1, 1)))
        self.assertFalse(normal_p((1,)))
        self.assertTrue(misere_p((1,)))
        self.assertTrue(misere_p((1, 1, 1)))


if __name__ == "__main__":
    unittest.main()
