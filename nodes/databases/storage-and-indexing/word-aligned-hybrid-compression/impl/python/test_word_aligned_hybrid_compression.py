# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-aligned-hybrid-compression/. The authors are listed in prov/KZ8EQQ.jsonl.

import random
import unittest

from word_aligned_hybrid_compression import (
    ALL_ONES, GROUP, MAX_COUNT, WAH, append_fill, compress, counting_group_fills,
    decompress, wah_and, wah_op, wah_or, wah_xor, word_count,
)


def random_bits(rng, n, kind):
    """Bitmaps of three shapes: uniform, sparse, and long runs."""
    if kind == "uniform":
        return [rng.randrange(2) for _ in range(n)]
    if kind == "sparse":
        return [1 if rng.random() < 0.01 else 0 for _ in range(n)]
    bits, b = [], rng.randrange(2)
    while len(bits) < n:
        bits.extend([b] * rng.randint(1, 200))
        b ^= 1
    return bits[:n]


def cases(seed, count):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.choice([0, 1, 30, 31, 32, 62, 93, 200, 1000, 3000])
        yield rng, n, rng.choice(["uniform", "sparse", "runs"])


class TestWAH(unittest.TestCase):
    def test_figure_2_of_the_paper(self):
        bits = [1] + [0] * 20 + [1] * 3 + [0] * 79 + [1] * 25
        self.assertEqual(len(bits), 128)
        x = compress(bits)
        self.assertEqual(x.words, [0x40000380, 0x80000002, 0x001FFFFF])
        self.assertEqual((x.active, x.nbits), (0xF, 4))
        self.assertEqual(decompress(x), bits)

    def test_round_trip(self):
        for rng, n, kind in cases(1, 150):
            bits = random_bits(rng, n, kind)
            x = compress(bits)
            self.assertEqual(decompress(x), bits)
            self.assertEqual(x.groups(), n // GROUP)
            for word in x.words:
                self.assertLess(word, 1 << 32)

    def test_theorem_3_word_count(self):
        for rng, n, kind in cases(2, 150):
            bits = random_bits(rng, n, kind)
            m = n // GROUP
            self.assertEqual(compress(bits).size(), m - counting_group_fills(bits))

    def test_size_bound_from_set_bits(self):
        for rng, n, kind in cases(3, 150):
            bits = random_bits(rng, n, kind)
            h = sum(bits[: GROUP * (n // GROUP)])
            self.assertLessEqual(compress(bits).size(), 2 * h + 1)

    def test_operations_against_bitwise_lists(self):
        ops = [(wah_and, lambda a, b: a & b), (wah_or, lambda a, b: a | b),
               (wah_xor, lambda a, b: a ^ b)]
        for rng, n, kind in cases(4, 200):
            xb = random_bits(rng, n, kind)
            yb = random_bits(rng, n, rng.choice(["uniform", "sparse", "runs"]))
            x, y = compress(xb), compress(yb)
            for fn, f in ops:
                stats = {}
                z = fn(x, y, stats)
                expect = [f(a, b) for a, b in zip(xb, yb)]
                self.assertEqual(decompress(z), expect)
                # The result is the same word list that COMPRESS gives.
                self.assertEqual(z, compress(expect))
                mx, my, m = x.size(), y.size(), n // GROUP
                if m > 0:
                    self.assertGreaterEqual(stats["steps"], max(mx, my))
                    self.assertLessEqual(stats["steps"], min(mx + my - 1, m))
                else:
                    self.assertEqual(stats["steps"], 0)

    def test_hand_cases(self):
        zero = compress([0] * 93)
        ones = compress([1] * 93)
        self.assertEqual(zero.words, [0x80000003])
        self.assertEqual(ones.words, [0xC0000003])
        self.assertEqual(wah_and(zero, ones).words, [0x80000003])
        self.assertEqual(wah_or(zero, ones).words, [0xC0000003])
        self.assertEqual(wah_xor(ones, ones).words, [0x80000003])
        empty = compress([])
        self.assertEqual(wah_and(empty, empty), WAH([], 0, 0))
        with self.assertRaises(ValueError):
            wah_and(compress([0] * 31), compress([0] * 62))

    def test_long_fill_splits_at_max_count(self):
        z = []
        append_fill(z, 1, MAX_COUNT + 5)
        self.assertEqual([word_count(w) for w in z], [MAX_COUNT, 5])
        append_fill(z, 1, 2)
        self.assertEqual([word_count(w) for w in z], [MAX_COUNT, 7])
        x = WAH(z, 0, 0)
        y = WAH([0x80000000 | (MAX_COUNT), 0x80000007], 0, 0)
        stats = {}
        r = wah_op(x, y, lambda a, b: a & b, stats)
        self.assertEqual(r.words, y.words)
        self.assertEqual(stats["steps"], 2)
        self.assertEqual(ALL_ONES, (1 << 31) - 1)


if __name__ == "__main__":
    unittest.main()
