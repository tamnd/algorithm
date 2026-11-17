# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-reflection-method/. The authors are listed in prov/EA23M6.jsonl.
import math
import random

import pytest

import anim
from double_reflection_method import double_reflection, rotation_minimizing_frames, sample_curve


def helix(a, b):
    w = math.hypot(a, b)

    def c(u):
        return (a * math.cos(u), a * math.sin(u), b * u)

    def dc(u):
        return (-a * math.sin(u), a * math.cos(u), b)

    def exact_r(u, theta0):
        # The rotation minimizing normal: theta(u) = theta0 - (b / w) u from the Frenet normal.
        n = (-math.cos(u), -math.sin(u), 0.0)
        bn = (b * math.sin(u) / w, -b * math.cos(u) / w, a / w)
        th = theta0 - b * u / w
        return anim.add(anim.scale(n, math.cos(th)), anim.scale(bn, math.sin(th)))

    return c, dc, exact_r


def twisted_cubic():
    def c(u):
        return (u, u * u, u**3)

    def dc(u):
        return (1.0, 2 * u, 3 * u * u)

    def ddc(u):
        return (0.0, 2.0, 6 * u)

    return c, dc, ddc


def rk4_rmf(dc, ddc, a, b, steps, r0):
    # Reference: RK4 on the defining equation r' = -(r . t') t, with t' = (x'' - (t . x'') t) / |x'|.
    def f(u, r):
        d1, d2 = dc(u), ddc(u)
        sp = anim.norm(d1)
        t = anim.scale(d1, 1.0 / sp)
        dt = anim.scale(anim.sub(d2, anim.scale(t, anim.dot(t, d2))), 1.0 / sp)
        return anim.scale(t, -anim.dot(r, dt))

    h = (b - a) / steps
    r = r0
    for k in range(steps):
        u = a + k * h
        k1 = f(u, r)
        k2 = f(u + h / 2, anim.add(r, anim.scale(k1, h / 2)))
        k3 = f(u + h / 2, anim.add(r, anim.scale(k2, h / 2)))
        k4 = f(u + h, anim.add(r, anim.scale(k3, h)))
        r = anim.add(r, anim.scale(anim.add(anim.add(k1, k4), anim.scale(anim.add(k2, k3), 2.0)), h / 6))
    return r


