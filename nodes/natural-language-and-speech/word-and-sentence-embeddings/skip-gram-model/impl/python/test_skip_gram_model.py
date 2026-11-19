# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skip-gram-model/. The authors are listed in prov/PV50G4.jsonl.

import math
import random

from skip_gram_model import (
    corpus_loss,
    free_score_optimum,
    inclusion_probability,
    pair_gradient,
    pair_loss,
    probabilities,
    train,
    training_pairs,
)


def rand_matrix(rng, n, d, scale=0.5):
    return [[rng.uniform(-scale, scale) for _ in range(d)] for _ in range(n)]


def cos(u, v):
    return sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))


def test_probabilities_sum_to_one():
    rng = random.Random(1)
    vin, uout = rand_matrix(rng, 12, 5, 2.0), rand_matrix(rng, 12, 5, 2.0)
    for w in range(12):
        p = probabilities(vin, uout, w)
        assert abs(sum(p) - 1.0) < 1e-12 and min(p) > 0


def test_gradient_against_finite_differences():
    rng = random.Random(2)
    vin, uout = rand_matrix(rng, 7, 4), rand_matrix(rng, 7, 4)
    h = 1e-6
    for w, c in [(0, 3), (5, 5), (6, 1)]:
        gv, gu = pair_gradient(vin, uout, w, c)
        for mat, row, grad in [(vin, w, gv)] + [(uout, j, gu[j]) for j in range(7)]:
            for k in range(4):
                old = mat[row][k]
                mat[row][k] = old + h
                up = pair_loss(vin, uout, w, c)
                mat[row][k] = old - h
                down = pair_loss(vin, uout, w, c)
                mat[row][k] = old
                assert abs((up - down) / (2 * h) - grad[k]) < 1e-5


def test_window_pairs_and_inclusion_probability():
    rng = random.Random(3)
    pairs = training_pairs([[0, 1, 2, 3, 4]], 1, rng)
    assert pairs == [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)]
    c_max, trials = 3, 6000
    hits = {1: 0, 2: 0, 3: 0}
    for _ in range(trials):
        for w, c in training_pairs([[0, 1, 2, 3, 4, 5, 6]], c_max, rng):
            if w == 3 and c > 3:
                hits[c - 3] += 1
    for dist in (1, 2, 3):
        assert abs(hits[dist] / trials - inclusion_probability(dist, c_max)) < 0.02
    assert [inclusion_probability(k, 5) for k in range(1, 7)] == [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]


def test_free_scores_optimum_is_the_conditional_frequency():
    pairs = [(0, 1)] * 3 + [(0, 2)] + [(1, 0)] * 2 + [(1, 2)] * 2
    best = free_score_optimum(pairs, 3)
    assert best[0] == [0.0, 0.75, 0.25] and best[1] == [0.5, 0.0, 0.5]

    def log_lik(q):
        return sum(math.log(q[w][c]) for w, c in pairs)

    rng = random.Random(4)
    top = log_lik(best)
    for _ in range(200):
        q = {}
        for w in best:
            raw = [rng.random() + 1e-9 for _ in range(3)]
            q[w] = [x / sum(raw) for x in raw]
        assert log_lik(q) <= top


def planted_corpus(seed=0, sentences=60, length=6):
    rng = random.Random(seed)
    groups = [(list(range(0, 4)), list(range(8, 11))), (list(range(4, 8)), list(range(11, 14)))]
    corpus = []
    for _ in range(sentences):
        words, ctx = groups[rng.randrange(2)]
        corpus.append([rng.choice(words) if k % 2 == 0 else rng.choice(ctx) for k in range(length)])
    return corpus, groups


def test_planted_clusters_come_apart():
    corpus, groups = planted_corpus(seed=5)
    rng = random.Random(5)
    vin, uout = train(corpus, 14, d=6, c_max=2, epochs=4, lr=0.1, seed=5)
    (a, _), (b, _) = groups
    inside = [cos(vin[u], vin[v]) for g in (a, b) for k, u in enumerate(g) for v in g[k + 1:]]
    across = [cos(vin[u], vin[v]) for u in a for v in b]
    assert min(inside) > max(across)
    pairs = training_pairs(corpus, 2, rng)
    start = corpus_loss([[0.0] * 6 for _ in range(14)], uout, pairs)
    assert corpus_loss(vin, uout, pairs) < 0.8 * start
