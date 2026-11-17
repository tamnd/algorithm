# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ricker-model/. The authors are listed in prov/ZBTGC3.jsonl.
"""Tests of the Ricker model against the page values and the closed forms."""

import math
import random

import pytest

from ricker_model import (
    attractor,
    fit_stock_recruitment,
    from_stock_recruitment,
    lyapunov,
    multiplier,
    orbit,
    step,
    to_stock_recruitment,
    two_cycle,
    two_cycle_limit,
)


def close(xs, ys, tol=1e-6):
    return len(xs) == len(ys) and all(abs(a - b) < tol for a, b in zip(xs, ys))


def test_page_trace_and_scaling():
    assert close(orbit(1.5, 0.2, 6), [0.664023, 1.099139, 0.947260, 1.025241, 0.987149, 1.006362])
    scaled = orbit(1.5, 0.2, 6)
    assert close(orbit(1.5, 200.0, 6, K=1000.0), [1000 * u for u in scaled], tol=1e-9)
    assert orbit(2.0, 0.5, 0) == []
    with pytest.raises(ValueError):
        orbit(2.0, 0.5, 3, K=0)


def test_stock_recruitment_forms():
    rng = random.Random(61)
    for _ in range(200):
        r, K = rng.uniform(0.1, 3), rng.uniform(1, 1000)
        a, b = to_stock_recruitment(r, K)
        s = rng.uniform(0, 3 * K)
        assert abs(a * s * math.exp(-b * s) - step(r, s, K)) < 1e-9 * max(1, s)
        r2, K2 = from_stock_recruitment(a, b)
        assert abs(r2 - r) < 1e-12 and abs(K2 - K) < 1e-9 * K
    with pytest.raises(ValueError):
        from_stock_recruitment(0.5, 1)


def test_fixed_point_and_bound():
    for r in (0.5, 1.0, 1.5, 1.9):
        assert abs(multiplier(r, [1.0]) - (1 - r)) < 1e-12
        assert close(attractor(r), [1.0], tol=1e-8)
    rng = random.Random(62)
    for _ in range(2000):
        r = rng.uniform(0.1, 4)
        u = rng.uniform(1e-6, 10)
        v = step(r, u)
        assert 0 < v <= math.exp(r - 1) / r * (1 + 1e-12)


def test_two_cycle():
    assert two_cycle(2.0) is None
    for r in (2.1, 2.3, 2.5):
        p, q = two_cycle(r)
        assert abs(p + q - 2) < 1e-12
        assert abs(step(r, p) - q) < 1e-9 and abs(step(r, q) - p) < 1e-9
        d = q - 1
        assert abs(multiplier(r, [p, q]) - ((1 - r) ** 2 - r * r * d * d)) < 1e-9
        assert close(attractor(r), [p, q], tol=1e-7)
    assert close(two_cycle(2.3), [0.407845, 1.592155])
    assert abs(multiplier(2.3, two_cycle(2.3)) + 0.164925) < 1e-6
    r_c = two_cycle_limit()
    assert abs(r_c - 2.526468) < 1e-6
    p, q = two_cycle(r_c)
    assert abs((q - 1) ** 2 - ((r_c - 1) ** 2 + 1) / r_c ** 2) < 1e-9


def test_four_cycle_chaos_and_lyapunov():
    assert close(attractor(2.6), [0.181222, 0.390846, 1.523166, 1.904765])
    assert attractor(3.0) is None
    assert abs(lyapunov(1.5) - math.log(0.5)) < 1e-9
    assert lyapunov(3.0) > 0.3
    assert lyapunov(2.6) < 0


def test_boom_and_bust_at_r_three():
    peak = math.exp(2) / 3
    assert abs(peak - 2.463019) < 1e-6
    assert abs(step(3.0, peak) - 0.030572) < 1e-6
    xs = orbit(3.0, 0.3, 20000)[1000:]
    assert max(xs) <= peak + 1e-12 and min(xs) >= step(3.0, peak) - 1e-12


def test_fit_recovers_parameters():
    rng = random.Random(63)
    a, b = math.exp(1.2), 0.004
    stock = [rng.uniform(10, 800) for _ in range(400)]
    recruits = [a * s * math.exp(-b * s) * math.exp(rng.gauss(0, 0.2)) for s in stock]
    a_hat, b_hat = fit_stock_recruitment(stock, recruits)
    assert abs(math.log(a_hat) - 1.2) < 0.06 and abs(b_hat - b) < 0.0002
    exact = fit_stock_recruitment([1, 2, 3], [a * s * math.exp(-b * s) for s in (1, 2, 3)])
    assert abs(exact[0] - a) < 1e-9 and abs(exact[1] - b) < 1e-12
