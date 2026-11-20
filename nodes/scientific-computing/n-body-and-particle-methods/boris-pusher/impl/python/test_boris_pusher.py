# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boris-pusher/. The authors are listed in prov/F8XC41.jsonl.
import math
import random

import pytest

from boris_pusher import boris_run, boris_velocity, cross, rotation_angle, start_velocity


def norm(a):
    return math.sqrt(sum(c * c for c in a))


def rotate(v, axis, angle):
    """Rodrigues rotation of v about the unit vector axis by angle (right-hand rule)."""
    c, s = math.cos(angle), math.sin(angle)
    kv = cross(axis, v)
    kd = sum(axis[i] * v[i] for i in range(3))
    return tuple(v[i] * c + kv[i] * s + axis[i] * kd * (1 - c) for i in range(3))


def rand_vec(rng, r=1.0):
    return tuple(rng.uniform(-r, r) for _ in range(3))


def field_a(x):
    e = (0.1 * x[0] - 0.05 * x[1], -0.2 + 0.1 * math.cos(x[2]), 0.05 * x[2])
    b = (0.3 + 0.1 * x[1], 0.1 * x[0], 1.0 + 0.2 * math.sin(x[0]))
    return e, b


def flip_b(field):
    def g(x):
        e, b = field(x)
        return e, tuple(-c for c in b)

    return g


def test_page_example():
    assert boris_velocity((1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0, 1.0) == pytest.approx(
        (0.6, -0.8, 0.0), abs=1e-15
    )
    assert boris_velocity((1.0, 0.0, 0.0), (0.5, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0, 1.0) == pytest.approx(
        (1.0, -1.0, 0.0), abs=1e-15
    )
    assert rotation_angle(1.0) == pytest.approx(math.atan2(0.8, 0.6), abs=1e-15)


def test_pure_magnetic_field_is_exact_rotation():
    rng = random.Random(1)
    for _ in range(300):
        v = rand_vec(rng, 3)
        b = rand_vec(rng, 2)
        qm, h = rng.uniform(-2, 2), rng.uniform(0.01, 3)
        got = boris_velocity(v, (0, 0, 0), b, qm, h)
        bn = norm(b)
        axis = tuple(c / bn for c in b)
        # dv/dt = (q/m) v x B turns v about B by the angle -(q/m)|B| t; Boris turns it by -2 atan(Omega h / 2)
        want = rotate(v, axis, -rotation_angle(qm * bn * h))
        assert got == pytest.approx(want, abs=1e-12)
        assert norm(got) == pytest.approx(norm(v), rel=1e-14)


def test_speed_conserved_over_many_steps_in_nonuniform_b():
    def field(x):
        return (0.0, 0.0, 0.0), (0.2 * x[1], 0.1, 1.0 + 0.5 * math.sin(x[0]))

    v0 = (0.3, -0.7, 0.2)
    _, v = boris_run((0.1, 0.2, 0.3), v0, field, 1.3, 0.2, 10000)
    assert norm(v) == pytest.approx(norm(v0), rel=1e-12)


def test_matches_implicit_midpoint_form():
    rng = random.Random(2)
    for _ in range(300):
        v, e, b = rand_vec(rng, 2), rand_vec(rng, 2), rand_vec(rng, 2)
        qm, h = rng.uniform(-2, 2), rng.uniform(0.01, 2)
        w = boris_velocity(v, e, b, qm, h)
        mid = tuple((w[i] + v[i]) / 2 for i in range(3))
        c = cross(mid, b)
        for i in range(3):
            assert (w[i] - v[i]) / h == pytest.approx(qm * (e[i] + c[i]), abs=1e-10)


def test_e_cross_b_drift_is_a_fixed_point():
    rng = random.Random(3)
    for _ in range(100):
        b = rand_vec(rng, 2)
        e0 = rand_vec(rng, 1)
        bb = sum(c * c for c in b)
        eb = sum(e0[j] * b[j] for j in range(3))
        e = tuple(e0[i] - b[i] * eb / bb for i in range(3))  # the part of E normal to B
        vd = tuple(c / bb for c in cross(e, b))
        w = boris_velocity(vd, e, b, rng.uniform(-3, 3), rng.uniform(0.1, 5))
        assert w == pytest.approx(vd, abs=1e-12)


def test_time_reversible_with_b_reversed():
    # Forward: (x_0, v_{-1/2}) -> (x_T, v_{T-1/2}). One more kick gives v_{T+1/2}.
    # Backward from (x_T, -v_{T+1/2}) with B -> -B gives (x_0, -v_{1/2}).
    h, qm, steps = 0.1, 1.0, 400
    x0, vm = (0.5, -0.2, 0.1), (0.2, 0.4, -0.1)
    xt, vt = boris_run(x0, vm, field_a, qm, h, steps)
    e, b = field_a(xt)
    vnext = boris_velocity(vt, e, b, qm, h)
    xb, vb = boris_run(xt, tuple(-c for c in vnext), flip_b(field_a), qm, h, steps)
    e, b = field_a(x0)
    v_half = boris_velocity(vm, e, b, qm, h)
    assert xb == pytest.approx(x0, abs=1e-9)
    assert vb == pytest.approx(tuple(-c for c in v_half), abs=1e-9)


def det(a):
    a = [row[:] for row in a]
    n, d = len(a), 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if p != c:
            a[c], a[p] = a[p], a[c]
            d = -d
        d *= a[c][c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n):
                a[r][k] -= f * a[c][k]
    return d


def test_one_step_preserves_phase_space_volume():
    rng = random.Random(4)
    for _ in range(10):
        z = [rng.uniform(-1, 1) for _ in range(6)]
        qm, h = rng.uniform(-2, 2), rng.uniform(0.05, 0.8)

        def step(z):
            x, v = boris_run(tuple(z[:3]), tuple(z[3:]), field_a, qm, h, 1)
            return list(x) + list(v)

        eps = 1e-5
        cols = []
        for k in range(6):
            zp, zm = z[:], z[:]
            zp[k] += eps
            zm[k] -= eps
            fp, fm = step(zp), step(zm)
            cols.append([(fp[i] - fm[i]) / (2 * eps) for i in range(6)])
        jac = [[cols[k][i] for k in range(6)] for i in range(6)]
        assert det(jac) == pytest.approx(1.0, abs=1e-7)


def rk4_run(x, v, field, qm, h, steps):
    def f(z):
        e, b = field(z[:3])
        c = cross(z[3:], b)
        return z[3:] + tuple(qm * (e[i] + c[i]) for i in range(3))

    z = tuple(x) + tuple(v)
    for _ in range(steps):
        k1 = f(z)
        k2 = f(tuple(z[i] + 0.5 * h * k1[i] for i in range(6)))
        k3 = f(tuple(z[i] + 0.5 * h * k2[i] for i in range(6)))
        k4 = f(tuple(z[i] + h * k3[i] for i in range(6)))
        z = tuple(z[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(6))
    return z[:3]


def test_second_order_convergence():
    x0, v0, qm, t_end = (0.3, 0.1, -0.2), (0.4, -0.3, 0.2), 1.5, 2.0
    ref = rk4_run(x0, v0, field_a, qm, t_end / 2000, 2000)
    errs = []
    for n in (40, 80, 160):
        h = t_end / n
        x, _ = boris_run(x0, start_velocity(x0, v0, field_a, qm, h), field_a, qm, h, n)
        errs.append(norm(tuple(x[i] - ref[i] for i in range(3))))
    for e1, e2 in zip(errs, errs[1:]):
        assert 3.5 < e1 / e2 < 4.5
