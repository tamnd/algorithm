# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muscle/. The authors are listed in prov/VY1X3J.jsonl.

import itertools
import random
from fractions import Fraction

from muscle import (GAP, kimura_distance, kmer_distance, le_score, leaves, muscle, pair_score,
                    progressive, refine, sp_score, upgma)

EPS = 1e-9


def exact_sp(seqs):
    """Oracle: the maximum SP score, by dynamic programming over the k-dimensional lattice."""
    k = len(seqs)
    lens = [len(s) for s in seqs]
    best = {tuple([0] * k): 0.0}
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
            if best[v] + c > best.get(w, -1e18):
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


def is_alignment_of(rows, seqs):
    if len(rows) != len(seqs) or len({len(r) for r in rows}) > 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def rand_seq(rng, lo, hi, alpha="ACGT"):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def test_example():
    seqs = ["ACGGTGG", "ACGTGG", "ATGTTGC", "ACGTTG"]
    tree1 = upgma([[kmer_distance(a, b) for b in seqs] for a in seqs])
    assert tree1 == (2, (3, (0, 1)))
    cache = {}
    msa1 = progressive(tree1, seqs, cache)
    assert [msa1[i] for i in range(4)] == ["ACGGTGG-", "AC-GTGG-", "AT-GTTGC", "AC-GTTG-"]
    tree2 = upgma([[kimura_distance(msa1[i], msa1[j]) for j in range(4)] for i in range(4)])
    assert tree2 == ((0, 1), (2, 3))
    msa2 = progressive(tree2, seqs, cache)
    assert [msa2[i] for i in range(4)] == ["ACGGTGG", "AC-GTGG", "ATGTTGC", "ACGTTG-"]
    rows = muscle(seqs)
    assert rows == ["ACGGTGG", "ACG-TGG", "ATGTTGC", "ACGTTG-"]
    assert sp_score([msa2[i] for i in range(4)]) < sp_score(rows)
    assert abs(sp_score(rows) - exact_sp(seqs)) < EPS


def test_edges():
    assert muscle([]) == []
    assert muscle(["ACG"]) == ["ACG"]
    assert muscle(["AC", "AC", "AC"]) == ["AC", "AC", "AC"]
    assert is_alignment_of(muscle(["A", "", "AT"]), ["A", "", "AT"])


def test_kmer_distance_against_brute_force():
    rng = random.Random(4)
    for _ in range(300):
        x, y = rand_seq(rng, 0, 7), rand_seq(rng, 0, 7)
        xs = [x[i:i + 2] for i in range(len(x) - 1)]
        ys = [y[i:i + 2] for i in range(len(y) - 1)]
        shared = 0
        for t in xs:  # greedy matching of equal words is a maximum matching
            if t in ys:
                ys.remove(t)
                shared += 1
        denom = min(len(x), len(y)) - 1
        want = Fraction(1) if denom <= 0 else 1 - Fraction(shared, denom)
        assert kmer_distance(x, y) == want


def test_upgma_recovers_ultrametric_clusters():
    rng = random.Random(8)
    for _ in range(60):
        k = rng.randint(2, 7)
        groups = [frozenset([i]) for i in range(k)]
        height = {g: 0 for g in groups}
        true_sets = set()
        h = 0
        while len(groups) > 1:
            a, b = rng.sample(groups, 2)
            h += rng.randint(1, 4)
            g = a | b
            groups = [x for x in groups if x not in (a, b)] + [g]
            height[g] = h
            true_sets.add(g)
        d = [[Fraction(0)] * k for _ in range(k)]
        for i in range(k):
            for j in range(k):
                if i != j:
                    d[i][j] = 2 * min(height[g] for g in true_sets if i in g and j in g)
        t = upgma(d)
        got = set()

        def walk(x):
            if not isinstance(x, int):
                got.add(leaves(x))
                walk(x[0])
                walk(x[1])

        walk(t)
        assert got == true_sets


def test_le_score_on_single_rows_is_the_pair_score():
    for a in "ACGT":
        for b in "ACGT" + GAP:
            assert abs(le_score([a], [b]) - pair_score(a, b)) < EPS
            assert abs(le_score([b], [a]) - pair_score(b, a)) < EPS


def test_kimura_distance():
    assert kimura_distance("ACGT", "ACGT") == 0
    assert kimura_distance("A-GT", "ACGA") > 0
    assert kimura_distance("AAAA", "CCCC") == 3.0


def test_two_sequences_are_optimal():
    rng = random.Random(3)
    for _ in range(80):
        s, t = rand_seq(rng, 0, 4), rand_seq(rng, 0, 4)
        rows = muscle([s, t])
        best = max(sum(pair_score(x, y) for x, y in zip(a, b)) for a, b in all_pair_alignments(s, t))
        assert abs(sp_score(rows) - best) < EPS


def test_refinement_never_decreases_sp_and_beats_nothing_optimal():
    rng = random.Random(2024)
    for _ in range(40):
        k = rng.choice([3, 3, 4])
        seqs = [rand_seq(rng, 1, 4 if k == 3 else 3, "ACG") for _ in range(k)]
        tree = upgma([[kmer_distance(a, b) for b in seqs] for a in seqs])
        start = progressive(tree, seqs, {})
        ids = sorted(start)
        refined = refine(dict(start), tree)
        before = sp_score([start[i] for i in ids])
        after = sp_score([refined[i] for i in ids])
        assert after >= before - EPS
        rows = muscle(seqs)
        assert is_alignment_of(rows, seqs)
        assert sp_score(rows) <= exact_sp(seqs) + EPS
