# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mini-batch-k-means/. The authors are listed in prov/A9SG65.jsonl.

import random
from fractions import Fraction as F

from mini_batch_k_means import cost, mini_batch_k_means, nearest, sq_dist


class ScriptedRng:
    """Returns the given index lists from sample(), to replay a fixed run."""

    def __init__(self, batches):
        self.batches = list(batches)

    def sample(self, population, m):
        return self.batches.pop(0)


def mean(ps):
    return tuple(sum(p[t] for p in ps) / len(ps) for t in range(len(ps[0])))


def test_trace_example() -> None:
    x = [(F(0),), (F(1),), (F(10),), (F(11),)]
    rng = ScriptedRng([[1, 3], [0, 2], [1, 0]])
    centers, counts = mini_batch_k_means(x, 2, 2, 3, rng, init=[x[0], x[2]])
    assert counts == [4, 2]
    assert centers == [(F(1, 2),), (F(21, 2),)]


def test_center_is_mean_of_its_samples() -> None:
    rng = random.Random(6)
    for _ in range(40):
        n = rng.randrange(3, 30)
        x = [(F(rng.randrange(-20, 21)), F(rng.randrange(-20, 21))) for _ in range(n)]
        k = rng.randrange(1, min(n, 5) + 1)
        log = []
        centers, counts = mini_batch_k_means(x, k, rng.randrange(1, n + 1), rng.randrange(1, 8), rng, log=log)
        for j in range(k):
            got = [p for c, p in log if c == j]
            assert len(got) == counts[j]
            if got:
                # the learning rate 1/count makes the center the running mean;
                # the initial position is forgotten at the first update
                assert centers[j] == mean(got)


def test_full_batch_first_step_is_lloyd() -> None:
    rng = random.Random(12)
    for _ in range(40):
        n = rng.randrange(2, 15)
        x = [(F(rng.randrange(-9, 10)),) for _ in range(n)]
        init = [x[i] for i in rng.sample(range(n), rng.randrange(1, n + 1))]
        k = len(init)
        centers, _ = mini_batch_k_means(x, k, n, 1, rng, init=init)
        for j in range(k):
            members = [p for p in x if nearest(p, init) == j]
            assert centers[j] == (mean(members) if members else init[j])


def test_float_blobs_close_to_good_solution() -> None:
    rng = random.Random(3)
    true = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0)]
    x = [(cx + rng.gauss(0, 1), cy + rng.gauss(0, 1)) for cx, cy in true for _ in range(300)]
    init = [x[0], x[300], x[600]]  # one seed per blob
    centers, counts = mini_batch_k_means(x, 3, 50, 60, rng, init=init)
    assert sum(counts) == 3000
    for c, m in zip(centers, true):
        assert sq_dist(c, m) < 0.25
    assert cost(x, centers) < 1.05 * cost(x, true)
