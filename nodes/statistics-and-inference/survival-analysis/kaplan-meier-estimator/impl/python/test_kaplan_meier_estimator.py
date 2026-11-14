# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kaplan-meier-estimator/. The authors are listed in prov/FNVF5H.jsonl.

import math
import random
from fractions import Fraction

import pytest

from kaplan_meier_estimator import greenwood_variance, kaplan_meier

# 6-MP arm of Freireich et al. (1963), as listed by Gehan (1965). 0 marks a censored time.
MP_T = [6, 6, 6, 6, 7, 9, 10, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25, 32, 32, 34, 35]
MP_D = [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
PL_T = [1, 1, 2, 2, 3, 4, 4, 5, 5, 8, 8, 8, 8, 11, 11, 12, 12, 15, 17, 22, 23]


def product_limit(times, events, t):
    """The product-limit formula written out: product over event times s <= t of (1 - d(s)/n(s))."""
    s = Fraction(1)
    for u in sorted({y for y, e in zip(times, events) if e}):
        if u > t:
            break
        n = sum(1 for y in times if y >= u)
        d = sum(1 for y, e in zip(times, events) if y == u and e)
        s *= Fraction(n - d, n)
    return s


def redistribute_to_the_right(times, events):
    """Efron's construction: start with mass 1/n on each subject, ordered by time with
    events before censorings at equal times; each censored subject, in turn, gives its
    mass in equal parts to every subject after it. Returns 1 - (event mass up to t) as a function."""
    n = len(times)
    order = sorted(range(n), key=lambda k: (times[k], -events[k]))
    mass = [Fraction(1, n)] * n
    for pos, k in enumerate(order):
        if not events[k] and pos < n - 1:
            share = mass[pos] / (n - 1 - pos)
            for later in range(pos + 1, n):
                mass[later] += share
            mass[pos] = Fraction(0)

    def surv(t):
        return 1 - sum((mass[p] for p, k in enumerate(order) if events[k] and times[k] <= t), Fraction(0))

    return surv


def random_data(rng, n, tmax, pcens):
    times = [rng.randint(1, tmax) for _ in range(n)]
    events = [0 if rng.random() < pcens else 1 for _ in range(n)]
    return times, events


def test_six_mp_table() -> None:
    km = kaplan_meier(MP_T, MP_D, exact=True)
    rows = [(s.time, s.at_risk, s.events, s.survival) for s in km.steps]
    assert rows == [
        (6, 21, 3, Fraction(6, 7)),
        (7, 17, 1, Fraction(96, 119)),
        (10, 15, 1, Fraction(64, 85)),
        (13, 12, 1, Fraction(176, 255)),
        (16, 11, 1, Fraction(32, 51)),
        (22, 7, 1, Fraction(64, 119)),
        (23, 6, 1, Fraction(160, 357)),
    ]
    assert km(5) == 1 and km(9) == Fraction(96, 119) and km(34) == Fraction(160, 357)
    assert km.median() == 23
    assert math.isclose(math.sqrt(greenwood_variance(km, 23)), 0.13459, abs_tol=5e-5)
    assert math.isclose(math.sqrt(greenwood_variance(km, 6)), 0.07636, abs_tol=5e-5)
    # The largest time, 35, is censored, so S-hat is undefined after 35.
    assert km(35) == Fraction(160, 357)
    with pytest.raises(ValueError):
        km(35.5)


def test_placebo_arm_is_the_empirical_survival_function() -> None:
    km = kaplan_meier(PL_T, [1] * len(PL_T), exact=True)
    assert [s.survival for s in km.steps] == [Fraction(k, 21) for k in (19, 17, 16, 14, 12, 8, 6, 4, 3, 2, 1, 0)]
    assert km.median() == 8
    assert km(100) == 0


def test_against_product_limit_formula() -> None:
    rng = random.Random(20261114)
    for _ in range(300):
        n = rng.randint(1, 25)
        times, events = random_data(rng, n, rng.randint(1, 12), rng.random())
        km = kaplan_meier(times, events, exact=True)
        t_max = max(times)
        for t in range(0, t_max + 2):
            try:
                got = km(t)
            except ValueError:
                assert t > t_max and not any(e for y, e in zip(times, events) if y == t_max)
                continue
            assert got == product_limit(times, events, t)


def test_no_censoring_gives_empirical_survival() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 30)
        times = [rng.randint(1, 10) for _ in range(n)]
        km = kaplan_meier(times, [1] * n, exact=True)
        for t in range(0, 12):
            assert km(t) == Fraction(sum(1 for y in times if y > t), n)


