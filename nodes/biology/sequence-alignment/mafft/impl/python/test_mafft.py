# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mafft/. The authors are listed in prov/4TVG52.jsonl.

import itertools
import random
from fractions import Fraction

from mafft import (GAP, anchors_for, chain_segments, column_vectors, correlation, find_segments,
                   group_align, mafft, pair_score, progressive, profile_nw, sp_score,
                   tuple_distance, upgma)


def exact_sp(seqs):
    """Oracle: the maximum SP score, by dynamic programming over the k-dimensional lattice."""
    k = len(seqs)
    lens = [len(s) for s in seqs]
    best = {tuple([0] * k): 0}
    moves = [m for m in itertools.product((0, 1), repeat=k) if any(m)]
    for v in sorted(itertools.product(*[range(n + 1) for n in lens]), key=sum):
        if v not in best:
            continue
        for m in moves:
            w = tuple(a + b for a, b in zip(v, m))
            if any(w[i] > lens[i] for i in range(k)):
                continue
            col = [seqs[i][v[i]] if m[i] else GAP for i in range(k)]
            c = sum(pair_score(col[i], col[j]) for i in range(k) for j in range(i + 1, k))
            if best[v] + c > best.get(w, -10 ** 9):
                best[w] = best[v] + c
    return best[tuple(lens)]


def all_pair_alignments(s, t):
    if not s and not t:
        yield "", ""
        return
    if s and t:
        for a, b in all_pair_alignments(s[1:], t[1:]):
            yield s[0] + a, t[0] + b
    if s:
        for a, b in all_pair_alignments(s[1:], t):
            yield s[0] + a, GAP + b
    if t:
        for a, b in all_pair_alignments(s, t[1:]):
            yield GAP + a, t[0] + b


def matched_pairs(a, b):
    """Residue index pairs (i, j) placed in the same column of a pairwise alignment."""
    out, i, j = set(), 0, 0
    for x, y in zip(a, b):
        if x != GAP and y != GAP:
            out.add((i, j))
        i += x != GAP
        j += y != GAP
    return out


def is_alignment_of(rows, seqs):
    if len(rows) != len(seqs) or len({len(r) for r in rows}) > 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def rand_seq(rng, lo, hi, alpha="ACGT"):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def test_example():
    seqs = ["AACCGGTTAC", "CCGGTTACAA", "ACCGGTAC"]
    assert upgma([[tuple_distance(a, b) for b in seqs] for a in seqs]) == (1, (0, 2))
    u, v = column_vectors([seqs[0]]), column_vectors([seqs[2]])
    c = correlation(u, v)
    assert round(c[-1]) == 6 and round(c[-2]) == 5
    assert find_segments(u, v, -1) == [(1, 0, 7, 6)]
    assert anchors_for([seqs[0]], [seqs[2]]) == [(4, 3)]
    pair = group_align([seqs[0]], [seqs[2]])
    assert pair == ["AACCGGTTAC", "-ACCGG-TAC"]
    assert anchors_for(pair, [seqs[1]]) == [(6, 4)]
    rows = mafft(seqs)
    assert rows == ["AACCGGTTAC--", "--CCGGTTACAA", "-ACCGG-TAC--"]
    assert sp_score(rows) == exact_sp(seqs) == 3


def test_edges():
    assert mafft([]) == []
    assert mafft(["ACG"]) == ["ACG"]
    assert mafft(["AC", "AC", "AC"]) == ["AC", "AC", "AC"]
    assert is_alignment_of(mafft(["A", "", "AT"]), ["A", "", "AT"])


