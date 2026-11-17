# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orf-finding/. The authors are listed in prov/1C4YKG.jsonl.
"""Tests of the ORF finder and of the shared helper bioseq.py."""

import itertools
import math
import random
import unittest

import bioseq
from bioseq import (CODON_TABLE, DNA, STOPS, gc_content, global_align, hamming, kmers,
                    mutate, phred_to_prob, prob_to_phred, random_dna, revcomp,
                    semiglobal_align, simulate_reads, translate)
from orf_finding import Orf, find_orfs, longest_orf, orf_sequence


# ---------------------------------------------------------------- bioseq


def all_alignments(a, b):
    """Every alignment of a and b as a list of ops in M, I, D (brute force)."""
    if not a and not b:
        yield []
        return
    if a and b:
        for rest in all_alignments(a[1:], b[1:]):
            yield ["M"] + rest
    if a:
        for rest in all_alignments(a[1:], b):
            yield ["I"] + rest
    if b:
        for rest in all_alignments(a, b[1:]):
            yield ["D"] + rest


def score_ops(a, b, ops, match, mismatch, gap):
    i = j = 0
    total = 0
    for op in ops:
        if op == "M":
            total += match if a[i] == b[j] else mismatch
            i, j = i + 1, j + 1
        elif op == "I":
            total += gap
            i += 1
        else:
            total += gap
            j += 1
    assert i == len(a) and j == len(b)
    return total


def expand(cigar):
    ops, num = [], ""
    for ch in cigar:
        if ch.isdigit():
            num += ch
        else:
            ops.extend(ch * int(num))
            num = ""
    return ops