def test_equals_redistribute_to_the_right() -> None:
    rng = random.Random(1967)
    for _ in range(300):
        n = rng.randint(1, 20)
        times, events = random_data(rng, n, rng.randint(1, 8), rng.random())
        km = kaplan_meier(times, events, exact=True)
        rtr = redistribute_to_the_right(times, events)
        for step in km.steps:
            assert step.survival == rtr(step.time)


def test_self_consistency_equation() -> None:
    # Efron (1967): S(t) = (1/n) [#{y_i > t} + sum over censored y_i <= t of S(t) / S(y_i)].
    rng = random.Random(831)
    for _ in range(200):
        n = rng.randint(1, 20)
        times, events = random_data(rng, n, 9, rng.random())
        km = kaplan_meier(times, events, exact=True)
        for t in range(0, max(times) + 1):
            s = km(t)
            rhs = sum(1 for y in times if y > t) + sum(
                (s / km(y) for y, e in zip(times, events) if not e and y <= t and km(y) > 0), Fraction(0)
            )
            assert s == rhs / n


def test_float_and_exact_agree() -> None:
    rng = random.Random(3)
    for _ in range(100):
        times, events = random_data(rng, 40, 15, 0.4)
        a = kaplan_meier(times, events)
        b = kaplan_meier(times, events, exact=True)
        for x, y in zip(a.steps, b.steps):
            assert x[:3] == y[:3] and math.isclose(x.survival, float(y.survival), rel_tol=1e-12, abs_tol=1e-15)


def log_lik(times, events, support, probs, tail):
    """Log-likelihood of a distribution with mass probs[j] at support[j] and mass tail after support[-1]."""
    total = 0.0
    for y, e in zip(times, events):
        if e:
            p = probs[support.index(y)]
        else:
            p = sum(q for s, q in zip(support, probs) if s > y) + tail
        if p <= 0:
            return -math.inf
        total += math.log(p)
    return total


def test_kaplan_meier_maximizes_the_likelihood() -> None:
    rng = random.Random(1958)
    for _ in range(60):
        times, events = random_data(rng, 15, 10, 0.4)
        if not any(events):
            continue
        km = kaplan_meier(times, events)
        support = [s.time for s in km.steps]
        prev, probs = 1.0, []
        for s in km.steps:
            probs.append(prev - s.survival)
            prev = s.survival
        best = log_lik(times, events, support, probs, prev)
        for _ in range(200):
            w = [rng.expovariate(1.0) for _ in range(len(support) + 1)]
            z = sum(w)
            alt = log_lik(times, events, support, [x / z for x in w[:-1]], w[-1] / z)
            assert alt <= best + 1e-9


def test_greenwood_without_censoring_is_binomial_variance() -> None:
    rng = random.Random(1926)
    for _ in range(200):
        n = rng.randint(2, 30)
        times = [rng.randint(1, 10) for _ in range(n)]
        km = kaplan_meier(times, [1] * n, exact=True)
        for t in range(0, 11):
            s = km(t)
            assert greenwood_variance(km, t) == s * (1 - s) / n


def test_last_time_rules_and_median() -> None:
    km = kaplan_meier([1, 2, 3], [1, 0, 1], exact=True)
    assert km(3) == 0 and km(10) == 0
    km = kaplan_meier([1, 2, 3], [1, 1, 0], exact=True)
    assert km(2) == Fraction(1, 3) and km(3) == Fraction(1, 3)
    with pytest.raises(ValueError):
        km(4)
    assert km.median() == 2
    assert kaplan_meier([5, 6], [0, 0]).median() is None
    # A censoring tied with an event stays in the risk set at that time.
    km = kaplan_meier([2, 2, 4], [1, 0, 1], exact=True)
    assert km.steps[0].at_risk == 3 and km(2) == Fraction(2, 3)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        kaplan_meier([], [])
    with pytest.raises(ValueError):
        kaplan_meier([1, 2], [1])
    with pytest.raises(ValueError):
        kaplan_meier([1, 2], [1, 2])
