# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-back-projection/. The authors are listed in prov/4TK0K9.jsonl.

import math
import random

from universal_back_projection import (back_projection_term, ball_data, ball_initial_pressure, ball_pressure,
                                       ball_pressure_dt, gauss_legendre, sample, solid_angle_element,
                                       sphere_detectors, universal_back_projection,
                                       universal_back_projection_exact_b)

R, C, S = 10.0, 1.54, 0.8  # mm, mm/us, mm
CENTRE = (2.0, -1.0, 1.5)
POINTS = [CENTRE, (2.5, -1.0, 1.5), (3.0, 0.0, 1.0), (0.0, 0.0, 0.0)]


def _b_exact(centre):
    def b(r0, t):
        return 2.0 * ball_pressure(r0, t, centre, S, C) - 2.0 * t * ball_pressure_dt(r0, t, centre, S, C)
    return b


def test_gauss_legendre_integrates_polynomials_exactly() -> None:
    n = 7
    xs, ws = gauss_legendre(n)
    for deg in range(2 * n):
        want = 0.0 if deg % 2 else 2.0 / (deg + 1)
        assert abs(sum(w * x ** deg for x, w in zip(xs, ws)) - want) < 1e-13


def test_solid_angles_of_the_sphere() -> None:
    dets = sphere_detectors(R, 20, 40)
    inside = sum(solid_angle_element((0.0, 0.0, 0.0), d)[0] for d in dets)
    assert abs(inside - 4.0 * math.pi) < 1e-12
    off = sum(solid_angle_element((3.0, -2.0, 4.0), d)[0] for d in dets)
    assert abs(off - 4.0 * math.pi) < 1e-3
    outside = sum(solid_angle_element((14.0, 0.0, 0.0), d)[0] for d in dets)
    assert abs(outside) < 1e-3


def test_the_forward_model_starts_at_rest_from_the_initial_pressure() -> None:
    x = (4.0, 1.0, -2.0)
    for y in ((2.3, -0.8, 1.1), (2.9, -1.4, 2.0), (5.0, 5.0, 5.0)):
        assert abs(ball_pressure(y, 0.0, CENTRE, S, C) - ball_initial_pressure(y, CENTRE, S)) < 1e-14
        assert abs(ball_pressure_dt(y, 0.0, CENTRE, S, C)) < 1e-14
    # The wave equation p_tt = c^2 (p_xx + p_yy + p_zz) by finite differences.
    t, h = 1.7, 1e-3
    p = lambda y, s: ball_pressure(y, s, CENTRE, S, C)
    ptt = (p(x, t + h) - 2 * p(x, t) + p(x, t - h)) / h ** 2
    lap = 0.0
    for i in range(3):
        e = [0.0, 0.0, 0.0]
        e[i] = h
        xp = tuple(x[j] + e[j] for j in range(3))
        xm = tuple(x[j] - e[j] for j in range(3))
        lap += (p(xp, t) - 2 * p(x, t) + p(xm, t)) / h ** 2
    assert abs(ptt - C * C * lap) < 1e-4 * max(1.0, abs(ptt))
    # The time derivative agrees with a difference quotient.
    d = (p(x, t + h) - p(x, t - h)) / (2 * h)
    assert abs(d - ball_pressure_dt(x, t, CENTRE, S, C)) < 1e-6


def test_exact_data_on_a_sphere_give_the_initial_pressure() -> None:
    dets = sphere_detectors(R, 20, 40)
    out = universal_back_projection_exact_b(_b_exact(CENTRE), dets, C, POINTS)
    for value, r in zip(out, POINTS):
        assert abs(value - ball_initial_pressure(r, CENTRE, S)) < 1e-9


def test_centred_ball_hand_example() -> None:
    # At t = R / c the detector sees p = 0 and dp/dt = -c / (2R), so b = 1.
    z = (0.0, 0.0, 0.0)
    t = R / C
    assert abs(ball_pressure((R, 0.0, 0.0), t, z, S, C)) < 1e-100
    assert abs(ball_pressure_dt((R, 0.0, 0.0), t, z, S, C) + C / (2 * R)) < 1e-15
    dets = sphere_detectors(R, 6, 12)
    assert abs(universal_back_projection_exact_b(_b_exact(z), dets, C, [z])[0] - 1.0) < 1e-12


def test_both_terms_of_b_are_needed() -> None:
    dets = sphere_detectors(R, 20, 40)
    r = POINTS[1]
    far = universal_back_projection_exact_b(lambda r0, t: -2.0 * t * ball_pressure_dt(r0, t, CENTRE, S, C), dets, C, [r])[0]
    assert abs(far - ball_initial_pressure(r, CENTRE, S)) > 3e-3


def test_back_projection_term_of_a_linear_signal() -> None:
    dt = 0.05
    p = [0.7 + 0.3 * k * dt for k in range(20)]
    b = back_projection_term(p, dt)
    for value in b:
        assert abs(value - 1.4) < 1e-12


def test_sample_interpolates_linearly_and_is_zero_outside() -> None:
    b = [0.0, 1.0, 4.0, 9.0]
    assert abs(sample(b, 0.5, 0.75) - 2.5) < 1e-15
    assert sample(b, 0.5, -0.1) == 0.0
    assert sample(b, 0.5, 2.0) == 0.0


def test_the_back_projection_is_linear_in_the_data() -> None:
    rng = random.Random(4401)
    dets = sphere_detectors(R, 4, 8)
    nt, dt = 40, 0.4
    d1 = [[rng.gauss(0, 1) for _ in range(nt)] for _ in dets]
    d2 = [[rng.gauss(0, 1) for _ in range(nt)] for _ in dets]
    mix = [[2.0 * a - 3.0 * b for a, b in zip(r1, r2)] for r1, r2 in zip(d1, d2)]
    pts = [(1.0, 2.0, -1.0), (0.0, -3.0, 0.5)]
    u1 = universal_back_projection(d1, dets, dt, C, pts, 4 * math.pi)
    u2 = universal_back_projection(d2, dets, dt, C, pts, 4 * math.pi)
    um = universal_back_projection(mix, dets, dt, C, pts, 4 * math.pi)
    for a, b, m in zip(u1, u2, um):
        assert abs(m - (2.0 * a - 3.0 * b)) < 1e-10


def test_sampled_data_converge_with_the_square_of_the_time_step() -> None:
    dets = sphere_detectors(R, 20, 40)
    pts = POINTS[:2]
    errors = []
    for dt in (0.04, 0.02):
        nt = int(2 * R / C / dt) + 3
        data = ball_data(dets, CENTRE, S, C, dt, nt)
        out = universal_back_projection(data, dets, dt, C, pts)
        errors.append(max(abs(v - ball_initial_pressure(r, CENTRE, S)) for v, r in zip(out, pts)))
    assert errors[1] < 2e-3
    assert 3.0 < errors[0] / errors[1] < 5.0


def test_half_the_sphere_is_not_enough() -> None:
    dets = [d for d in sphere_detectors(R, 20, 40) if d[0][2] > 0.0]
    out = universal_back_projection_exact_b(_b_exact(CENTRE), dets, C, POINTS[:3])
    assert abs(out[0] - 0.5771) < 1e-3
    errs = [abs(v - ball_initial_pressure(r, CENTRE, S)) for v, r in zip(out, POINTS)]
    assert max(errs) > 0.4
