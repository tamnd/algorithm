# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nei-gojobori-method/. The authors are listed in prov/10S5MW.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from bioseq import CODON_TABLE, DNA, STOPS
from nei_gojobori_method import codon_differences, codon_sites, jukes_cantor, nei_gojobori

SENSE = sorted(c for c in CODON_TABLE if c not in STOPS)


def test_codon_sites():
    assert codon_sites("TTA") == (F(2, 3), F(7, 3))
    assert codon_sites("GCT") == (F(1), F(2))
    assert codon_sites("CTA") == (F(4, 3), F(5, 3))
    assert codon_sites("ATG") == (F(0), F(3))
    assert codon_sites("TGG") == (F(0), F(3))
    # AGA: CGA is Arg, TGA is a stop (nonsynonymous), AGG is Arg.
    assert codon_sites("AGA") == (F(2, 3), F(7, 3))
    assert len(SENSE) == 61
    assert sum(codon_sites(c)[0] for c in SENSE) == F(134, 3)


def test_sites_match_the_neighbours():
    # 3 s(c) is the number of the nine one-base neighbours of c that code the same amino acid.
    for c in SENSE:
        same = 0
        for i in range(3):
            for b in DNA:
                if b != c[i] and CODON_TABLE[c[:i] + b + c[i + 1:]] == CODON_TABLE[c]:
                    same += 1
        assert 3 * codon_sites(c)[0] == same


def test_codon_differences():
    assert codon_differences("TTT", "GTA") == (F(1, 2), F(3, 2))
    assert codon_differences("CTT", "CTC") == (F(1), F(0))
    assert codon_differences("GAA", "GAT") == (F(0), F(1))
    assert codon_differences("AAA", "AAA") == (F(0), F(0))
    # TTT to CAA: the pathway TTT, TAT, TAA passes a stop codon.
    assert codon_differences("TTT", "CAA") == (F(1, 2), F(5, 2))
    assert codon_differences("TTT", "CAA", skip_stop_paths=False) == (F(1, 3), F(8, 3))


def brute_differences(x, y):
    pos = [i for i in range(3) if x[i] != y[i]]
    rows = []
    for order in itertools.permutations(pos):
        cur, syn, stop = x, 0, False
        for i in order:
            nxt = cur[:i] + y[i] + cur[i + 1:]
            stop |= nxt in STOPS
            syn += CODON_TABLE[nxt] == CODON_TABLE[cur]
            cur = nxt
        rows.append((syn, len(pos) - syn, stop))
    kept = [r for r in rows if not r[2]] or rows
    return F(sum(r[0] for r in kept), len(kept)), F(sum(r[1] for r in kept), len(kept)), len(pos)


def test_all_codon_pairs():
    for x in SENSE:
        for y in SENSE:
            sd, nd = codon_differences(x, y)
            bsd, bnd, k = brute_differences(x, y)
            assert (sd, nd) == (bsd, bnd)
            assert sd + nd == k
            assert codon_differences(y, x) == (sd, nd)


def test_example():
    x = "ATGGCTTTACCTGAAAAAGGGTGGTTTCAT"
    y = "ATGGCCCTACCTGATAAAGGATGGGTACAT"
    r = nei_gojobori(x, y)
    assert r.codons == 10
    assert r.syn_sites == F(17, 3) and r.nonsyn_sites == F(73, 3)
    assert r.syn_diffs == F(7, 2) and r.nonsyn_diffs == F(5, 2)
    assert r.p_s == pytest.approx(21 / 34)
    assert r.p_n == pytest.approx(15 / 146)
    assert r.d_s == pytest.approx(-0.75 * math.log(1 - 4 * 21 / 34 / 3))
    assert r.d_n == pytest.approx(0.1104935, abs=1e-6)
    assert r.omega == pytest.approx(r.d_n / r.d_s)


def test_jukes_cantor():
    assert jukes_cantor(0.0) == 0.0
    assert jukes_cantor(0.3) == pytest.approx(-0.75 * math.log(0.6))
    assert jukes_cantor(0.75) is None
    with pytest.raises(ValueError):
        jukes_cantor(-0.1)


def test_identical_and_special_cases():
    rng = random.Random(5)
    seq = "".join(rng.choice(SENSE) for _ in range(50))
    r = nei_gojobori(seq, seq)
    assert r.d_s == 0.0 and r.d_n == 0.0 and r.omega is None
    assert r.syn_sites + r.nonsyn_sites == 150
    # Gaps and N are left out; lower case is accepted.
    r2 = nei_gojobori("atgNNNtta---", "ATGAAACTAGGG")
    assert r2.codons == 2 and r2.syn_diffs == 1
    with pytest.raises(ValueError):
        nei_gojobori("ATGTAA", "ATGTTA")
    with pytest.raises(ValueError):
        nei_gojobori("ATGT", "ATGT")


def test_only_synonymous_or_only_nonsynonymous_changes():
    rng = random.Random(11)
    a, b, c = [], [], []
    syn = non = 0
    for _ in range(200):
        x = rng.choice(SENSE)
        others = [x[:i] + d + x[i + 1:] for i in range(3) for d in DNA if d != x[i]]
        same = [y for y in others if CODON_TABLE[y] == CODON_TABLE[x]]
        diff = [y for y in others if y not in STOPS and CODON_TABLE[y] != CODON_TABLE[x]]
        a.append(x)
        b.append(rng.choice(same) if same else x)
        c.append(rng.choice(diff))
        syn += bool(same)
        non += 1
    r = nei_gojobori("".join(a), "".join(b))
    assert r.nonsyn_diffs == 0 and r.syn_diffs == syn and r.d_n == 0.0
    r = nei_gojobori("".join(a), "".join(c))
    assert r.syn_diffs == 0 and r.nonsyn_diffs == non and r.d_s == 0.0
