# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/admittance-control/. The authors are listed in prov/373QBF.jsonl.

import math

from admittance_control import CartesianRobot, admittance_step, free_space, simulate, wall


def hold(x0):
    return lambda t: ([x0], [0.0])


def series_force(depth, k_env, kp, ka):
    return depth / (1.0 / k_env + 1.0 / kp + 1.0 / ka)


def virtual_error(dt, steps):
    # Critically damped virtual dynamics under a constant force, against the exact solution.
    ma, ka, f = 1.0, 100.0, 5.0
    w = math.sqrt(ka / ma)
    da = 2.0 * w * ma
    xc, vc = [0.0], [0.0]
    worst = 0.0
    for k in range(steps):
        xc, vc = admittance_step(xc, vc, [0.0], [0.0], [f], [ma], [da], [ka], dt)
        t = (k + 1) * dt
        exact = f / ka * (1.0 - (1.0 + w * t) * math.exp(-w * t))
        worst = max(worst, abs(xc[0] - exact))
    return worst, xc[0]


def test_virtual_dynamics_first_order_accurate():
    e1, end1 = virtual_error(2e-3, 1000)
    e2, _ = virtual_error(1e-3, 2000)
    assert abs(end1 - 0.05) < 1e-6
    assert e1 < 1e-3
    assert 1.7 < e1 / e2 < 2.3


def test_free_space_tracks_the_goal():
    robot = CartesianRobot()
    da = 2.0 * math.sqrt(1000.0)  # critical damping of the virtual dynamics
    out = simulate(robot, free_space, hold(0.9), [0.8], [1.0], [da], [1000.0], 1e-3, 1000)
    _, x, xc, f = out[-1]
    assert f[0] == 0.0
    assert abs(xc[0] - 0.9) < 1e-3
    assert abs(x[0] - xc[0]) < 1e-5


def test_contact_force_is_three_springs_in_series():
    robot = CartesianRobot(mass=5.0, kp=1e5)
    for k_env in (1e4, 1e5):
        out = simulate(robot, wall(1.0, k_env), hold(1.02), [0.98], [1.0], [1000.0], [1000.0], 1e-3, 3000)
        force = -out[-1][3][0]
        assert abs(force - series_force(0.02, k_env, 1e5, 1000.0)) < 1e-6


def test_light_damping_chatters_on_a_stiff_wall():
    robot = CartesianRobot(mass=5.0, kp=1e5)
    ranges = []
    for k_env in (1e4, 1e5):
        out = simulate(robot, wall(1.0, k_env), hold(1.02), [0.98], [1.0], [100.0], [1000.0], 1e-3, 3000)
        tail = [-o[3][0] for o in out[-300:]]
        ranges.append(max(tail) - min(tail))
        if k_env == 1e4:
            assert abs(tail[-1] - series_force(0.02, k_env, 1e5, 1000.0)) < 1e-6
    assert ranges[0] < 1e-6
    assert ranges[1] > 10.0


def test_light_virtual_mass_breaks_the_discrete_integration():
    # Semi-implicit Euler needs 2 Da dt + Ka dt^2 < 4 Ma; here the left side is 2.001 > 0.4.
    xc, vc = [0.0], [0.0]
    for _ in range(200):
        xc, vc = admittance_step(xc, vc, [0.0], [0.0], [1.0], [0.1], [1000.0], [1000.0], 1e-3)
    assert abs(xc[0]) > 1e6


def test_discrete_stability_boundary():
    # Ma = 1, Ka = 1000, dt = 1 ms: the bound 2 Da dt + Ka dt^2 < 4 Ma gives Da < 1999.5.
    ends = []
    for da in (1990.0, 2010.0):
        xc, vc = [1.0], [0.0]
        for _ in range(3000):
            xc, vc = admittance_step(xc, vc, [0.0], [0.0], [0.0], [1.0], [da], [1000.0], 1e-3)
        ends.append(abs(xc[0]) + abs(vc[0]))
    assert ends[0] < 0.5  # the slow overdamped mode decays like exp(-t / 2)
    assert ends[1] > 1e3
