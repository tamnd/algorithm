# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tandem-repeat-finding/. The authors are listed in prov/3VVNE0.jsonl.
"""Tests of the tandem repeat finder: WDP against Smith-Waterman on copies of the
pattern, the sum of heads law against enumeration, and planted repeats."""

import itertools
import random
import unittest
from fractions import Fraction

from bioseq import hamming, mutate, random_dna
from tandem_repeat_finding import (Repeat, find_tandem_repeats, heads_distribution,
                                   is_rotation, sum_of_heads_threshold, wraparound_align)

MATCH, MISMATCH, INDEL = 2, 7, 7


def smith_waterman(a, b, match=MATCH, mismatch=MISMATCH, indel=INDEL):
    """Best local alignment score of a and b with linear gaps."""
    prev = [0] * (len(b) + 1)
    best = 0
    for x in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for y in range(1, len(b) + 1):
            sub = match if a[x - 1] == b[y - 1] else -mismatch
            cur[y] = max(0, prev[y - 1] + sub, prev[y] - indel, cur[y - 1] - indel)
            best = max(best, cur[y])
        prev = cur
    return best


def score_of(text, pattern, cols):
    """The score of an alignment given as columns, and a check of its shape."""
    total, last_x, last_j = 0, None, None
    d = len(pattern)
    for x, j in cols:
        if x is not None:
            assert last_x is None or x == last_x + 1
            last_x = x
        if j is not None:
            assert last_j is None or j == (last_j + 1) % d
            last_j = j
        if x is None or j is None:
            total -= INDEL
        else:
            total += MATCH if text[x] == pattern[j] else -MISMATCH
    return total


def best_rotation_distance(unit, pattern):
    if len(unit) != len(pattern):
        return len(unit) + len(pattern)
    return min(hamming(unit, pattern[r:] + pattern[:r]) for r in range(len(pattern)))


def add_indels(rng, seq, rate):
    """Delete or insert one random base at each position with probability rate.

    Draw order per position: one rng.random(); if it is below rate, one
    rng.random() < 0.5 for a deletion, and for an insertion one rng.choice.
    """
    out = []
    for c in seq:
        if rng.random() < rate:
            if rng.random() < 0.5:
                continue
            out.append(rng.choice("ACGT"))
        out.append(c)
    return "".join(out)


def planted(rng, d, sub_rate, indel_rate, flank=200):
    unit = random_dna(rng, d)
    left, right = random_dna(rng, flank), random_dna(rng, flank)
    rep = add_indels(rng, mutate(rng, unit * max(4, 120 // d), sub_rate), indel_rate)
    return unit, left + rep + right, flank, flank + len(rep)


def found(unit, d, reports, a, b, max_dist):
    for r in reports:
        overlap = min(r.end, b) - max(r.start, a)
        if r.period == d and overlap >= 0.8 * (b - a) and best_rotation_distance(unit, r.pattern) <= max_dist:
            return True
    return False


class TestWraparound(unittest.TestCase):
    def test_equals_smith_waterman_on_copies(self):
        rng = random.Random(11)
        for trial in range(250):
            alphabet = "AC" if trial % 2 else "ACGT"
            d = rng.randint(1, 6)
            pattern = "".join(rng.choice(alphabet) for _ in range(d))
            text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 28)))
            score, a, b, cols = wraparound_align(text, pattern)
            copies = pattern * (2 * len(text) // d + 3)
            self.assertEqual(score, smith_waterman(text, copies))
            self.assertEqual(score_of(text, pattern, cols), score)
            used = [x for x, _ in cols if x is not None]
            self.assertEqual(used, list(range(a, b)))

    def test_tandem_example(self):
        score, a, b, cols = wraparound_align("TTACGACGACGTTT", "ACG")
        self.assertEqual((score, a, b), (18, 2, 11))
        self.assertEqual([j for _, j in cols], [0, 1, 2] * 3)

    def test_indel_in_a_copy(self):
        # ACG ACG AG ACG ACG: 14 matches and one deleted C
        score, a, b, cols = wraparound_align("ACGACGAGACGACG", "ACG")
        self.assertEqual((score, a, b), (14 * MATCH - INDEL, 0, 14))
        self.assertIn((None, 1), cols)


class TestSumOfHeads(unittest.TestCase):
    def test_distribution_against_enumeration(self):
        for w in range(1, 11):
            for k in range(1, 5):
                p = Fraction(3, 4)
                exact = [Fraction(0)] * (w + 1)
                for bits in itertools.product((0, 1), repeat=w):
                    count, run = 0, 0
                    for t in range(w + 1):
                        if t < w and bits[t]:
                            run += 1
                            continue
                        if run >= k:
                            count += run
                        run = 0
                    ones = sum(bits)
                    exact[count] += p ** ones * (1 - p) ** (w - ones)
                self.assertEqual(heads_distribution(w, k, p), exact)

    def test_threshold_is_the_lower_quantile(self):
        c = sum_of_heads_threshold(100, 5, 0.75)
        self.assertEqual(c, 27)
        q = heads_distribution(100, 5, Fraction(3, 4))
        self.assertLessEqual(sum(q[:c]), Fraction(1, 20))
        self.assertGreater(sum(q[:c + 1]), Fraction(1, 20))


class TestFinder(unittest.TestCase):
    def test_perfect_repeat(self):
        s = "TTGCA" + "ACG" * 10 + "GGTCA"
        self.assertEqual(find_tandem_repeats(s), [Repeat(5, 35, 3, "ACG", 60, 10.0)])

    def test_planted_substitutions(self):
        hits = 0
        periods = [2, 3, 5, 7, 11, 15, 20, 25, 33, 45]
        for seed in range(30):
            rng = random.Random(1000 + seed)
            d = periods[seed % len(periods)]
            unit, s, a, b = planted(rng, d, 0.05, 0.0)
            hits += found(unit, d, find_tandem_repeats(s), a, b, 2)
        self.assertGreaterEqual(hits, 29)

    def test_planted_with_indels(self):
        hits = 0
        periods = [3, 7, 12, 20, 30]
        for seed in range(20):
            rng = random.Random(2000 + seed)
            d = periods[seed % len(periods)]
            unit, s, a, b = planted(rng, d, 0.03, 0.01)
            hits += found(unit, d, find_tandem_repeats(s), a, b, 2)
        self.assertGreaterEqual(hits, 17)

    def test_random_dna_has_no_repeats(self):
        for seed in range(5):
            rng = random.Random(seed)
            self.assertEqual(find_tandem_repeats(random_dna(rng, 2000)), [])

    def test_rotation(self):
        self.assertTrue(is_rotation("ACG", "GAC"))
        self.assertFalse(is_rotation("ACG", "AGC"))


if __name__ == "__main__":
    unittest.main()
