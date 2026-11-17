# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-reaction-method/. The authors are listed in prov/4TMPNZ.jsonl.
"""Tests of the first reaction method.

A sample mean of n values with exact mean mu and variance var must satisfy
|mean - mu| <= 4 sqrt(var / n). A distribution must pass a chi-square test
with chi2_sf(statistic, df) > 0.001.
"""

import math
import random

from biostoch import (
    binom_pmf,
    check_mean,
    chi2_sf,
    mean_var,
    poisson,
    poisson_pmf,
    ssa_direct,
)
from first_reaction_method import first_reaction_method

Z = 4.0

DEATH = [(-1,)]


def death_prop(x):
    return (1.0 * x[0],)


IMMIG_DEATH = [(1,), (-1,)]


def immig_death_prop(x):
    return (10.0, 1.0 * x[0])


# 0 -> A (c = 4), 2A -> B (c = 0.5, propensity 0.5 x_A (x_A - 1) / 2),
# B -> 2A (c = 1). No closed form; used to compare methods.
DIMER = [(1, 0), (-2, 1), (2, -1)]


def dimer_prop(x):
    return (4.0, 0.5 * x[0] * (x[0] - 1) / 2.0, 1.0 * x[1])


def pooled_cells(cells):
    """Pool (observed, expected) cells left to right until each expected
    count is at least 5; a short last group joins the one before it."""
    pooled, acc = [], [0, 0.0]
    for o, e in cells:
        acc = [acc[0] + o, acc[1] + e]
        if acc[1] >= 5.0:
            pooled.append(acc)
            acc = [0, 0.0]
    if acc != [0, 0.0]:
        if pooled:
            pooled[-1] = [pooled[-1][0] + acc[0], pooled[-1][1] + acc[1]]
        else:
            pooled.append(acc)
    return pooled


def chi_square_ok(samples, pmf, support):
    n = len(samples)
    counts = {}
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
    assert all(s in support for s in counts)
    cells = [(counts.get(k, 0), n * pmf(k)) for k in support]
    pooled = pooled_cells(cells)
    stat = sum((o - e) ** 2 / e for o, e in pooled)
    return chi2_sf(stat, len(pooled) - 1) > 0.001


def two_sample_ok(xs, ys):
    """Chi-square test that two samples of equal size have the same law."""
    keys = sorted(set(xs) | set(ys))
    cx, cy = {}, {}
    for v in xs:
        cx[v] = cx.get(v, 0) + 1
    for v in ys:
        cy[v] = cy.get(v, 0) + 1
    # Each cell: (label, count in xs, count in ys); pool by the smaller count.
    cells = []
    acc = [0, 0]
    for k in keys:
        acc[0] += cx.get(k, 0)
        acc[1] += cy.get(k, 0)
        if (acc[0] + acc[1]) / 2 >= 5:
            cells.append(acc)
            acc = [0, 0]
    if acc != [0, 0]:
        cells[-1] = [cells[-1][0] + acc[0], cells[-1][1] + acc[1]]
    nx, ny = len(xs), len(ys)
    stat = 0.0
    for ox, oy in cells:
        tot = ox + oy
        ex, ey = tot * nx / (nx + ny), tot * ny / (nx + ny)
        stat += (ox - ex) ** 2 / ex + (oy - ey) ** 2 / ey
    return chi2_sf(stat, len(cells) - 1) > 0.001


def test_pure_death_law():
    rng = random.Random(21)
    q = math.exp(-1)
    xs = [first_reaction_method(rng, (10,), DEATH, death_prop, 1.0)[1][-1][0] for _ in range(1500)]
    assert chi_square_ok(xs, lambda k: binom_pmf(k, 10, q), list(range(11)))
    m, _ = mean_var(xs)
    assert check_mean(m, 10 * q, 10 * q * (1 - q), len(xs), Z)


