# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-tracking-control-se3/. The authors are listed in prov/R3QEN8.jsonl.

"""Geometric tracking control of a quadrotor on SE(3) (Lee, Leok and McClamroch 2010).

Frames and signs. The world frame {s} has its z axis up and gravity is -g e3 with
g = 9.81 m/s^2. The body frame {b} has its z axis along the thrust. The paper uses a
z axis that points down; this file converts every equation to z up (the signs of the
gravity and thrust terms change, the attitude part does not).

Model (rigid body, thrust along the body z axis, moment M in body coordinates):
    x' = v,  m v' = f R e3 - m g e3,  R' = R [W],  J W' = M - W x J W.

Controller, for a desired position xd(t) with its first two derivatives and a desired
heading direction b1d(t):
    ex = x - xd, ev = v - vd
    A  = -kx ex - kv ev + m g e3 + m ad          (the force the body should produce)
    f  = A . (R e3)
    b3d = A / |A|,  b2d = b3d x b1d / |b3d x b1d|,  Rd = [b2d x b3d, b2d, b3d]
    eR = (1/2) vee(Rd^T R - R^T Rd),  eW = W - R^T Rd Wd
    M  = -kR eR - kW eW + W x J W - J ([W] R^T Rd Wd - R^T Rd Wd')
Wd and Wd' are the angular velocity and acceleration of Rd. The caller may give them;
otherwise they are estimated by backward differences of Rd between control steps.
"""

import math

import rbm

E3 = [0.0, 0.0, 1.0]


def psi(r, rd):
    """The attitude error function Psi = (1/2) trace(I - Rd^T R), in [0, 2]."""
    return 0.5 * (3.0 - sum(rd[i][j] * r[i][j] for i in range(3) for j in range(3)))


def attitude_errors(r, w, rd, wd):
    """eR = (1/2) vee(Rd^T R - R^T Rd) and eW = W - R^T Rd Wd."""
    rdt_r = rbm.mul(rbm.transpose(rd), r)
    er = rbm.scale(rbm.vee3(rbm.sub(rdt_r, rbm.transpose(rdt_r))), 0.5)
    rt_rd = rbm.transpose(rdt_r)
    ew = rbm.sub(w, rbm.matvec(rt_rd, wd))
    return er, ew, rt_rd


def attitude_moment(r, w, rd, wd, dwd, J, kr, kw):
    """The moment of the attitude loop, lines L6 and L7 of the page."""
    er, ew, rt_rd = attitude_errors(r, w, rd, wd)  # @line L6
    jw = rbm.matvec(J, w)
    a = rbm.matvec(rt_rd, wd)
    b = rbm.matvec(rt_rd, dwd)
    ff = rbm.matvec(J, rbm.sub(rbm.cross(w, a), b))
    m = [-kr * er[i] - kw * ew[i] + rbm.cross(w, jw)[i] - ff[i] for i in range(3)]  # @line L7
    return m, er, ew


def desired_rotation(a, b1d):
    """Rd = [b2d x b3d, b2d, b3d] with b3d = a / |a|. Needs a != 0 and b1d not parallel to a."""
    na = rbm.norm(a)
    if na == 0.0:
        raise ValueError("the commanded force is zero; the thrust direction is undefined")
    b3 = [x / na for x in a]
    c = rbm.cross(b3, b1d)
    nc = rbm.norm(c)
    if nc < 1e-9:
        raise ValueError("b1d is parallel to the thrust direction")
    b2 = [x / nc for x in c]
    b1 = rbm.cross(b2, b3)
    return [[b1[i], b2[i], b3[i]] for i in range(3)]


class GeometricController:
    """The tracking controller. Gains kx, kv in N/m and N s/m, kR, kW in N m and N m s."""

    def __init__(self, m, J, kx, kv, kr, kw, dt, g=9.81):
        self.m, self.J, self.g, self.dt = m, J, g, dt
        self.kx, self.kv, self.kr, self.kw = kx, kv, kr, kw
        self.rd_prev = None
        self.wd_prev = None
        self.last = {}

    def command(self, state, ref, wd=None, dwd=None):
        """Return (f, M) for state (x, v, R, W) and ref (xd, vd, ad, b1d)."""
        x, v, r, w = state
        xd, vd, ad, b1d = ref
        ex = rbm.sub(x, xd)  # @line L1
        ev = rbm.sub(v, vd)  # @line L1
        a = [-self.kx * ex[i] - self.kv * ev[i] + self.m * self.g * E3[i] + self.m * ad[i] for i in range(3)]  # @line L2
        re3 = [r[0][2], r[1][2], r[2][2]]
        f = rbm.dot(a, re3)  # @line L3
        rd = desired_rotation(a, b1d)  # @line L4
        if wd is None:  # @line L5
            if self.rd_prev is None:
                wd = [0.0, 0.0, 0.0]
            else:
                wd = rbm.scale(rbm.so3_log(rbm.mul(rbm.transpose(self.rd_prev), rd)), 1.0 / self.dt)
            dwd = [0.0] * 3 if self.wd_prev is None else rbm.scale(rbm.sub(wd, self.wd_prev), 1.0 / self.dt)
            self.rd_prev, self.wd_prev = rd, wd
        elif dwd is None:
            dwd = [0.0, 0.0, 0.0]
        m, er, ew = attitude_moment(r, w, rd, wd, dwd, self.J, self.kr, self.kw)  # @line L6
        self.last = {"ex": ex, "ev": ev, "eR": er, "eW": ew, "Rd": rd, "psi": psi(r, rd)}
        return f, m


