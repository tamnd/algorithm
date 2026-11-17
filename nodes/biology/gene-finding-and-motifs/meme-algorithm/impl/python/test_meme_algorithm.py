# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meme-algorithm/. The authors are listed in prov/FD26PV.jsonl.

import math
import random

import pytest

from bioseq import DNA, random_dna
from meme_algorithm import (_encode, best_sites, consensus, e_step, letter_frequencies, m_step, meme, objective,
                            start_model)

# Sample data of Rosalind problem BA2F (k = 8, t = 5).
SAMPLE = [
    "CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA",
    "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG",
    "TAGTACCGAGACCGAAAGAAGTATACAGGCGT",
    "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",
    "AATCCACCAGCTCCACGTGCAATGTTGGCCTA",
]


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


def random_simplex(rng):
    v = [rng.random() + 1e-3 for _ in range(4)]
    s = sum(v)
    return [x / s for x in v]


def test_objective_never_decreases():
    r = meme(SAMPLE, 8)
    assert all(b >= a - 1e-9 for a, b in zip(r.objective, r.objective[1:]))
    rng = random.Random(3)
    for _ in range(4):
        seqs = [random_dna(rng, 15) for _ in range(4)]
        r = meme(seqs, 4, max_iter=60)
        assert all(b >= a - 1e-9 for a, b in zip(r.objective, r.objective[1:]))


def test_e_step_is_the_bayes_posterior_and_the_threshold():
    rng = random.Random(8)
    seqs = [random_dna(rng, 12) for _ in range(3)]
    X = _encode(seqs, 3)
    theta = [random_simplex(rng) for _ in range(3)]
    theta0 = random_simplex(rng)
    for lam in (0.05, 0.3, 0.7):
        z = e_step(X, theta, theta0, lam)
        for x, zk in zip(X, z):
            p1 = math.prod(theta[j][c] for j, c in enumerate(x))
            p0 = math.prod(theta0[c] for c in x)
            assert abs(zk - lam * p1 / (lam * p1 + (1 - lam) * p0)) < 1e-12
            llr = math.log(p1 / p0)
            cut = math.log((1 - lam) / lam)
            if abs(llr - cut) > 1e-9:
                assert (zk > 0.5) == (llr > cut)


def test_m_step_maximizes_the_expected_log_posterior():
    rng = random.Random(11)
    seqs = [random_dna(rng, 10) for _ in range(3)]
    L, beta = 3, 0.5
    X = _encode(seqs, L)
    mu = letter_frequencies(seqs)
    z = [rng.random() for _ in X]

    def q_value(theta, theta0, lam):
        v = 0.0
        for x, zk in zip(X, z):
            v += zk * (math.log(lam) + sum(math.log(theta[j][c]) for j, c in enumerate(x)))
            v += (1 - zk) * (math.log(1 - lam) + sum(math.log(theta0[c]) for c in x))
        v += sum(beta * mu[a] * math.log(theta[j][a]) for j in range(L) for a in range(4))
        v += sum(beta * mu[a] * math.log(theta0[a]) for a in range(4))
        return v

    theta, theta0, lam = m_step(X, z, L, beta, mu)
    top = q_value(theta, theta0, lam)
    for _ in range(200):
        t = [random_simplex(rng) for _ in range(L)]
        assert q_value(t, random_simplex(rng), rng.uniform(0.01, 0.99)) <= top
        # Small moves away from the M step values do not help either.
        eps = 1e-3
        t2 = [[p + eps * (1 if a == 0 else -1 / 3) for a, p in enumerate(row)] for row in theta]
        assert q_value(t2, theta0, lam) <= top


def test_rosalind_ba2f_consensus_is_the_median_string():
    r = meme(SAMPLE, 8)
    # AAGTGCCA is a median string of this input (total distance 9, the optimum).
    assert consensus(r.theta) == "AAGTGCCA"
    sites = best_sites(SAMPLE, 8, r.z)
    assert [s[q:q + 8] for s, q in zip(SAMPLE, sites)][:2] == ["AACGGCCA", "AAGTGCCA"]


def test_start_model():
    th = start_model("ACG", 0.7)
    assert [round(sum(row), 12) for row in th] == [1, 1, 1]
    assert th[2][DNA.index("G")] == 0.7


def test_planted_success_rate():
    # Measured on seeds 0 to 2: the consensus of theta equals the planted motif
    # in 2 of 3 runs (seed 0 misses). The code is deterministic; the test asks
    # for at least 2. Three seeds keep the test fast on a loaded machine.
    hits = 0
    for seed in range(3):
        motif, seqs, _ = plant(random.Random(seed), 10, 100, 8, 1)
        hits += consensus(meme(seqs, 8).theta) == motif
    assert hits >= 2


def test_errors():
    with pytest.raises(ValueError):
        meme(["ACG"], 4)
    with pytest.raises(ValueError):
        meme(["ACGT"], 2, m=0.2)
    with pytest.raises(ValueError):
        meme(["AAAA"], 2)
    with pytest.raises(ValueError):
        meme(["ACGTACGT"], 2, starts=["ACG"])
    with pytest.raises(ValueError):
        meme([], 2)
