# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-motif-search/. The authors are listed in prov/5WRFD0.jsonl.

import itertools
import random

import pytest

from bioseq import DNA, kmers, random_dna
from greedy_motif_search import count_matrix, greedy_motif_search, most_probable, motif_score

# Sample data of Rosalind problems BA2D and BA2E (k = 3, t = 5).
SAMPLE = ["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"]


def plant(rng, n, G, L, d):
    """Plant a random motif with exactly d changes in each of n random sequences.

    Draw order: random_dna for the motif; then for each sequence random_dna(G),
    rng.randrange(G - L + 1), rng.sample(range(L), d) and one rng.choice per
    changed position.
    """
    motif = random_dna(rng, L)
    seqs, starts = [], []
    for _ in range(n):
        bg = random_dna(rng, G)
        q = rng.randrange(G - L + 1)
        inst = list(motif)
        for j in rng.sample(range(L), d):
            inst[j] = rng.choice([b for b in DNA if b != inst[j]])
        seqs.append(bg[:q] + "".join(inst) + bg[q + L:])
        starts.append(q)
    return motif, seqs, starts


def consensus(windows):
    return "".join(max(DNA, key=lambda a: (col.count(a), -DNA.index(a))) for col in zip(*windows))


def brute_best_score(seqs, L):
    ranges = [range(len(s) - L + 1) for s in seqs]
    return min(motif_score([s[q:q + L] for s, q in zip(seqs, p)]) for p in itertools.product(*ranges))


def test_rosalind_ba2d_without_pseudocounts():
    r = greedy_motif_search(SAMPLE, 3)
    assert r.motifs == ("CAG", "CAG", "CAA", "CAA", "CAA")
    assert r.starts == (6, 6, 0, 5, 0)
    assert r.score == 2


def test_rosalind_ba2e_with_pseudocounts():
    r = greedy_motif_search(SAMPLE, 3, pseudo=1)
    assert r.motifs == ("TTC", "ATC", "TTC", "ATC", "TTC")
    assert r.score == 2


def test_most_probable_matches_float_profile():
    rng = random.Random(5)
    for _ in range(40):
        L = rng.randint(2, 5)
        rows = [random_dna(rng, L) for _ in range(rng.randint(1, 4))]
        seq = random_dna(rng, rng.randint(L, 15))
        pseudo = rng.randint(0, 1)
        counts = count_matrix(rows, L, pseudo)
        total = len(rows) + 4 * pseudo
        probs = []
        for w in kmers(seq, L):
            p = 1.0
            for j, a in enumerate(w):
                p *= counts[j][DNA.index(a)] / total
            probs.append(p)
        # The first window with the largest probability (exact ties come from equal products).
        assert most_probable(seq, counts) == probs.index(max(probs))


def test_not_optimal_without_pseudocounts():
    seqs = ["CAGAACCT", "GCTGTGAC", "ATAAACTA"]
    r = greedy_motif_search(seqs, 3)
    assert r.score == 2 and brute_best_score(seqs, 3) == 1
    # With one pseudocount the seed AAC reaches GAC, and the optimum is found.
    r1 = greedy_motif_search(seqs, 3, pseudo=1)
    assert r1.motifs == ("AAC", "GAC", "AAC") and r1.score == 1


def test_score_is_never_below_the_optimum():
    rng = random.Random(9)
    for _ in range(20):
        seqs = [random_dna(rng, 7) for _ in range(3)]
        for pseudo in (0, 1):
            r = greedy_motif_search(seqs, 3, pseudo)
            assert r.score == motif_score(r.motifs) >= brute_best_score(seqs, 3)
            assert all(s[q:q + 3] == m for s, q, m in zip(seqs, r.starts, r.motifs))


def test_planted_success_rate_with_pseudocounts():
    # Measured on seeds 0 to 9: the consensus equals the planted motif in 10 of 10
    # runs with pseudocount 1 and in 0 of 10 runs without. The test asks for at least 8 and at most 3.
    hits = {0: 0, 1: 0}
    for seed in range(10):
        motif, seqs, _ = plant(random.Random(seed), 10, 100, 8, 1)
        for pseudo in (0, 1):
            hits[pseudo] += consensus(greedy_motif_search(seqs, 8, pseudo).motifs) == motif
    assert hits[1] >= 8
    assert hits[0] <= 3


def test_errors():
    with pytest.raises(ValueError):
        greedy_motif_search(["ACG"], 4)
    with pytest.raises(ValueError):
        greedy_motif_search([], 2)
    with pytest.raises(ValueError):
        greedy_motif_search(["ACGT"], 2, pseudo=-1)
    with pytest.raises(ValueError):
        greedy_motif_search(["ACXT"], 2)
