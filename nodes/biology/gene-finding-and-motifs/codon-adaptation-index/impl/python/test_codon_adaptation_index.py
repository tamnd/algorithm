# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/codon-adaptation-index/. The authors are listed in prov/QCTP6D.jsonl.
"""Tests of the codon adaptation index."""

import math
import random
import unittest
from fractions import Fraction

from bioseq import CODON_TABLE, STOPS
from codon_adaptation_index import (ZERO_COUNT, cai, codon_counts, counted_codons,
                                    relative_adaptiveness, synonym_families)

FAM = synonym_families()
SENSE = sorted(c for c in CODON_TABLE if c not in STOPS)


def random_gene(rng, n, prefer=None, bias=0.0):
    """n random sense codons. With probability bias a codon is the preferred
    codon of its amino acid (prefer maps an amino acid to a codon)."""
    out = []
    for _ in range(n):
        c = rng.choice(SENSE)
        if prefer is not None and rng.random() < bias:
            c = prefer[CODON_TABLE[c]]
        out.append(c)
    return "".join(out)


def cai_rscu(gene, reference):
    """Sharp and Li eqs [1] and [3] to [5]: CAI_obs / CAI_max from RSCU values."""
    X = codon_counts(reference)
    Xf = {c: (Fraction(x) if x else ZERO_COUNT) for c, x in X.items()}
    rscu, rscu_max = {}, {}
    for aa, cods in FAM.items():
        mean = sum(Xf[c] for c in cods) / len(cods)
        for c in cods:
            rscu[c] = Xf[c] / mean
        for c in cods:
            rscu_max[c] = max(rscu[d] for d in cods)
    cods = [c for c in counted_codons(gene, rscu)]
    L = len(cods)
    obs = math.exp(sum(math.log(rscu[c]) for c in cods) / L)
    best = math.exp(sum(math.log(rscu_max[c]) for c in cods) / L)
    return obs / best


def cai_usage_table(gene, w):
    """Sharp and Li eq [8]: the sum over the codon usage table of the gene."""
    f = {}
    for c in counted_codons(gene, w):
        f[c] = f.get(c, 0) + 1
    L = sum(f.values())
    return math.exp(sum(n * math.log(w[c]) for c, n in f.items()) / L)


class TestWeights(unittest.TestCase):
    REF = ["GCT" * 4 + "AAA" * 2 + "GCC", "GCT" * 2 + "GCC" * 2 + "GCA" + "AAA" * 2 + "AAG"]

    def test_toy_table(self):
        w = relative_adaptiveness(self.REF)
        self.assertEqual(w["GCT"], 1)
        self.assertEqual(w["GCC"], Fraction(1, 2))
        self.assertEqual(w["GCA"], Fraction(1, 6))
        self.assertEqual(w["GCG"], Fraction(1, 12))
        self.assertEqual(w["AAA"], 1)
        self.assertEqual(w["AAG"], Fraction(1, 4))

    def test_unused_amino_acid_gets_weight_one(self):
        w = relative_adaptiveness(self.REF)
        for c in FAM["L"] + FAM["M"] + FAM["W"]:
            self.assertEqual(w[c], 1)

    def test_weights_in_unit_interval_with_a_one_per_family(self):
        rng = random.Random(1)
        ref = [random_gene(rng, 200) for _ in range(5)]
        w = relative_adaptiveness(ref)
        self.assertEqual(set(w), set(SENSE))
        for aa, cods in FAM.items():
            self.assertTrue(all(0 < w[c] <= 1 for c in cods))
            self.assertEqual(max(w[c] for c in cods), 1)

    def test_stops_and_unknown_codons_are_not_counted(self):
        X = codon_counts(["ATGTAANNNGCTTGAGC"])
        self.assertEqual(sum(X.values()), 2)
        self.assertEqual(X["ATG"], 1)
        self.assertEqual(X["GCT"], 1)


