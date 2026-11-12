# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-family-distribution/. The authors are listed in prov/RGQ0M9.jsonl.

import math
import random

from exponential_family_distribution import (
    BERNOULLI,
    GAUSSIAN,
    POISSON,
    entropy,
    gaussian_natural,
    gradient,
    hessian,
    log_likelihood,
    log_partition_direct,
    max_entropy_on_finite_set,
    moments_direct,
)

CASES = [
    (BERNOULLI, [math.log(3)]),
    (BERNOULLI, [-1.3]),
    (POISSON, [math.log(2)]),
    (POISSON, [1.7]),
    (GAUSSIAN, gaussian_natural(1.0, 2.0)),
    (GAUSSIAN, gaussian_natural(-0.5, 0.3)),
]


def test_closed_form_log_partition_matches_definition() -> None:
    for fam, eta in CASES:
        assert abs(fam.A(eta) - log_partition_direct(fam, eta)) < 1e-8


def test_gradient_of_A_is_mean_of_T() -> None:
    for fam, eta in CASES:
        mean, _ = moments_direct(fam, eta)
        g = gradient(fam.A, eta)
        assert all(abs(a - b) < 1e-6 * max(1.0, abs(b)) for a, b in zip(g, mean))


def test_hessian_of_A_is_covariance_of_T() -> None:
    for fam, eta in CASES:
        _, cov = moments_direct(fam, eta)
        H = hessian(fam.A, eta)
        for j in range(len(eta)):
            for k in range(len(eta)):
                assert abs(H[j][k] - cov[j][k]) < 1e-4 * max(1.0, abs(cov[j][k]))


def test_page_numbers() -> None:
    mean, cov = moments_direct(BERNOULLI, [math.log(3)])
    assert abs(mean[0] - 0.75) < 1e-12 and abs(cov[0][0] - 3 / 16) < 1e-12
    mean, cov = moments_direct(GAUSSIAN, gaussian_natural(1.0, 2.0))
    assert abs(mean[0] - 1) < 1e-8 and abs(mean[1] - 3) < 1e-8
    assert abs(cov[0][0] - 2) < 1e-6 and abs(cov[0][1] - 4) < 1e-6 and abs(cov[1][1] - 16) < 1e-5


def test_log_partition_is_convex() -> None:
    rng = random.Random(3)
    for fam, lo, hi in [(BERNOULLI, -5, 5), (POISSON, -3, 2)]:
        for _ in range(200):
            a, b, t = rng.uniform(lo, hi), rng.uniform(lo, hi), rng.random()
            assert fam.A([t * a + (1 - t) * b]) <= t * fam.A([a]) + (1 - t) * fam.A([b]) + 1e-12
    for _ in range(50):
        e = [rng.uniform(-2, 2), -rng.uniform(0.1, 2)]
        f = [rng.uniform(-2, 2), -rng.uniform(0.1, 2)]
        t = rng.random()
        mid = [t * x + (1 - t) * y for x, y in zip(e, f)]
        assert GAUSSIAN.A(mid) <= t * GAUSSIAN.A(e) + (1 - t) * GAUSSIAN.A(f) + 1e-12


def test_sufficient_statistic() -> None:
    # two Poisson samples with the same size and sum: the likelihood ratio does not depend on eta
    xs, ys = [3, 1, 4, 1, 5], [2, 2, 2, 3, 5]
    ratios = [log_likelihood(POISSON, [e], xs) - log_likelihood(POISSON, [e], ys) for e in (-1.0, 0.0, 0.7, 2.0)]
    assert max(ratios) - min(ratios) < 1e-9


def test_maximum_entropy_with_a_mean_constraint() -> None:
    values = [0, 1, 2, 3, 4, 5]
    p = max_entropy_on_finite_set(values, 1.5)
    assert abs(sum(p) - 1) < 1e-12 and abs(sum(a * b for a, b in zip(p, values)) - 1.5) < 1e-9
    # p_k is geometric in k: an exponential family with T(x) = x
    ratios = [p[k + 1] / p[k] for k in range(5)]
    assert max(ratios) - min(ratios) < 1e-9
    # every other distribution with the same mean has lower entropy
    rng = random.Random(1957)
    best = entropy(p)
    for _ in range(500):
        # a direction d with sum d = 0 and sum k d_k = 0 keeps both constraints
        d = [rng.uniform(-1, 1) for _ in values]
        # project out the constraint directions (1,...,1) and (0,...,5) by Gram-Schmidt
        u1 = [1.0] * 6
        u2 = [v - 2.5 for v in values]
        for u in (u1, u2):
            c = sum(a * b for a, b in zip(d, u)) / sum(a * a for a in u)
            d = [a - c * b for a, b in zip(d, u)]
        step = 0.05 * rng.random()
        q = [a + step * b for a, b in zip(p, d)]
        if min(q) > 0:
            assert entropy(q) < best
