# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/branch-and-bound-motif-search/. The authors are listed in prov/6XQ8GR.jsonl.

import itertools
import random

import pytest

from bioseq import DNA, random_dna
from branch_and_bound_motif_search import (
    bb_median_string,
    bb_motif_search,
    consensus,
    motif_score,
    total_distance,
)

# Sample data of Rosalind problem BA2D (k = 3, t = 5).
SAMPLE = ["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"]


def windows(seqs, starts, L):
    return [s[q:q + L] for s, q in zip(seqs, starts)]


def brute_sites(seqs, L):
    """The lexicographically first tuple of starts with the smallest motif score."""
    ranges = [range(len(s) - L + 1) for s in seqs]
    return min(itertools.product(*ranges), key=lambda p: (motif_score(windows(seqs, p, L)), p))


def brute_median(seqs, L):
    """The first string in ACGT order with the smallest total distance."""
    pats = ("".join(t) for t in itertools.product(DNA, repeat=L))
    return min(pats, key=lambda v: (total_distance(v, seqs), [DNA.index(c) for c in v]))


def plant(rng, n, G, L, d):
    """Plant a random motif with exactly d changes in each of n random sequences.

    Draw order: random_dna for the motif; then for each sequence random_dna(G),
    rng.randrange(G - L + 1) for the start, rng.sample(range(L), d) for the
    changed positions, and one rng.choice per changed position.
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


def test_sample_sites():
    r = bb_motif_search(SAMPLE, 3)
    assert r.score == 2
    assert r.starts == (4, 4, 7, 3, 8)
    assert windows(SAMPLE, r.starts, 3) == ["TTC", "ATC", "TTC", "GTC", "TTC"]
    assert r.starts == brute_sites(SAMPLE, 3)
    assert r.nodes == 166


def test_sample_median():
    r = bb_median_string(SAMPLE, 3)
    assert r == ("CAA", 2, 45)
    assert brute_median(SAMPLE, 3) == "CAA"
    assert sorted(v for v in ("".join(t) for t in itertools.product(DNA, repeat=3))
                  if total_distance(v, SAMPLE) == 2) == ["CAA", "TCA", "TTC"]


def test_against_brute_force_random():
    rng = random.Random(2024)
    for _ in range(25):
        n = rng.randint(2, 4)
        L = rng.randint(2, 4)
        seqs = [random_dna(rng, rng.randint(L, 7)) for _ in range(n)]
        sites = bb_motif_search(seqs, L)
        med = bb_median_string(seqs, L)
        p = brute_sites(seqs, L)
        assert sites.starts == p
        assert sites.score == motif_score(windows(seqs, p, L))
        assert med.pattern == brute_median(seqs, L)
        assert med.distance == total_distance(med.pattern, seqs)
        # The equivalence: the smallest motif score equals the smallest total distance.
        assert sites.score == med.distance


def test_consensus_of_optimal_sites_is_a_median():
    rng = random.Random(7)
    for _ in range(15):
        seqs = [random_dna(rng, 8) for _ in range(3)]
        r = bb_motif_search(seqs, 3)
        v = consensus(windows(seqs, r.starts, 3))
        assert total_distance(v, seqs) == r.score


def test_pruning_on_planted_motif():
    rng = random.Random(11)
    motif, seqs, _ = plant(rng, 6, 40, 7, 1)
    r = bb_median_string(seqs, 7)
    full = sum(4 ** k for k in range(8))
    assert r.distance <= total_distance(motif, seqs) <= 6
    assert r.nodes < full // 10


def test_position_tree_prunes():
    rng = random.Random(3)
    _, seqs, _ = plant(rng, 4, 12, 4, 0)
    r = bb_motif_search(seqs, 4)
    assert r.score == 0
    assert r.nodes < sum(9 ** k for k in range(5))


def test_errors():
    with pytest.raises(ValueError):
        bb_motif_search(["ACG"], 4)
    with pytest.raises(ValueError):
        bb_median_string([], 2)
    with pytest.raises(ValueError):
        bb_median_string(["ACGN"], 2)
    with pytest.raises(ValueError):
        bb_motif_search(["ACGT"], 0)
