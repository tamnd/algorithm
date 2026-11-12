# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-rate-schedule/. The authors are listed in prov/2F4BBA.jsonl.

import math
from fractions import Fraction as F

import pytest

from learning_rate_schedule import (
    cosine_annealing,
    exponential_decay,
    inverse_sqrt,
    linear_scaling,
    linear_warmup,
    multi_step_decay,
    one_cycle,
    one_cycle_momentum,
    polynomial_decay,
    sgd_with_schedule,
    sgdr,
    sgdr_position,
    step_decay,
)


def test_step_decay_boundaries_exact() -> None:
    eta0, gamma = F(1, 10), F(1, 10)
    assert step_decay(0, eta0, gamma, 30) == F(1, 10)
    assert step_decay(29, eta0, gamma, 30) == F(1, 10)
    assert step_decay(30, eta0, gamma, 30) == F(1, 100)
    assert step_decay(60, eta0, gamma, 30) == F(1, 1000)
    assert multi_step_decay(49, eta0, gamma, [50, 75]) == F(1, 10)
    assert multi_step_decay(50, eta0, gamma, [50, 75]) == F(1, 100)
    assert multi_step_decay(75, eta0, gamma, [50, 75]) == F(1, 1000)


def test_exponential_and_polynomial_exact() -> None:
    assert exponential_decay(0, F(1, 10), F(1, 2)) == F(1, 10)
    assert exponential_decay(3, F(1, 10), F(1, 2)) == F(1, 80)
    assert polynomial_decay(0, F(1, 10), 100, 2) == F(1, 10)
    assert polynomial_decay(50, F(1, 10), 100, 2) == F(1, 40)
    assert polynomial_decay(100, F(1, 10), 100, 2) == 0
    assert polynomial_decay(150, F(1, 10), 100, 2, F(1, 1000)) == F(1, 1000)


def test_cosine_boundaries() -> None:
    assert cosine_annealing(0, 0.1, 0.001, 100) == 0.1
    assert cosine_annealing(100, 0.1, 0.001, 100) == 0.001
    # The midpoint is the mean of the two ends.
    assert math.isclose(cosine_annealing(50, 0.1, 0.001, 100), 0.0505, rel_tol=1e-12)
    # The curve is symmetric about the midpoint: eta(t) + eta(T - t) = eta_max + eta_min.
    for t in range(101):
        s = cosine_annealing(t, 0.1, 0.001, 100) + cosine_annealing(100 - t, 0.1, 0.001, 100)
        assert math.isclose(s, 0.101, rel_tol=1e-12)
    # Nonincreasing.
    vals = [cosine_annealing(t, 0.1, 0.0, 100) for t in range(101)]
    assert all(a >= b for a, b in zip(vals, vals[1:]))


def test_sgdr_restarts() -> None:
    assert [sgdr_position(t, 10, 2) for t in (0, 9, 10, 29, 30, 69, 70)] == [
        (0, 10), (9, 10), (0, 20), (19, 20), (0, 40), (39, 40), (0, 80)]
    for t in (0, 10, 30, 70, 150):
        assert sgdr(t, 0.1, 0.0, 10, 2) == 0.1
    # With t_mult = 1 every cycle has the same length.
    assert sgdr(25, 0.1, 0.0, 10) == sgdr(5, 0.1, 0.0, 10)


def test_linear_warmup_exact() -> None:
    peak = F(1, 10)
    after = lambda s: polynomial_decay(s, peak, 90, 1)
    assert linear_warmup(0, 10, 0, peak, after) == 0
    assert linear_warmup(5, 10, 0, peak, after) == F(1, 20)
    assert linear_warmup(10, 10, 0, peak, after) == peak
    assert linear_warmup(100, 10, 0, peak, after) == 0
    # Goyal et al.: start at the small batch rate and end at k times it.
    assert linear_warmup(0, 5, F(1, 10), F(32, 10), after) == F(1, 10)
    assert linear_scaling(F(1, 10), 8192, 256) == F(16, 5)


def test_inverse_sqrt_peak_and_decay() -> None:
    d, w = 512, 4000
    peak = inverse_sqrt(w, d, w)
    assert math.isclose(peak, (d * w) ** -0.5, rel_tol=1e-12)
    assert math.isclose(inverse_sqrt(1, d, w), d ** -0.5 * w ** -1.5, rel_tol=1e-12)
    # Linear before the peak, 1 / sqrt(step) after it.
    assert math.isclose(inverse_sqrt(1000, d, w), peak / 4, rel_tol=1e-12)
    assert math.isclose(inverse_sqrt(16000, d, w), peak / 2, rel_tol=1e-12)
    assert max(inverse_sqrt(s, d, w) for s in range(1, 20000)) == peak
    with pytest.raises(ValueError):
        inverse_sqrt(0, d, w)


def test_one_cycle_shape_exact() -> None:
    total, top = 100, F(1, 10)
    assert one_cycle(0, total, top) == F(1, 100)
    assert one_cycle(45, total, top) == top
    assert one_cycle(90, total, top) == F(1, 100)
    assert one_cycle(100, total, top) == F(1, 100000)
    vals = [one_cycle(t, total, top) for t in range(total + 1)]
    assert max(vals) == top and vals.index(top) == 45
    assert one_cycle_momentum(0, total) == F(95, 100)
    assert one_cycle_momentum(45, total) == F(85, 100)
    assert one_cycle_momentum(90, total) == F(95, 100)


def test_schedule_drives_gradient_descent() -> None:
    # f(w) = w^2 / 2 has gradient w; with eta_t the iterate is the product of (1 - eta_t).
    sched = lambda t: step_decay(t, F(1, 2), F(1, 2), 2)
    path = sgd_with_schedule(lambda w: w, F(1), sched, 4)
    assert path == [F(1), F(1, 2), F(1, 4), F(3, 16), F(9, 64)]
