# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cpg-island-detection/. The authors are listed in prov/0S3A9K.jsonl.
"""Tests of the CpG island HMM and of the window rule."""

import itertools
import math
import random
import unittest

from bioseq import random_dna
from cpg_island_detection import (BASES, STATES, CpgModel, composition_model, hmm_islands,
                                  obs_exp_cpg, path_log_prob, runs, viterbi_cpg,
                                  window_flags, window_islands)


def random_dist(rng, keys):
    v = [rng.random() + 0.05 for _ in keys]
    z = sum(v)
    return {k: x / z for k, x in zip(keys, v)}


def random_model(rng):
    return CpgModel(random_dist(rng, STATES),
                    {j: random_dist(rng, STATES) for j in STATES},
                    {k: random_dist(rng, BASES) for k in STATES},
                    {k: {p: random_dist(rng, BASES) for p in BASES} for k in STATES})


def toy_model():
    """The model of the page example: no dependence on the previous base."""
    plus = {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1}
    minus = {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
    return CpgModel({"+": 0.5, "-": 0.5},
                    {"+": {"+": 0.8, "-": 0.2}, "-": {"+": 0.2, "-": 0.8}},
                    {"+": plus, "-": minus},
                    {"+": {p: plus for p in BASES}, "-": {p: minus for p in BASES}})


def brute_window_flags(s, w, min_gc, min_oe):
    out = []
    for i in range(len(s) - w + 1):
        x = s[i:i + w]
        c, g = x.count("C"), x.count("G")
        cg = sum(1 for j in range(w - 1) if x[j:j + 2] == "CG")
        oe = cg * w / (c * g) if c and g else 0.0
        out.append((c + g) / w > min_gc and oe > min_oe)
    return out


class TestViterbi(unittest.TestCase):
    def test_against_all_paths(self):
        rng = random.Random(11)
        for _ in range(40):
            model = random_model(rng)
            n = rng.randrange(1, 9)
            seq = "".join(rng.choice(BASES) for _ in range(n))
            score, path = viterbi_cpg(seq, model)
            best = max(path_log_prob(seq, "".join(p), model)
                       for p in itertools.product(STATES, repeat=n))
            self.assertAlmostEqual(score, best, places=9)
            self.assertAlmostEqual(path_log_prob(seq, path, model), score, places=9)

    def test_page_example(self):
        score, path = viterbi_cpg("ATATCGCGCGTATA", toy_model())
        self.assertEqual(path, "----++++++----")
        self.assertEqual(runs(path), [(4, 10)])
        self.assertAlmostEqual(score, path_log_prob("ATATCGCGCGTATA", path, toy_model()), places=12)

    def test_long_sequence_does_not_underflow(self):
        rng = random.Random(12)
        seq = random_dna(rng, 20000, 0.45)
        score, path = viterbi_cpg(seq, composition_model())
        self.assertTrue(math.isfinite(score))
        self.assertEqual(len(path), 20000)

    def test_finds_planted_island(self):
        rng = random.Random(13)
        left, isl, right = random_dna(rng, 3000, 0.4), random_dna(rng, 800, 0.7), random_dna(rng, 3000, 0.4)
        seq = left + isl + right
        found = hmm_islands(seq, composition_model(), min_len=200)
        self.assertEqual(len(found), 1)
        a, b = found[0]
        overlap = min(b, 3800) - max(a, 3000)
        self.assertGreater(overlap, 0.8 * 800)
        self.assertLess((b - a) - overlap, 200)

    def test_rejects_bad_letters(self):
        with self.assertRaises(ValueError):
            viterbi_cpg("ACGN", toy_model())
        with self.assertRaises(ValueError):
            viterbi_cpg("", toy_model())


class TestRuns(unittest.TestCase):
    def test_runs(self):
        self.assertEqual(runs("++--+-++"), [(0, 2), (4, 5), (6, 8)])
        self.assertEqual(runs("----"), [])
        self.assertEqual(runs("+"), [(0, 1)])


class TestWindow(unittest.TestCase):
    def test_obs_exp(self):
        # CGCGAATT: C 2, G 2, CG 2, n 8, so 2 * 8 / (2 * 2) = 4.
        self.assertEqual(obs_exp_cpg(2, 2, 2, 8), 4.0)
        self.assertEqual(obs_exp_cpg(0, 3, 0, 8), 0.0)

    def test_sliding_counts_match_direct_counts(self):
        rng = random.Random(14)
        for _ in range(30):
            n = rng.randrange(2, 60)
            s = random_dna(rng, n, rng.random())
            w = rng.randrange(2, n + 1)
            gc, oe = rng.choice([0.3, 0.5, 0.6]), rng.choice([0.2, 0.6, 1.0])
            self.assertEqual(window_flags(s, w, gc, oe), brute_window_flags(s, w, gc, oe))

    def test_islands_are_unions_of_marked_windows(self):
        rng = random.Random(15)
        for _ in range(30):
            s = random_dna(rng, rng.randrange(10, 80), 0.55)
            w = rng.randrange(2, 10)
            flags = brute_window_flags(s, w, 0.5, 0.6)
            covered = [False] * len(s)
            for i, ok in enumerate(flags):
                if ok:
                    for j in range(i, i + w):
                        covered[j] = True
            got = window_islands(s, w, 0.5, 0.6)
            self.assertEqual(runs("".join("+" if x else "-" for x in covered)), got)

    def test_page_window_example(self):
        s = "ATATATCGCGCGATATAT"
        self.assertEqual(window_islands(s, 6, 0.5, 0.6), [(4, 14)])

    def test_planted_island_with_window_rule(self):
        rng = random.Random(16)
        seq = random_dna(rng, 3000, 0.35) + random_dna(rng, 800, 0.7) + random_dna(rng, 3000, 0.35)
        found = [r for r in window_islands(seq) if r[1] - r[0] >= 300]
        self.assertEqual(len(found), 1)
        a, b = found[0]
        self.assertTrue(a < 3200 and b > 3600)

    def test_short_input(self):
        self.assertEqual(window_flags("ACG", 200), [])
        self.assertEqual(window_islands("ACG"), [])


if __name__ == "__main__":
    unittest.main()
