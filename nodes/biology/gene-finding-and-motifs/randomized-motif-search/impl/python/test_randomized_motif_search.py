# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-motif-search/. The authors are listed in prov/V85QPB.jsonl.

import itertools
import random

import pytest

from bioseq import DNA, random_dna
from randomized_motif_search import count_matrix, improve, most_probable, motif_score, randomized_motif_search

# Sample data of Rosalind problem BA2F (k = 8, t = 5).
SAMPLE = [
    "CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA",
    "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG",
    "TAGTACCGAGACCGAAAGAAGTATACAGGCGT",
    "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",
    "AATCCACCAGCTCCACGTGCAATGTTGGCCTA",
]
SAMPLE_ANSWER = ("TCTCGGGG", "CCAAGGTG", "TACAGGCG", "TTCAGGTG", "TCCACGTG")


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


def test_rosalind_ba2f_sample():
    # Score 9 is the optimum of this input (the branch and bound median search gives distance 9).
    r = randomized_motif_search(SAMPLE, 8, 1000, seed=0)
    assert r.motifs == SAMPLE_ANSWER
    assert r.score == motif_score(SAMPLE_ANSWER) == 9


def test_draw_order_and_best_of_runs():
    seqs = SAMPLE
    rng = random.Random(3)
    runs = []
    for _ in range(30):
        starts = [rng.randrange(len(s) - 8 + 1) for s in seqs]
        runs.append(improve(seqs, 8, starts))
    r = randomized_motif_search(seqs, 8, 30, seed=3)
    best = min(runs, key=lambda x: x.score)  # min keeps the first of equal scores
    assert (r.motifs, r.starts, r.score) == (best.motifs, best.starts, best.score)
    assert r.steps == tuple(x.steps for x in runs)


def test_each_run_ends_in_a_local_optimum_within_the_step_bound():
    rng = random.Random(7)
    for _ in range(60):
        n, L = rng.randint(2, 6), rng.randint(2, 6)
        seqs = [random_dna(rng, rng.randint(L, 20)) for _ in range(n)]
        starts = [rng.randrange(len(s) - L + 1) for s in seqs]
        start_score = motif_score([s[q:q + L] for s, q in zip(seqs, starts)])
        r = improve(seqs, L, starts)
        assert r.score == motif_score(r.motifs) <= start_score
        assert all(s[q:q + L] == m for s, q, m in zip(seqs, r.starts, r.motifs))
        assert r.steps <= start_score - r.score + 1 <= L * (n - (n + 3) // 4) + 1
        # One more profile step does not lower the score.
        counts = count_matrix(r.motifs, L)
        again = [s[q:q + L] for s in seqs for q in [most_probable(s, counts)]]
        assert motif_score(again) >= r.score


def test_score_is_never_below_the_optimum():
    rng = random.Random(9)
    for _ in range(20):
        seqs = [random_dna(rng, 7) for _ in range(3)]
        r = randomized_motif_search(seqs, 3, 20, seed=rng.randrange(1000))
        assert r.score >= brute_best_score(seqs, 3)


def test_planted_success_rate():
    # Measured on seeds 0 to 9 with 100 restarts: the consensus equals the
    # planted motif in 10 of 10 runs. The test asks for at least 8.
    hits = 0
    for seed in range(10):
        motif, seqs, _ = plant(random.Random(seed), 10, 100, 8, 1)
        hits += consensus(randomized_motif_search(seqs, 8, 100, seed=seed).motifs) == motif
    assert hits >= 8


def test_errors():
    with pytest.raises(ValueError):
        randomized_motif_search(["ACG"], 4, 1)
    with pytest.raises(ValueError):
        randomized_motif_search(["ACGT"], 2, 0)
    with pytest.raises(ValueError):
        randomized_motif_search(["ACGT"], 2, 1, pseudo=0)
    with pytest.raises(ValueError):
        improve(["ACGT", "ACGT"], 2, [0, 3])
    with pytest.raises(ValueError):
        randomized_motif_search([], 2, 1)
