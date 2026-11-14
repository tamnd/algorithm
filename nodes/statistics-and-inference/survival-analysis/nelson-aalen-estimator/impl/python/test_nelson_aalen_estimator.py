# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nelson-aalen-estimator/. The authors are listed in prov/2X5FTW.jsonl.

import math
import random
from fractions import Fraction

import pytest

from nelson_aalen_estimator import evaluate, nelson_aalen, survival_from_hazard

# 6-MP arm of Freireich et al. (1963), as listed by Gehan (1965). 0 marks a censored time.
MP_T = [6, 6, 6, 6, 7, 9, 10, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25, 32, 32, 34, 35]
MP_D = [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]


def direct(times, events, t):
    """Direct summation over the distinct event times s <= t of d(s)/n(s), d(s)/n(s)^2 and d(s)(n(s)-d(s))/n(s)^3."""
    h = v = w = Fraction(0)
    for s in sorted({y for y, e in zip(times, events) if e}):
        if s > t:
            break
        n = sum(1 for y in times if y >= s)
        d = sum(1 for y, e in zip(times, events) if y == s and e)
        h += Fraction(d, n)
        v += Fraction(d, n * n)
        w += Fraction(d * (n - d), n**3)
    return h, v, w


def test_six_mp_table() -> None:
    steps = nelson_aalen(MP_T, MP_D, exact=True)
    assert [(s.time, s.at_risk, s.events) for s in steps] == [
        (6, 21, 3), (7, 17, 1), (10, 15, 1), (13, 12, 1), (16, 11, 1), (22, 7, 1), (23, 6, 1)
    ]
    h = Fraction(3, 21) + Fraction(1, 17) + Fraction(1, 15) + Fraction(1, 12) + Fraction(1, 11) + Fraction(1, 7) + Fraction(1, 6)
    assert steps[-1].cum_hazard == h
    assert math.isclose(float(h), 0.75211, abs_tol=5e-6)
    assert math.isclose(float(steps[-1].var_poisson), 0.07810, abs_tol=5e-6)
    assert steps[0].var_poisson == Fraction(3, 441) and steps[0].var_binomial == Fraction(54, 9261)
    assert math.isclose(survival_from_hazard(steps, 23), 0.47137, abs_tol=5e-6)
    assert evaluate(steps, 5) == 0 and evaluate(steps, 100) == h


def test_against_direct_summation() -> None:
    rng = random.Random(1969)
    for _ in range(300):
        n = rng.randint(1, 25)
        times = [rng.randint(1, rng.randint(1, 12)) for _ in range(n)]
        p = rng.random()
        events = [0 if rng.random() < p else 1 for _ in range(n)]
        steps = nelson_aalen(times, events, exact=True)
        for t in range(0, max(times) + 2):
            h, v, w = direct(times, events, t)
            assert evaluate(steps, t) == h
            assert evaluate(steps, t, "var_poisson") == v
            assert evaluate(steps, t, "var_binomial") == w


def test_exp_minus_h_is_at_least_kaplan_meier() -> None:
    rng = random.Random(1972)
    for _ in range(200):
        n = rng.randint(1, 25)
        times = [rng.randint(1, 10) for _ in range(n)]
        events = [rng.randint(0, 1) for _ in range(n)]
        steps = nelson_aalen(times, events)
        s = 1.0
        for st in steps:
            s *= 1 - st.events / st.at_risk
            assert math.exp(-st.cum_hazard) >= s - 1e-15


def test_sequential_ties_equal_broken_ties() -> None:
    # Breaking the ties among events at t_j into distinct nearby times gives the sequential sum.
    rng = random.Random(1978)
    for _ in range(200):
        n = rng.randint(1, 20)
        times = [rng.randint(1, 6) for _ in range(n)]
        events = [rng.randint(0, 1) for _ in range(n)]
        seq = nelson_aalen(times, events, exact=True, ties="sequential")
        # Spread the events of each tie over distinct times just below the next integer.
        # Censorings at t move after all events at t, to t + 0.9, keeping them at risk.
        spread, k = [], {}
        for y, e in zip(times, events):
            if e:
                k[y] = k.get(y, 0) + 1
                spread.append(y + Fraction(k[y], 1000))
            else:
                spread.append(y + Fraction(9, 10))
        broken = nelson_aalen(spread, events, exact=True)
        for t in range(0, 8):
            assert evaluate(seq, t) == evaluate(broken, t + Fraction(1, 2))


def test_monte_carlo_mean_and_variance() -> None:
    # T ~ Exp(1), C ~ Exp(0.5), n = 40, t = log 2, so H(t) = log 2. r = 2000, seed 2026.
    rng = random.Random(2026)
    n, r, t = 40, 2000, math.log(2)
    hs, vs = [], []
    for _ in range(r):
        y, d = [], []
        for _ in range(n):
            a, b = rng.expovariate(1.0), rng.expovariate(0.5)
            y.append(min(a, b))
            d.append(1 if a <= b else 0)
        steps = nelson_aalen(y, d)
        hs.append(evaluate(steps, t))
        vs.append(evaluate(steps, t, "var_poisson"))
    mean = sum(hs) / r
    var = sum((x - mean) ** 2 for x in hs) / (r - 1)
    assert abs(mean - t) < 4 * math.sqrt(var / r)
    assert abs(sum(vs) / r / var - 1) < 0.15


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        nelson_aalen([], [])
    with pytest.raises(ValueError):
        nelson_aalen([1, 2], [1, 3])
    with pytest.raises(ValueError):
        nelson_aalen([1, 2], [1, 1], ties="efron")
