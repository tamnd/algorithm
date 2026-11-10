# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-gradient-descent/. The authors are listed in prov/X8NYQC.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from online_gradient_descent import (
    absolute_losses,
    best_fixed_absolute,
    best_fixed_squared,
    online_gradient_descent,
    project,
    sqrt_step,
    squared_losses,
    strongly_convex_step,
)


def oracle_points(zs, lo, hi, step, x1, grad):
    """A direct loop for x_{t+1} = clip(x_t - eta_t g_t)."""
    xs = [x1]
    for t, z in enumerate(zs, start=1):
        y = xs[-1] - step(t) * grad(xs[-1], z)
        xs.append(min(hi, max(lo, y)))
    return xs[:-1]


def sign_grad(x, z):
    return 1 if x > z else (-1 if x < z else 0)


def grid_min(f, lo, hi, k=40):
    return min(f(lo + (hi - lo) * F(i, k)) for i in range(k + 1))


def test_worked_example():
    zs = [F(2), F(-1), F(2), F(2)]
    xs, total, grads = online_gradient_descent(squared_losses(zs), 4, F(0), F(1), strongly_convex_step(2), F(1, 2))
    assert xs == [F(1, 2), F(1), F(0), F(2, 3)]
    assert total == F(433, 36)
    assert best_fixed_squared(zs, F(0), F(1)) == 7
    assert grads == [F(-3), F(4), F(-4), F(-8, 3)]
    bound = sum(g * g / (4 * t) for t, g in enumerate(grads, start=1))
    assert bound == F(217, 36)
    assert total - 7 == F(181, 36) <= bound


def test_absolute_losses_exact_against_oracle_and_bound():
    rng = random.Random(2003)
    for _ in range(600):
        lo = F(rng.randrange(-3, 2))
        hi = lo + rng.randrange(1, 4)
        d = hi - lo
        t_max = rng.randrange(1, 40)
        zs = [F(rng.randrange(-8, 9), 2) for _ in range(t_max)]
        # a rational, nonincreasing step close to D / (G sqrt t), with G = 1
        step = lambda t, d=d: d / math.isqrt(4 * t)
        xs, total, grads = online_gradient_descent(absolute_losses(zs), t_max, lo, hi, step)
        assert xs == oracle_points(zs, lo, hi, step, (lo + hi) / 2, sign_grad)
        assert all(lo <= x <= hi for x in xs)
        assert total == sum(abs(x - z) for x, z in zip(xs, zs))
        best = best_fixed_absolute(zs, lo, hi)
        assert best <= grid_min(lambda x: sum(abs(x - z) for z in zs), lo, hi)
        regret = total - best
        bound = d * d / (2 * step(t_max)) + sum(step(t) * g * g / 2 for t, g in enumerate(grads, start=1))
        assert regret <= bound


def test_absolute_losses_tuned_step():
    rng = random.Random(7)
    for _ in range(600):
        t_max = rng.randrange(1, 80)
        zs = [rng.randrange(0, 101) / 100 for _ in range(t_max)]
        xs, total, _ = online_gradient_descent(absolute_losses(zs), t_max, 0.0, 1.0, sqrt_step(1.0, 1.0))
        regret = total - best_fixed_absolute(zs, 0.0, 1.0)
        assert regret <= 1.5 * math.sqrt(t_max) - 0.5 + 1e-9


def test_strongly_convex_squared_losses_exact():
    rng = random.Random(2007)
    lo, hi = F(0), F(1)
    for _ in range(600):
        t_max = rng.randrange(1, 40)
        zs = [F(rng.randrange(-10, 21), 10) for _ in range(t_max)]
        step = strongly_convex_step(2)
        xs, total, grads = online_gradient_descent(squared_losses(zs), t_max, lo, hi, step)
        assert xs == oracle_points(zs, lo, hi, step, F(1, 2), lambda x, z: 2 * (x - z))
        best = best_fixed_squared(zs, lo, hi)
        assert best <= grid_min(lambda x: sum((x - z) ** 2 for z in zs), lo, hi)
        regret = total - best
        assert regret <= sum(g * g / (4 * t) for t, g in enumerate(grads, start=1))
        big_g = max(abs(g) for g in grads)
        harmonic = sum(F(1, t) for t in range(1, t_max + 1))
        assert regret <= big_g**2 / 4 * harmonic
        assert regret <= big_g**2 / 4 * (1 + math.log(t_max)) + 1e-12


def test_squared_losses_inside_interval_give_the_running_mean():
    rng = random.Random(11)
    for _ in range(200):
        t_max = rng.randrange(2, 30)
        zs = [F(rng.randrange(0, 11), 10) for _ in range(t_max)]
        xs, _, _ = online_gradient_descent(squared_losses(zs), t_max, F(0), F(1), strongly_convex_step(2))
        for t in range(1, t_max):
            assert xs[t] == sum(zs[:t]) / t


def test_adaptive_adversary():
    for t_max in (1, 2, 10, 100, 1000):
        adversary_z = []

        def adversary(t, x):
            z = 0.0 if x >= 0.5 else 1.0
            adversary_z.append(z)
            return abs(x - z), (1 if x > z else -1)

        _, total, _ = online_gradient_descent(adversary, t_max, 0.0, 1.0, sqrt_step(1.0, 1.0))
        regret = total - best_fixed_absolute(adversary_z, 0.0, 1.0)
        assert regret <= 1.5 * math.sqrt(t_max) - 0.5 + 1e-9


def test_fixed_step_with_known_horizon():
    rng = random.Random(5)
    for _ in range(100):
        t_max = rng.randrange(1, 100)
        zs = [rng.random() * 2 - 0.5 for _ in range(t_max)]
        eta = 1.0 / math.sqrt(t_max)
        _, total, _ = online_gradient_descent(absolute_losses(zs), t_max, 0.0, 1.0, lambda t: eta)
        assert total - best_fixed_absolute(zs, 0.0, 1.0) <= math.sqrt(t_max) + 1e-9


def test_random_signs_force_sqrt_regret():
    rng = random.Random(42)
    t_max, runs = 100, 300
    avg = 0.0
    for _ in range(runs):
        eps = [rng.choice((-1, 1)) for _ in range(t_max)]
        adversary = lambda t, x: (eps[t - 1] * x, eps[t - 1])
        _, total, _ = online_gradient_descent(adversary, t_max, -1.0, 1.0, sqrt_step(2.0, 1.0))
        avg += total + abs(sum(eps))
    avg /= runs
    assert avg >= math.sqrt(t_max / 3) - 1.0
    assert avg <= 1.5 * 2 * math.sqrt(t_max)


def test_bad_input():
    with pytest.raises(ValueError):
        online_gradient_descent(absolute_losses([F(0)]), 1, F(1), F(0), strongly_convex_step(1))
    with pytest.raises(ValueError):
        online_gradient_descent(absolute_losses([F(0)]), 1, F(0), F(1), strongly_convex_step(1), F(2))
    assert project(F(5), F(0), F(1)) == 1
    assert project(F(-5), F(0), F(1)) == 0
