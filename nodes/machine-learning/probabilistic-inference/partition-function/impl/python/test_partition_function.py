# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partition-function/. The authors are listed in prov/VFPG8P.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from partition_function import Feature, derivatives_along, moments, partition_function


def test_two_spins():
    # One feature [x1 == x2] with w = 2: Z = 2 + 1 + 1 + 2 = 6.
    f = Feature((0, 1), {(a, b): int(a == b) for a in (0, 1) for b in (0, 1)})
    assert partition_function([f], [2, 2], [F(2)]) == 6
    mean, cov = moments([f], [2, 2], [F(2)])
    assert mean == [F(2, 3)] and cov == [[F(2, 9)]]
    assert derivatives_along([f], [2, 2], [F(2)], [1]) == (F(2, 3), F(2, 9))


def test_bayesian_network_has_z_one():
    # P(A) P(B | A) as a log-linear model with one indicator feature per table entry.
    pa = {0: F(1, 4), 1: F(3, 4)}
    pb = {(0, 0): F(1, 2), (1, 0): F(1, 2), (0, 1): F(1, 5), (1, 1): F(4, 5)}
    feats, w = [], []
    for a in (0, 1):
        feats.append(Feature((0,), {(x,): int(x == a) for x in (0, 1)}))
        w.append(pa[a])
    for (b, a), p in pb.items():
        feats.append(Feature((1, 0), {(y, x): int((y, x) == (b, a)) for y in (0, 1) for x in (0, 1)}))
        w.append(p)
    assert partition_function(feats, [2, 2], w) == 1


def random_model(rng):
    n = rng.randint(1, 4)
    card = [rng.choice([2, 3]) for _ in range(n)]
    feats = []
    for _ in range(rng.randint(1, 4)):
        scope = tuple(rng.sample(range(n), rng.randint(1, min(2, n))))
        feats.append(Feature(scope, {a: rng.randint(0, 2) for a in product(*(range(card[v]) for v in scope))}))
    w = [F(rng.randint(1, 5), rng.randint(1, 5)) for _ in feats]
    return feats, card, w


def test_gradient_is_the_mean_and_hessian_is_the_covariance():
    rng = random.Random(6)
    for _ in range(150):
        feats, card, w = random_model(rng)
        mean, cov = moments(feats, card, w)
        k = len(feats)
        for _ in range(3):
            u = [rng.randint(0, 2) for _ in range(k)]
            d1, d2 = derivatives_along(feats, card, w, u)
            assert d1 == sum(ui * mi for ui, mi in zip(u, mean))
            assert d2 == sum(u[i] * cov[i][j] * u[j] for i in range(k) for j in range(k))
            assert d2 >= 0  # convexity of log Z along u
        for i in range(k):
            e = [int(j == i) for j in range(k)]
            assert derivatives_along(feats, card, w, e)[0] == mean[i]