class TestBioseq(unittest.TestCase):
    def test_genetic_code(self):
        self.assertEqual(len(CODON_TABLE), 64)
        self.assertEqual(sum(1 for aa in CODON_TABLE.values() if aa != "*"), 61)
        self.assertEqual(STOPS, frozenset({"TAA", "TAG", "TGA"}))
        self.assertEqual(CODON_TABLE["ATG"], "M")
        self.assertEqual(CODON_TABLE["TGG"], "W")
        self.assertEqual(CODON_TABLE["TTT"], "F")
        self.assertEqual(CODON_TABLE["GGG"], "G")
        self.assertEqual(CODON_TABLE["AGA"], "R")
        self.assertEqual(len(set(CODON_TABLE.values()) - {"*"}), 20)
        # the number of codons of each amino acid (degeneracy) in table 1
        counts = {}
        for aa in CODON_TABLE.values():
            counts[aa] = counts.get(aa, 0) + 1
        self.assertEqual((counts["L"], counts["S"], counts["R"]), (6, 6, 6))
        self.assertEqual((counts["M"], counts["W"], counts["I"]), (1, 1, 3))

    def test_translate(self):
        self.assertEqual(translate("ATGGCCTAA"), "MA*")
        self.assertEqual(translate("CATGGCCTAAG", 1), "MA*")
        self.assertEqual(translate("ATGNNN"), "MX")
        self.assertEqual(translate("ATGGC"), "M")
        with self.assertRaises(ValueError):
            translate("ATG", 3)

    def test_revcomp(self):
        rng = random.Random(1)
        self.assertEqual(revcomp("AACGTT"), "AACGTT")
        self.assertEqual(revcomp("ATGC"), "GCAT")
        for _ in range(50):
            s = random_dna(rng, rng.randrange(0, 40))
            self.assertEqual(revcomp(revcomp(s)), s)

    def test_phred(self):
        self.assertAlmostEqual(phred_to_prob(20), 0.01, places=15)
        self.assertAlmostEqual(phred_to_prob(30), 0.001, places=15)
        self.assertAlmostEqual(prob_to_phred(0.05), 13.0103, places=4)
        for q in (0, 10, 20, 30, 40):
            self.assertAlmostEqual(prob_to_phred(phred_to_prob(q)), q, places=9)

    def test_small_functions(self):
        self.assertEqual(hamming("ACGT", "ACCA"), 2)
        with self.assertRaises(ValueError):
            hamming("A", "AC")
        self.assertEqual(kmers("ACGTA", 3), ["ACG", "CGT", "GTA"])
        self.assertEqual(kmers("AC", 3), [])
        self.assertEqual(gc_content("GGCA"), 0.75)
        self.assertEqual(gc_content(""), 0.0)

    def test_random_dna_and_mutate(self):
        rng = random.Random(7)
        n = 10000
        s = random_dna(rng, n, gc=0.6)
        self.assertEqual(set(s) <= set(DNA), True)
        # GC count is Binomial(n, 0.6): mean n p, variance n p (1 - p)
        p = 0.6
        self.assertLessEqual(abs(gc_content(s) * n - n * p), 4 * math.sqrt(n * p * (1 - p)))
        self.assertEqual(random_dna(random.Random(3), 50), random_dna(random.Random(3), 50))
        m = mutate(rng, s, 0.1)
        d = hamming(s, m)
        self.assertLessEqual(abs(d - n * 0.1), 4 * math.sqrt(n * 0.1 * 0.9))
        self.assertEqual(mutate(rng, s, 0.0), s)
        self.assertEqual(hamming(s, mutate(rng, s, 1.0)), n)

    def test_simulate_reads(self):
        rng = random.Random(11)
        genome = random_dna(rng, 2000)
        reads = simulate_reads(rng, genome, 300, 50, 0.0)
        strands = set()
        for r in reads:
            read, pos, strand, true_seq = r
            frag = genome[pos:pos + 50]
            self.assertEqual(true_seq, frag if strand == "+" else revcomp(frag))
            self.assertEqual(read, true_seq)
            strands.add(strand)
        self.assertEqual(strands, {"+", "-"})
        noisy = simulate_reads(rng, genome, 200, 50, 0.05)
        errors = sum(hamming(r.read, r.true_seq) for r in noisy)
        total = 200 * 50
        self.assertLessEqual(abs(errors - total * 0.05), 4 * math.sqrt(total * 0.05 * 0.95))

    def test_alignment_against_brute_force(self):
        rng = random.Random(5)
        for match, mismatch, gap in ((1, -1, -1), (2, -1, -2), (1, 0, -1)):
            for _ in range(60):
                a = random_dna(rng, rng.randrange(0, 6))
                b = random_dna(rng, rng.randrange(0, 6))
                best = max(score_ops(a, b, ops, match, mismatch, gap) for ops in all_alignments(a, b))
                score, cigar = global_align(a, b, match, mismatch, gap)
                self.assertEqual(score, best)
                self.assertEqual(score_ops(a, b, expand(cigar), match, mismatch, gap), score)
                # semiglobal: all of a against the best substring of b
                best_sg = max(
                    max(score_ops(a, b[s:e], ops, match, mismatch, gap) for ops in all_alignments(a, b[s:e]))
                    for s in range(len(b) + 1) for e in range(s, len(b) + 1))
                sc, cg, start = semiglobal_align(a, b, match, mismatch, gap, with_start=True)
                self.assertEqual(sc, best_sg)
                self.assertEqual(semiglobal_align(a, b, match, mismatch, gap), (sc, cg))
                ops = expand(cg)
                used = sum(1 for op in ops if op != "I")
                self.assertEqual(score_ops(a, b[start:start + used], ops, match, mismatch, gap), sc)

    def test_alignment_cases(self):
        self.assertEqual(global_align("ACGT", "ACGT"), (4, "4M"))
        self.assertEqual(global_align("ACGT", "AGT"), (2, "1M1I2M"))
        self.assertEqual(global_align("", "AC"), (-2, "2D"))
        self.assertEqual(semiglobal_align("CGT", "AACGTAA", with_start=True), (3, "3M", 2))


# ---------------------------------------------------------------- ORF finding


def naive_orfs(seq, min_codons, mode="start-stop", starts=("ATG",)):
    """All ORFs by a direct check of every pair of codon positions in the six frames."""
    s = seq.upper()
    G = len(s)
    out = set()
    for strand, t in (("+", s), ("-", revcomp(s))):
        stops = [j for j in range(G - 2) if t[j:j + 3] in STOPS]
        for j in stops:
            f = j % 3
            # the previous in-frame stop, or None
            prev = max((k for k in stops if k < j and k % 3 == f), default=None)
            lo = f if prev is None else prev + 3
            if mode == "start-stop":
                cands = [i for i in range(lo, j, 3) if t[i:i + 3] in starts]
                if not cands:
                    continue
                i = min(cands)
            else:
                i = lo
            n = (j - i) // 3
            if n >= min_codons:
                a, b = i, j + 3
                if strand == "-":
                    a, b = G - b, G - a
                out.add(Orf(strand, f, a, b, n))
    return sorted(out, key=lambda o: (o.start, o.end, o.strand, o.frame))


