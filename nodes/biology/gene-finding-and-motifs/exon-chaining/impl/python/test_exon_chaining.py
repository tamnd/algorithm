# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exon-chaining/. The authors are listed in prov/BSR162.jsonl.
"""Tests of exon chaining against brute force over all subsets and a second method."""

import bisect
import itertools
import random
import unittest
from fractions import Fraction

from exon_chaining import Exon, chain_weight, exon_chaining, is_chain

PAGE_EXAMPLE = [
    Exon(1, 5, 5),
    Exon(3, 9, 8),
    Exon(7, 12, 6),
    Exon(10, 14, 4),
    Exon(13, 20, 9),
    Exon(15, 18, 3),
    Exon(21, 24, 5),
]


def brute_force(exons):
    """The best weight over all subsets of pairwise non-overlapping exons."""
    best = 0
    order = sorted(range(len(exons)), key=lambda j: (exons[j].left, exons[j].right))
    for r in range(1, len(exons) + 1):
        for subset in itertools.combinations(order, r):
            if is_chain(exons, subset):
                best = max(best, chain_weight(exons, subset))
    return best


def by_right_ends(exons):
    """Weighted interval scheduling in the textbook form: sort by right end, binary search."""
    order = sorted(range(len(exons)), key=lambda j: exons[j].right)
    rights = [exons[j].right for j in order]
    opt = [0] * (len(order) + 1)
    for t, j in enumerate(order, 1):
        p = bisect.bisect_left(rights, exons[j].left)  # exons with right < left
        opt[t] = max(opt[t - 1], opt[p] + exons[j].weight)
    return opt[-1]


def random_exons(rng, n, span, wmax, allow_negative=False):
    out = []
    for _ in range(n):
        a = rng.randint(1, span)
        b = rng.randint(a, min(span, a + rng.randint(0, span // 3)))
        lo = -wmax if allow_negative else 1
        out.append(Exon(a, b, rng.randint(lo, wmax)))
    return out


class TestExonChaining(unittest.TestCase):
    def test_page_example(self):
        best, chain = exon_chaining(PAGE_EXAMPLE)
        self.assertEqual(best, 25)
        self.assertEqual(chain, [0, 2, 4, 6])
        self.assertTrue(is_chain(PAGE_EXAMPLE, chain))
        self.assertEqual(brute_force(PAGE_EXAMPLE), 25)

    def test_empty_and_single(self):
        self.assertEqual(exon_chaining([]), (0, []))
        self.assertEqual(exon_chaining([Exon(4, 4, 7)]), (7, [0]))
        self.assertEqual(exon_chaining([Exon(4, 9, -2)]), (0, []))

    def test_touching_exons_overlap(self):
        exons = [Exon(1, 5, 3), Exon(5, 9, 4)]
        self.assertEqual(exon_chaining(exons), (4, [1]))
        exons = [Exon(1, 5, 3), Exon(6, 9, 4)]
        self.assertEqual(exon_chaining(exons), (7, [0, 1]))

    def test_against_brute_force(self):
        rng = random.Random(20261118)
        for trial in range(300):
            n = rng.randint(1, 9)
            exons = random_exons(rng, n, 30, 10, allow_negative=(trial % 3 == 0))
            best, chain = exon_chaining(exons)
            self.assertEqual(best, brute_force(exons))
            self.assertTrue(is_chain(exons, chain))
            self.assertEqual(chain_weight(exons, chain), best)

    def test_against_right_end_method(self):
        rng = random.Random(7)
        for _ in range(200):
            exons = random_exons(rng, rng.randint(1, 60), 200, 50)
            best, chain = exon_chaining(exons)
            self.assertEqual(best, by_right_ends(exons))
            self.assertEqual(chain_weight(exons, chain), best)

    def test_fraction_weights(self):
        rng = random.Random(3)
        for _ in range(50):
            exons = [Exon(e.left, e.right, Fraction(e.weight, rng.randint(1, 7)))
                     for e in random_exons(rng, 8, 25, 9)]
            best, chain = exon_chaining(exons)
            self.assertEqual(best, brute_force(exons))
            self.assertEqual(chain_weight(exons, chain), best)

    def test_bad_interval(self):
        with self.assertRaises(ValueError):
            exon_chaining([Exon(5, 4, 1)])


if __name__ == "__main__":
    unittest.main()
