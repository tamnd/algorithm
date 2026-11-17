# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-alignment/. The authors are listed in prov/1P4EX1.jsonl.

import random
from itertools import combinations

from bioseq import mutate, random_dna, revcomp, semiglobal_align, simulate_reads
from selective_alignment import MATCH, MISMATCH, GAP, Hit, build_index, chain, selective_align

A, B, C = "TTCCTAAGAA", "ACGGATTAGG", "CCGGGTAACC"
DECOY = "GCAT" + "TTCCTACGAACCGTGTAACC" + "ACTT"


def test_worked_example():
    targets = [A + B + C, A + C, DECOY]
    decoy = [False, False, True]
    idx = build_index(targets, 5)
    r1, r2, r3 = (A + B)[:20], A + C, DECOY[4:24]
    assert selective_align(r1, targets, decoy, idx, 5) == [Hit(0, "+", 40, 0)]
    assert selective_align(r2, targets, decoy, idx, 5) == [Hit(1, "+", 40, 0)]
    assert selective_align(r3, targets, decoy, idx, 5) == []
    # The decoy copy differs from A + C at two places, so each scores 40 - 2 * 6 = 28 against the other.
    assert semiglobal_align(r2, DECOY, MATCH, MISMATCH, GAP)[0] == 28
    assert semiglobal_align(r3, A + C, MATCH, MISMATCH, GAP)[0] == 28
    # Without the decoy the read from the decoy is mapped to t2.
    idx2 = build_index(targets[:2], 5)
    assert selective_align(r3, targets[:2], decoy[:2], idx2, 5) == [Hit(1, "+", 28, 0)]
    # The reverse strand of r1 maps the same way.
    assert selective_align(revcomp(r1), targets, decoy, idx, 5) == [Hit(0, "-", 40, 0)]


def brute_chain(anchors, k, band):
    a = sorted(set(anchors), key=lambda x: (x[1], x[0]))
    best = 0
    for size in range(1, len(a) + 1):
        for sub in combinations(a, size):
            s, ok = k, True
            for (qi, ri), (qj, rj) in zip(sub, sub[1:]):
                gap = abs((rj - qj) - (ri - qi))
                if not (qi < qj and ri < rj and gap <= band):
                    ok = False
                    break
                s += min(qj - qi, rj - ri, k) - gap
            if ok:
                best = max(best, s)
    return best


def test_chain_against_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        k = rng.randint(3, 6)
        anchors = [(rng.randrange(20), rng.randrange(25)) for _ in range(rng.randint(1, 8))]
        band = rng.randint(0, 5)
        s, c = chain(anchors, k, band)
        assert s == brute_chain(anchors, k, band)
        total = k
        for (qi, ri), (qj, rj) in zip(c, c[1:]):
            gap = abs((rj - qj) - (ri - qi))
            assert qi < qj and ri < rj and gap <= band
            total += min(qj - qi, rj - ri, k) - gap
        assert total == s


def random_targets(rng):
    exons = [random_dna(rng, rng.randint(20, 60)) for _ in range(5)]
    tx = ["".join(e for e in exons if rng.random() < 0.6) or exons[0] for _ in range(3)]
    decoys = [mutate(rng, random_dna(rng, 10) + rng.choice(tx) + random_dna(rng, 10), 0.05)]
    return tx + decoys, [False] * len(tx) + [True]


def test_exact_reads_are_always_found_with_the_top_score():
    rng = random.Random(2)
    for _ in range(25):
        targets, decoy = random_targets(rng)
        idx = build_index(targets, 9)
        for src in range(3):
            seq = targets[src]
            if len(seq) < 30:
                continue
            for r in simulate_reads(rng, seq, 6, 30, 0.0):
                out = selective_align(r.read, targets, decoy, idx, 9)
                assert Hit(src, r.strand, 60, r.pos) in out or any(
                    h.target == src and h.score == 60 for h in out)


def test_returned_alignments_are_real_and_above_the_threshold():
    rng = random.Random(3)
    for _ in range(25):
        targets, decoy = random_targets(rng)
        idx = build_index(targets, 9)
        for src in range(3):
            seq = targets[src]
            if len(seq) < 30:
                continue
            for r in simulate_reads(rng, seq, 6, 30, 0.04):
                for h in selective_align(r.read, targets, decoy, idx, 9):
                    q = r.read if h.strand == "+" else revcomp(r.read)
                    assert not decoy[h.target]
                    assert h.score >= 0.65 * MATCH * len(q)
                    assert h.score <= semiglobal_align(q, targets[h.target], MATCH, MISMATCH, GAP)[0]
                    window = targets[h.target][h.start:h.start + len(q) + 8]
                    assert semiglobal_align(q, window, MATCH, MISMATCH, GAP)[0] >= h.score


def test_decoy_rule():
    rng = random.Random(4)
    for _ in range(40):
        tx = random_dna(rng, 60)
        copy = mutate(rng, tx, 0.04)
        targets, decoy = [tx, "GG" + copy + "CC"], [False, True]
        idx = build_index(targets, 7)
        read = copy[10:40]
        out = selective_align(read, targets, decoy, idx, 7)
        d = semiglobal_align(read, targets[1], MATCH, MISMATCH, GAP)[0]
        t = semiglobal_align(read, targets[0], MATCH, MISMATCH, GAP)[0]
        if d > t:
            assert out == []
        else:
            assert all(h.target == 0 for h in out)
        # A read that is the same in both is kept.
        if tx[40:60] == copy[40:60]:
            assert selective_align(tx[40:60], targets, decoy, idx, 7)


def test_random_reads_do_not_map():
    rng = random.Random(5)
    targets = [random_dna(rng, 500) for _ in range(4)]
    idx = build_index(targets, 11)
    for _ in range(100):
        assert selective_align(random_dna(rng, 50), targets, [False] * 4, idx, 11) == []


def test_reads_with_errors_are_mostly_found():
    rng = random.Random(6)
    found = total = 0
    targets = [random_dna(rng, 400) for _ in range(3)]
    idx = build_index(targets, 11)
    for src, seq in enumerate(targets):
        for r in simulate_reads(rng, seq, 40, 60, 0.02):
            total += 1
            found += any(h.target == src for h in selective_align(r.read, targets, [False] * 3, idx, 11))
    assert found >= 0.95 * total