def dynamics(state, f, moment, m, J, Jinv, g=9.81):
    """Time derivative of (x, v, R, W) with z up."""
    x, v, r, w = state
    re3 = [r[0][2], r[1][2], r[2][2]]
    acc = [f * re3[i] / m - g * E3[i] for i in range(3)]
    rdot = rbm.mul(r, rbm.hat3(w))
    jw = rbm.matvec(J, w)
    wdot = rbm.matvec(Jinv, rbm.sub(moment, rbm.cross(w, jw)))
    return v, acc, rdot, wdot


def _axpy(state, k, h):
    x, v, r, w = state
    dx, dv, dr, dw = k
    return (
        [x[i] + h * dx[i] for i in range(3)],
        [v[i] + h * dv[i] for i in range(3)],
        [[r[i][j] + h * dr[i][j] for j in range(3)] for i in range(3)],
        [w[i] + h * dw[i] for i in range(3)],
    )


def orthonormalize(r):
    """Gram-Schmidt on the columns of r, to remove the drift of the integrator."""
    c0 = [r[i][0] for i in range(3)]
    c1 = [r[i][1] for i in range(3)]
    n0 = rbm.norm(c0)
    c0 = [x / n0 for x in c0]
    d = rbm.dot(c0, c1)
    c1 = [c1[i] - d * c0[i] for i in range(3)]
    n1 = rbm.norm(c1)
    c1 = [x / n1 for x in c1]
    c2 = rbm.cross(c0, c1)
    return [[c0[i], c1[i], c2[i]] for i in range(3)]


def rk4_step(state, f, moment, dt, m, J, Jinv, g=9.81):
    """One classical Runge-Kutta step with f and M held (zero-order hold), then re-orthonormalize R."""
    k1 = dynamics(state, f, moment, m, J, Jinv, g)
    k2 = dynamics(_axpy(state, k1, dt / 2), f, moment, m, J, Jinv, g)
    k3 = dynamics(_axpy(state, k2, dt / 2), f, moment, m, J, Jinv, g)
    k4 = dynamics(_axpy(state, k3, dt), f, moment, m, J, Jinv, g)
    x, v, r, w = state
    out = []
    for idx in range(4):
        a, b, c, d = k1[idx], k2[idx], k3[idx], k4[idx]
        if idx == 2:
            out.append([[r[i][j] + dt / 6 * (a[i][j] + 2 * b[i][j] + 2 * c[i][j] + d[i][j]) for j in range(3)] for i in range(3)])
        else:
            base = state[idx]
            out.append([base[i] + dt / 6 * (a[i] + 2 * b[i] + 2 * c[i] + d[i]) for i in range(3)])
    out[2] = orthonormalize(out[2])
    return tuple(out)


def simulate(ctrl, state, ref_fn, t_end, record=None):
    """Run the closed loop with control period ctrl.dt. ref_fn(t) returns (xd, vd, ad, b1d).

    record(t, state, ctrl) is called after each command, if given. Returns the final state.
    """
    Jinv = rbm.inv(ctrl.J)
    steps = int(round(t_end / ctrl.dt))
    for k in range(steps):
        t = k * ctrl.dt
        f, moment = ctrl.command(state, ref_fn(t))
        if record is not None:
            record(t, state, ctrl)
        state = rk4_step(state, f, moment, ctrl.dt, ctrl.m, ctrl.J, Jinv, ctrl.g)  # @line L8
    return state


def lee_quadrotor(dt):
    """The vehicle and the gains of the numerical example of Lee, Leok and McClamroch (2010)."""
    m = 4.34
    J = [[0.0820, 0.0, 0.0], [0.0, 0.0845, 0.0], [0.0, 0.0, 0.1377]]
    return GeometricController(m, J, 16.0 * m, 5.6 * m, 8.81, 2.54, dt)
