# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-imputation/. The authors are listed in prov/W9KZM4.jsonl.

import math
import random
from fractions import Fraction

from multiple_imputation import (
    impute_normal_regression,
    multiple_imputation,
    pooled_interval,
    regression_posterior,
    rubin_pool,
)
from stdist import norm_ppf, t_ppf


def mean_analysis(x, y):
    n = len(y)
    m = sum(y) / n
    s2 = sum((v - m) ** 2 for v in y) / (n - 1)  # divisor n - 1
    return m, s2 / n


def test_rubin_rules_hand_example_exact():
    p = rubin_pool([Fraction(1), Fraction(2), Fraction(3)], [Fraction(1, 2)] * 3)
    assert p.qbar == 2 and p.w == Fraction(1, 2) and p.b == 1
    assert p.t == Fraction(11, 6) and p.r == Fraction(8, 3) and p.lam == Fraction(8, 11)
    assert abs(p.df - 121 / 32) < 1e-12  # (m - 1)(1 + 1/r)^2 = 2 (11/8)^2


def test_no_between_variance():
    p = rubin_pool([1.5, 1.5, 1.5, 1.5], [0.2, 0.3, 0.1, 0.2])
    assert p.b == 0 and abs(p.t - 0.2) < 1e-15 and math.isinf(p.df)
    lo, hi = pooled_interval(p)
    assert abs(hi - 1.5 - norm_ppf(0.975) * math.sqrt(0.2)) < 1e-12


def test_barnard_rubin_df_limits():
    rng = random.Random(1)
    for _ in range(200):
        m = rng.randint(2, 30)
        qs = [rng.gauss(0, 1) for _ in range(m)]
        us = [rng.uniform(0.1, 2) for _ in range(m)]
        rub = rubin_pool(qs, us)
        for nu in (5, 30, 1000):
            br = rubin_pool(qs, us, df_com=nu)
            assert br.df <= rub.df + 1e-9 and br.df <= nu
        big = rubin_pool(qs, us, df_com=1e12)
        assert abs(big.df - rub.df) <= 1e-6 * rub.df


def test_interval_uses_t_quantile():
    p = rubin_pool([1.0, 2.0, 4.0], [0.5, 0.5, 0.5])
    lo, hi = pooled_interval(p, 0.9)
    assert abs((hi - lo) / 2 - t_ppf(0.95, p.df) * math.sqrt(p.t)) < 1e-12


def test_observed_values_never_change():
    rng = random.Random(2)
    x = [[1.0, rng.gauss(0, 1)] for _ in range(30)]
    y = [1 + 2 * r[1] + rng.gauss(0, 1) if i % 3 else None for i, r in enumerate(x)]
    for _ in range(5):
        yc = impute_normal_regression(y, x, rng)
        assert all(a == b for a, b in zip(y, yc) if a is not None)
        assert all(v is not None for v in yc)


def test_draws_match_posterior_predictive_moments():
    # y* | data is t with mean x0' beta-hat and variance RSS/(n_obs - p - 2) (1 + x0' V x0).
    xo = [[1.0, v] for v in (0, 1, 2, 3, 4, 5, 6, 8, 9, 11)]
    yo = [1.2, 2.9, 5.3, 6.8, 9.4, 10.6, 13.5, 17.1, 18.7, 23.4]
    x0 = [1.0, 7.0]
    beta, rss, v, dfr = regression_posterior(xo, yo)
    mean = beta[0] + 7 * beta[1]
    quad = sum(x0[i] * v[i][j] * x0[j] for i in range(2) for j in range(2))
    var = rss / (dfr - 2) * (1 + quad)
    rng = random.Random(3)
    r = 20000
    draws = [impute_normal_regression(yo + [None], xo + [x0], rng)[-1] for _ in range(r)]
    dm = sum(draws) / r
    dv = sum((d - dm) ** 2 for d in draws) / (r - 1)
    assert abs(dm - mean) < 4 * math.sqrt(var / r)
    assert abs(dv / var - 1) < 0.06


def mar_sample(rng, n):
    x, y = [], []
    for _ in range(n):
        u = rng.gauss(0, 1)
        v = 1 + 2 * u + rng.gauss(0, 1)
        p_miss = 1 / (1 + math.exp(-(-0.5 + 1.5 * u)))  # depends on x only: MAR
        x.append([1.0, u])
        y.append(None if rng.random() < p_miss else v)
    return x, y


def test_coverage_under_mar_measured():
    # Measured, not proved. Target: E y = 1.
    rng = random.Random(4)
    reps, n = 200, 200
    z = norm_ppf(0.975)
    hit_mi = hit_cc = hit_si = 0
    for rep in range(reps):
        x, y = mar_sample(rng, n)
        pooled, _ = multiple_imputation(y, x, mean_analysis, m=10, seed=rep)
        lo, hi = pooled_interval(pooled)
        hit_mi += lo <= 1 <= hi
        obs = [v for v in y if v is not None]
        m, u = mean_analysis(None, obs)
        hit_cc += abs(m - 1) <= z * math.sqrt(u)
        beta, _, _, _ = regression_posterior([x[i] for i, v in enumerate(y) if v is not None], obs)
        filled = [v if v is not None else beta[0] + beta[1] * r[1] for v, r in zip(y, x)]
        m, u = mean_analysis(None, filled)
        hit_si += abs(m - 1) <= z * math.sqrt(u)
    assert abs(hit_mi / reps - 0.95) < 0.05
    assert hit_cc / reps < 0.5  # complete cases are biased under this MAR mechanism
    assert hit_si / reps < hit_mi / reps  # single imputation understates the variance