class TestOrfFinding(unittest.TestCase):
    def test_example_of_the_page(self):
        seq = "GATGAAAATGTTTTGACTAGGGCATCCATG"
        self.assertEqual(revcomp(seq), "CATGGATGCCCTAGTCAAAACATTTTCATC")
        self.assertEqual([translate(seq, f) for f in range(3)], ["DENVLTRASM", "MKMF*LGHP", "*KCFD*GIH"])
        self.assertEqual([translate(revcomp(seq), f) for f in range(3)], ["HGCPSQNIFI", "MDALVKTFS", "WMP*SKHFH"])
        orfs = find_orfs(seq, 0)
        self.assertEqual(orfs, [Orf("+", 1, 1, 16, 4), Orf("-", 2, 16, 25, 2)])
        self.assertEqual(orf_sequence(seq, orfs[0]), "ATGAAAATGTTTTGA")
        self.assertEqual(orf_sequence(seq, orfs[1]), "ATGCCCTAG")
        self.assertEqual(translate(orf_sequence(seq, orfs[1])), "MP*")
        self.assertEqual(find_orfs(seq, 3), [Orf("+", 1, 1, 16, 4)])
        self.assertEqual(longest_orf(seq), Orf("+", 1, 1, 16, 4))
        ss = find_orfs(seq, 0, mode="stop-stop")
        self.assertEqual(ss, [Orf("+", 1, 1, 16, 4), Orf("+", 2, 2, 5, 0), Orf("+", 2, 5, 20, 4),
                              Orf("-", 2, 16, 28, 3)])

    def test_against_naive_scan(self):
        rng = random.Random(2024)
        for trial in range(200):
            seq = random_dna(rng, rng.randrange(0, 120), gc=rng.choice((0.3, 0.5, 0.7)))
            for mode in ("start-stop", "stop-stop"):
                for k in (0, 3, 10):
                    self.assertEqual(find_orfs(seq, k, mode), naive_orfs(seq, k, mode))
        seq = random_dna(rng, 300)
        alt = ("ATG", "GTG", "TTG")
        self.assertEqual(find_orfs(seq, 5, starts=alt), naive_orfs(seq, 5, starts=alt))

    def test_orf_properties(self):
        rng = random.Random(99)
        seq = random_dna(rng, 3000)
        for o in find_orfs(seq, 20):
            protein = translate(orf_sequence(seq, o))
            self.assertEqual(protein[0], "M")
            self.assertEqual(protein[-1], "*")
            self.assertEqual(protein.count("*"), 1)
            self.assertEqual(len(protein) - 1, o.codons)
            self.assertEqual((o.end - o.start) % 3, 0)

    def test_planted_gene_is_found(self):
        rng = random.Random(3)
        sense = [c for c, aa in CODON_TABLE.items() if aa != "*" and c != "ATG"]
        gene = "ATG" + "".join(rng.choice(sense) for _ in range(149)) + "TAA"
        seq = random_dna(rng, 500) + revcomp(gene) + random_dna(rng, 500)
        hits = [o for o in find_orfs(seq, 100) if o.strand == "-" and o.start == 500]
        self.assertEqual(len(hits), 1)
        o = hits[0]
        # the frame on the minus strand is the offset of the ORF in revcomp(seq)
        self.assertEqual((o.end, o.codons, o.frame), (500 + len(gene), 150, (len(seq) - o.end) % 3))
        self.assertEqual(orf_sequence(seq, o), gene)

    def test_edge_cases(self):
        self.assertEqual(find_orfs("", 0), [])
        self.assertEqual(find_orfs("ATGAAA", 0), [])  # no stop: not an ORF
        self.assertEqual(find_orfs("ATGTAA", 0), [Orf("+", 0, 0, 6, 1)])  # revcomp TTACAT has no ATG
        self.assertEqual(find_orfs("TTACAT", 0), [Orf("-", 0, 0, 6, 1)])
        self.assertEqual(find_orfs("TAA", 0, mode="stop-stop"), [Orf("+", 0, 0, 3, 0)])
        self.assertIsNone(longest_orf("AAAAAA"))
        with self.assertRaises(ValueError):
            find_orfs("ATG", 0, mode="other")


if __name__ == "__main__":
    unittest.main()
