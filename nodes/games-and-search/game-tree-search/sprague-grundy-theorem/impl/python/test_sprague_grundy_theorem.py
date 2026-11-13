# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sprague-grundy-theorem/. The authors are listed in prov/AMWPCY.jsonl.

import random
import unittest

from sprague_grundy_theorem import (
    component_grundy,
    mover_loses,
    sum_grundy,
    sum_grundy_brute,
    sum_options,
    winning_moves,
)

GAMES = [None, (1, 2), (1, 2, 3), (1, 3, 4), (2, 3), (1, 4)]


def random_sum(rng, parts, top):
    return tuple((rng.choice(GAMES), rng.randint(0, top)) for _ in range(parts))


class TestTheorem(unittest.TestCase):
    def test_xor_zero_iff_brute_force_loss(self):
        rng = random.Random(1935)
        for _ in range(1500):
            s = random_sum(rng, rng.choice([2, 3]), 9)
            self.assertEqual(sum_grundy(s) == 0, mover_loses(s), s)

    def test_sum_value_is_xor(self):
        rng = random.Random(1939)
        for _ in range(600):
            s = random_sum(rng, rng.choice([2, 3]), 7)
            self.assertEqual(sum_grundy_brute(s), sum_grundy(s), s)

    def test_equivalent_to_nim_heap(self):
        # G + H and *g(G) + H have the same outcome for every H tried
        rng = random.Random(1956)
        for _ in range(800):
            g = (rng.choice(GAMES[1:]), rng.randint(0, 12))
            h = random_sum(rng, rng.choice([1, 2]), 8)
            heap = (None, component_grundy(g))
            self.assertEqual(mover_loses((g,) + h), mover_loses((heap,) + h))

    def test_winning_moves(self):
        rng = random.Random(7)
        for _ in range(500):
            s = random_sum(rng, 3, 9)
            ws = winning_moves(s)
            self.assertEqual(bool(ws), not mover_loses(s))
            for i, d in ws:
                t = s[:i] + (d,) + s[i + 1:]
                self.assertIn(t, set(sum_options(s)))
                self.assertTrue(mover_loses(t))

    def test_page_example(self):
        s = (((1, 2), 5), ((1, 3, 4), 6), (None, 3))
        self.assertEqual([component_grundy(c) for c in s], [2, 2, 3])
        self.assertEqual(sum_grundy(s), 3)
        self.assertEqual(
            sorted(winning_moves(s)),
            [(0, ((1, 2), 4)), (1, ((1, 3, 4), 3)), (2, (None, 0))],
        )


class TestTightness(unittest.TestCase):
    def test_misere_counterexample(self):
        # *0 and *2 + *2 both have value 0; under misere play the mover
        # wins the first (no move) and loses the second.
        self.assertEqual(sum_grundy(((None, 2), (None, 2))), 0)

        def misere_mover_loses(s):
            opts = list(sum_options(s))
            if not opts:
                return False
            return all(not misere_mover_loses(t) for t in opts)

        self.assertFalse(misere_mover_loses(((None, 0),)))
        self.assertTrue(misere_mover_loses(((None, 2), (None, 2))))


if __name__ == "__main__":
    unittest.main()
