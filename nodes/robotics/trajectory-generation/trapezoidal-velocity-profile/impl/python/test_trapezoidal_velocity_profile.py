# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapezoidal-velocity-profile/. The authors are listed in prov/E287FS.jsonl.
"""Tests: check values, end conditions, limits on a grid, and minimum time by the envelope bound."""

import random
from fractions import Fraction as F

from trapezoidal_velocity_profile import move, trapezoid, trapezoid_fixed_time, trapezoid_sample


def envelope_distance(T, V, A, steps=4000):
    """Largest distance any rest-to-rest motion can cover in time T.

    Every admissible velocity satisfies v(t) <= min(A t, V, A (T - t)), so
    the integral of this envelope bounds the distance. Midpoint rule on a
    piecewise linear function with at most three kinks: error below
    A T^2 / steps^2.
    """
    h = T / steps
    return sum(min(A * (k + 0.5) * h, V, A * (T - (k + 0.5) * h)) for k in range(steps)) * h


def test_check_value_exact():
    Ta, vp, T = trapezoid(F(1), F(1), F(2))
    assert (Ta, vp, T) == (F(1, 2), 1, F(3, 2))
    assert trapezoid_sample(F(1), Ta, vp, T, T) == (1, 0, 0)
    assert trapezoid_sample(F(1), Ta, vp, T, Ta)[0] == F(1, 4)
    assert trapezoid_sample(F(1), Ta, vp, T, T - Ta)[0] == F(3, 4)


def test_triangle_case():
    Ta, vp, T = trapezoid(0.18, 1.0, 2.0)
    assert abs(Ta - 0.3) < 1e-12 and abs(vp - 0.6) < 1e-12 and abs(T - 0.6) < 1e-12
    # The boundary case D = V^2 / A is a triangle that just reaches V.
    Ta, vp, T = trapezoid(F(1, 2), F(1), F(2))
    assert (Ta, vp, T) == (F(1, 2), 1, 1)


def test_limits_and_ends_on_grid():
    rng = random.Random(5)
    for _ in range(200):
        D, V, A = rng.uniform(0.01, 3), rng.uniform(0.1, 2), rng.uniform(0.1, 5)
        Ta, vp, T = trapezoid(D, V, A)
        assert vp <= V + 1e-12
        prev = 0.0
        for k in range(201):
            s, ds, dds = trapezoid_sample(D, Ta, vp, T, T * k / 200)
            assert -1e-12 <= ds <= V + 1e-12 and abs(dds) <= A + 1e-12
            assert s >= prev - 1e-12
            prev = s
        s, ds, _ = trapezoid_sample(D, Ta, vp, T, T)
        assert abs(s - D) < 1e-12 and ds == 0
        # Position is continuous at the two switch times.
        for ts in (Ta, T - Ta):
            lo = trapezoid_sample(D, Ta, vp, T, ts - 1e-9)[0]
            hi = trapezoid_sample(D, Ta, vp, T, ts + 1e-9)[0]
            assert abs(lo - hi) < 1e-8


def test_minimum_time():
    rng = random.Random(6)
    for _ in range(40):
        D, V, A = rng.uniform(0.05, 3), rng.uniform(0.2, 2), rng.uniform(0.2, 5)
        T = trapezoid(D, V, A)[2]
        # The profile reaches the envelope bound at T ...
        assert abs(envelope_distance(T, V, A) - D) < 1e-5 * max(1.0, D)
        # ... and a profile 0.1 % faster would have to beat the bound.
        assert envelope_distance(0.999 * T, V, A) < D


def test_fixed_time_synchronization():
    # Axis 1 is the slowest; axis 2 is stretched to end at the same time.
    T1 = trapezoid(1.0, 1.0, 2.0)[2]
    Ta2 = trapezoid_fixed_time(0.4, 2.0, T1)
    vp2 = 2.0 * Ta2
    s, ds, _ = trapezoid_sample(0.4, Ta2, vp2, T1, T1)
    assert abs(s - 0.4) < 1e-12 and ds == 0
    assert abs(trapezoid_sample(0.4, Ta2, vp2, T1, T1 / 2)[0] - 0.2) < 1e-12
    try:
        trapezoid_fixed_time(1.0, 2.0, 1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("T below 2 sqrt(D / A) must fail")


def test_signed_move():
    f, T = move(2.0, 1.0, 1.0, 2.0)
    assert abs(T - 1.5) < 1e-12
    q, dq, _ = f(T)
    assert abs(q - 1.0) < 1e-12 and dq == 0
    assert f(0.25)[1] < 0
    g, T0 = move(1.0, 1.0, 1.0, 2.0)
    assert T0 == 0.0 and g(0.0)[0] == 1.0
