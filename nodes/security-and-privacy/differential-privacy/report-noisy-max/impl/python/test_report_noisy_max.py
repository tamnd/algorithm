# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/report-noisy-max/. The authors are listed in prov/GKS5RH.jsonl.

import itertools
import math
import random

import pytest

import dpkit
from report_noisy_max import accuracy_gap, laplace_sample, noise_scale, report_noisy_max

UNIVERSE = (0, 1, 2)


def lap_pdf(z, b):
    return math.exp(-abs(z) / b) / (2 * b)


def lap_cdf(z, b):
    return 0.5 * math.exp(z / b) if z < 0 else 1 - 0.5 * math.exp(-z / b)


def simpson(g, a, b, n):
    h = (b - a) / n
    s = g(a) + g(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * g(a + i * h)
    return s * h / 3


def exact_pmf(scores, b):
    """Oracle: P(index i wins) = integral of pdf_i(y) prod_{j != i} cdf_j(y) dy.

    The integrand is smooth between the scores, so Simpson's rule is used on
    each piece between sorted break points, with a step of at most b / 12
    between the scores. The tails go out to 40 b on pieces that grow as the
    integrand decays, with at most 64 steps per piece. The total error is
    below 1e-5 on the inputs of these tests.
    """
    pts = sorted(set(scores))
    steps = (40, 24, 12, 6, 3, 1)
    edges = [pts[0] - k * b for k in steps] + pts + [pts[-1] + k * b for k in reversed(steps)]
    out = {}
    for i, ci in enumerate(scores):
        def g(y, i=i, ci=ci):
            v = lap_pdf(y - ci, b)
            for j, cj in enumerate(scores):
                if j != i:
                    v *= lap_cdf(y - cj, b)
            return v
        total = 0.0
        for lo, hi in zip(edges, edges[1:]):
            if hi > lo:
                steps_here = max(8, 2 * math.ceil(6 * (hi - lo) / b))
                if lo < pts[0] or hi > pts[-1]:
                    steps_here = min(64, steps_here)
                total += simpson(g, lo, hi, steps_here)
        out[i] = total
    return out


def histogram(x):
    return tuple(sum(1 for r in x if r == v) for v in UNIVERSE)


def all_datasets(max_n):
    for n in range(max_n + 1):
        for x in itertools.combinations_with_replacement(UNIVERSE, n):
            yield x


ADD_REMOVE = [(x, y) for x in all_datasets(3) for y in dpkit.neighbors_add_remove(x, UNIVERSE)]
REPLACE = [(x, y) for x in all_datasets(3) for y in dpkit.neighbors_replace(x, UNIVERSE)]


def worst_loss(b, pairs):
    cache = {}

    def mech(x):
        h = histogram(x)
        if h not in cache:
            cache[h] = exact_pmf(list(h), b)
        return cache[h]

    best = 0.0
    for x, y in pairs:
        p, q = mech(x), mech(y)
        best = max(best, dpkit.max_privacy_loss(p, q), dpkit.max_privacy_loss(q, p))
    return best


def test_oracle_sums_to_one_and_is_symmetric():
    rng = random.Random(40)
    for _ in range(200):
        m = rng.randint(1, 4)
        scores = [rng.randint(0, 5) for _ in range(m)]
        pmf = exact_pmf(scores, rng.uniform(0.5, 3.0))
        assert abs(sum(pmf.values()) - 1) < 1e-5
        for i in range(m):
            for j in range(m):
                if scores[i] == scores[j]:
                    assert abs(pmf[i] - pmf[j]) < 1e-9
                if scores[i] > scores[j]:
                    assert pmf[i] > pmf[j]


def test_counts_under_add_remove_are_epsilon_dp():
    for eps in (0.5, 1.0):
        loss = worst_loss(noise_scale(1, eps), ADD_REMOVE)
        assert loss <= eps + 1e-5


def test_counts_under_replace_with_scale_one_over_epsilon():
    # A measurement: under replace one count rises and another falls.
    # The scale 1 / epsilon then gives a loss near 1.556 > 1 on these datasets.
    eps = 1.0
    loss = worst_loss(noise_scale(1, eps, monotone=True), REPLACE)
    assert loss > 1.5 * eps
    assert worst_loss(noise_scale(1, eps, monotone=False), REPLACE) <= eps + 1e-5


def test_sampler_matches_oracle():
    rng = random.Random(41)
    n = 2000
    scores = [3, 1, 2, 3]
    b = noise_scale(1, 1.0)
    pmf = exact_pmf(scores, b)
    emp = dpkit.empirical_pmf(report_noisy_max(scores, 1.0, rng) for _ in range(n))
    t = dpkit.hoeffding_margin(n, 1e-6 / len(scores))
    for i in range(len(scores)):
        assert abs(emp.get(i, 0.0) - pmf[i]) <= t


def test_laplace_sampler_tail():
    rng = random.Random(42)
    n = 2000
    b = 2.0
    hits = sum(abs(laplace_sample(b, rng)) > 4.6052 for _ in range(n))
    assert abs(hits / n - 0.1) <= dpkit.hoeffding_margin(n, 1e-6)


def test_accuracy_bound_holds_on_random_instances():
    rng = random.Random(43)
    for _ in range(500):
        m = rng.randint(1, 4)
        scores = [rng.randint(0, 6) for _ in range(m)]
        eps = rng.uniform(0.3, 1.5)
        beta = rng.uniform(0.01, 0.5)
        b = noise_scale(1, eps)
        pmf = exact_pmf(scores, b)
        gap = accuracy_gap(b, m, beta)
        bad = sum(p for i, p in pmf.items() if scores[i] < max(scores) - gap)
        assert bad <= beta + 1e-5


def test_edge_cases():
    rng = random.Random(0)
    with pytest.raises(ValueError):
        report_noisy_max([], 1.0, rng)
    with pytest.raises(ValueError):
        report_noisy_max([1, 2], 0.0, rng)
    with pytest.raises(ValueError):
        accuracy_gap(1.0, 0, 0.1)
    assert report_noisy_max([7], 1.0, rng) == 0
    assert noise_scale(2, 0.5) == 4.0
    assert noise_scale(2, 0.5, monotone=False) == 8.0
    # A huge gap makes the true maximum win almost surely.
    assert all(report_noisy_max([0, 1000, 0], 1.0, rng) == 1 for _ in range(200))