class TestIndex(unittest.TestCase):
    def test_page_example(self):
        w = relative_adaptiveness(TestWeights.REF)
        gene = "ATGGCCAAGGCTAAAGCGTGGTAA"
        self.assertEqual(counted_codons(gene, w), ["GCC", "AAG", "GCT", "AAA", "GCG"])
        self.assertAlmostEqual(cai(gene, w), 96 ** (-1 / 5), places=12)
        self.assertAlmostEqual(cai(gene, w), 0.40137, places=5)

    def test_rpsU_start_with_table1_weights(self):
        # The first five codons of E. coli rpsU after the start, with the w values of
        # Sharp and Li (1987), Table 1: CCG 1.00, GTA 0.495, ATT 0.185, AAA 1.000.
        w = {c: Fraction(1) for c in SENSE}
        w["GTA"], w["ATT"] = Fraction("0.495"), Fraction("0.185")
        got = cai("CCGGTAATTAAAGTA", w)
        self.assertAlmostEqual(got, (0.495 * 0.185 * 0.495) ** 0.2, places=12)
        self.assertAlmostEqual(got, 0.5386, places=4)

    def test_power_equals_exact_product(self):
        rng = random.Random(2)
        ref = [random_gene(rng, 150) for _ in range(4)]
        w = relative_adaptiveness(ref)
        for _ in range(20):
            gene = random_gene(rng, rng.randrange(1, 40))
            cods = counted_codons(gene, w)
            if not cods:
                continue
            prod = Fraction(1)
            for c in cods:
                prod *= w[c]
            self.assertTrue(math.isclose(cai(gene, w) ** len(cods), float(prod), rel_tol=1e-9))

    def test_three_formulas_agree(self):
        rng = random.Random(3)
        for _ in range(10):
            ref = [random_gene(rng, rng.randrange(20, 120)) for _ in range(3)]
            w = relative_adaptiveness(ref)
            gene = random_gene(rng, 60)
            a = cai(gene, w)
            self.assertAlmostEqual(a, cai_rscu(gene, ref), places=12)
            self.assertAlmostEqual(a, cai_usage_table(gene, w), places=12)

    def test_range_and_optimal_gene(self):
        rng = random.Random(4)
        w = relative_adaptiveness([random_gene(rng, 300) for _ in range(3)])
        best = {aa: max(cods, key=lambda c: (w[c], c)) for aa, cods in FAM.items()}
        optimal = "".join(best[CODON_TABLE[c]] for c in _codons_of(random_gene(rng, 50)))
        self.assertAlmostEqual(cai(optimal, w), 1.0, places=12)
        for _ in range(20):
            v = cai(random_gene(rng, 30), w)
            self.assertTrue(0 < v <= 1)

    def test_order_of_codons_does_not_matter(self):
        rng = random.Random(5)
        w = relative_adaptiveness([random_gene(rng, 200)])
        cods = _codons_of(random_gene(rng, 40))
        a = cai("".join(cods), w)
        rng.shuffle(cods)
        self.assertAlmostEqual(a, cai("".join(cods), w), places=12)

    def test_single_codon_amino_acids_and_stops_skipped(self):
        w = relative_adaptiveness(TestWeights.REF)
        self.assertAlmostEqual(cai("GCC", w), 0.5, places=12)
        self.assertAlmostEqual(cai("ATGGCCTGGTGGTAGNNN", w), 0.5, places=12)
        with self.assertRaises(ValueError):
            cai("ATGTGGTAA", w)

    def test_biased_genes_score_higher(self):
        rng = random.Random(6)
        prefer = {aa: rng.choice(cods) for aa, cods in FAM.items()}
        ref = [random_gene(rng, 300, prefer, 0.8) for _ in range(5)]
        w = relative_adaptiveness(ref)
        high = [cai(random_gene(rng, 200, prefer, 0.8), w) for _ in range(10)]
        low = [cai(random_gene(rng, 200), w) for _ in range(10)]
        self.assertGreater(min(high), max(low))


def _codons_of(seq):
    return [seq[i:i + 3] for i in range(0, len(seq) - 2, 3)]


if __name__ == "__main__":
    unittest.main()