def test_pure_death_moments_from_100():
    rng = random.Random(22)
    reps = 150
    xs = [first_reaction_method(rng, (100,), DEATH, death_prop, 1.0)[1][-1][0] for _ in range(reps)]
    mu = 100 * math.exp(-1)
    var = mu * (1 - math.exp(-1))
    m, v = mean_var(xs)
    assert check_mean(m, mu, var, reps, Z)
    assert abs(v / var - 1) <= Z * math.sqrt(2 / (reps - 1))


def test_immigration_death_from_zero():
    rng = random.Random(23)
    lam = 10 * (1 - math.exp(-1))
    xs = [first_reaction_method(rng, (0,), IMMIG_DEATH, immig_death_prop, 1.0)[1][-1][0] for _ in range(1500)]
    m, _ = mean_var(xs)
    assert check_mean(m, lam, lam, len(xs), Z)
    assert chi_square_ok(xs, lambda k: poisson_pmf(k, lam), list(range(max(xs) + 1)))


def test_immigration_death_stationary():
    rng = random.Random(24)
    reps = 800
    xs = []
    for _ in range(reps):
        x0 = poisson(rng, 10.0)
        xs.append(first_reaction_method(rng, (x0,), IMMIG_DEATH, immig_death_prop, 0.5)[1][-1][0])
    m, v = mean_var(xs)
    assert check_mean(m, 10.0, 10.0, reps, Z)
    assert abs(v / 10.0 - 1) <= Z * math.sqrt(2 / (reps - 1))


def test_one_step_law():
    # The minimum of independent Exp(a_j) is Exp(a0), and its index is j
    # with probability a_j / a0.
    x = (5, 4)
    a = dimer_prop(x)
    a0 = sum(a)
    rng = random.Random(25)
    reps = 3000
    waits, picks = [], []
    for _ in range(reps):
        times, states, _ = first_reaction_method(rng, x, DIMER, dimer_prop, math.inf, 1)
        waits.append(times[1])
        picks.append(DIMER.index((states[1][0] - x[0], states[1][1] - x[1])))
    m, v = mean_var(waits)
    assert check_mean(m, 1 / a0, 1 / a0 ** 2, reps, Z)
    assert chi_square_ok(picks, lambda j: a[j] / a0, [0, 1, 2])


def test_same_law_as_direct_method():
    # The state of A at t = 2 from (3, 1), first reaction against direct.
    reps = 1200
    rng_f, rng_d = random.Random(26), random.Random(27)
    fx = [first_reaction_method(rng_f, (3, 1), DIMER, dimer_prop, 2.0)[1][-1] for _ in range(reps)]
    dx = [ssa_direct(rng_d, (3, 1), DIMER, dimer_prop, 2.0)[1][-1] for _ in range(reps)]
    assert two_sample_ok([s[0] for s in fx], [s[0] for s in dx])
    assert two_sample_ok([s[1] for s in fx], [s[1] for s in dx])
    # Conservation: x_A + 2 x_B changes only by the source reaction.
    assert all(s[0] + 2 * s[1] >= 5 for s in fx)


class CountingRandom(random.Random):
    def __init__(self, seed):
        super().__init__(seed)
        self.calls = 0

    def expovariate(self, lambd=1.0):
        self.calls += 1
        return super().expovariate(lambd)


def test_draws_per_step():
    # One exponential per reaction with a positive propensity in each step.
    rng = CountingRandom(28)
    times, states, _ = first_reaction_method(rng, (3, 0), DIMER, dimer_prop, math.inf, 40)
    expected = 0
    for x in states[:-1]:
        expected += sum(1 for v in dimer_prop(x) if v > 0)
    assert rng.calls == expected
    # Pure death to extinction: x0 events, then a step with no draw.
    times, states, complete = first_reaction_method(random.Random(29), (6,), DEATH, death_prop, math.inf)
    assert complete and len(times) == 7 and states[-1] == (0,)
