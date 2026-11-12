# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-neighbor-embedding/. The authors are listed in prov/WVHAJS.jsonl.

import math
import random

from stochastic_neighbor_embedding import (
    bandwidth_search,
    conditional_row,
    cost,
    gradient,
    input_affinities,
    sne,
    squared_distances,
)


def blobs(rng, n_per=6, centers=((0.0, 0.0, 0.0), (6.0, 0.0, 0.0), (0.0, 6.0, 0.0))):
    return [[c + rng.gauss(0.0, 1.0) for c in center] for center in centers for _ in range(n_per)]


def test_bandwidth_reaches_target_perplexity():
    rng = random.Random(7)
    x = blobs(rng)
    d = squared_distances(x)
    for perp in (2.0, 4.0, 8.0, 15.0):
        for i in range(len(x)):
            beta, p = bandwidth_search(d[i], i, perp, tol=1e-6)
            h = -sum(v * math.log2(v) for v in p if v > 0.0)
            assert abs(2.0 ** h - perp) <= 1e-4 * perp
            assert abs(sum(p) - 1.0) < 1e-12 and p[i] == 0.0 and beta > 0.0


def test_entropy_decreases_in_beta():
    rng = random.Random(3)
    x = blobs(rng)
    d = squared_distances(x)
    hs = [conditional_row(d[0], 0, b)[1] for b in (0.01, 0.1, 0.5, 1.0, 2.0, 5.0)]
    assert all(a > b for a, b in zip(hs, hs[1:]))
    assert abs(conditional_row(d[0], 0, 0.0)[1] - math.log2(len(x) - 1)) < 1e-12


def test_gradient_matches_finite_differences():
    rng = random.Random(11)
    x = blobs(rng, n_per=4)
    p, _ = input_affinities(x, 3.0)
    y = [[rng.gauss(0.0, 1.0) for _ in range(2)] for _ in x]
    g = gradient(p, y)
    h = 1e-6
    for i in range(len(y)):
        for k in range(2):
            y[i][k] += h
            up = cost(p, y)
            y[i][k] -= 2 * h
            down = cost(p, y)
            y[i][k] += h
            assert abs((up - down) / (2 * h) - g[i][k]) < 1e-6


def test_fit_lowers_cost_and_keeps_clusters():
    rng = random.Random(5)
    x = blobs(rng)
    y, p = sne(x, random.Random(1), perplexity=4.0, iters=300)
    r = random.Random(1)
    start = [[r.gauss(0.0, 1e-2) for _ in range(2)] for _ in x]
    assert cost(p, y) < cost(p, start)
    # each point's nearest map neighbor comes from the same blob
    dy = squared_distances(y)
    for i in range(len(y)):
        j = min((k for k in range(len(y)) if k != i), key=lambda k: dy[i][k])
        assert i // 6 == j // 6
