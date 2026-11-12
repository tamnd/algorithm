# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-sne/. The authors are listed in prov/5T99ZY.jsonl.

import math
import random

from t_sne import conditional_row, gradient, joint_affinities, kl, squared_distances, student_q, tsne


def blobs(rng, n_per=6, centers=((0.0, 0.0, 0.0, 0.0), (8.0, 0.0, 0.0, 0.0), (0.0, 8.0, 0.0, 0.0))):
    return [[c + rng.gauss(0.0, 1.0) for c in center] for center in centers for _ in range(n_per)]


def test_conditional_rows_meet_perplexity():
    x = blobs(random.Random(2))
    d = squared_distances(x)
    for i in range(len(x)):
        p = conditional_row(d[i], i, 5.0, tol=1e-7)
        h = -sum(v * math.log2(v) for v in p if v > 0.0)
        assert abs(2.0 ** h - 5.0) < 1e-5


def test_joint_affinities_are_symmetric_and_normalized():
    x = blobs(random.Random(4))
    n = len(x)
    p = joint_affinities(x, 5.0)
    assert abs(sum(map(sum, p)) - 1.0) < 1e-12
    for i in range(n):
        assert p[i][i] == 0.0
        assert sum(p[i]) > 1.0 / (2.0 * n)  # every point keeps some weight
        for j in range(n):
            assert p[i][j] == p[j][i]


def test_student_q_hand_example():
    q, w = student_q([[0.0], [1.0], [3.0]])
    # weights 1/2, 1/10, 1/5 for the pairs (0,1), (0,2), (1,2); each counted twice
    z = 2 * (0.5 + 0.1 + 0.2)
    assert abs(q[0][1] - 0.5 / z) < 1e-15 and abs(q[1][2] - 0.2 / z) < 1e-15


def test_gradient_matches_finite_differences():
    rng = random.Random(9)
    x = blobs(rng, n_per=4)
    p = joint_affinities(x, 4.0)
    y = [[rng.gauss(0.0, 1.0) for _ in range(2)] for _ in x]
    g = gradient(p, y)
    h = 1e-6
    for i in range(len(y)):
        for k in range(2):
            y[i][k] += h
            up = kl(p, y)
            y[i][k] -= 2 * h
            down = kl(p, y)
            y[i][k] += h
            assert abs((up - down) / (2 * h) - g[i][k]) < 1e-6


def test_exact_method_lowers_kl_on_seeded_set():
    x = blobs(random.Random(5))
    y, p = tsne(x, random.Random(1), perplexity=5.0, iters=300)
    r = random.Random(1)
    start = [[r.gauss(0.0, 1e-2) for _ in range(2)] for _ in x]
    before, after = kl(p, start), kl(p, y)
    assert after < 0.5 * before
    dy = squared_distances(y)
    for i in range(len(y)):
        j = min((k for k in range(len(y)) if k != i), key=lambda k: dy[i][k])
        assert i // 6 == j // 6
