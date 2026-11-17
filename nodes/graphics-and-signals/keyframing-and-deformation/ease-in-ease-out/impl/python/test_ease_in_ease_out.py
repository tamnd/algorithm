# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ease-in-ease-out/. The authors are listed in prov/M1V8Y9.jsonl.
import math
import random

import pytest

from ease_in_ease_out import (
    const_accel,
    const_accel_speed,
    ease_between,
    sine_ease,
    sine_speed,
    smoothstep,
    smoothstep_speed,
)


def curves(rng):
    out = [(sine_ease, sine_speed), (smoothstep, smoothstep_speed)]
    out.append((lambda t: const_accel(t, 0.2, 0.8), lambda t: const_accel_speed(t, 0.2, 0.8)))
    for _ in range(5):
        t1 = rng.uniform(0.01, 0.5)
        t2 = rng.uniform(t1, 0.99)
        out.append((lambda t, a=t1, b=t2: const_accel(t, a, b), lambda t, a=t1, b=t2: const_accel_speed(t, a, b)))
    return out


def test_end_values_and_monotone(rng=random.Random(1)):
    for f, _ in curves(rng):
        assert abs(f(0.0)) < 1e-15 and abs(f(1.0) - 1.0) < 1e-12
        prev = -1.0
        for k in range(2001):
            s = f(k / 2000.0)
            assert s >= prev - 1e-15 and -1e-15 <= s <= 1.0 + 1e-12
            prev = s


def test_zero_slope_at_both_ends(rng=random.Random(2)):
    h = 1e-6
    for f, v in curves(rng):
        assert f(h) / h < 1e-4
        assert (1.0 - f(1.0 - h)) / h < 1e-4
        assert abs(v(0.0)) < 1e-12 and abs(v(1.0)) < 1e-12


def test_speed_is_the_derivative(rng=random.Random(3)):
    h = 1e-6
    for f, v in curves(rng):
        for _ in range(50):
            t = rng.uniform(0.01, 0.99)
            num = (f(t + h) - f(t - h)) / (2 * h)
            # Near a kink of the speed at t1 or t2, the centered difference errs
            # by at most h / 4 times the acceleration, which is below 1e-4 here.
            assert abs(num - v(t)) < 1e-4


def test_const_accel_against_integrated_speed(rng=random.Random(4)):
    # Reference: integrate the trapezoid speed profile with a fine midpoint rule.
    for _ in range(5):
        t1 = rng.uniform(0.05, 0.5)
        t2 = rng.uniform(t1, 0.95)
        m = 4000
        acc = 0.0
        for k in range(m):
            acc += const_accel_speed((k + 0.5) / m, t1, t2) / m
            if (k + 1) % 400 == 0:
                assert abs(acc - const_accel((k + 1) / m, t1, t2)) < 1e-5


def test_check_values():
    assert abs(sine_ease(0.5) - 0.5) < 1e-15 and abs(smoothstep(0.5) - 0.5) < 1e-15
    assert abs(sine_ease(0.25) - (1 - math.sqrt(0.5)) / 2) < 1e-15
    assert abs(smoothstep(0.25) - 0.15625) < 1e-15
    assert abs(sine_speed(0.5) - math.pi / 2) < 1e-15 and abs(smoothstep_speed(0.5) - 1.5) < 1e-15
    assert abs(const_accel_speed(0.5, 0.2, 0.8) - 1.25) < 1e-15
    assert abs(const_accel(0.2, 0.2, 0.8) - 0.125) < 1e-15
    assert abs(const_accel(0.5, 0.2, 0.8) - 0.5) < 1e-15
    with pytest.raises(ValueError):
        const_accel(0.5, 0.6, 0.4)


def test_symmetry(rng=random.Random(5)):
    for _ in range(100):
        t = rng.random()
        assert abs(sine_ease(t) + sine_ease(1 - t) - 1) < 1e-14
        assert abs(smoothstep(t) + smoothstep(1 - t) - 1) < 1e-14
        assert abs(const_accel(t, 0.3, 0.7) + const_accel(1 - t, 0.3, 0.7) - 1) < 1e-12


def test_ease_between():
    p = ease_between((0.0, 2.0), (4.0, 6.0), 0.25)
    assert abs(p[0] - 0.625) < 1e-14 and abs(p[1] - 2.625) < 1e-14
