# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/li-stephens-model/. The authors are listed in prov/QN36N8.jsonl.

import itertools
import math
import random

import pytest

from li_stephens_model import (emission, enumerate_likelihood, forward, most_likely_path, path_probability,
                               posterior, switch_probabilities, watterson_theta)


def random_case(rng, k, m):
    panel = [[rng.randrange(2) for _ in range(m)] for _ in range(k)]
    h = [rng.randrange(2) for _ in range(m)]
    rho = [rng.choice([0.0, 0.3, 2.0, 10.0]) for _ in range(m - 1)]
    return panel, h, rho


def test_watterson_theta_and_emission():
    assert watterson_theta(2) == 1.0
    assert watterson_theta(3) == pytest.approx(2.0 / 3.0)
    same, diff = emission(4, 1.0)
    assert same == pytest.approx(4.5 / 5.0)
    assert diff == pytest.approx(0.5 / 5.0)
    assert same + diff == pytest.approx(1.0)
    with pytest.raises(ValueError):
        watterson_theta(1)


def test_transition_rows_sum_to_one():
    k = 5
    for s in switch_probabilities([0.0, 0.5, 3.0, 100.0], k):
        for x in range(k):
            row = [(1.0 - s) * (x == y) + s / k for y in range(k)]
            assert sum(row) == pytest.approx(1.0)


def test_example_by_hand():
    panel = [[0, 0, 1], [1, 1, 1]]
    h = [0, 1, 1]
    rho = [2 * math.log(2), 2 * math.log(2)]  # so s = 1/2 in both gaps
    theta = 1.0
    assert switch_probabilities(rho, 2) == pytest.approx([0.5, 0.5])
    logp, _, _ = forward(panel, h, rho, theta)
    total, post = enumerate_likelihood(panel, h, rho, theta)
    assert math.exp(logp) == pytest.approx(total)
    # Emissions 5/6 and 1/6; stay 3/4 and switch 1/4. alpha_1 = (5/12, 1/12),
    # alpha_2 = (1/18, 5/36), and both haplotypes match at the last site.
    assert total == pytest.approx(35 / 216)
    assert post[1] == pytest.approx([2 / 7, 5 / 7])


def test_forward_matches_enumeration():
    rng = random.Random(11)
    for _ in range(60):
        k, m = rng.randint(1, 3), rng.randint(1, 5)
        panel, h, rho = random_case(rng, k, m)
        theta = rng.choice([0.01, 0.2, 1.0]) if k == 1 else rng.choice([None, 0.01, 0.5])
        t = watterson_theta(k) if theta is None else theta
        logp, alphas, _ = forward(panel, h, rho, theta)
        total, _ = enumerate_likelihood(panel, h, rho, t)
        assert logp == pytest.approx(math.log(total), rel=1e-9, abs=1e-9)
        for a in alphas:
            assert sum(a) == pytest.approx(1.0)


def test_posterior_matches_enumeration():
    rng = random.Random(12)
    for _ in range(40):
        k, m = rng.randint(2, 4), rng.randint(1, 4)
        panel, h, rho = random_case(rng, k, m)
        post = posterior(panel, h, rho)
        _, want = enumerate_likelihood(panel, h, rho, watterson_theta(k))
        for row, wrow in zip(post, want):
            assert row == pytest.approx(wrow, abs=1e-9)


def test_viterbi_matches_enumeration():
    rng = random.Random(13)
    for _ in range(40):
        k, m = rng.randint(2, 3), rng.randint(1, 5)
        panel, h, rho = random_case(rng, k, m)
        t = watterson_theta(k)
        path = most_likely_path(panel, h, rho)
        best = max(path_probability(p, panel, h, rho, t) for p in itertools.product(range(k), repeat=m))
        assert path_probability(path, panel, h, rho, t) == pytest.approx(best)


def test_limits_of_rho():
    rng = random.Random(14)
    k, m = 3, 6
    panel, h, _ = random_case(rng, k, m)
    t = watterson_theta(k)
    same, diff = emission(k, t)
    e = [[same if panel[x][j] == h[j] else diff for j in range(m)] for x in range(k)]
    # No recombination: one haplotype is copied along the whole sequence.
    logp, _, _ = forward(panel, h, [0.0] * (m - 1))
    assert math.exp(logp) == pytest.approx(sum(math.prod(row) for row in e) / k)
    # Free recombination: the sites are independent.
    logp, _, _ = forward(panel, h, [1e6] * (m - 1))
    assert math.exp(logp) == pytest.approx(math.prod(sum(e[x][j] for x in range(k)) / k for j in range(m)))


def test_mosaic_is_recovered():
    rng = random.Random(15)
    k, m = 6, 400
    panel = [[rng.randrange(2) for _ in range(m)] for _ in range(k)]
    truth = [0] * 150 + [3] * 130 + [5] * 120
    h = [panel[x][j] for j, x in enumerate(truth)]
    rho = [0.05] * (m - 1)
    path = most_likely_path(panel, h, rho)
    agree = sum(a == b for a, b in zip(path, truth)) / m
    assert agree > 0.95
    post = posterior(panel, h, rho)
    assert sum(post[j][truth[j]] for j in range(m)) / m > 0.9


def test_long_input_does_not_underflow():
    rng = random.Random(16)
    panel, h, rho = random_case(rng, 4, 3000)
    logp, _, _ = forward(panel, h, rho)
    assert math.isfinite(logp) and logp < -100


def test_bad_input():
    with pytest.raises(ValueError):
        forward([], [0], [])
    with pytest.raises(ValueError):
        forward([[0, 1]], [0, 1, 1], [0.1])
    with pytest.raises(ValueError):
        forward([[0, 1], [1, 1]], [0, 1], [])
    with pytest.raises(ValueError):
        forward([[0, 1], [1, 1]], [0, 1], [-1.0])
    with pytest.raises(ValueError):
        forward([[0, 2], [1, 1]], [0, 1], [0.1])
    with pytest.raises(ValueError):
        forward([[0, 1], [1, 1]], [0, 1], [0.1], theta=0.0)
