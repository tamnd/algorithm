# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tau-leaping/. The authors are listed in prov/Q8TJ4W.jsonl.
"""Tests of tau-leaping.

Tau-leaping is approximate, so the tests check two things: the code gives
the exact law of the leap chain where that law is known, and the error of
the leap chain against the exact process is small where the step is short
and large where it is long.

A sample mean of n values with exact mean mu and variance var must satisfy
|mean - mu| <= 4 sqrt(var / n). A sample variance must be within the
relative tolerance 4 sqrt(2 / (n - 1)) of the exact variance (near-normal
data).
"""

import math
import random

from biostoch import check_mean, mean_var, poisson, ssa_direct
from tau_leaping import adaptive_tau_leap, fixed_step_leap, highest_order_factors

Z = 4.0

DEATH = [(-1,)]


def death_prop(x):
    return (1.0 * x[0],)


IMMIG_DEATH = [(1,), (-1,)]


def immig_death_prop(x):
    return (10.0, 1.0 * x[0])


def immig_death_1000(x):
    return (1000.0, 1.0 * x[0])


def var_ok(v, var, n):
    return abs(v / var - 1) <= Z * math.sqrt(2 / (n - 1))


def leap_death_moments(x0, tau, steps):
    """Mean and variance of the fixed step leap chain for X -> 0 at rate 1:
    x' = x - Poisson(x tau), so m' = (1 - tau) m and
    V' = (1 - tau)^2 V + tau m."""
    m, v = float(x0), 0.0
    for _ in range(steps):
        v = (1 - tau) ** 2 * v + tau * m
        m = (1 - tau) * m
    return m, v


def test_order_factors():
    # 2A -> B, A + B -> C, B -> 0.
    g = highest_order_factors([(2, 0), (1, 1), (0, 1)])
    assert g[0](11) == 2 + 1 / 10
    assert g[1](11) == 2.0
    g = highest_order_factors([(1, 0), (0, 1)])
    assert g[0](5) == 1.0 and g[1](5) == 1.0
    g = highest_order_factors([(3, 0), (1, 2)])
    assert g[0](7) == 3 + 1 / 6 + 2 / 5
    assert g[1](7) == 1.5 * (2 + 1 / 6)


def test_long_fixed_step_is_biased():
    # tau = 0.5 on pure death from 100: the leap chain has mean 25 and
    # variance 37.5 at t = 1, while the exact X(1) has mean 36.79.
    rng = random.Random(41)
    n = 400
    xs = [fixed_step_leap(rng, (100,), DEATH, death_prop, 0.5, 1.0)[1][-1][0] for _ in range(n)]
    mu, var = leap_death_moments(100, 0.5, 2)
    assert (mu, var) == (25.0, 37.5)
    m, v = mean_var(xs)
    assert check_mean(m, mu, var, n, Z)
    assert var_ok(v, var, n)
    q = math.exp(-1)
    assert not check_mean(m, 100 * q, 100 * q * (1 - q), n, Z)


def test_short_fixed_step_is_close():
    # tau = 0.01: the leap chain has mean 36.603 at t = 1, 0.5 percent
    # below the exact 36.788.
    rng = random.Random(42)
    n = 300
    xs = [fixed_step_leap(rng, (100,), DEATH, death_prop, 0.01, 1.0)[1][-1][0] for _ in range(n)]
    mu, var = leap_death_moments(100, 0.01, 100)
    m, v = mean_var(xs)
    assert check_mean(m, mu, var, n, Z)
    assert var_ok(v, var, n)
    exact = 100 * math.exp(-1)
    assert abs(mu - exact) / exact < 0.006


def test_stationary_variance_of_fixed_step():
    # For immigration-death the leap chain has the stationary mean 10 and
    # the stationary variance 20 / (2 - tau); the exact law is Poisson(10).
    rng = random.Random(43)
    n = 2000
    tau = 0.5
    xs = [fixed_step_leap(rng, (poisson(rng, 10.0),), IMMIG_DEATH, immig_death_prop, tau, 10.0)[1][-1][0]
          for _ in range(n)]
    m, v = mean_var(xs)
    leap_var = 20 / (2 - tau)
    assert check_mean(m, 10.0, leap_var, n, Z)
    assert var_ok(v, leap_var, n)
    assert not var_ok(v, 10.0, n)


def test_negative_counts_are_rejected():
    rng = random.Random(44)
    rejected = 0
    for _ in range(200):
        times, states, info = fixed_step_leap(rng, (3,), DEATH, death_prop, 1.0, 3.0)
        assert all(s[0] >= 0 for s in states)
        assert times[-1] == 3.0 or states[-1] == (0,)
        rejected += info["rejected"]
    assert rejected > 0


def test_all_critical_is_the_direct_method():
    # A <-> B with 8 molecules: every reaction is critical (L_j < 10), so
    # each step fires one reaction after an Exp(a0) wait, with the same
    # draws as ssa_direct.
    stoich = [(-1, 1), (1, -1)]
    reactants = [(1, 0), (0, 1)]

    def prop(x):
        return (1.0 * x[0], 2.0 * x[1])

    for seed in range(5):
        a = adaptive_tau_leap(random.Random(seed), (8, 0), stoich, prop, reactants, 3.0)
        b = ssa_direct(random.Random(seed), (8, 0), stoich, prop, 3.0)
        assert a[0] == b[0] and a[1] == b[1]
        assert a[2]["ssa_steps"] == 0


def test_adaptive_pure_death_is_close():
    # eps = 0.03 from 1000: about 34 leaps instead of about 632 events, and
    # the mean at t = 1 is within 3 percent of 1000 e^-1.
    rng = random.Random(45)
    n = 200
    xs, steps = [], 0
    for _ in range(n):
        times, states, info = adaptive_tau_leap(rng, (1000,), DEATH, death_prop, [(1,)], 1.0)
        xs.append(states[-1][0])
        steps += info["leaps"] + info["ssa_steps"]
    m, _ = mean_var(xs)
    exact = 1000 * math.exp(-1)
    assert abs(m - exact) / exact < 0.03
    assert steps / n < 50
    assert all(x >= 0 for x in xs)


def test_adaptive_stationary_variance_is_inflated():
    # Immigration-death with rates 1000 and 1: the leap condition holds
    # (steps near 0.44) and the mean stays at 1000, but the stationary
    # variance is near 2000 / (2 - 0.44), not the exact 1000.
    rng = random.Random(46)
    n = 1000
    xs = [adaptive_tau_leap(rng, (poisson(rng, 1000.0),), IMMIG_DEATH, immig_death_1000,
                            [(0,), (1,)], 5.0)[1][-1][0] for _ in range(n)]
    m, v = mean_var(xs)
    assert check_mean(m, 1000.0, 2000 / (2 - 0.52), n, Z)
    assert v / 1000.0 - 1 > Z * math.sqrt(2 / (n - 1))
