# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-decay/. The authors are listed in prov/PZMNKF.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from exponential_decay import DecayedAggregate, base_factor, exp_factor


def brute(items, beta, t):
    c = sum(beta ** (t - ti) for ti, _ in items if ti <= t)
    s = sum(beta ** (t - ti) * x for ti, x in items if ti <= t)
    return c, s


def test_page_example():
    a = DecayedAggregate(base_factor(F(1, 2)))
    for t, x in [(0, 4), (1, 8), (1, 6), (3, 2)]:
        a.add(t, x)
    assert a.count(3) == F(13, 8)
    assert a.total(3) == 6
    assert a.average() == F(48, 13)
    assert a.count(5) == F(13, 32)


def random_items(rng, n):
    t, out = 0, []
    for _ in range(n):
        t += rng.choice([0, 0, 1, 2, 5])
        out.append((t, F(rng.randint(-20, 20))))
    return out


def test_against_brute_force_exact():
    rng = random.Random(1)
    for _ in range(150):
        beta = F(rng.randint(1, 9), 10)
        items = random_items(rng, rng.randint(1, 30))
        a = DecayedAggregate(base_factor(beta))
        for k, (ti, x) in enumerate(items):
            a.add(ti, x)
            for q in (ti, ti + 1, ti + 3):
                c, s = brute(items[: k + 1], beta, q)
                assert a.count(q) == c and a.total(q) == s


def test_merge_exact():
    rng = random.Random(2)
    for _ in range(100):
        beta = F(rng.randint(1, 9), 10)
        items = random_items(rng, rng.randint(2, 30))
        left, right = DecayedAggregate(base_factor(beta)), DecayedAggregate(base_factor(beta))
        for it in items:
            (left if rng.random() < 0.5 else right).add(*it)
        m = left.merge(right)
        q = items[-1][0] + 2
        assert (m.count(q), m.total(q)) == brute(items, beta, q)


def test_unit_gaps_equal_corrected_ema():
    # one item per step: S/C is the bias-corrected EMA with 1 - alpha = beta
    rng = random.Random(3)
    for _ in range(50):
        beta = F(rng.randint(1, 9), 10)
        xs = [F(rng.randint(-9, 9)) for _ in range(rng.randint(1, 20))]
        a = DecayedAggregate(base_factor(beta))
        s = 0
        for t, x in enumerate(xs, 1):
            a.add(t, x)
            s = (1 - beta) * x + beta * s  # EMA from s_0 = 0
            assert a.average() == s / (1 - beta ** t)


def test_constant_rate_count_and_half_life():
    lam = 0.05
    a = DecayedAggregate(exp_factor(lam))
    for t in range(2000):
        a.add(t)
    assert abs(a.count(1999) - 1 / (1 - math.exp(-lam))) < 1e-9
    half = math.log(2) / lam
    assert abs(a.count(1999 + half) - a.count(1999) / 2) < 1e-9


def test_time_must_not_go_back():
    a = DecayedAggregate(exp_factor(1.0))
    a.add(5)
    with pytest.raises(ValueError):
        a.add(4)
