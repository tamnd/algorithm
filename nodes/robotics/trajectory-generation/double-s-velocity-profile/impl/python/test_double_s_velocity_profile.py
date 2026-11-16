# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-s-velocity-profile/. The authors are listed in prov/07FRKR.jsonl.
"""Tests: closed form times, exact end state, limits on a grid, and the peak velocity by bisection."""

import random
from fractions import Fraction as F

from double_s_velocity_profile import double_s, jerk_segments, peak_velocity_distance, sample


def end_state(D, V, A, J):
    Tj, Ta, Tv, vp, T = double_s(D, V, A, J)
    seg = jerk_segments(Tj, Ta, Tv, J)
    return sample(seg, T), seg, (Tj, Ta, Tv, vp, T)


def test_long_move_exact():
    # D = 1 m, V = 1 m/s, A = 2 m/s^2, J = 8 m/s^3: every phase is present.
    (s, v, a, _), _, (Tj, Ta, Tv, vp, T) = end_state(F(1), F(1), F(2), F(8))
    assert (Tj, Ta, Tv, vp, T) == (F(1, 4), F(3, 4), F(1, 4), 1, F(7, 4))
    assert (s, v, a) == (1, 0, 0)
    assert T == F(1) / 1 + F(1) / 2 + F(2) / 8  # D/V + V/A + A/J


def test_feedrate_example():
    # 100 mm at 50 mm/s, 500 mm/s^2 and 10000 mm/s^3 takes 2.15 s.
    T = double_s(F(100), F(50), F(500), F(10000))[4]
    assert T == F(215, 100)


def test_branches():
    # No cruise, A reached: D = 0.3 > 2 A^3 / J^2 = 0.25.
    Tj, Ta, Tv, vp, T = double_s(0.3, 1.0, 2.0, 8.0)
    assert Tv == 0 and abs(Tj - 0.25) < 1e-12 and vp < 1.0
    # No cruise, A not reached: D = 0.2 < 0.25.
    Tj, Ta, Tv, vp, T = double_s(0.2, 1.0, 2.0, 8.0)
    assert Tv == 0 and abs(Ta - 2 * Tj) < 1e-12 and 8.0 * Tj < 2.0
    assert abs(vp - 0.08 ** (1 / 3)) < 1e-12
    # V reached but not A: V J < A^2.
    Tj, Ta, Tv, vp, T = double_s(1.0, 0.25, 2.0, 8.0)
    assert vp == 0.25 and abs(Tj - (0.25 / 8) ** 0.5) < 1e-12 and Tv > 0


def test_peak_velocity_by_bisection():
    rng = random.Random(21)
    for _ in range(300):
        D, V, A, J = rng.uniform(0.01, 2), rng.uniform(0.1, 2), rng.uniform(0.1, 4), rng.uniform(0.5, 50)
        Tj, Ta, Tv, vp, T = double_s(D, V, A, J)
        if Tv > 0:
            assert vp == V and abs(peak_velocity_distance(V, A, J) + V * Tv - D) < 1e-9
            continue
        lo, hi = 0.0, V
        for _ in range(200):
            mid = (lo + hi) / 2
            if peak_velocity_distance(mid, A, J) < D:
                lo = mid
            else:
                hi = mid
        assert abs(vp - lo) < 1e-9


def test_limits_and_end_state():
    rng = random.Random(22)
    for _ in range(150):
        D, V, A, J = rng.uniform(0.01, 2), rng.uniform(0.1, 2), rng.uniform(0.1, 4), rng.uniform(0.5, 50)
        (s, v, a, _), seg, (Tj, Ta, Tv, vp, T) = end_state(D, V, A, J)
        assert abs(s - D) < 1e-9 and abs(v) < 1e-9 and abs(a) < 1e-9
        assert min(d for d, _ in seg) >= -1e-12
        prev = 0.0
        for k in range(301):
            s, v, a, j = sample(seg, T * k / 300)
            assert -1e-9 <= v <= V + 1e-9 and abs(a) <= A + 1e-9 and abs(j) <= J
            assert s >= prev - 1e-12
            prev = s


def test_compared_with_trapezoid():
    # The jerk bound never makes the move faster. When V and A are both
    # reached, it costs exactly A / J; it costs nothing in the limit J -> infinity.
    rng = random.Random(23)
    for _ in range(200):
        D, V, A, J = rng.uniform(0.01, 2), rng.uniform(0.1, 2), rng.uniform(0.1, 4), rng.uniform(0.5, 50)
        Tj, Ta, Tv, vp, T = double_s(D, V, A, J)
        T_trap = D / V + V / A if D * A >= V * V else 2 * (D / A) ** 0.5
        assert T >= T_trap - 1e-12
        if Tv > 0 and V * J >= A * A:
            assert abs(T - (T_trap + A / J)) < 1e-12
    T = double_s(1.0, 1.0, 2.0, 1e9)[4]
    assert abs(T - 1.5) < 1e-6


def test_bad_input():
    try:
        double_s(1, 1, 0, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("A = 0 must fail")
