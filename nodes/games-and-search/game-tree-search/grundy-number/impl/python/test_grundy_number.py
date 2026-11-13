# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grundy-number/. The authors are listed in prov/VC5H7C.jsonl.

import random
import sys
import unittest

from grundy_number import (
    DAWSONS_KAYLES,
    KAYLES,
    eventual_period,
    grundy,
    grundys_game_table,
    guy_smith_certifies,
    last_exception,
    mover_loses,
    octal_table,
    subtraction_table,
)

sys.setrecursionlimit(10000)


def heap_options(moves):
    return lambda h: [h - m for m in moves if m <= h]


class TestSubtractionGames(unittest.TestCase):
    N = 200

    def test_periodic_sequences(self):
        cases = {
            (1, 2): [0, 1, 2],
            (1, 2, 3): [0, 1, 2, 3],
            (1, 3, 4): [0, 1, 0, 1, 2, 3, 2],
        }
        for moves, period in cases.items():
            for n in range(self.N + 1):
                self.assertEqual(grundy(n, heap_options(moves)), period[n % len(period)], (moves, n))

    def test_table_and_period_detection(self):
        self.assertEqual(eventual_period(subtraction_table((1, 3, 4), 100), 4), (4, 7))
        self.assertEqual(eventual_period(subtraction_table((2, 3), 100), 3), (3, 5))
        self.assertEqual(subtraction_table((2, 3), 9), [0, 0, 1, 1, 2, 0, 0, 1, 1, 2])

    def test_zero_iff_loss(self):
        rng = random.Random(31)
        for _ in range(60):
            moves = tuple(sorted(rng.sample(range(1, 9), rng.randint(1, 4))))
            opts = heap_options(moves)
            for n in range(80):
                g = grundy(n, opts)
                self.assertEqual(g == 0, mover_loses(n, opts))
                self.assertLessEqual(g, len(moves))


class TestNim(unittest.TestCase):
    def test_heap_value_is_size(self):
        for n in range(120):
            self.assertEqual(grundy(n, lambda h: range(h)), n)

    def test_nim_is_octal_333(self):
        self.assertEqual(octal_table((3,) * 40, 40), list(range(41)))


class TestOctalGames(unittest.TestCase):
    def test_kayles(self):
        g = octal_table(KAYLES, 400)
        self.assertEqual(g[:13], [0, 1, 2, 3, 1, 4, 3, 2, 1, 4, 2, 6, 4])
        self.assertEqual(last_exception(g, 12), 70)
        self.assertTrue(guy_smith_certifies(g, 71, 12, 2))
        self.assertFalse(guy_smith_certifies(g, 70, 12, 2))
        self.assertEqual(g[71:83], [7, 4, 1, 2, 8, 1, 4, 7, 2, 1, 8, 2])
        self.assertEqual((g[70], g[82]), (6, 2))

    def test_kayles_by_recursion(self):
        # positions are sorted tuples of row lengths
        def options(p):
            out = set()
            for i, h in enumerate(p):
                rest = p[:i] + p[i + 1:]
                for k in (1, 2):
                    for left in range(0, h - k + 1):
                        right = h - k - left
                        q = tuple(sorted(rest + tuple(x for x in (left, right) if x)))
                        out.add(q)
            return out

        g = octal_table(KAYLES, 14)
        for n in range(15):
            self.assertEqual(grundy((n,) if n else (), options), g[n])
        self.assertEqual(grundy((3, 5), options), g[3] ^ g[5])

    def test_dawsons_kayles_period_34(self):
        g = octal_table(DAWSONS_KAYLES, 600)
        self.assertEqual(last_exception(g, 34), 52)
        self.assertTrue(guy_smith_certifies(g, 53, 34, 2))

    def test_grundys_game_prefix(self):
        self.assertEqual(grundys_game_table(14), [0, 0, 0, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 3, 2])


if __name__ == "__main__":
    unittest.main()
