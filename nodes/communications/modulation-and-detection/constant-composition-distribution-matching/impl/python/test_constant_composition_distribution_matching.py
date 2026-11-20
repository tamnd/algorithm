# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-composition-distribution-matching/. The authors are listed in prov/EKQBW6.jsonl.

import itertools
import math
import random
import unittest

from constant_composition_distribution_matching import (
    composition,
    decode,
    encode,
    multinomial,
    num_bits,
    rank,
    rate,
    unrank,
)


def all_words(c, symbols):
    """All words of the composition c in lexicographic order of the symbol indices, by brute force."""
    pool = [s for s, cs in enumerate(c) for _ in range(cs)]
    idx = sorted(set(itertools.permutations(pool)))
    return [[symbols[s] for s in w] for w in idx]


def to_bits(v, k):
    return [(v >> (k - 1 - t)) & 1 for t in range(k)]


def divergence(c, probs):
    n = sum(c)
    return sum((cs / n) * math.log((cs / n) / p) for cs, p in zip(c, probs) if cs > 0)


def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)


class TestCCDM(unittest.TestCase):
    def test_multinomial(self):
        self.assertEqual(multinomial([4, 3, 2, 1]), 12600)
        self.assertEqual(multinomial([2, 2, 1]), 30)
        self.assertEqual(multinomial([2, 2]), 6)
        self.assertEqual(multinomial([0, 5, 0]), 1)
        self.assertEqual(num_bits([4, 3, 2, 1]), 13)
        self.assertEqual(num_bits([2, 2, 1]), 4)

    def test_unrank_matches_sorted_permutations(self):
        for c in ([2, 2], [2, 2, 1], [3, 1, 1], [1, 1, 1, 1], [2, 1, 2, 1], [4, 0, 2]):
            symbols = list(range(len(c)))
            words = all_words(c, symbols)
            self.assertEqual(len(words), multinomial(c))
            for r, w in enumerate(words):
                self.assertEqual(unrank(r, c, symbols), w)
                self.assertEqual(rank(w, c, symbols), r)

    def test_paper_codebook(self):
        c, symbols = [2, 2], [0, 1]
        book = ["".join(map(str, encode(to_bits(v, 2), c, symbols))) for v in range(4)]
        self.assertEqual(book, ["0011", "0110", "1001", "1100"])

    def test_page_example(self):
        c, symbols = [2, 2, 1], [1, 3, 5]
        self.assertEqual(encode([0, 0, 0, 0], c, symbols), [1, 1, 3, 3, 5])
        self.assertEqual(encode([1, 0, 1, 1], c, symbols), [3, 5, 1, 1, 3])
        self.assertEqual(encode([1, 1, 1, 1], c, symbols), [5, 3, 3, 1, 1])
        ranks = [rank(encode(to_bits(v, 4), c, symbols), c, symbols) for v in range(16)]
        self.assertEqual(ranks, [0, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 29])

    def test_bijection_and_composition(self):
        for c in ([2, 2, 1], [3, 2, 2, 1], [3, 3, 2], [5, 1], [1, 2, 0, 3]):
            symbols = [2 * s + 1 for s in range(len(c))]
            k = num_bits(c)
            seen = set()
            for v in range(1 << k):
                word = encode(to_bits(v, k), c, symbols)
                self.assertEqual([word.count(a) for a in symbols], c)
                self.assertEqual(decode(word, c, symbols), to_bits(v, k))
                seen.add(tuple(word))
            self.assertEqual(len(seen), 1 << k)

    def test_encoder_order(self):
        c, symbols = [3, 2, 2, 1], [1, 3, 5, 7]
        k = num_bits(c)
        prev = -1
        for v in range(1 << k):
            r = rank(encode(to_bits(v, k), c, symbols), c, symbols)
            self.assertEqual(r, -((-v * multinomial(c)) // (1 << k)))
            self.assertGreater(r, prev)
            prev = r

    def test_long_words(self):
        rng = random.Random(41)
        probs = [0.4, 0.3, 0.2, 0.1]
        c = composition(probs, 400)
        symbols = [1, 3, 5, 7]
        k = num_bits(c)
        for _ in range(20):
            bits = [rng.randrange(2) for _ in range(k)]
            word = encode(bits, c, symbols)
            self.assertEqual([word.count(a) for a in symbols], c)
            self.assertEqual(decode(word, c, symbols), bits)

    def test_composition_is_optimal(self):
        rng = random.Random(42)
        for _ in range(40):
            size = rng.randint(2, 4)
            raw = [rng.random() + 0.01 for _ in range(size)]
            probs = [x / sum(raw) for x in raw]
            n = rng.randint(1, 9)
            c = composition(probs, n)
            self.assertEqual(sum(c), n)
            best = min(
                divergence(list(cc), probs)
                for cc in itertools.product(range(n + 1), repeat=size)
                if sum(cc) == n
            )
            self.assertLess(divergence(c, probs), best + 1e-12)
        self.assertEqual(composition([0.4, 0.3, 0.2, 0.1], 10), [4, 3, 2, 1])
        self.assertEqual(composition([0.5, 0.0, 0.5], 4), [2, 0, 2])

    def test_rates(self):
        probs = [0.4, 0.3, 0.2, 0.1]
        h = entropy(probs)
        table = {10: 13, 20: 30, 50: 84, 100: 175, 200: 358, 1000: 1831}
        for n, k in table.items():
            c = composition(probs, n)
            self.assertEqual(num_bits(c), k, n)
            self.assertLessEqual(rate(c), entropy([cs / n for cs in c]) + 1e-12)
            bound = ((len(probs) - 1) * math.log2(n + 1) + 1) / n
            self.assertLessEqual(entropy([cs / n for cs in c]) - rate(c), bound)
        self.assertAlmostEqual(h, 1.8464, delta=1e-4)

    def test_errors(self):
        with self.assertRaises(ValueError):
            encode([0, 1], [2, 2, 1], [1, 3, 5])
        with self.assertRaises(ValueError):
            unrank(30, [2, 2, 1], [1, 3, 5])
        with self.assertRaises(ValueError):
            rank([1, 1, 1, 3, 5], [2, 2, 1], [1, 3, 5])
        with self.assertRaises(ValueError):
            composition([0.5, 0.6], 3)


if __name__ == "__main__":
    unittest.main()
