# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vortex-particle-method/. The authors are listed in prov/4WPAHS.jsonl.
import math
import random

import pytest

from vortex_particle_method import (kernel, lamb_oseen_speed, lamb_oseen_vorticity, lattice_particles, velocities,
                                    velocity_at, vortex_step)


def blob_vorticity(x, y, xs, ys, gs, delta):
    return sum(g * math.exp(-((x - a) ** 2 + (y - b) ** 2) / delta ** 2) for a, b, g in zip(xs, ys, gs)) / (
        math.pi * delta ** 2)


def test_page_example_pair_velocities():
    us, vs = velocities([-0.5, 0.5], [0.0, 0.0], [2 * math.pi, 2 * math.pi], 0.5)
    w = 1 - math.exp(-4)
    assert us == pytest.approx([0.0, 0.0], abs=1e-15)
    assert vs == pytest.approx([-w, w], abs=1e-15)
    assert w == pytest.approx(0.981684, abs=1e-6)


def test_direct_sum_matches_the_pointwise_sum_and_has_no_self_velocity():
    rng = random.Random(1)
    xs = [rng.uniform(-1, 1) for _ in range(40)]
    ys = [rng.uniform(-1, 1) for _ in range(40)]
    gs = [rng.uniform(-1, 1) for _ in range(40)]
    us, vs = velocities(xs, ys, gs, 0.3)
    for p in range(40):
        u, v = velocity_at(xs[p], ys[p], xs, ys, gs, 0.3)
        assert (us[p], vs[p]) == pytest.approx((u, v), abs=1e-12)
    assert velocities([0.3], [0.7], [5.0], 0.2) == ([0.0], [0.0])


def test_velocity_is_divergence_free_and_its_curl_is_the_blob_vorticity():
    rng = random.Random(2)
    xs = [rng.uniform(-1, 1) for _ in range(10)]
    ys = [rng.uniform(-1, 1) for _ in range(10)]
    gs = [rng.uniform(-1, 1) for _ in range(10)]
    delta, e = 0.4, 1e-4
    for _ in range(20):
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        ue, ve = velocity_at(x + e, y, xs, ys, gs, delta)
        uw, vw = velocity_at(x - e, y, xs, ys, gs, delta)
        un, vn = velocity_at(x, y + e, xs, ys, gs, delta)
        us, vs = velocity_at(x, y - e, xs, ys, gs, delta)
        div = (ue - uw + vn - vs) / (2 * e)
        curl = (ve - vw - (un - us)) / (2 * e)
        assert div == pytest.approx(0, abs=1e-6)
        assert curl == pytest.approx(blob_vorticity(x, y, xs, ys, gs, delta), abs=1e-5)


def test_far_field_is_the_point_vortex():
    u, v = kernel(0.0, 3.0, 0.1)
    assert u == pytest.approx(-1 / (2 * math.pi * 3.0), rel=1e-12) and v == 0.0


def test_co_rotating_pair_rotates_at_the_predicted_rate():
    d, delta, g = 1.0, 0.5, 1.0
    omega = g * (1 - math.exp(-d * d / delta ** 2)) / (math.pi * d * d)
    xs, ys, gs = [-d / 2, d / 2], [0.0, 0.0], [g, g]
    h, steps = 0.05, 200
    for _ in range(steps):
        xs, ys = vortex_step(xs, ys, gs, delta, h)
    assert math.hypot(xs[1] - xs[0], ys[1] - ys[0]) == pytest.approx(d, abs=1e-3)
    angle = math.atan2(ys[1], xs[1])
    expected = (omega * h * steps + math.pi) % (2 * math.pi) - math.pi
    assert angle == pytest.approx(expected, abs=2e-3)


def test_linear_impulse_is_exact_and_angular_impulse_is_nearly_conserved():
    rng = random.Random(3)
    n = 30
    xs = [rng.uniform(-1, 1) for _ in range(n)]
    ys = [rng.uniform(-1, 1) for _ in range(n)]
    gs = [rng.uniform(-1, 1) for _ in range(n)]

    def impulses(xs, ys):
        return (sum(g * x for g, x in zip(gs, xs)), sum(g * y for g, y in zip(gs, ys)),
                sum(g * (x * x + y * y) for g, x, y in zip(gs, xs, ys)))

    i0 = impulses(xs, ys)
    for _ in range(50):
        xs, ys = vortex_step(xs, ys, gs, 0.2, 0.01)
    i1 = impulses(xs, ys)
    assert i1[0] == pytest.approx(i0[0], abs=1e-12) and i1[1] == pytest.approx(i0[1], abs=1e-12)
    assert i1[2] == pytest.approx(i0[2], abs=1e-4)


def test_lamb_oseen_velocity_is_reproduced():
    # Gaussian blobs smear the vortex: the blob field is the Lamb-Oseen vortex at t + delta^2 / (4 nu)
    g, nu, t = 1.0, 0.01, 1.0
    xs, ys, gs = lattice_particles(lambda r: lamb_oseen_vorticity(r, g, nu, t), 0.05, 0.6)
    assert len(xs) <= 500
    assert sum(gs) == pytest.approx(g, abs=1e-3)
    errors = {}
    for delta in (0.1, 0.05):
        smeared, exact = 0.0, 0.0
        for r in (0.05, 0.1, 0.2, 0.3, 0.5):
            for a in (0.3, 1.1):
                u, v = velocity_at(r * math.cos(a), r * math.sin(a), xs, ys, gs, delta)
                ut = -u * math.sin(a) + v * math.cos(a)
                smeared = max(smeared, abs(ut - lamb_oseen_speed(r, g, nu, t + delta * delta / (4 * nu))))
                exact = max(exact, abs(ut - lamb_oseen_speed(r, g, nu, t)))
        assert smeared < 1e-4
        errors[delta] = exact
    # the smoothing error is second order in delta
    assert 3.0 < errors[0.1] / errors[0.05] < 4.5


def test_lamb_oseen_vortex_is_a_steady_rotation():
    g, nu, t, delta = 1.0, 0.01, 1.0, 0.15
    xs, ys, gs = lattice_particles(lambda r: lamb_oseen_vorticity(r, g, nu, t), 0.1, 0.6)
    r0 = [math.hypot(x, y) for x, y in zip(xs, ys)]
    a0 = [math.atan2(y, x) for x, y in zip(xs, ys)]
    h, steps = 0.05, 20
    for _ in range(steps):
        xs, ys = vortex_step(xs, ys, gs, delta, h)
    for x, y, r, a in zip(xs, ys, r0, a0):
        assert math.hypot(x, y) == pytest.approx(r, abs=5e-4)
        if r > 0:
            w = lamb_oseen_speed(r, g, nu, t + delta * delta / (4 * nu)) / r
            turn = (math.atan2(y, x) - a - w * h * steps + math.pi) % (2 * math.pi) - math.pi
            assert abs(turn) < 5e-3
