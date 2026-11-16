# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-tracking-control-se3/. The authors are listed in prov/R3QEN8.jsonl.

import math
import random

import rbm
from geometric_tracking_control_se3 import (
    GeometricController,
    attitude_errors,
    attitude_moment,
    desired_rotation,
    lee_quadrotor,
    orthonormalize,
    psi,
    simulate,
)

ZERO = [0.0, 0.0, 0.0]


def rand_rot(rng, max_angle=math.pi):
    axis = [rng.gauss(0.0, 1.0) for _ in range(3)]
    n = rbm.norm(axis)
    ang = rng.uniform(0.0, max_angle)
    return rbm.so3_exp([ang * a / n for a in axis])


def is_rotation(r, tol=1e-12):
    rtr = rbm.mul(rbm.transpose(r), r)
    ok = all(abs(rtr[i][j] - (1.0 if i == j else 0.0)) < tol for i in range(3) for j in range(3))
    return ok and abs(rbm.det(r) - 1.0) < tol


def test_rbm_helper_self_test():
    assert rbm.self_test()


def test_errors_match_the_logarithm():
    # With Rd^T R = exp([xi]) and theta = |xi| < pi: eR = sin(theta) xi / theta and Psi = 1 - cos(theta).
    rng = random.Random(1)
    for _ in range(300):
        rd = rand_rot(rng)
        xi = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        th = rbm.norm(xi)
        if th > 3.0 or th < 1e-6:
            continue
        r = rbm.mul(rd, rbm.so3_exp(xi))
        er, ew, _ = attitude_errors(r, ZERO, rd, ZERO)
        want = [math.sin(th) / th * x for x in xi]
        assert max(abs(a - b) for a, b in zip(er, want)) < 1e-12
        assert abs(psi(r, rd) - (1.0 - math.cos(th))) < 1e-12
        assert max(abs(x) for x in ew) == 0.0


def test_upside_down_is_a_critical_point():
    # At a rotation error of pi, eR = 0: the attitude loop exerts no moment there.
    r = rbm.rot_x(math.pi)
    er, _, _ = attitude_errors(r, ZERO, rbm.eye(3), ZERO)
    assert max(abs(x) for x in er) < 1e-15
    assert abs(psi(r, rbm.eye(3)) - 2.0) < 1e-15


def test_desired_rotation_is_a_rotation_with_the_thrust_axis():
    rng = random.Random(2)
    for _ in range(300):
        a = [rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(1, 50)]
        b1d = [math.cos(rng.uniform(0, 6.3)), math.sin(rng.uniform(0, 6.3)), 0.0]
        rd = desired_rotation(a, b1d)
        assert is_rotation(rd)
        b3 = [rd[i][2] for i in range(3)]
        b2 = [rd[i][1] for i in range(3)]
        na = rbm.norm(a)
        assert max(abs(b3[i] - a[i] / na) for i in range(3)) < 1e-12
        assert abs(rbm.dot(b2, b1d)) < 1e-12


