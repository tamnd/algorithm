# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-filter/. The authors are listed in prov/JZ7RY4.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from histogram_filter import centers, gaussian_prior, gaussian_transition, histogram_filter, mean_var


def kalman_1d(mu, var, u, q, z, r):
    """The scalar Kalman filter for x_t = x_(t-1) + u + N(0, q), z = x + N(0, r)."""
    mu, var = mu + u, var + q
    k = var / (var + r)
    return mu + k * (z - mu), (1.0 - k) * var


def run_histogram(g, steps, a=-20.0, b=20.0):
    p = gaussian_prior(a, b, g, 0.0, 2.0)
    c = centers(a, b, g)
    trans = gaussian_transition(a, b, g, 1.0, 0.5)
    for z in steps:
        lik = [math.exp(-0.5 * (z - ck) ** 2) for ck in c]
        p = histogram_filter(p, trans, lik)
    return mean_var(a, b, p)


def run_kalman(steps):
    mu, var = 0.0, 4.0
    for z in steps:
        mu, var = kalman_1d(mu, var, 1.0, 0.25, z, 1.0)
    return mu, var


def test_matches_kalman_filter_and_converges_with_finer_grid():
    rng = random.Random(7)
    x, steps = rng.gauss(0.0, 2.0), []
    for _ in range(6):
        x += 1.0 + rng.gauss(0.0, 0.5)
        steps.append(x + rng.gauss(0.0, 1.0))
    mu, var = run_kalman(steps)
    errs = []
    for g in (40, 160, 640):
        m, v = run_histogram(g, steps)
        errs.append(abs(m - mu) + abs(v - var))
    assert errs[0] > errs[1] > errs[2]
    assert errs[2] < 1e-3


def test_transition_columns_sum_to_one_and_mass_is_kept():
    trans = gaussian_transition(0.0, 10.0, 25, 3.7, 0.8)
    for i in range(25):
        assert abs(sum(trans[k][i] for k in range(25)) - 1.0) < 1e-12
    # a move far to the right puts all the mass in the last cell
    trans = gaussian_transition(0.0, 10.0, 25, 100.0, 0.5)
    assert all(abs(trans[24][i] - 1.0) < 1e-12 for i in range(25))
    p = histogram_filter([1.0 / 25] * 25, trans, None)
    assert abs(sum(p) - 1.0) < 1e-12


def test_exact_against_sum_over_paths():
    # A small discrete model in exact arithmetic: 4 cells, a move that goes
    # 0, 1 or 2 cells to the right and stops at the last cell.
    g = 4

    def step(i, s):
        return min(i + s, g - 1)

    moves = {0: F(1, 10), 1: F(7, 10), 2: F(1, 5)}
    trans = [[sum((pr for s, pr in moves.items() if step(i, s) == k), F(0)) for i in range(g)] for k in range(g)]
    liks = [[F(1, 2), F(1, 4), F(1, 8), F(1, 8)], [F(1, 10), F(3, 5), F(1, 5), F(1, 10)], [F(1), F(1, 3), F(1, 3), F(1, 9)]]
    prior = [F(2, 5), F(3, 10), F(1, 5), F(1, 10)]
    p = prior
    for lik in liks:
        p = histogram_filter(p, trans, lik)
    joint = [F(0)] * g
    for path in itertools.product(range(g), repeat=len(liks) + 1):
        w = prior[path[0]]
        for t, lik in enumerate(liks):
            w *= trans[path[t + 1]][path[t]] * lik[path[t + 1]]
        joint[path[-1]] += w
    total = sum(joint)
    assert p == [j / total for j in joint]


def test_bimodal_measurement_and_its_resolution():
    a, b, g = 0.0, 10.0, 10
    c = centers(a, b, g)

    def lik(z):
        return [math.exp(-0.5 * ((z - abs(ck - 5.0)) / 0.5) ** 2) for ck in c]

    p1 = histogram_filter([0.1] * g, None, lik(2.0))
    assert abs(sum(p1) - 1.0) < 1e-12
    # two equal peaks, at cells 2 and 3 and at cells 6 and 7
    assert abs(p1[2] - p1[7]) < 1e-12 and abs(p1[3] - p1[6]) < 1e-12
    assert abs(p1[2] - 0.2455) < 1e-4
    p2 = histogram_filter(p1, gaussian_transition(a, b, g, 1.0, 0.5), lik(0.8))
    assert abs(sum(p2[:5]) - 0.8261) < 1e-4
    assert max(range(g), key=lambda k: p2[k]) == 4


def test_zero_likelihood_everywhere_raises():
    with pytest.raises(ValueError):
        histogram_filter([0.5, 0.5, 0.0], None, [0.0, 0.0, 1.0])
    with pytest.raises(ValueError):
        gaussian_transition(0.0, 1.0, 4, 0.0, 0.0)
