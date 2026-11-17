# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/haplotype-based-variant-calling/. The authors are listed in prov/REPJDG.jsonl.

import math
import random

from bioseq import global_align, random_dna, revcomp, simulate_reads
from haplotype_based_variant_calling import affine_align, build_graph, call, haplotypes, pair_hmm, variants_of


def enumerate_pair_hmm(read, quals, hap, gap_open=1e-3, gap_ext=0.1):
    """P(read | hap) as the sum over every state path, listed one by one."""
    n, L = len(hap), len(read)
    trans = {("M", "M"): 1 - 2 * gap_open, ("M", "I"): gap_open, ("M", "D"): gap_open,
             ("I", "I"): gap_ext, ("I", "M"): 1 - gap_ext, ("D", "D"): gap_ext, ("D", "M"): 1 - gap_ext}

    def emit(i, j):
        e = 10 ** (-quals[i] / 10)
        return 1 - e if read[i] == hap[j] else e / 3

    total = 0.0

    def walk(i, j, state, p):
        # i read bases and j haplotype bases are used; state is the state of the last step.
        nonlocal total
        if i == L:
            if state in ("M", "I"):
                total += p
            return
        if j < n and (state, "M") in trans:
            walk(i + 1, j + 1, "M", p * trans[(state, "M")] * emit(i, j))
        if (state, "I") in trans:
            walk(i + 1, j, "I", p * trans[(state, "I")] * 0.25)
        if j < n and (state, "D") in trans:
            walk(i, j + 1, "D", p * trans[(state, "D")])

    for j in range(n):
        walk(1, j + 1, "M", emit(0, j) / n)
    return total


def normalize(ref, v):
    """Shift a VCF-style indel to the left as far as the reference allows."""
    pos, a, b = v
    while len(a) != len(b) and pos > 0 and a[-1] == b[-1]:
        pos -= 1
        a, b = ref[pos] + a[:-1], ref[pos] + b[:-1]
    return pos, a, b


def test_pair_hmm_against_path_enumeration():
    rng = random.Random(3)
    for _ in range(40):
        hap = random_dna(rng, rng.randint(1, 5))
        read = random_dna(rng, rng.randint(1, 4))
        quals = [rng.randint(5, 40) for _ in read]
        go, ge = rng.uniform(0.01, 0.2), rng.uniform(0.05, 0.5)
        got = pair_hmm(read, quals, hap, go, ge)
        want = enumerate_pair_hmm(read, quals, hap, go, ge)
        assert abs(math.exp(got) - want) <= 1e-12 * max(1.0, want)


def test_pair_hmm_prefers_the_source_haplotype():
    rng = random.Random(4)
    hap = random_dna(rng, 60)
    alt = hap[:30] + ("A" if hap[30] != "A" else "C") + hap[31:]
    read = alt[10:50]
    quals = [30] * 40
    assert pair_hmm(read, quals, alt) > pair_hmm(read, quals, hap) + 5
    # One mismatch at Q30 against a match: about ln((1 - e) / (e / 3)) = ln(2997) = 8.0.
    assert abs(pair_hmm(read, quals, alt) - pair_hmm(read, quals, hap) - math.log(0.999 / (0.001 / 3))) < 0.01


def test_graph_counts_and_bubble():
    ref = "ACGTTGCAAGTC"
    alt = "ACGTTGTAAGTC"
    reads = [alt, alt, ref[2:]]
    counts, ref_edges = build_graph(ref, reads, 4)
    assert counts[("TTGT", "TGTA")] == 2
    assert ("TTGC", "TGCA") in ref_edges
    assert haplotypes(ref, reads, 4) == [ref, alt]
    # With one supporting read the edge is pruned.
    assert haplotypes(ref, [alt, ref], 4) == [ref]


def test_repeated_kmer_raises():
    try:
        haplotypes("ACGTACGTAA", ["ACGTACGTAA"], 4)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def ops_score(a, b, ops, match, mismatch, go, ge):
    i = j = 0
    s, prev = 0, None
    for op in ops:
        if op == "M":
            s += match if a[i] == b[j] else mismatch
            i, j = i + 1, j + 1
        else:
            s += ge if op == prev else go
            if op == "I":
                i += 1
            else:
                j += 1
        prev = op
    assert (i, j) == (len(a), len(b))
    return s


def test_affine_align_against_linear_and_brute_force():
    rng = random.Random(6)
    for _ in range(60):
        a = random_dna(rng, rng.randint(0, 7))
        b = random_dna(rng, rng.randint(0, 7))
        # With equal open and extend scores the gaps are linear, and bioseq.global_align is an oracle.
        ops = affine_align(a, b, 1, -1, -1, -1)
        assert ops_score(a, b, ops, 1, -1, -1, -1) == global_align(a, b, 1, -1, -1)[0]
    for _ in range(40):
        a = random_dna(rng, rng.randint(0, 4))
        b = random_dna(rng, rng.randint(0, 4))
        ops = affine_align(a, b)
        best = max(ops_score(a, b, list(w), 2, -3, -6, -1) for w in all_alignments(len(a), len(b)))
        assert ops_score(a, b, ops, 2, -3, -6, -1) == best


def all_alignments(n, m):
    if n == 0 and m == 0:
        yield ""
        return
    if n and m:
        for w in all_alignments(n - 1, m - 1):
            yield w + "M"
    if n:
        for w in all_alignments(n - 1, m):
            yield w + "I"
    if m:
        for w in all_alignments(n, m - 1):
            yield w + "D"


def test_variants_of():
    ref = "GATTACAGGCATTCGA"
    assert variants_of(ref, ref) == []
    assert variants_of(ref[:5] + "G" + ref[6:], ref) == [(5, "C", "G")]
    assert variants_of(ref[:8] + ref[10:], ref) == [(7, "GGC", "G")]
    assert variants_of(ref[:9] + "TT" + ref[9:], ref) == [(8, "G", "GTT")]


def simulate(seed):
    rng = random.Random(seed)
    ref = random_dna(rng, 120)
    hom = "G" if ref[30] != "G" else "T"
    snp = "A" if ref[50] != "A" else "C"
    h1 = ref[:30] + hom + ref[31:50] + snp + ref[51:]
    h2 = ref[:30] + hom + ref[31:80] + ref[82:]
    reads = []
    for h in (h1, h2):
        for s in simulate_reads(rng, h, 24, 40, 0.01):
            reads.append(s.read if s.strand == "+" else revcomp(s.read))
    truth = {(30, ref[30], hom): 2, (50, ref[50], snp): 1, normalize(ref, (79, ref[79:82], ref[79])): 1}
    return ref, h1, h2, reads, truth


def test_simulated_diploid_sample():
    ref, h1, h2, reads, truth = simulate(2017)
    res = call(ref, reads, [[20] * len(r) for r in reads])
    got = {c["variant"]: c["genotype"] for c in res["calls"]}
    assert got == truth
    for c in res["calls"]:
        assert max(c["posterior"]) > 0.999
    # Reads of 40 bases join the sites at 50 and 80, so the best pair is the true phase.
    H = res["haplotypes"]
    assert {H[i] for i in res["best_pair"]} == {h1, h2}
    # Two independent bubbles and one fixed change give 2^3 = 8 paths.
    assert len(H) == 8


def test_no_variants_without_alt_reads():
    rng = random.Random(9)
    ref = random_dna(rng, 80)
    reads = [ref[s:s + 30] for s in range(0, 51, 5)]
    res = call(ref, reads, [[30] * 30 for _ in reads])
    assert res["haplotypes"] == [ref]
    assert res["calls"] == []
