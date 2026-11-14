# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixture-sequential-probability-ratio-test/. The authors are listed in prov/7K0XX7.jsonl.
import itertools
import math
import random
from fractions import Fraction

import pytest

from mixture_sequential_probability_ratio_test import (
    always_valid_p_values,
    beta_bernoulli_ratio,
    msprt,
    msprt_ratio,
)

EXAMPLE = [0.8, 1.4, -0.2, 1.1, 0.9, 1.6, 0.3, 1.2]


def mixture_by_quadrature(xs: list[float], theta0: float, sigma: float, tau: float, m: int = 4000) -> float:
    """Integral over theta of prod f_theta(x_i) / f_theta0(x_i) times the N(theta0, tau^2) density."""
    lo, hi = theta0 - 12 * tau, theta0 + 12 * tau
    h = (hi - lo) / m
    acc = 0.0
    for i in range(m + 1):
        t = lo + i * h
        w = 1.0 if i in (0, m) else (4.0 if i % 2 else 2.0)
        log_lr = sum(((x - theta0) ** 2 - (x - t) ** 2) / (2 * sigma * sigma) for x in xs)
        prior = math.exp(-0.5 * ((t - theta0) / tau) ** 2) / (tau * math.sqrt(2 * math.pi))
        acc += w * math.exp(log_lr) * prior
    return acc * h / 3.0


def test_worked_example():
    p = always_valid_p_values(EXAMPLE, 0.0, 1.0, 1.0)
    want = [1.0, 0.7731, 0.7731, 0.7731, 0.6457, 0.2817, 0.2817, 0.1823]
    assert all(abs(a - b) < 1e-4 for a, b in zip(p, want))
    assert msprt(EXAMPLE, 0.0, 1.0, 1.0, 0.05) == (False, 8, p[-1])
    assert abs(msprt_ratio(6, 5.6, 1.0, 1.0) - 3.550) < 1e-3


def test_p_values_never_increase_and_reject_matches():
    rng = random.Random(3)
    xs = [rng.gauss(0.6, 1.0) for _ in range(200)]
    p = always_valid_p_values(xs, 0.0, 1.0, 0.5)
    assert all(a >= b for a, b in zip(p, p[1:]))
    rejected, n, pn = msprt(xs, 0.0, 1.0, 0.5, 0.05)
    first = next(i for i, v in enumerate(p, 1) if v <= 0.05)
    assert rejected and n == first and pn == p[n - 1]


def test_closed_form_matches_quadrature():
    rng = random.Random(8)
    for _ in range(20):
        sigma = rng.uniform(0.5, 2.0)
        tau = rng.uniform(0.2, 2.0)
        theta0 = rng.uniform(-1.0, 1.0)
        xs = [rng.gauss(theta0 + rng.uniform(-1, 1), sigma) for _ in range(rng.randint(1, 12))]
        s = sum(x - theta0 for x in xs)
        want = mixture_by_quadrature(xs, theta0, sigma, tau)
        assert abs(msprt_ratio(len(xs), s, sigma, tau) - want) < 1e-8 * max(1.0, want)


def test_beta_bernoulli_martingale_mean_one_exact():
    for a, b in ((1, 1), (2, 3), (5, 1)):
        for p0 in (Fraction(1, 2), Fraction(1, 3), Fraction(7, 10)):
            for n in range(0, 11):
                mean = sum(p0 ** sum(s) * (1 - p0) ** (n - sum(s)) * beta_bernoulli_ratio(sum(s), n - sum(s), a, b, p0)
                           for s in itertools.product((0, 1), repeat=n))
                assert mean == 1


def test_beta_bernoulli_stopped_mean_at_most_one_exact():
    # Stop when Lambda >= 1/alpha or after 12 flips: E0[Lambda_T] = 1 exactly for a bounded stopping time.
    p0, alpha = Fraction(1, 2), Fraction(1, 10)
    alive = {(0, 0): Fraction(1)}
    stopped = Fraction(0)
    reject = Fraction(0)
    for n in range(1, 13):
        nxt: dict[tuple[int, int], Fraction] = {}
        for (h, t), m in alive.items():
            for h2, t2, q in ((h + 1, t, p0), (h, t + 1, 1 - p0)):
                lam = beta_bernoulli_ratio(h2, t2, 1, 1, p0)
                if lam >= 1 / alpha or n == 12:
                    stopped += m * q * lam
                    reject += m * q * (lam >= 1 / alpha)
                else:
                    nxt[(h2, t2)] = nxt.get((h2, t2), Fraction(0)) + m * q
        alive = nxt
    assert stopped == 1
    assert reject <= alpha


def test_optional_stopping_size_against_naive_z_test():
    rng = random.Random(5)
    reps, horizon, alpha = 2000, 500, 0.05
    msprt_rej = naive_rej = 0
    for _ in range(reps):
        s = 0.0
        hit_m = hit_z = False
        for n in range(1, horizon + 1):
            s += rng.gauss(0.0, 1.0)
            hit_m = hit_m or msprt_ratio(n, s, 1.0, 1.0) >= 1 / alpha
            hit_z = hit_z or abs(s) / math.sqrt(n) >= 1.959964
            if hit_m and hit_z:
                break
        msprt_rej += hit_m
        naive_rej += hit_z
    se = math.sqrt(alpha * (1 - alpha) / reps)
    assert msprt_rej / reps < alpha
    assert naive_rej / reps > alpha + 10 * se


def test_power_one():
    rng = random.Random(12)
    for _ in range(50):
        xs = (rng.gauss(0.3, 1.0) for _ in range(5000))
        assert msprt(xs, 0.0, 1.0, 1.0, 0.05)[0]


def test_random_streams_against_direct_formula():
    rng = random.Random(77)
    for _ in range(500):
        sigma, tau = rng.uniform(0.3, 3), rng.uniform(0.1, 3)
        theta0 = rng.uniform(-2, 2)
        xs = [rng.gauss(theta0 + rng.uniform(-1, 1), sigma) for _ in range(rng.randint(1, 15))]
        p = 1.0
        for n in range(1, len(xs) + 1):
            mean = sum(xs[:n]) / n
            v = sigma ** 2 + n * tau ** 2
            lam = math.sqrt(sigma ** 2 / v) * math.exp(n * n * tau ** 2 * (mean - theta0) ** 2 / (2 * sigma ** 2 * v))
            p = min(p, 1 / lam)
        assert abs(always_valid_p_values(xs, theta0, sigma, tau)[-1] - p) < 1e-9 * max(1.0, p)


def test_bad_input():
    with pytest.raises(ValueError):
        msprt([1.0], 0.0, 0.0, 1.0, 0.05)
    with pytest.raises(ValueError):
        msprt([1.0], 0.0, 1.0, 1.0, 1.5)