def test_frames_are_right_handed_and_orthonormal(rng=random.Random(1)):
    coef = [[rng.uniform(-2, 2) for _ in range(4)] for _ in range(3)]

    def c(u):
        return tuple(sum(row[k] * u**k for k in range(4)) for row in coef)

    def dc(u):
        return tuple(sum(k * row[k] * u ** (k - 1) for k in range(1, 4)) for row in coef)

    frames = rotation_minimizing_frames(c, dc, 0.0, 1.0, 50, (rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
    for r, s, t in frames:
        for x in (r, s, t):
            assert abs(anim.dot(x, x) - 1.0) < 1e-12
        assert abs(anim.dot(r, s)) < 1e-12 and abs(anim.dot(r, t)) < 1e-12 and abs(anim.dot(s, t)) < 1e-12
        assert anim.norm(anim.sub(anim.cross(r, s), t)) < 1e-12


def test_helix_against_the_closed_form():
    c, dc, exact_r = helix(1.0, 0.5)
    t0 = anim.normalize(dc(0.0))
    r0 = exact_r(0.0, 0.3)
    assert abs(anim.dot(r0, t0)) < 1e-15
    errors = []
    for n in (16, 32, 64):
        frames = rotation_minimizing_frames(c, dc, 0.0, 2 * math.pi, n, r0)
        errors.append(max(anim.norm(anim.sub(fr[0], exact_r(2 * math.pi * i / n, 0.3))) for i, fr in enumerate(frames)))
    assert errors[-1] < 1e-5
    # Fourth order: halving the step divides the error by about 16.
    for e1, e2 in zip(errors, errors[1:]):
        assert 13.0 < e1 / e2 < 19.0


def test_twisted_cubic_against_rk4():
    c, dc, ddc = twisted_cubic()
    r0 = (0.0, 0.0, 1.0)
    ref = rk4_rmf(dc, ddc, 0.0, 1.0, 2000, r0)
    errors = []
    for n in (10, 20, 40, 80):
        r_end = rotation_minimizing_frames(c, dc, 0.0, 1.0, n, r0)[-1][0]
        errors.append(anim.norm(anim.sub(r_end, ref)))
    assert errors[-1] < 1e-6
    for e1, e2 in zip(errors[1:], errors[2:]):
        assert 12.0 < e1 / e2 < 20.0


def test_exact_on_a_plane_curve(rng=random.Random(2)):
    q = anim.q_normalize(tuple(rng.gauss(0, 1) for _ in range(4)))
    n_plane = anim.q_rotate(q, (0.0, 0.0, 1.0))

    def c(u):
        return anim.q_rotate(q, (math.cos(u), math.sin(2 * u), 0.0))

    def dc(u):
        return anim.q_rotate(q, (-math.sin(u), 2 * math.cos(2 * u), 0.0))

    alpha = 0.7
    t0 = anim.normalize(dc(0.0))
    r0 = anim.add(anim.scale(n_plane, math.cos(alpha)), anim.scale(anim.cross(n_plane, t0), math.sin(alpha)))
    frames = rotation_minimizing_frames(c, dc, 0.0, 3.0, 7, r0)
    for r, _, t in frames:
        exact = anim.add(anim.scale(n_plane, math.cos(alpha)), anim.scale(anim.cross(n_plane, t), math.sin(alpha)))
        assert anim.norm(anim.sub(r, exact)) < 1e-12


def test_exact_on_a_sphere():
    center, rho = (0.3, -1.0, 2.0), 1.7

    def angles(u):
        return 0.5 * math.sin(2 * u), u + 0.3 * u * u, math.cos(2 * u), 1 + 0.6 * u

    def c(u):
        ph, th, _, _ = angles(u)
        return anim.add(center, anim.scale((math.cos(ph) * math.cos(th), math.cos(ph) * math.sin(th), math.sin(ph)), rho))

    def dc(u):
        ph, th, dph, dth = angles(u)
        return anim.scale(
            (
                -math.sin(ph) * dph * math.cos(th) - math.cos(ph) * math.sin(th) * dth,
                -math.sin(ph) * dph * math.sin(th) + math.cos(ph) * math.cos(th) * dth,
                math.cos(ph) * dph,
            ),
            rho,
        )

    r0 = anim.scale(anim.sub(c(0.0), center), 1.0 / rho)
    frames = rotation_minimizing_frames(c, dc, 0.0, 2.5, 6, r0)
    points, _ = sample_curve(c, dc, 0.0, 2.5, 6)
    for (r, _, _), x in zip(frames, points):
        assert anim.norm(anim.sub(r, anim.scale(anim.sub(x, center), 1.0 / rho))) < 1e-12


def test_reversal_returns_the_first_frame():
    c, dc, _ = twisted_cubic()
    points, tangents = sample_curve(c, dc, 0.0, 1.0, 9)
    forward = double_reflection(points, tangents, (0.0, 0.0, 1.0))
    back = double_reflection(points[::-1], [anim.scale(t, -1.0) for t in tangents[::-1]], forward[-1][0])
    for (r, _, _), (rb, _, _) in zip(forward, back[::-1]):
        assert anim.norm(anim.sub(r, rb)) < 1e-12


def test_straight_line_keeps_the_frame():
    points = [(1.0 + k, 2.0 + 2 * k, -k) for k in range(5)]
    tangents = [(1.0, 2.0, -1.0)] * 5
    frames = double_reflection(points, tangents, (2.0, -1.0, 0.0))
    for r, s, t in frames:
        assert anim.norm(anim.sub(r, frames[0][0])) < 1e-15
        assert anim.norm(anim.sub(s, frames[0][1])) < 1e-15


def test_repeated_point_keeps_the_frame():
    c, dc, _ = twisted_cubic()
    points, tangents = sample_curve(c, dc, 0.0, 1.0, 6)
    base = double_reflection(points, tangents, (0.0, 0.0, 1.0))
    dup = double_reflection(points[:3] + points[2:], tangents[:3] + tangents[2:], (0.0, 0.0, 1.0))
    assert anim.norm(anim.sub(dup[2][0], dup[3][0])) < 1e-15
    for a, b in zip(base, dup[:3] + dup[4:]):
        assert anim.norm(anim.sub(a[0], b[0])) < 1e-14


def test_corner_at_a_repeated_point_is_the_smallest_rotation(rng=random.Random(3)):
    t0 = anim.normalize((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
    t1 = anim.normalize((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
    r0 = (1.0, 0.0, 0.0)
    frames = double_reflection([(0.0, 0.0, 0.0)] * 2, [t0, t1], r0)
    axis = anim.cross(t0, t1)
    angle = math.atan2(anim.norm(axis), anim.dot(t0, t1))
    q = anim.q_from_axis_angle(axis, angle)
    assert anim.norm(anim.sub(anim.q_rotate(q, t0), t1)) < 1e-12
    assert anim.norm(anim.sub(frames[1][0], anim.q_rotate(q, frames[0][0]))) < 1e-12


def test_too_coarse_step_raises():
    # The chord is along x, and the next tangent is the mirror image of t_0 in the plane x = 1/2.
    t0 = anim.normalize((1.0, 1.0, 0.0))
    t1 = anim.normalize((-1.0, 1.0, 0.0))
    with pytest.raises(ValueError):
        double_reflection([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [t0, t1], (0.0, 0.0, 1.0))


def test_initial_normal_is_projected():
    frames = double_reflection([(0.0, 0.0, 0.0)], [(0.0, 0.0, 2.0)], (1.0, 0.0, 5.0))
    assert frames[0][0] == pytest.approx((1.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        double_reflection([], [], (1.0, 0.0, 0.0))
