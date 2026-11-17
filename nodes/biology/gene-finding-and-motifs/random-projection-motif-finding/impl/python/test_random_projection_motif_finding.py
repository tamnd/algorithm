# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-projection-motif-finding/. The authors are listed in prov/24V46J.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from bioseq import DNA, random_dna
from random_projection_motif_finding import (_encode, binomial_tail, hit_probability, letter_frequencies, oops_em,
                                             oops_score, projection, trials_needed)


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


def test_hit_probability_by_enumeration():
    for L in range(1, 9):
        for d in range(L + 1):
            for k in range(L + 1):
                # Over all k-sets of positions and all d-sets of changed positions.
                good = sum(1 for I in itertools.combinations(range(L), k)
                           for D in itertools.combinations(range(L), d) if not set(I) & set(D))
                assert hit_probability(L, d, k) == Fraction(good, math.comb(L, k) * math.comb(L, d))
    assert hit_probability(15, 4, 7) == Fraction(330, 6435)


def test_hit_probability_by_simulation():
    # Fresh motif copy and fresh projection in every round; tolerance z = 4.
    rng = random.Random(77)
    L, d, k, n, s, N = 15, 4, 7, 20, 4, 4000
    p = float(hit_probability(L, d, k))
    P = float(binomial_tail(n, hit_probability(L, d, k), s))
    single = enough = 0
    for _ in range(N):
        pos = set(rng.sample(range(L), k))
        hits = sum(1 for _ in range(n) if not pos & set(rng.sample(range(L), d)))
        single += hits
        enough += hits >= s
    assert abs(single / (N * n) - p) <= 4 * math.sqrt(p * (1 - p) / (N * n))
    assert abs(enough / N - P) <= 4 * math.sqrt(P * (1 - P) / N)


def test_binomial_tail_and_trials():
    p = Fraction(1, 3)
    assert binomial_tail(4, p, 0) == 1
    assert binomial_tail(4, p, 4) == Fraction(1, 81)
    assert binomial_tail(4, p, 3) == 4 * Fraction(2, 81) + Fraction(1, 81)
    for (n, L, d, k, s, q) in [(20, 15, 4, 7, 4, 0.95), (8, 10, 2, 5, 4, 0.95), (10, 12, 3, 6, 3, 0.99)]:
        m = trials_needed(n, L, d, k, s, q)
        P = float(binomial_tail(n, hit_probability(L, d, k), s))
        assert 1 - (1 - P) ** m >= q > 1 - (1 - P) ** (m - 1)
    assert trials_needed(20, 15, 4, 7, 4, 0.95) == 172


def test_oops_em_never_lowers_the_score():
    rng = random.Random(4)
    _, seqs, _ = plant(rng, 6, 40, 8, 1)
    X = _encode(seqs, 8)
    mu = letter_frequencies(seqs)
    for _ in range(3):
        theta = []
        for _ in range(8):
            row = [rng.random() + 0.05 for _ in range(4)]
            theta.append([x / sum(row) for x in row])
        _, history = oops_em(X, theta, mu, 1.0, 15)
        assert all(b >= a - 1e-9 for a, b in zip(history, history[1:]))
        # The penalized score of the proof, step by step from the random start.
        def penalized(t):
            return oops_score(X, t, mu) + sum(mu[a] * math.log(t[j][a]) for j in range(8) for a in range(4))
        before = penalized(theta)
        for _ in range(5):
            theta, _ = oops_em(X, theta, mu, 1.0, 1)
            after = penalized(theta)
            assert after >= before - 1e-9
            before = after


def test_draw_order():
    _, seqs, _ = plant(random.Random(2), 5, 30, 8, 1)
    r = projection(seqs, 8, 3, 4, s=3, seed=9)
    rng = random.Random(9)
    assert r.projections == tuple(tuple(sorted(rng.sample(range(8), 3))) for _ in range(4))
    assert r == projection(seqs, 8, 3, 4, s=3, seed=9)


def test_planted_success_rate():
    # (n, G, L, d) = (8, 60, 10, 2), k = 5, s = 4 and the 37 trials that give a
    # 0.95 chance of at least one good bucket. Measured on seeds 0 to 4: the
    # consensus equals the planted motif in 4 of 5 runs. The test asks for at least 3.
    T = trials_needed(8, 10, 2, 5, 4, 0.95)
    hits = 0
    for seed in range(5):
        motif, seqs, _ = plant(random.Random(seed), 8, 60, 10, 2)
        hits += projection(seqs, 10, 5, T, s=4, seed=seed).consensus == motif
    assert hits >= 3


def test_errors():
    with pytest.raises(ValueError):
        projection(["ACGT"], 5, 2, 1)
    with pytest.raises(ValueError):
        projection(["ACGTACGT"], 4, 5, 1)
    with pytest.raises(ValueError):
        projection(["ACGTACGT"], 4, 2, 0)
    with pytest.raises(ValueError):
        projection(["ACGTACGT", "TTTTACGA"], 4, 2, 1, s=3)
    with pytest.raises(ValueError):
        trials_needed(20, 15, 4, 7, 4, 1.0)
    with pytest.raises(ValueError):
        hit_probability(4, 5, 2)
