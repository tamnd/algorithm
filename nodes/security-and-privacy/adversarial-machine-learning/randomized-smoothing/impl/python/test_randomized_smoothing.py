# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-smoothing/. The authors are listed in prov/HVTX47.jsonl.

"""Tests of randomized smoothing on seeded synthetic classifiers only."""

import math
import random
from statistics import NormalDist

import mlkit as m
from randomized_smoothing import (
    ABSTAIN,
    binomial_p_value,
    binomial_upper_tail,
    certified_accuracy,
    certify,
    distance_to_boundary,
    exact_top_probability,
    linear_classifier,
    lower_confidence_bound,
    predict,
    radius_from_probabilities,
)

PHI = NormalDist()


def test_check_value_of_the_radius():
    r = radius_from_probabilities(0.5, 0.9, 0.1)
    assert abs(r - 0.64078) < 1e-5
    assert abs(r - 0.5 * PHI.inv_cdf(0.9)) < 1e-12


def test_binomial_tail_against_direct_sum():
    for n in (1, 5, 20, 60):
        for k in range(n + 2):
            for p in (0.01, 0.3, 0.5, 0.77, 0.99):
                direct = sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
                assert abs(binomial_upper_tail(k, n, p) - direct) < 1e-12


def test_clopper_pearson_bound_meets_alpha():
    for n in (1, 10, 100, 1000):
        for alpha in (0.001, 0.05):
            assert abs(lower_confidence_bound(n, n, alpha) - alpha ** (1.0 / n)) < 1e-9
            for k in sorted({1, n // 3, n // 2, n - 1, n} - {0}):
                p = lower_confidence_bound(k, n, alpha)
                assert abs(binomial_upper_tail(k, n, p) - alpha) < 1e-9
                assert p <= k / n
    assert lower_confidence_bound(0, 10, 0.05) == 0.0


def test_clopper_pearson_exact_coverage():
    # P_p(bound(K) > p) <= alpha for every p, computed exactly over all outcomes K.
    for n in (5, 12, 40):
        for alpha in (0.05, 0.2):
            bounds = [lower_confidence_bound(k, n, alpha) for k in range(n + 1)]
            assert all(a <= b for a, b in zip(bounds, bounds[1:]))
            for t in range(1, 200):
                p = t / 200
                miss = sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1) if bounds[k] > p)
                assert miss <= alpha + 1e-12


def test_p_value():
    assert binomial_p_value(5, 10) == 1.0
    assert abs(binomial_p_value(10, 10) - 2 * 0.5 ** 10) < 1e-15
    assert abs(binomial_p_value(0, 10) - 2 * 0.5 ** 10) < 1e-15


def test_linear_certificate_is_sound_and_close_to_the_distance():
    rng = random.Random(2019)
    w, b = [1.5, -2.0, 0.5], 0.25
    f = linear_classifier(w, b)
    sigma, alpha = 0.5, 0.01
    wrong, ratio = 0, []
    for _ in range(60):
        x = [rng.uniform(-1, 1) for _ in range(3)]
        c, r = certify(f, sigma, x, 20, 400, alpha, rng)
        exact_c, _ = exact_top_probability(w, b, x, sigma)
        dist = distance_to_boundary(w, b, x)
        if c != ABSTAIN:
            # For a linear f, g = f, and the exact certified radius is the distance to the boundary.
            if c != exact_c or r > dist:
                wrong += 1
            ratio.append(r / dist)
    assert wrong <= 2
    assert len(ratio) > 30
    assert sum(ratio) / len(ratio) > 0.7


def test_exact_radius_of_a_linear_model_is_the_distance():
    rng = random.Random(5)
    for _ in range(200):
        w = [rng.uniform(-2, 2) for _ in range(4)]
        b = rng.uniform(-1, 1)
        x = [rng.uniform(-1, 1) for _ in range(4)]
        sigma = rng.uniform(0.1, 1.0)
        _, pa = exact_top_probability(w, b, x, sigma)
        if 0.5 < pa < 1 - 1e-12:
            assert abs(sigma * PHI.inv_cdf(pa) - distance_to_boundary(w, b, x)) < 1e-6


def test_certified_ball_keeps_the_smoothed_label():
    # Inside the certified ball the exact top probability of g stays above 1/2.
    rng = random.Random(7)
    w, b = [0.8, 0.6], -0.2
    f = linear_classifier(w, b)
    for _ in range(40):
        x = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        c, r = certify(f, 0.25, x, 20, 300, 0.001, rng)
        if c == ABSTAIN:
            continue
        for _ in range(20):
            d = [rng.gauss(0, 1), rng.gauss(0, 1)]
            s = rng.random() * r / m.norm2(d)
            xd = [a + s * v for a, v in zip(x, d)]
            label, p = exact_top_probability(w, b, xd, 0.25)
            assert label == c and p > 0.5


def test_abstains_on_the_boundary():
    rng = random.Random(8)
    f = linear_classifier([1.0, 0.0], 0.0)
    abstain = sum(1 for _ in range(50) if certify(f, 0.5, [0.0, 0.3], 10, 200, 0.05, rng)[0] == ABSTAIN)
    assert abstain >= 45
    assert sum(1 for _ in range(50) if predict(f, 0.5, [0.0, 0.3], 200, 0.05, rng) != ABSTAIN) <= 6


def test_relu_network_base_classifier():
    rng = random.Random(11)
    net = m.tiny_relu_net(rng, 2, 6, 3)

    def f(x):
        return m.argmax(m.forward(net, x))

    results, labels = [], []
    for _ in range(15):
        x = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        labels.append(f(x))
        results.append(certify(f, 0.25, x, 20, 200, 0.01, rng))
    acc0 = certified_accuracy(results, labels, 0.0)
    acc1 = certified_accuracy(results, labels, 0.2)
    assert 0.0 <= acc1 <= acc0 <= 1.0
    assert all(r <= 0.25 * PHI.inv_cdf(0.01 ** (1 / 200)) + 1e-12 for _, r in results)


def test_more_samples_give_a_larger_radius_bound():
    for n in (100, 1000, 10000):
        pa = lower_confidence_bound(int(0.9 * n), n, 0.001)
        assert pa < 0.9
    a = lower_confidence_bound(90, 100, 0.001)
    b = lower_confidence_bound(900, 1000, 0.001)
    c = lower_confidence_bound(9000, 10000, 0.001)
    assert a < b < c < 0.9
