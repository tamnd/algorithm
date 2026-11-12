# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x-means/. The authors are listed in prov/X2J8SA.jsonl.

import math
import random

from x_means import bic, lloyd, sq_dist, x_means


def blobs(rng, centers, m, sd=1.0):
    return [tuple(c + rng.gauss(0, sd) for c in cen) for cen in centers for _ in range(m)]


def test_bic_equals_direct_log_likelihood() -> None:
    rng = random.Random(1)
    for _ in range(30):
        d = rng.randrange(1, 4)
        K = rng.randrange(1, 4)
        x = [tuple(rng.uniform(-5, 5) for _ in range(d)) for _ in range(rng.randrange(K + 2, 30))]
        centers, labels = lloyd(x, x[:K])
        R = len(x)
        sse = sum(sq_dist(p, centers[a]) for p, a in zip(x, labels))
        var = sse / (d * (R - K))
        # sum over points of log( (R_j / R) * N(x | mu_j, var I) )
        ll = 0.0
        for p, a in zip(x, labels):
            rj = labels.count(a)
            ll += math.log(rj / R) - d / 2 * math.log(2 * math.pi * var) - sq_dist(p, centers[a]) / (2 * var)
        expected = ll - ((K - 1) + K * d + 1) / 2 * math.log(R)
        assert abs(bic(x, centers, labels) - expected) < 1e-7 * max(1.0, abs(expected))


def test_finds_three_separated_blobs() -> None:
    for seed in range(3):
        rng = random.Random(seed)
        x = blobs(rng, [(0, 0), (12, 0), (0, 12)], 120)
        centers, labels, score = x_means(x, 1, 10, rng)
        assert len(centers) == 3
        found = sorted((round(c[0] / 12), round(c[1] / 12)) for c in centers)
        assert found == [(0, 0), (0, 1), (1, 0)]


def test_one_blob_is_not_split() -> None:
    rng = random.Random(7)
    x = blobs(rng, [(3, -2)], 300)
    centers, labels, score = x_means(x, 1, 10, rng)
    assert len(centers) == 1


def test_respects_k_max_and_scores() -> None:
    rng = random.Random(4)
    x = blobs(rng, [(0, 0), (10, 0), (20, 0), (30, 0), (40, 0), (50, 0)], 40, sd=0.5)
    centers, labels, score = x_means(x, 1, 4, rng)
    assert len(centers) <= 4
    assert score == bic(x, centers, labels)
