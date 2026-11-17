# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-hmm-gene-finder/. The authors are listed in prov/FHW813.jsonl.
"""Tests of the GHMM decoder, against enumeration of all parses."""

import math
import random
import unittest

from bioseq import DNA
from generalized_hmm_gene_finder import NEG, Ghmm, ghmm_viterbi, parse_score, toy_gene_model


def all_parses(n, K, max_dur):
    """Every parse of 0..n as a list of (state index, a, b)."""
    def rec(a):
        if a == n:
            yield []
            return
        for q in range(K):
            for l in range(1, min(max_dur[q], n - a) + 1):
                for rest in rec(a + l):
                    yield [(q, a, a + l)] + rest
    return rec(0)


def random_model(rng, x, K):
    """A GHMM with random tables; some entries are impossible."""
    def maybe(v):
        return NEG if rng.random() < 0.15 else v

    names = tuple("S%d" % q for q in range(K))
    start = [maybe(math.log(rng.random() + 0.01)) for _ in range(K)]
    trans = [[maybe(math.log(rng.random() + 0.01)) for _ in range(K)] for _ in range(K)]
    end = [maybe(math.log(rng.random() + 0.01)) for _ in range(K)]
    max_dur = [rng.randrange(1, 5) for _ in range(K)]
    dur = {(q, l): maybe(math.log(rng.random() + 0.01)) for q in range(K) for l in range(1, 6)}
    emit = [{c: math.log(rng.random() + 0.05) for c in DNA} for _ in range(K)]
    bonus = [rng.uniform(-1, 1) for _ in range(K)]

    def log_seg(q, a, b):
        # A score that depends on the segment as a whole, not only on its bases.
        return sum(emit[q][c] for c in x[a:b]) + bonus[q] * (x[a] == x[b - 1])

    return Ghmm(names, start, trans, end, max_dur, lambda q, l: dur[(q, l)], log_seg)


class TestDecoder(unittest.TestCase):
    def test_against_enumeration(self):
        rng = random.Random(21)
        for trial in range(60):
            K = rng.randrange(1, 4)
            n = rng.randrange(1, 8)
            x = "".join(rng.choice(DNA) for _ in range(n))
            m = random_model(rng, x, K)
            best = NEG
            for p in all_parses(n, K, m.max_dur):
                best = max(best, parse_score(m, [(m.states[q], a, b) for q, a, b in p]))
            score, parse = ghmm_viterbi(m, n)
            if best == NEG:
                self.assertEqual(score, NEG)
                self.assertIsNone(parse)
                continue
            self.assertAlmostEqual(score, best, places=9)
            self.assertAlmostEqual(parse_score(m, parse), score, places=9)
            self.assertEqual(parse[0][1], 0)
            self.assertEqual(parse[-1][2], n)
            for (_, a1, b1), (_, a2, b2) in zip(parse, parse[1:]):
                self.assertEqual(b1, a2)

    def test_hmm_is_a_special_case(self):
        # With max_dur 1 a GHMM is an HMM, and the decoder is the Viterbi algorithm.
        rng = random.Random(22)
        x = "".join(rng.choice(DNA) for _ in range(30))
        m = random_model(rng, x, 2)
        m = m._replace(max_dur=[1, 1], log_dur=lambda q, l: 0.0, log_start=[0.0, 0.0],
                       log_trans=[[math.log(0.9), math.log(0.1)], [math.log(0.2), math.log(0.8)]],
                       log_end=[0.0, 0.0])
        score, parse = ghmm_viterbi(m, len(x))
        V = [m.log_seg(q, 0, 1) for q in range(2)]
        for i in range(1, len(x)):
            V = [max(V[p] + m.log_trans[p][q] for p in range(2)) + m.log_seg(q, i, i + 1) for q in range(2)]
        self.assertAlmostEqual(score, max(V), places=9)
        self.assertEqual(len(parse), len(x))


class TestToyGeneModel(unittest.TestCase):
    N = {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
    I = {"A": 0.2, "C": 0.15, "G": 0.15, "T": 0.5}
    E = [{"A": 0.1, "C": 0.1, "G": 0.7, "T": 0.1},
         {"A": 0.7, "C": 0.1, "G": 0.1, "T": 0.1},
         {"A": 0.1, "C": 0.7, "G": 0.1, "T": 0.1}]

    def draw(self, rng, dist, n):
        keys = sorted(dist)
        return "".join(rng.choices(keys, [dist[k] for k in keys], k=n))

    def draw_exon(self, rng, n):
        return "".join(self.draw(rng, self.E[j % 3], 1) for j in range(n))

    def test_prefix_sums_match_direct_sums(self):
        rng = random.Random(23)
        x = "".join(rng.choice(DNA) for _ in range(40)) + "GTAAAAG"
        m = toy_gene_model(x, self.N, self.I, self.E, max_dur=50)
        for _ in range(100):
            a = rng.randrange(0, len(x))
            b = rng.randrange(a + 1, len(x) + 1)
            direct_n = sum(math.log(self.N[c]) for c in x[a:b])
            direct_e = sum(math.log(self.E[(i - a) % 3][x[i]]) for i in range(a, b))
            self.assertAlmostEqual(m.log_seg(0, a, b), direct_n, places=9)
            self.assertAlmostEqual(m.log_seg(1, a, b), direct_e, places=9)
            ok = x[a:a + 2] == "GT" and x[b - 2:b] == "AG"
            self.assertEqual(m.log_seg(2, a, b) > NEG, ok)

    def test_planted_gene(self):
        rng = random.Random(24)
        parts = [("N", self.draw(rng, self.N, 120)), ("E", self.draw_exon(rng, 90)),
                 ("I", "GT" + self.draw(rng, self.I, 60) + "AG"), ("E", self.draw_exon(rng, 60)),
                 ("N", self.draw(rng, self.N, 120))]
        x = "".join(p for _, p in parts)
        truth = "".join(s * len(p) for s, p in parts)
        m = toy_gene_model(x, self.N, self.I, self.E, max_dur=150)
        score, parse = ghmm_viterbi(m, len(x))
        self.assertGreater(score, NEG)
        self.assertEqual([s for s, _, _ in parse], ["N", "E", "I", "E", "N"])
        called = "".join(s * (b - a) for s, a, b in parse)
        agree = sum(1 for u, v in zip(truth, called) if u == v)
        self.assertGreater(agree / len(x), 0.95)
        intron = parse[2]
        self.assertEqual(x[intron[1]:intron[1] + 2], "GT")
        self.assertEqual(x[intron[2] - 2:intron[2]], "AG")

    def test_no_parse(self):
        # A sequence longer than any intergenic segment, and with no GT...AG and no
        # room for a gene, has no parse.
        m = toy_gene_model("A" * 12, self.N, self.I, self.E, max_dur=5, min_exon=20)
        self.assertEqual(ghmm_viterbi(m, 12), (NEG, None))


if __name__ == "__main__":
    unittest.main()
