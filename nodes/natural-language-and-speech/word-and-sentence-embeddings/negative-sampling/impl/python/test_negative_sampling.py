# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/negative-sampling/. The authors are listed in prov/9W46SG.jsonl.

import math
import random

from negative_sampling import (
    NoiseSampler,
    discard_probability,
    expected_local_objective,
    noise_distribution,
    pair_gradient,
    pair_loss,
    train,
)


def cos(u, v):
    return sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))


def test_noise_distribution_hand_values():
    p = noise_distribution([8, 4, 2, 1, 1])
    assert abs(sum(p) - 1.0) < 1e-12
    assert [round(x, 4) for x in p] == [0.4222, 0.251, 0.1493, 0.0888, 0.0888]
    assert noise_distribution([8, 4, 2, 1, 1], power=1.0) == [0.5, 0.25, 0.125, 0.0625, 0.0625]


def test_sampler_frequencies_and_skip():
    counts = [8, 4, 2, 1, 1]
    s = NoiseSampler(counts)
    rng = random.Random(1)
    n = 20000
    freq = [0] * 5
    for _ in range(n):
        freq[s.draw(rng)] += 1
    assert all(abs(f / n - p) < 0.01 for f, p in zip(freq, noise_distribution(counts)))
    for _ in range(500):
        assert 0 not in s.negatives(rng, 5, 0)


def test_discard_probability():
    assert discard_probability(1e-5) == 0.0
    assert discard_probability(1e-6) == 0.0
    assert abs(discard_probability(1e-3) - 0.9) < 1e-12
    assert abs(discard_probability(0.01) - (1 - math.sqrt(1e-3))) < 1e-12


def test_gradient_against_finite_differences():
    rng = random.Random(2)
    vin = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(6)]
    uout = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(6)]
    h = 1e-6
    for w, c, neg in [(0, 1, [2, 3, 3]), (4, 4, [5]), (2, 5, [])]:
        gv, gu = pair_gradient(vin, uout, w, c, neg)
        for mat, row, grad in [(vin, w, gv)] + [(uout, j, gu.get(j, [0.0] * 4)) for j in range(6)]:
            for k in range(4):
                old = mat[row][k]
                mat[row][k] = old + h
                up = pair_loss(vin, uout, w, c, neg)
                mat[row][k] = old - h
                down = pair_loss(vin, uout, w, c, neg)
                mat[row][k] = old
                assert abs((up - down) / (2 * h) - grad[k]) < 1e-5


def test_cell_objective_peaks_at_shifted_pmi():
    for n_wc, n_w, n_c, total, k in [(4, 5, 5, 10, 2), (1, 5, 5, 10, 2), (3, 7, 2, 40, 5), (9, 10, 12, 50, 1)]:
        lo, hi = -20.0, 20.0
        for _ in range(200):  # ternary search on a concave function
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if expected_local_objective(m1, n_wc, n_w, n_c, total, k) < expected_local_objective(m2, n_wc, n_w, n_c, total, k):
                lo = m1
            else:
                hi = m2
        assert abs((lo + hi) / 2 - (math.log(n_wc * total / (n_w * n_c)) - math.log(k))) < 1e-6


def test_planted_clusters_come_apart():
    rng = random.Random(3)
    groups = [(list(range(0, 4)), list(range(8, 11))), (list(range(4, 8)), list(range(11, 14)))]
    corpus = []
    for _ in range(60):
        words, ctx = groups[rng.randrange(2)]
        corpus.append([rng.choice(words) if k % 2 == 0 else rng.choice(ctx) for k in range(6)])
    vin, _ = train(corpus, 14, d=6, window=2, k=3, epochs=5, lr=0.05, seed=3)
    (a, _), (b, _) = groups
    inside = [cos(vin[u], vin[v]) for g in (a, b) for k, u in enumerate(g) for v in g[k + 1:]]
    across = [cos(vin[u], vin[v]) for u in a for v in b]
    assert min(inside) > max(across)
