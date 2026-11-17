# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pseudoalignment/. The authors are listed in prov/6KKBA9.jsonl.

import random

from bioseq import mutate, random_dna, revcomp, simulate_reads
from pseudoalignment import PseudoIndex, equivalence_classes, naive_pseudoalign, pseudoalign

X, E, Y = "CAGAACC", "TGCTGT", "GACATAA"


def spell(run):
    return run[0] + "".join(x[-1] for x in run[1:])


def test_worked_example():
    t = [X + E + Y, X + Y]
    idx = PseudoIndex(t, 5)
    forward = {spell(c): sorted(col) for c, col in zip(idx.contigs, idx.contig_color)}
    assert forward["CAGAACC"] == [0, 1]
    assert forward["AACCTGCTGTGACA"] == [0]
    assert forward["AACCGACA"] == [1]
    assert forward["GACATAA"] == [0, 1]
    assert len(idx.contigs) == 8
    read = t[0][1:19]
    assert read == "AGAACCTGCTGTGACATA"
    trace = []
    assert pseudoalign(idx, read, trace) == {0}
    assert trace == [0, 2, 12]
    trace = []
    assert pseudoalign(idx, t[1], trace) == {1}
    assert trace == [0, 3, 7]
    # The reverse strand gives the same set.
    assert pseudoalign(idx, revcomp(read)) == {0}
    # A read that holds only shared k-mers fits both.
    assert pseudoalign(idx, X) == {0, 1}
    # A read with no k-mer in the index is not mapped.
    assert pseudoalign(idx, "TTTTTTTTTT") == frozenset()


def random_transcripts(rng):
    exons = [random_dna(rng, rng.randint(8, 30)) for _ in range(rng.randint(3, 6))]
    out = []
    for _ in range(rng.randint(2, 5)):
        pick = [e for e in exons if rng.random() < 0.6] or [exons[0]]
        out.append("".join(pick))
    return out


def check_contigs(idx):
    seen = set()
    for c, col in zip(idx.contigs, idx.contig_color):
        for a, b in zip(c, c[1:]):
            assert a[1:] == b[:-1]
            assert idx.successors(a) == [b] and idx.predecessors(b) == [a]
        for x in c:
            assert idx.color[x] == col and x not in seen
            seen.add(x)
    assert seen == set(idx.color)


def test_contigs_partition_the_kmers():
    rng = random.Random(1)
    for _ in range(150):
        t = random_transcripts(rng)
        check_contigs(PseudoIndex(t, rng.choice([3, 4, 5, 7])))


def test_error_free_reads_equal_naive_and_hold_the_source():
    rng = random.Random(2)
    for _ in range(80):
        t = random_transcripts(rng)
        k = rng.choice([5, 7, 9])
        idx = PseudoIndex(t, k)
        for src, seq in enumerate(t):
            if len(seq) < 12:
                continue
            for r in simulate_reads(rng, seq, 10, min(len(seq), 25), 0.0):
                got = pseudoalign(idx, r.read)
                assert got == naive_pseudoalign(idx, r.read)
                assert src in got


def test_reads_with_errors_give_a_superset_of_naive():
    rng = random.Random(3)
    for _ in range(80):
        t = random_transcripts(rng)
        idx = PseudoIndex(t, rng.choice([3, 4, 5]))
        for seq in t:
            if len(seq) < 12:
                continue
            for r in simulate_reads(rng, seq, 10, min(len(seq), 25), 0.08):
                assert pseudoalign(idx, r.read) >= naive_pseudoalign(idx, r.read)


def test_naive_set_holds_exactly_the_transcripts_with_all_kmers():
    rng = random.Random(4)
    for _ in range(60):
        t = random_transcripts(rng)
        k = 6
        idx = PseudoIndex(t, k)
        for _ in range(10):
            src = rng.randrange(len(t))
            seq = t[src]
            if len(seq) < 15:
                continue
            a = rng.randrange(len(seq) - 14)
            read = seq[a:a + 15]
            want = {j for j, s in enumerate(t)
                    if all(x in s or x in revcomp(s) for x in (read[i:i + k] for i in range(15 - k + 1)))}
            assert naive_pseudoalign(idx, read) == want == pseudoalign(idx, read)


def test_skipping_saves_lookups():
    rng = random.Random(5)
    t = [random_dna(rng, 300) for _ in range(3)]
    t.append(t[0][:150] + t[1][150:])
    idx = PseudoIndex(t, 21)
    total = lookups = 0
    for seq in t:
        for r in simulate_reads(rng, seq, 50, 100, 0.0):
            trace = []
            pseudoalign(idx, r.read, trace)
            lookups += len(trace)
            total += 100 - 21 + 1
    assert lookups * 5 < total


def test_equivalence_classes():
    t = [X + E + Y, X + Y]
    idx = PseudoIndex(t, 5)
    reads = [X + E + Y, X + Y, X, Y, "TTTTTTTT", revcomp(X + Y)]
    assert equivalence_classes(idx, reads) == [((0,), 1), ((0, 1), 2), ((1,), 2)]


def test_cycles_are_cut():
    # A transcript made of a repeated unit gives a cycle of k-mers with no branch.
    idx = PseudoIndex(["ACGTTACGTTACGTT"], 4)
    check_contigs(idx)
    rng = random.Random(6)
    for _ in range(50):
        unit = random_dna(rng, rng.randint(5, 9))
        idx = PseudoIndex([unit * 4], 4)
        check_contigs(idx)
        read = mutate(rng, (unit * 4)[2:2 + 2 * len(unit)], 0.0)
        assert pseudoalign(idx, read) == naive_pseudoalign(idx, read) == {0}