def test_fft_correlation_matches_direct_sum():
    rng = random.Random(1)
    for _ in range(100):
        xs = [rand_seq(rng, 1, 5, "ACGT-") for _ in range(rng.randint(1, 3))]
        n = len(xs[0])
        xs = [(r + GAP * n)[:n] for r in xs]
        ys = [rand_seq(rng, 1, 6, "ACGT") for _ in range(rng.randint(1, 2))]
        ys = [(r * 6)[:len(ys[0])] for r in ys]
        u, v = column_vectors(xs), column_vectors(ys)
        c = correlation(u, v)
        for lag in range(-(len(u) - 1), len(v)):
            want = sum(sum(a * b for a, b in zip(u[i], v[i + lag]))
                       for i in range(len(u)) if 0 <= i + lag < len(v))
            assert abs(c[lag] - float(want)) < 1e-9


def test_chain_against_brute_force():
    rng = random.Random(2)
    for _ in range(200):
        segs = list({(rng.randint(0, 8), rng.randint(0, 8), rng.randint(1, 3), Fraction(rng.randint(1, 5)))
                     for _ in range(rng.randint(0, 6))})
        best = 0
        for r in range(1, len(segs) + 1):
            for sub in itertools.combinations(sorted(segs), r):
                if all(a[0] + a[2] <= b[0] and a[1] + a[2] <= b[1] for a, b in zip(sub, sub[1:])):
                    best = max(best, sum(s[3] for s in sub))
        got = chain_segments(segs)
        assert all(a[0] + a[2] <= b[0] and a[1] + a[2] <= b[1] for a, b in zip(got, got[1:]))
        assert sum(s[3] for s in got) == best


def test_anchored_pair_alignment_is_best_through_the_anchors():
    rng = random.Random(3)
    for _ in range(100):
        s, t = rand_seq(rng, 0, 5), rand_seq(rng, 0, 5)
        if rng.random() < 0.5:
            t = (s[rng.randint(0, 1):] + t[:2])[:5]
        s, t = s or "A", t or "C"
        rows = group_align([s], [t])
        anchors = set(anchors_for([s], [t]))
        assert is_alignment_of(rows, [s, t])
        assert anchors <= matched_pairs(*rows)
        best = max(sum(pair_score(x, y) for x, y in zip(a, b))
                   for a, b in all_pair_alignments(s, t) if anchors <= matched_pairs(a, b))
        assert sp_score(rows) == best


def test_profile_nw_on_two_rows_is_optimal():
    rng = random.Random(4)
    for _ in range(100):
        s, t = rand_seq(rng, 0, 5), rand_seq(rng, 0, 5)
        rows = profile_nw([s], [t])
        best = max(sum(pair_score(x, y) for x, y in zip(a, b)) for a, b in all_pair_alignments(s, t))
        assert sp_score(rows) == best


def test_tuple_distance():
    assert tuple_distance("ACGT", "ACGT") == 0
    assert tuple_distance("AAAA", "CCCC") == 1
    assert tuple_distance("ACCGGTAC", "AACCGGTTAC") == 0
    assert tuple_distance("A", "ACGT") == 1


def test_three_sequences_against_exact_sp():
    rng = random.Random(2024)
    for _ in range(40):
        seqs = [rand_seq(rng, 1, 5, "ACG") for _ in range(3)]
        rows = mafft(seqs)
        assert is_alignment_of(rows, seqs)
        assert sp_score(rows) <= exact_sp(seqs)
        tree = upgma([[tuple_distance(a, b) for b in seqs] for a in seqs])
        aln = progressive(tree, seqs)
        assert is_alignment_of([aln[i] for i in range(3)], seqs)


def test_longer_related_sequences_stay_valid():
    rng = random.Random(7)
    base = rand_seq(rng, 40, 40)
    seqs = []
    for _ in range(5):
        s = list(base)
        for _ in range(4):
            p = rng.randrange(len(s))
            op = rng.random()
            if op < 0.4:
                s[p] = rng.choice("ACGT")
            elif op < 0.7:
                del s[p]
            else:
                s.insert(p, rng.choice("ACGT"))
        seqs.append("".join(s))
    rows = mafft(seqs)
    assert is_alignment_of(rows, seqs)
