# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-steps-physics/. The authors are listed in prov/R4RWDE.jsonl.

"""Tests of small steps: the XPBD update, a pendulum against a reference ODE solve, and substeps against iterations."""

import math

import small_steps_physics as ss


def pendulum_reference(t_end, steps=20000):
    """Classical Runge-Kutta on theta'' = -g cos(theta) for a rod of length 1 from the +x axis, y up."""
    th, om = 0.0, 0.0
    h = t_end / steps

    def f(t, o):
        return o, -9.81 * math.cos(t)

    for _ in range(steps):
        k1 = f(th, om)
        k2 = f(th + h / 2 * k1[0], om + h / 2 * k1[1])
        k3 = f(th + h / 2 * k2[0], om + h / 2 * k2[1])
        k4 = f(th + h * k3[0], om + h * k3[1])
        th += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        om += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return math.cos(th), math.sin(th)


def test_example_one_compliant_constraint():
    """Two unit masses 1.5 apart, rest 1, alpha~ = 1: dlambda = -0.5 / 3, each end moves by 1/6."""
    x = [(0.0, 0.0), (1.5, 0.0)]
    lam = [0.0]
    ss.solve_constraints(x, [1.0, 1.0], [(0, 1, 1.0, 0.01)], lam, 0.1)
    assert abs(lam[0] + 0.5 / 3.0) < 1e-15
    assert abs(x[0][0] - 1.0 / 6.0) < 1e-15 and abs(x[1][0] - (1.5 - 1.0 / 6.0)) < 1e-15


def test_rigid_constraint_is_one_projection():
    x = [(0.0, 0.0), (0.3, 0.4)]
    ss.solve_constraints(x, [0.0, 2.0], [(0, 1, 1.0, 0.0)], [0.0], 0.01)
    assert x[0] == (0.0, 0.0) and abs(math.hypot(*x[1]) - 1.0) < 1e-15


def test_pendulum_converges_to_the_reference_at_first_order():
    ref = pendulum_reference(0.5)
    errs = []
    for n in (10, 100):
        x, w, c = ss.chain(2, 1.0)
        x, _ = ss.simulate(x, [(0.0, 0.0)] * 2, w, c, 1.0 / 60.0, 30, n, 1)
        errs.append(math.dist(x[1], ref))
    assert 7.0 < errs[0] / errs[1] < 13.0 and errs[1] < 5e-3


def test_iterations_do_not_reduce_the_error_of_one_constraint():
    """One constraint is solved exactly by one iteration, so only substeps reduce the time error."""
    out = []
    for k in (1, 50):
        x, w, c = ss.chain(2, 1.0)
        x, _ = ss.simulate(x, [(0.0, 0.0)] * 2, w, c, 1.0 / 60.0, 30, 1, k)
        out.append(x[1])
    assert math.dist(out[0], out[1]) < 1e-12


def test_substeps_beat_iterations_for_the_same_budget():
    """Measured on a 20 particle chain with a last particle 1000 times heavier."""
    res = {}
    for n, k in ((1, 100), (100, 1)):
        x, w, c = ss.chain(20, 0.1, [1.0] * 19 + [1000.0])
        x, _ = ss.simulate(x, [(0.0, 0.0)] * 20, w, c, 1.0 / 60.0, 30, n, k)
        res[n] = ss.stretch(x, c)
    assert res[100] < res[1] / 30.0


def test_stretch_falls_fast_with_more_substeps():
    """Measured: on a uniform chain, ten times more substeps cut the stretch by about 100."""
    s = []
    for n in (5, 50):
        x, w, c = ss.chain(20, 0.1)
        x, _ = ss.simulate(x, [(0.0, 0.0)] * 20, w, c, 1.0 / 60.0, 20, n, 1)
        s.append(ss.stretch(x, c))
    assert s[0] / s[1] > 50.0


def test_free_fall_with_substeps_is_symplectic_euler():
    x, w, c = ss.chain(2, 1.0)
    w = [1.0, 1.0]
    x, _ = ss.simulate(x, [(0.0, 0.0)] * 2, w, [], 0.1, 10, 1, 1)
    assert abs(x[0][1] + 5.3955) < 1e-12
    x, _ = ss.simulate([(0.0, 0.0)], [(0.0, 0.0)], [1.0], [], 1.0, 1, 4, 1)
    assert abs(x[0][1] + 9.81 * 0.0625 * 10) < 1e-12
