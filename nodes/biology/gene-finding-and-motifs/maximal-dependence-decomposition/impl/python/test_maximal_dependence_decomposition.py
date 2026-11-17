# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-dependence-decomposition/. The authors are listed in prov/7S803Q.jsonl.
"""Tests of maximal dependence decomposition."""

import itertools
import math
import random
import unittest
from fractions import Fraction

from bioseq import random_dna
from maximal_dependence_decomposition import (BASES, Leaf, Split, base_distribution, build_mdd,
                                              chi_squared, consensus, leaves, log_prob, prob)


def chi_float(sites, i, j, c):
    """The chi-squared statistic by the textbook formula, in floating point."""
    n = len(sites)
    obs = [[sum(1 for s in sites if (s[i] == c) == m and s[j] == b) for b in BASES] for m in (True, False)]
    rows = [sum(r) for r in obs]
    cols = [obs[0][k] + obs[1][k] for k in range(4)]
    t = 0.0
    for r in range(2):
        for k in range(4):
            e = rows[r] * cols[k] / n
            if e > 0:
                t += (obs[r][k] - e) ** 2 / e
    return t


def dependent_sites(rng, n):
    """Sites of length 6. Position 0 is G with probability 0.6; after a G at 0,
    position 3 is A with probability 0.85, otherwise position 3 is uniform.
    The other positions are independent."""
    out = []
    for _ in range(n):
        s = list(random_dna(rng, 6, 0.5))
        s[0] = "G" if rng.random() < 0.6 else rng.choice("ACT")
        if s[0] == "G" and rng.random() < 0.85:
            s[3] = "A"
        else:
            s[3] = rng.choice(BASES)
        out.append("".join(s))
    return out


class TestChiSquared(unittest.TestCase):
    def test_hand_example(self):
        # Position 0 against position 1, consensus G at 0. Matches GA, GA, GC; non-matches TC, TC, AT.
        sites = ["GA", "GA", "GC", "TC", "TC", "AT"]
        # Table: match row A2 C1 T0; other row A0 C2 T1. Column totals A2 C3 T1, n 6.
        # Expected 1, 1.5, 0.5 in each row. Sum of (O-E)^2/E = 2 * (1 + 1/6 + 1/2) = 10/3.
        self.assertEqual(chi_squared(sites, 0, 1, "G"), Fraction(10, 3))

    def test_matches_float_formula(self):
        rng = random.Random(31)
        for _ in range(20):
            sites = [random_dna(rng, 5, rng.random()) for _ in range(rng.randrange(2, 40))]
            c = consensus(sites)
            for i, j in itertools.permutations(range(5), 2):
                self.assertAlmostEqual(float(chi_squared(sites, i, j, c[i])), chi_float(sites, i, j, c[i]), places=9)

    def test_independent_columns_give_zero(self):
        # Every combination once: the indicator and the base are independent.
        sites = ["".join(p) for p in itertools.product(BASES, repeat=2)]
        self.assertEqual(chi_squared(sites, 0, 1, "A"), 0)


class TestTree(unittest.TestCase):
    def test_consensus(self):
        self.assertEqual(consensus(["GTA", "GTC", "ATC"]), "GTC")
        self.assertEqual(consensus(["AC", "CA"]), "AA")

    def test_planted_dependence_found_at_root(self):
        rng = random.Random(32)
        sites = dependent_sites(rng, 600)
        tree = build_mdd(sites, min_size=30)
        self.assertIsInstance(tree, Split)
        self.assertIn(tree.pos, (0, 3))
        c = consensus(sites)
        S = {i: sum(chi_float(sites, i, j, c[i]) for j in range(6) if j != i) for i in range(6)}
        self.assertEqual(tree.pos, max(range(6), key=lambda i: (S[i], -i)))
        self.assertEqual(sum(size for _, size in leaves(tree)), 600)

    def test_independent_sites_give_a_leaf(self):
        rng = random.Random(33)
        sites = [random_dna(rng, 5, 0.5) for _ in range(400)]
        tree = build_mdd(sites, cutoff=30.0)
        self.assertIsInstance(tree, Leaf)
        self.assertEqual(tree.positions, (0, 1, 2, 3, 4))

    def test_min_size_stops_the_split(self):
        rng = random.Random(34)
        sites = dependent_sites(rng, 600)
        self.assertIsInstance(build_mdd(sites, min_size=10 ** 6), Leaf)

    def test_probabilities_sum_to_one(self):
        rng = random.Random(35)
        sites = [s[:4] for s in dependent_sites(rng, 300)]
        tree = build_mdd(sites, min_size=10, cutoff=5.0)
        self.assertIsInstance(tree, Split)
        total = sum(prob("".join(x), tree) for x in itertools.product(BASES, repeat=4))
        self.assertEqual(total, 1)
        for x in ("GACA", "TTTT", "CGTA"):
            self.assertAlmostEqual(log_prob(x, tree), math.log(prob(x, tree)), places=12)

    def test_leaf_is_a_weight_matrix(self):
        sites = ["GTAAGT", "GTGAGT", "GTAAGA", "GTAGGT"]
        tree = build_mdd(sites, cutoff=1e9)
        x = "GTAAGT"
        expect = Fraction(1)
        for j in range(6):
            expect *= base_distribution(sites, j, Fraction(1, 2))[x[j]]
        self.assertEqual(prob(x, tree), expect)

    def test_mdd_beats_weight_matrix_on_dependent_data(self):
        rng = random.Random(36)
        train, test = dependent_sites(rng, 800), dependent_sites(rng, 400)
        mdd = build_mdd(train, min_size=30)
        wmm = build_mdd(train, cutoff=1e9)
        self.assertGreater(sum(log_prob(x, mdd) for x in test), sum(log_prob(x, wmm) for x in test))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            build_mdd([])
        with self.assertRaises(ValueError):
            build_mdd(["ACG", "AC"])
        with self.assertRaises(ValueError):
            build_mdd(["ACN"])


if __name__ == "__main__":
    unittest.main()
