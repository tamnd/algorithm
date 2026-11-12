# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-surface/. The authors are listed in prov/5W3KF8.jsonl.

import math

import pytest

from sweep_surface import (frenet_frame, rmf_double_reflection, sweep_grid, sweep_point,
                           tube_jacobian_factor)

A, B = 2.0, 1.0                      # the helix (a cos t, a sin t, b t)
C = math.hypot(A, B)
TAU = B / C ** 2                     # torsion b / (a^2 + b^2)


def helix(t):
    return (A * math.cos(t), A * math.sin(t), B * t)


def dhelix(t):
    return (-A * math.sin(t), A * math.cos(t), B)


def ddhelix(t):
    return (-A * math.cos(t), -A * math.sin(t), 0.0)


def exact_rmf_normal(t):
    """r(t) = cos(th) N + sin(th) B with th = -tau s and s = c t: the RMF turns against Frenet."""
    th = -TAU * C * t
    n = (-math.cos(t), -math.sin(t), 0.0)
    b = (B * math.sin(t) / C, -B * math.cos(t) / C, A / C)
    return tuple(math.cos(th) * x + math.sin(th) * y for x, y in zip(n, b))


def rmf_error(n, t1=4 * math.pi):
    ts = [t1 * k / n for k in range(n + 1)]
    frames = rmf_double_reflection([helix(t) for t in ts], [dhelix(t) for t in ts], exact_rmf_normal(0))
    return max(math.dist(f[1], exact_rmf_normal(t)) for f, t in zip(frames, ts))


def test_helix_frenet_frame():
    for t in (0.0, 0.7, 3.0):
        tt, nn, bb = frenet_frame(dhelix(t), ddhelix(t))
        assert math.dist(nn, (-math.cos(t), -math.sin(t), 0.0)) < 1e-15
        assert math.dist(bb, (B * math.sin(t) / C, -B * math.cos(t) / C, A / C)) < 1e-15


def test_helix_rmf_against_closed_form():
    e1, e2 = rmf_error(100), rmf_error(200)
    assert e2 < 2e-6
    assert 12 < e1 / e2 < 20          # fourth order: halving the step divides the error by about 16


def test_frames_stay_orthonormal_and_right_handed():
    ts = [0.05 * k for k in range(400)]
    for t, r, s in rmf_double_reflection([helix(t) for t in ts], [dhelix(t) for t in ts], (1.0, 0.0, 0.0)):
        assert abs(math.hypot(*r) - 1) < 1e-12 and abs(sum(x * y for x, y in zip(t, r))) < 1e-12
        cr = (t[1] * r[2] - t[2] * r[1], t[2] * r[0] - t[0] * r[2], t[0] * r[1] - t[1] * r[0])
        assert math.dist(cr, s) < 1e-15


def test_planar_curve_rmf_is_frenet():
    ell = lambda t: (3 * math.cos(t), math.sin(t), 0.0)
    dell = lambda t: (-3 * math.sin(t), math.cos(t), 0.0)
    ddell = lambda t: (-3 * math.cos(t), -math.sin(t), 0.0)
    ts = [2 * math.pi * k / 300 for k in range(301)]
    frames = rmf_double_reflection([ell(t) for t in ts], [dell(t) for t in ts], frenet_frame(dell(0), ddell(0))[1])
    for (t, r, s), u in zip(frames, ts):
        _, nn, bb = frenet_frame(dell(u), ddell(u))
        assert math.dist(r, nn) < 1e-5 and math.dist(s, bb) < 1e-5


def test_straight_line():
    with pytest.raises(ValueError):
        frenet_frame((1.0, 0.0, 0.0), (2.0, 0.0, 0.0))
    pts = [(float(k), 0.0, 0.0) for k in range(10)]
    frames = rmf_double_reflection(pts, [(1.0, 0.0, 0.0)] * 10, (0.0, 1.0, 1.0))
    assert all(f[1] == frames[0][1] for f in frames)


def test_tube_points_are_at_the_radius():
    rho = 0.4
    profile = [(rho * math.cos(2 * math.pi * k / 12), rho * math.sin(2 * math.pi * k / 12)) for k in range(12)]
    rows = sweep_grid(helix, dhelix, profile, 0.0, 2 * math.pi, 80, (-1.0, 0.0, 0.0))
    for k, row in enumerate(rows):
        c = helix(2 * math.pi * k / 80)
        assert all(abs(math.dist(p, c) - rho) < 1e-12 for p in row)


def test_fat_tube_folds_over():
    """A tube of radius 2 about a unit circle: every station reaches the point (0, 0, sqrt 3)."""
    rho, phi = 2.0, math.pi / 3
    hits = []
    for u in (0.0, 1.0, 2.5):
        c = (math.cos(u), math.sin(u), 0.0)
        frame = ((-math.sin(u), math.cos(u), 0.0), (-math.cos(u), -math.sin(u), 0.0), (0.0, 0.0, 1.0))
        hits.append(sweep_point(c, frame, rho * math.cos(phi), rho * math.sin(phi)))
    assert all(math.dist(h, (0.0, 0.0, math.sqrt(3))) < 1e-15 for h in hits)
    assert abs(tube_jacobian_factor(1.0, rho, phi)) < 1e-15
    assert tube_jacobian_factor(1.0, 0.9, 0.0) > 0 and tube_jacobian_factor(1.0, 1.1, 0.0) < 0
