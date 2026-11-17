# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-map/. The authors are listed in prov/DM7V7K.jsonl.
"""Tests of the logistic map against the page values and the closed forms."""

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction

import pytest

from logistic_map import attractor, fixed_points, lyapunov, multiplier, orbit, two_cycle


def close(xs, ys, tol=1e-6):
    return len(xs) == len(ys) and all(abs(a - b) < tol for a, b in zip(xs, ys))


def test_page_traces():
    assert close(orbit(2.8, 0.2, 6), [0.448, 0.692429, 0.596319, 0.674023, 0.615205, 0.662838])
    assert close(orbit(3.2, 0.2, 6), [0.512, 0.799539, 0.512884, 0.799469, 0.513019, 0.799458])
    assert orbit(3.0, 0.5, 0) == []
    with pytest.raises(ValueError):
        orbit(3.0, 0.5, -1)


def test_exact_step_with_fractions():
    x = orbit(Fraction(14, 5), Fraction(1, 5), 2)
    assert x == [Fraction(56, 125), Fraction(14, 5) * Fraction(56, 125) * Fraction(69, 125)]


def test_fixed_points_and_stability():
    for r in (1.5, 2.0, 2.8):
        _, xs = fixed_points(r)
        assert abs(multiplier(r, [xs]) - (2 - r)) < 1e-12
        assert close(attractor(r), [xs], tol=1e-8)
    assert abs(fixed_points(2.8)[1] - 0.642857) < 1e-6
    assert attractor(0.8) is not None and abs(attractor(0.8)[0]) < 1e-9
    assert multiplier(2.5, [0.0]) == 2.5


def test_two_cycle():
    assert two_cycle(3.0) is None
    for r in (3.1, 3.2, 3.3, 3.4):
        p, q = two_cycle(r)
        assert abs(r * p * (1 - p) - q) < 1e-12 and abs(r * q * (1 - q) - p) < 1e-12
        assert abs(multiplier(r, [p, q]) - (-r * r + 2 * r + 4)) < 1e-12
        assert close(attractor(r), [p, q], tol=1e-7)
    assert close(two_cycle(3.2), [0.513045, 0.799455])
    assert abs(multiplier(3.2, two_cycle(3.2)) - 0.16) < 1e-12
    assert abs(multiplier(1 + math.sqrt(6), two_cycle(1 + math.sqrt(6))) + 1) < 1e-9
    assert abs(multiplier(1 + math.sqrt(5), two_cycle(1 + math.sqrt(5)))) < 1e-9


def test_period_four_and_three():
    assert close(attractor(3.5), sorted([0.826941, 0.500884, 0.874997, 0.382820]))
    assert close(attractor(3.83), [0.156149, 0.504666, 0.957417])
    assert attractor(3.7) is None


def test_r_four_closed_form_and_lyapunov():
    rng = random.Random(7)
    for _ in range(20):
        theta = rng.uniform(0, math.pi)
        xs = orbit(4.0, math.sin(theta) ** 2, 10)
        exact = [math.sin(2 ** t * theta) ** 2 for t in range(1, 11)]
        assert close(xs, exact, tol=1e-6)
    assert abs(lyapunov(4.0) - math.log(2)) < 0.01
    assert lyapunov(3.7) > 0.3
    assert abs(lyapunov(3.2) - math.log(0.16) / 2) < 1e-3


def test_float_orbit_loses_all_digits_by_step_52():
    getcontext().prec = 300
    x, ref = 0.2, Decimal(1) / Decimal(5)
    first = None
    for t in range(1, 100):
        x = 4 * x * (1 - x)
        ref = 4 * ref * (1 - ref)
        if abs(Decimal(x) - ref) > Decimal("0.1"):
            first = t
            break
    assert first == 52


def test_interval_is_invariant():
    rng = random.Random(8)
    for _ in range(2000):
        r = rng.uniform(0, 4)
        x = rng.random()
        assert 0 <= orbit(r, x, 1)[0] <= 1
    assert orbit(4.2, 0.5, 1)[0] > 1
