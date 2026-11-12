# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birth-death-process/. The authors are listed in prov/PEBREY.jsonl.

import math
import random
from fractions import Fraction as F

from birth_death_process import (
    expected_reconstructed,
    extinction_probability,
    kendall_alpha_beta,
    kendall_alpha_beta_critical,
    pgf,
    probability,
    reconstructed_count,
    simulate_count,
    simulate_tree,
    survival_probability,
)

RATES = [(F(1), F(1, 2)), (F(2), F(3)), (F(3, 2), F(0)), (F(1, 3), F(1, 5))]


def test_mean_and_total_exact() -> None:
    for lam, mu in RATES:
        for z in (F(1, 3), F(2), F(7, 2)):
            if (lam - mu) * (z - 1) < 0:
                continue  # z = exp((lam - mu) t) with t > 0
            alpha, beta = kendall_alpha_beta(lam, mu, z)
            assert 0 <= alpha < 1 and 0 <= beta < 1
            assert alpha + (1 - alpha) == 1
            assert (1 - alpha) / (1 - beta) == z  # E[N(t)] = exp(r t)


def test_branching_property_exact() -> None:
    """G_{t+s}(x) = G_t(G_s(x)): the semigroup law, with z_{t+s} = z_t z_s."""
    xs = [F(0), F(1, 4), F(2, 3), F(1)]
    for lam, mu in RATES:
        zs = (F(3, 2), F(5, 2)) if lam > mu else (F(1, 2), F(4, 5))
        a1, b1 = kendall_alpha_beta(lam, mu, zs[0])
        a2, b2 = kendall_alpha_beta(lam, mu, zs[1])
        a3, b3 = kendall_alpha_beta(lam, mu, zs[0] * zs[1])
        for x in xs:
            assert pgf(pgf(x, a2, b2), a1, b1) == pgf(x, a3, b3)
    for a, b in ((F(1, 2), F(3, 4)), (F(2), F(1, 3))):
        p, q, s = (kendall_alpha_beta_critical(v) for v in (a, b, a + b))
        for x in xs:
            assert pgf(pgf(x, *q), *p) == pgf(x, *s)


def test_small_time_rates() -> None:
    """For small t, P(N = 2) ~ lam t and P(N = 0) ~ mu t."""
    lam, mu, t = 1.3, 0.4, 1e-6
    alpha, beta = kendall_alpha_beta(lam, mu, math.exp((lam - mu) * t))
    assert abs(probability(0, alpha, beta) / t - mu) < 1e-4
    assert abs(probability(2, alpha, beta) / t - lam) < 1e-4


def test_yule_case_is_geometric() -> None:
    z = F(5)
    alpha, beta = kendall_alpha_beta(F(1), F(0), z)
    assert alpha == 0
    for n in range(1, 8):
        assert probability(n, alpha, beta) == F(1, 5) * F(4, 5) ** (n - 1)


def test_extinction_limits() -> None:
    for lam, mu in ((1.0, 0.5), (0.5, 1.0), (2.0, 0.0)):
        alpha, _ = kendall_alpha_beta(lam, mu, math.exp((lam - mu) * 60))
        assert abs(alpha - extinction_probability(lam, mu)) < 1e-9
        assert abs(1 - alpha - survival_probability(lam, mu, 60)) < 1e-12
    alpha, _ = kendall_alpha_beta_critical(1e9)
    assert abs(alpha - extinction_probability(1.0, 1.0)) < 1e-8


def test_simulated_counts_match_kendall() -> None:
    rng = random.Random(21)
    lam, mu, t, reps = 1.0, 0.5, 2.0, 40000
    counts = [simulate_count(lam, mu, t, rng) for _ in range(reps)]
    alpha, beta = kendall_alpha_beta(lam, mu, math.exp((lam - mu) * t))
    for n in range(4):
        p = probability(n, alpha, beta)
        freq = counts.count(n) / reps
        assert abs(freq - p) < 4 * math.sqrt(p * (1 - p) / reps)
    mean = sum(counts) / reps
    var = sum(probability(n, alpha, beta) * n * n for n in range(400)) - math.e ** 2
    assert abs(mean - math.e) < 4 * math.sqrt(var / reps)


def test_reconstructed_lineages() -> None:
    rng = random.Random(22)
    lam, mu, t_max, reps = 1.0, 0.6, 3.0, 8000
    times = (0.5, 1.5, 2.5, 2.9)
    totals = [0] * len(times)
    sq = [0] * len(times)
    for _ in range(reps):
        tree = simulate_tree(lam, mu, t_max, rng)
        for i, s in enumerate(times):
            c = reconstructed_count(tree, s)
            totals[i] += c
            sq[i] += c * c
    for i, s in enumerate(times):
        mean = totals[i] / reps
        sd = math.sqrt(sq[i] / reps - mean * mean)
        assert abs(mean - expected_reconstructed(lam, mu, s, t_max)) < 4 * sd / math.sqrt(reps)
