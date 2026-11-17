# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gibbs-motif-sampler/. The authors are listed in prov/2BA89G.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from bioseq import DNA, random_dna
from gibbs_motif_sampler import (background_from, column_counts, draw, gibbs_motif_sampler, log_target,
                                 site_weights)

TINY = ["ACGA", "CGAT", "TACG"]
TINY_L = 2
QF = {"A": Fraction(3, 10), "C": Fraction(2, 10), "G": Fraction(2, 10), "T": Fraction(3, 10)}


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


def rising(b, m):
    v = Fraction(1)
    for k in range(m):
        v *= b + k
    return v


def exact_target(seqs, starts, L, b, q):
    """pi(starts) up to a constant, exactly: prod over columns and letters of (b)_c, over prod of q of the sites."""
    windows = [s[p:p + L] for s, p in zip(seqs, starts)]
    v = Fraction(1)
    for col in column_counts(windows, L):
        for c in col:
            v *= rising(b, c)
    for w in windows:
        for a in w:
            v /= q[a]
    return v


def states(seqs, L):
    return list(itertools.product(*[range(len(s) - L + 1) for s in seqs]))


def conditional(seqs, L, b, q, state, i):
    """The full conditional of the site of sequence i from site_weights, normalized."""
    others = [s[p:p + L] for k, (s, p) in enumerate(zip(seqs, state)) if k != i]
    w = site_weights(seqs[i], column_counts(others, L), len(others), b, q)
    total = sum(w)
    return [x / total for x in w]


def chi2_sf_df4(x):
    # Survival function of the chi-square distribution with 4 degrees of freedom.
    return math.exp(-x / 2) * (1 + x / 2)


@pytest.mark.parametrize("b", [Fraction(1), Fraction(1, 2)])
def test_site_weights_are_the_exact_full_conditional(b):
    pi = {t: exact_target(TINY, t, TINY_L, b, QF) for t in states(TINY, TINY_L)}
    for t in pi:
        for i in range(len(TINY)):
            row = [pi[t[:i] + (x,) + t[i + 1:]] for x in range(len(TINY[i]) - TINY_L + 1)]
            total = sum(row)
            assert conditional(TINY, TINY_L, b, QF, t, i) == [r / total for r in row]


def test_both_scans_leave_the_target_invariant():
    b = Fraction(1)
    S = states(TINY, TINY_L)
    pi = {t: exact_target(TINY, t, TINY_L, b, QF) for t in S}
    z = sum(pi.values())
    pi = {t: v / z for t, v in pi.items()}
    n = len(TINY)
    kernels = []
    for i in range(n):
        K = {}
        for t in S:
            for x, p in enumerate(conditional(TINY, TINY_L, b, QF, t, i)):
                K[t, t[:i] + (x,) + t[i + 1:]] = p
        kernels.append(K)
    # Each single-site update (so the systematic scan, their product) keeps pi.
    for K in kernels:
        out = {u: sum(pi[t] * K.get((t, u), 0) for t in S) for u in S}
        assert out == pi
    # The random scan kernel is the average of the single-site kernels.
    out = {u: sum(pi[t] * sum(K.get((t, u), 0) for K in kernels) / n for t in S) for u in S}
    assert out == pi


def test_log_target_matches_the_weights():
    rng = random.Random(4)
    seqs = [random_dna(rng, 12) for _ in range(5)]
    L, b = 4, 1.0
    q = background_from(seqs)
    for _ in range(20):
        t = [rng.randrange(9) for _ in seqs]
        i = rng.randrange(5)
        others = [s[p:p + L] for k, (s, p) in enumerate(zip(seqs, t)) if k != i]
        w = site_weights(seqs[i], column_counts(others, L), 4, b, q)
        x, y = rng.randrange(9), rng.randrange(9)
        tx, ty = t[:i] + [x] + t[i + 1:], t[:i] + [y] + t[i + 1:]
        diff = log_target(seqs, tx, L, b, q) - log_target(seqs, ty, L, b, q)
        assert abs(diff - (math.log(w[x]) - math.log(w[y]))) < 1e-9


def test_draw_follows_the_weights():
    rng = random.Random(2024)
    weights = [1.0, 2.0, 3.0, 4.0, 5.0]
    N = 20000
    counts = [0] * 5
    for _ in range(N):
        counts[draw(rng, weights)] += 1
    expected = [N * w / 15 for w in weights]
    x = sum((c - e) ** 2 / e for c, e in zip(counts, expected))
    assert chi2_sf_df4(x) > 0.001


def test_start_draw_order_and_best_state():
    rng = random.Random(5)
    seqs = [random_dna(rng, 20) for _ in range(4)]
    r0 = gibbs_motif_sampler(seqs, 5, 0, seed=8)
    replay = random.Random(8)
    assert r0.starts == tuple(replay.randrange(16) for _ in seqs) and r0.iteration == 0
    r = gibbs_motif_sampler(seqs, 5, 30, seed=8)
    q = background_from(seqs)
    assert r.log_target == log_target(seqs, r.starts, 5, 1.0, q) >= r0.log_target
    assert r == gibbs_motif_sampler(seqs, 5, 30, seed=8)
    assert all(s[p:p + 5] == m for s, p, m in zip(seqs, r.starts, r.motifs))


def test_planted_success_rate():
    # Measured on seeds 0 to 9 with 100 iterations of the systematic scan: the
    # consensus equals the planted motif in 7 of 10 runs. The test asks for at least 5.
    hits = 0
    for seed in range(10):
        motif, seqs, _ = plant(random.Random(seed), 10, 100, 8, 1)
        hits += consensus(gibbs_motif_sampler(seqs, 8, 100, seed=seed).motifs) == motif
    assert hits >= 5


def test_errors():
    with pytest.raises(ValueError):
        gibbs_motif_sampler(["ACGT"], 2, 1)
    with pytest.raises(ValueError):
        gibbs_motif_sampler(["ACGT", "AC"], 3, 1)
    with pytest.raises(ValueError):
        gibbs_motif_sampler(["ACGT", "ACGT"], 2, 1, b=0)
    with pytest.raises(ValueError):
        gibbs_motif_sampler(["ACGT", "ACGT"], 2, 1, scan="other")
    with pytest.raises(ValueError):
        gibbs_motif_sampler(["ACGT", "ACGT"], 2, -1)
