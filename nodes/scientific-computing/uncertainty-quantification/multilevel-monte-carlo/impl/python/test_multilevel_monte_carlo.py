# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-monte-carlo/. The authors are listed in prov/SAT4ZW.jsonl.
import math
import random

from multilevel_monte_carlo import euler_gbm_mean, gbm_euler_sampler, mlmc, optimal_counts

S0, R, SIGMA, T = 1.0, 0.05, 0.2, 1.0
EXACT = S0 * math.exp(R * T)  # E[S_T] for geometric Brownian motion


def deterministic_sampler(l, n, rng):
    """P_l = 1 - 2^-(l+1) with no noise: Y_0 = 1/2 and Y_l = 2^-(l+1) for l >= 1."""
    y = 0.5 if l == 0 else 2.0 ** -(l + 1)
    return n * y, n * y * y, float(n * 2**l)


def test_telescoping_sum_is_exact_without_noise():
    res = mlmc(deterministic_sampler, 1e-3, 1.0, 1.0, 1.0, random.Random(0), l0=2, n0=4)
    big_l = res["L"]
    assert abs(res["estimate"] - (1.0 - 2.0 ** -(big_l + 1))) < 1e-15
    # the bias estimate of level L is 2^-(L+1); L is the first level where it is at most eps / sqrt(2)
    assert big_l == 10
    assert 2.0 ** -(big_l + 1) <= 1e-3 / math.sqrt(2) < 2.0**-big_l


def test_optimal_counts_reach_half_eps_squared():
    v = [0.04, 4e-4, 2e-4, 1e-4]
    c = [1.0, 3.0, 6.0, 12.0]
    eps = 0.001
    n = optimal_counts(v, c, eps)
    assert sum(vl / nl for vl, nl in zip(v, n)) <= eps**2 / 2
    # the counts follow sqrt(V_l / C_l), up to the rounding up
    for l in range(1, 4):
        ratio = n[l] / n[0]
        assert abs(ratio - math.sqrt(v[l] / c[l]) / math.sqrt(v[0] / c[0])) < 2e-3


def test_level_means_match_the_exact_euler_bias():
    sample = gbm_euler_sampler(S0, R, SIGMA, T)
    rng = random.Random(7)
    n = 4000
    for l in range(4):
        a, b, _ = sample(l, n, rng)
        mean = a / n
        se = math.sqrt((b / n - mean * mean) / n)
        exact = euler_gbm_mean(S0, R, T, l) - (euler_gbm_mean(S0, R, T, l - 1) if l > 0 else 0.0)
        assert abs(mean - exact) < 4 * se


def test_correction_variance_halves_per_level():
    sample = gbm_euler_sampler(S0, R, SIGMA, T)
    rng = random.Random(11)
    n = 3000
    v = []
    for l in range(1, 6):
        a, b, _ = sample(l, n, rng)
        v.append(b / n - (a / n) ** 2)
    for l in range(1, len(v)):
        assert 0.35 < v[l] / v[l - 1] < 0.65  # beta = 1 for Euler-Maruyama on GBM


def test_mlmc_rmse_on_gbm_is_below_eps():
    sample = gbm_euler_sampler(S0, R, SIGMA, T)
    eps = 0.002
    errors = []
    for seed in range(20):
        res = mlmc(sample, eps, 1.0, 1.0, 1.0, random.Random(seed))
        errors.append(res["estimate"] - EXACT)
        assert sum(vl / nl for vl, nl in zip(res["variances"], res["N"])) <= eps**2 / 2 * 1.0001
    rmse = math.sqrt(sum(e * e for e in errors) / len(errors))
    assert rmse < 1.3 * eps


def test_mlmc_is_cheaper_than_plain_monte_carlo():
    sample = gbm_euler_sampler(S0, R, SIGMA, T)
    eps = 0.001
    res = mlmc(sample, eps, 1.0, 1.0, 1.0, random.Random(3))
    v0 = res["variances"][0]
    plain_cost = 2 * v0 / eps**2 * 2 ** res["L"]
    assert res["cost"] < plain_cost