def test_zero_force_is_rejected():
    try:
        desired_rotation([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_thrust_matches_the_z_down_form_of_the_paper():
    # Lee et al. write the law with z down: f = -(-kx ex - kv ev - m g e3 + m ad) . R e3.
    # Map a z-up state with P = diag(1, -1, -1): x -> P x, R -> P R P.
    rng = random.Random(3)
    c = lee_quadrotor(0.01)
    p = [1.0, -1.0, -1.0]
    for _ in range(100):
        x = [rng.uniform(-2, 2) for _ in range(3)]
        v = [rng.uniform(-2, 2) for _ in range(3)]
        r = rand_rot(rng, 1.5)
        xd, vd, ad = ([rng.uniform(-2, 2) for _ in range(3)] for _ in range(3))
        f_up, _ = c.command((x, v, r, ZERO), (xd, vd, ad, [1.0, 0.0, 0.0]), ZERO, ZERO)
        rp = [[p[i] * r[i][j] * p[j] for j in range(3)] for i in range(3)]
        exd = [p[i] * (x[i] - xd[i]) for i in range(3)]
        evd = [p[i] * (v[i] - vd[i]) for i in range(3)]
        add = [p[i] * ad[i] for i in range(3)]
        e3 = [0.0, 0.0, 1.0]
        a_dn = [-c.kx * exd[i] - c.kv * evd[i] - c.m * c.g * e3[i] + c.m * add[i] for i in range(3)]
        f_dn = -rbm.dot(a_dn, [rp[0][2], rp[1][2], rp[2][2]])
        assert abs(f_up - f_dn) < 1e-9


def attitude_only(rd, r, w, J, kr, kw, dt, steps):
    """RK4 on (R, W) with the moment evaluated at every stage (continuous feedback), Wd = 0."""
    Jinv = rbm.inv(J)

    def deriv(r, w):
        m, _, _ = attitude_moment(r, w, rd, ZERO, ZERO, J, kr, kw)
        jw = rbm.matvec(J, w)
        return rbm.mul(r, rbm.hat3(w)), rbm.matvec(Jinv, rbm.sub(m, rbm.cross(w, jw)))

    def lyap(r, w):
        return 0.5 * rbm.dot(w, rbm.matvec(J, w)) + kr * psi(r, rd)

    out = [lyap(r, w)]
    for _ in range(steps):
        k1 = deriv(r, w)
        k2 = deriv(rbm.add(r, rbm.scale(k1[0], dt / 2)), rbm.add(w, rbm.scale(k1[1], dt / 2)))
        k3 = deriv(rbm.add(r, rbm.scale(k2[0], dt / 2)), rbm.add(w, rbm.scale(k2[1], dt / 2)))
        k4 = deriv(rbm.add(r, rbm.scale(k3[0], dt)), rbm.add(w, rbm.scale(k3[1], dt)))
        r = orthonormalize([[r[i][j] + dt / 6 * (k1[0][i][j] + 2 * k2[0][i][j] + 2 * k3[0][i][j] + k4[0][i][j]) for j in range(3)] for i in range(3)])
        w = [w[i] + dt / 6 * (k1[1][i] + 2 * k2[1][i] + 2 * k3[1][i] + k4[1][i]) for i in range(3)]
        out.append(lyap(r, w))
    return r, w, out


def test_attitude_lyapunov_function_does_not_increase():
    # With Rd constant and Wd = 0, V = (1/2) W.J W + kR Psi has V' = -kW |W|^2 <= 0.
    rng = random.Random(4)
    c = lee_quadrotor(0.01)
    for _ in range(4):
        rd = rand_rot(rng)
        r = rbm.mul(rd, rand_rot(rng, 3.0))
        w = [rng.uniform(-2, 2) for _ in range(3)]
        r, w, vals = attitude_only(rd, r, w, c.J, c.kr, c.kw, 0.01, 600)
        assert all(b <= a + 1e-9 for a, b in zip(vals, vals[1:]))
        assert vals[-1] < 1e-3 * vals[0]


def test_hover_from_an_offset():
    c = lee_quadrotor(0.01)
    state = ([1.0, -1.0, 0.5], ZERO, rbm.rpy(0.3, -0.2, 1.0), [0.5, 0.0, -0.5])
    fin = simulate(c, state, lambda t: (ZERO, ZERO, ZERO, [1.0, 0.0, 0.0]), 6.0)
    assert rbm.norm(fin[0]) < 1e-3
    assert rbm.norm(fin[1]) < 1e-3
    assert is_rotation(fin[2], 1e-9)


def test_recovery_from_almost_upside_down():
    # Case II of Lee et al., converted to z up: start 178 degrees from the desired attitude.
    c = lee_quadrotor(0.01)
    log = []
    state = (ZERO, ZERO, rbm.rot_x(math.radians(178.0)), ZERO)
    fin = simulate(c, state, lambda t: (ZERO, ZERO, ZERO, [1.0, 0.0, 0.0]), 6.0,
                   record=lambda t, s, cc: log.append((t, cc.last["psi"])))
    assert log[0][1] > 1.999
    assert any(p < 1.0 for t, p in log if t < 2.0)
    assert log[-1][1] < 1e-9
    assert rbm.norm(fin[0]) < 1e-3


def test_tracks_an_elliptic_helix():
    # Case I of Lee et al., converted to z up. The steady error comes from the zero-order
    # hold and the backward differences for Wd, and shrinks with the control period.
    w = math.pi

    def helix(t):
        xd = [0.4 * t, -0.4 * math.sin(w * t), -0.6 * math.cos(w * t)]
        vd = [0.4, -0.4 * w * math.cos(w * t), 0.6 * w * math.sin(w * t)]
        ad = [0.0, 0.4 * w * w * math.sin(w * t), 0.6 * w * w * math.cos(w * t)]
        return xd, vd, ad, [math.cos(w * t), -math.sin(w * t), 0.0]

    c = lee_quadrotor(0.005)
    errs = []
    simulate(c, (ZERO, ZERO, rbm.eye(3), ZERO), helix, 8.0,
             record=lambda t, s, cc: errs.append((t, rbm.norm(cc.last["ex"]))))
    assert errs[0][1] > 0.5
    assert max(e for t, e in errs if t >= 5.0) < 5e-3


def test_gains_do_not_need_the_paper_values():
    # A light vehicle with other gains also hovers; the law has no hidden constants.
    J = [[0.002, 0.0, 0.0], [0.0, 0.002, 0.0], [0.0, 0.0, 0.004]]
    c = GeometricController(0.5, J, 4.0, 2.0, 0.2, 0.03, 0.005)
    fin = simulate(c, ([0.3, 0.2, -0.4], ZERO, rbm.rot_y(1.2), ZERO),
                   lambda t: (ZERO, ZERO, ZERO, [0.0, 1.0, 0.0]), 8.0)
    assert rbm.norm(fin[0]) < 1e-3
