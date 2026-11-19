# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/continuous-bag-of-words/. The authors are listed in prov/GERBMV.jsonl.

import math
import random

from continuous_bag_of_words import examples, gradient, hidden, loss, probabilities, train


def rand_matrix(rng, n, d, scale=0.5):
    return [[rng.uniform(-scale, scale) for _ in range(d)] for _ in range(n)]


def cos(u, v):
    return sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))


def test_examples_of_a_sentence():
    got = examples([[0, 1, 2, 3]], 1)
    assert got == [([1], 0), ([0, 2], 1), ([1, 3], 2), ([2], 3)]
    assert examples([[5]], 2) == []


def test_hidden_is_mean_or_sum():
    vin = [[1.0, 0.0], [0.0, 2.0], [3.0, 3.0]]
    assert hidden(vin, [0, 1, 2]) == [4.0 / 3, 5.0 / 3]
    assert hidden(vin, [0, 1, 2], mean=False) == [4.0, 5.0]
    assert hidden(vin, [1, 2]) == hidden(vin, [2, 1])  # word order does not matter


def test_probabilities_sum_to_one():
    rng = random.Random(1)
    vin, uout = rand_matrix(rng, 10, 4, 2.0), rand_matrix(rng, 10, 4, 2.0)
    for ctx in ([0], [1, 2, 3, 4], [5, 5, 9]):
        p = probabilities(vin, uout, ctx)
        assert abs(sum(p) - 1.0) < 1e-12


def test_gradient_against_finite_differences():
    rng = random.Random(2)
    vin, uout = rand_matrix(rng, 6, 3), rand_matrix(rng, 6, 3)
    h = 1e-6
    for mean in (True, False):
        for ctx, center in [([1, 2, 4, 5], 3), ([0, 0, 2], 1)]:
            gv, gu = gradient(vin, uout, ctx, center, mean)
            for mat, grads in ((vin, gv), (uout, dict(enumerate(gu)))):
                for row in range(6):
                    for k in range(3):
                        old = mat[row][k]
                        mat[row][k] = old + h
                        up = loss(vin, uout, ctx, center, mean)
                        mat[row][k] = old - h
                        down = loss(vin, uout, ctx, center, mean)
                        mat[row][k] = old
                        ana = grads.get(row, [0.0] * 3)[k]
                        assert abs((up - down) / (2 * h) - ana) < 1e-5


def test_planted_clusters_come_apart():
    rng = random.Random(3)
    groups = [(list(range(0, 4)), list(range(8, 11))), (list(range(4, 8)), list(range(11, 14)))]
    corpus = []
    for _ in range(60):
        words, ctx = groups[rng.randrange(2)]
        corpus.append([rng.choice(words) if k % 2 == 0 else rng.choice(ctx) for k in range(6)])
    vin, _ = train(corpus, 14, d=6, c_max=2, epochs=6, lr=0.2, seed=3)
    (a, _), (b, _) = groups
    inside = [cos(vin[u], vin[v]) for g in (a, b) for k, u in enumerate(g) for v in g[k + 1:]]
    across = [cos(vin[u], vin[v]) for u in a for v in b]
    assert min(inside) > max(across)
